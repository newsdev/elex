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
    version='2.4.0',
    author='Jeremy Bowers, David Eads',
    author_email='jeremy.bowers@nytimes.com, deads@npr.org',
    url='https://github.com/newsdev/elex',
    description='Client for parsing the Associated Press\'s elections API',
    long_description=read('README.rst'),
    packages=('elex', 'elex.cli', 'elex.api', 'tests'),
    entry_points={
        'console_scripts': (
            'elex = elex.cli:main',
        ),
    },
    license="Apache License 2.0",
    keywords='election race candidate democracy news associated press',
    install_requires=reqs,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    )
)
