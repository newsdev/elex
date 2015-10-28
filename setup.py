import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='nyt-ap-elections',
    version='0.0.17',
    author='Jeremy Bowers',
    author_email='jeremy.bowers@nytimes.com',
    url='https://github.com/newsdev/nyt-ap-elections',
    description='Python client for parsing the Associated Press\'s elections API.',
    long_description=read('README.rst'),
    packages=['elex'],
    license="Apache License 2.0",
    keywords='election race candidate democracy news associated press',
    install_requires=['appnope==0.1.0','cffi==1.3.0','decorator==4.0.4','gnureadline==6.3.3','greenlet==0.4.7','ipython==4.0.0','ipython-genutils==0.1.0','lxml==3.4.4','path.py==8.1.2','pexpect==4.0.1','pickleshare==0.5','ptyprocess==0.5','pycparser==2.14','python-dateutil==2.4.2','readline==6.2.4.1','requests==2.8.1','simplegeneric==0.8.1','six==1.10.0','traitlets==4.0.0','wheel==0.24.0','peewee==2.6.4','psycopg2==2.6.1','pymongo==2.8'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)