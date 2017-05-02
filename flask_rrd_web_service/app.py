#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, make_response, request, render_template, jsonify
from pyRRD_Redis import RRD_redis
import datetime
import csv
from io import BytesIO, StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route('/')
def root():
    tags = RRD_redis('').ls()
    return render_template('rrd_list.html', tags=sorted(tags))


@app.route('/view/chart_js')
def view_chart_js():
    # URL params
    tag = request.args.get('tag', '', type=str)
    # populate template
    return render_template('view_chart_js.html', tag=tag)


@app.route('/view/chart_png')
def view_chart_png():
    # URL params
    tag = request.args.get('tag', '', type=str)
    # populate template
    return render_template('view_chart_png.html', tag=tag)


@app.route('/charts/tag/<string:tag_name>/1.png')
def plot(tag_name):
    # URL params
    size = int(request.args.get('size', 0))
    # live PNG generator
    rrd = RRD_redis(tag_name)
    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    for rrv in rrd.get(size=size):
        x.append(datetime.datetime.fromtimestamp(rrv.timestamp))
        y.append(rrv.value)
    ax.plot_date(x, y, '-', label=tag_name)
    # ax.legend()
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/api/get.json')
def get():
    # URL params
    tag_name = request.args.get('tag', '', type=str)
    size = request.args.get('size', 512, type=int)
    # tag_name must be set
    if not tag_name:
        return jsonify(status='error', message='tag arg must be set'), 400
    # limit request to 1 to 1024 item(s)
    size = max(1, min(size, 1024))
    # build json msg
    l_rrv = RRD_redis(tag_name).get(size=size)
    # return json msg or error
    if len(l_rrv) >= 1:
        l_js_msg = []
        for rrv in l_rrv:
            l_js_msg.append({'value': rrv.value, 'timestamp': rrv.timestamp})
        return jsonify(status='success', items=l_js_msg)
    else:
        return jsonify(status='error', message='tag not exist'), 400


@app.route('/api/get_last.json')
def get_last():
    # URL params
    tag_name = request.args.get('tag', '', type=str)
    # tag_name must be set
    if not tag_name:
        return jsonify(status='error', message='tag arg must be set'), 400
    # build json msg
    v = RRD_redis(tag_name).get(size=1)
    # return json msg or error
    if len(v) == 1:
        return jsonify(status='success', value=v[0].value, timestamp=v[0].timestamp, time_str=v[0].time_str)
    else:
        return jsonify(status='error', message='tag not exist'), 400


@app.route('/api/get_all.json')
def get_all():
    # request all RRDs and format a list
    d_list = {}
    for t_name in sorted(RRD_redis('').ls()):
        t = RRD_redis(t_name).get(size=1)[0]
        d_list[t_name] = {'value': t.value, 'update_str': t.time_str}
    # return json msg or error
    return jsonify(status='success', items=d_list)


@app.route('/api/get.csv')
def get_csv():
    # URL params
    tag = request.args.get('tag', '', type=str)
    size = request.args.get('size', 0, type=int)
    # init CSV writer
    si = StringIO()
    csv.register_dialect('csv_semicolon', delimiter=';', quoting=csv.QUOTE_NONE)
    writer = csv.writer(si, dialect='csv_semicolon')
    # populate CSV
    for rrv in RRD_redis(tag).get(size=size):
        writer.writerow([rrv.time_str, rrv.value])
    # format response
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=exp_%s.csv' % tag
    response.headers['Content-type'] = 'text/csv'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
