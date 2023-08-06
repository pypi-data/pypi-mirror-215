from setuptools import setup

setup(
    name='mypiprandomdata',
    version='0.7.0',
    packages=['mypiprandomdata'],
    package_data={'mypiprandomdata': ['data/*.txt', 'data/*.json']},
    entry_points={
        'console_scripts': [
            'mypiprandomdata = mypiprandomdata.cli:main'
        ]
    },
    install_requires=[],
    author='Inzmamul Haq',
    author_email='spat959@gmail.com',
    description='A package to generate random data.',
    keywords='random data generator',
    url='https://github.com/spat959/mypiprandomdata',
)
