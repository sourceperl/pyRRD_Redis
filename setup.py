from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pyRRD_Redis',
    version='0.0.17',
    license='MIT',
    url='https://github.com/sourceperl/pyRRD_Redis',
    platforms='any',
    install_requires=required,
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
        'scripts/csv_plot'
    ]
)
