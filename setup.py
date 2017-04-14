from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pyRRD_Redis',
    version='0.0.3',
    license='MIT',
    url='https://github.com/sourceperl/pyRRD_Redis',
    platforms='any',
    install_requires=required,
    py_modules=[
        'pyRRD_Redis'
    ],
    scripts=[
        'scripts/rrd2csv',
        'scripts/rrd2plot'
    ]
)
