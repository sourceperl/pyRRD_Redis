from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pyRRD_Redis',
    version='0.0.18',
    license='MIT',
    url='https://github.com/sourceperl/pyRRD_Redis',
    platforms='any',
    install_requires=required,
    packages=[
        'flask_rrd_web_service'
    ],
    include_package_data=True,
    zip_safe=False,
    py_modules=[
        'pyRRD_Redis'
    ],
    scripts=[
        'scripts/rrd_csv',
        'scripts/rrd_plot',
        'scripts/rrd_ls',
        'scripts/rrd_add',
        'scripts/rrd_len',
        'scripts/rrd_rm',
        'scripts/rrd_web_service',
        'scripts/csv_plot'
    ]
)
