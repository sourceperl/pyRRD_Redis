#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, make_response, request
from pyRRD_Redis import RRD_redis
import datetime
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.debug = True


@app.route("/add/<string:tag_name>/<int:value>")
@app.route("/add/<string:tag_name>/<float:value>")
def add(tag_name, value):
    rrd = RRD_redis('rrd:' + tag_name)
    rrd.add(value)
    return 'it\'s ok'


@app.route("/last/<string:tag_name>")
def last(tag_name):
    rrd = RRD_redis('rrd:' + tag_name)
    l_rrv = rrd.get(size=1)
    if len(l_rrv) == 1:
        return '<b>' + str(l_rrv[0].value) + '</b>'
    else:
        return '%s not exist' % tag_name


@app.route("/plot/<string:tag_name>.png")
def plot(tag_name):
    # size URL params (default is 0)
    size = int(request.args.get('size', 0))
    # live PNG generator
    rrd = RRD_redis('rrd:' + tag_name)
    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    for rrv in rrd.get(size=size):
        x.append(datetime.datetime.fromtimestamp(rrv.timestamp))
        y.append(rrv.value)
    ax.plot_date(x, y, '-', label=tag_name)
    ax.legend()
    # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
