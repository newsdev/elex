import os.path
from pip.download import PipSession
from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='elex',
    version='0.0.42',
    author='Jeremy Bowers',
    author_email='jeremy.bowers@nytimes.com',
    url='https://github.com/newsdev/elex',
    description='Python client for parsing the Associated Press\'s elections API.',
    long_description=read('README.rst'),
    packages=['elex', 'elex.cli', 'elex.parser', 'tests'],
    entry_points={
        'console_scripts': [
            'elex = elex.cli:main',
        ],
    },
    license="Apache License 2.0",
    keywords='election race candidate democracy news associated press',
    install_requires=reqs,
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
