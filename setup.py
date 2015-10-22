import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='nyt-ap-elections',
    version='0.0.4',
    author='Jeremy Bowers',
    author_email='jeremy.bowers@nytimes.com',
    url='https://github.com/newsdev/nyt-ap-elections',
    description='Python client for parsing the Associated Press\'s elections API.',
    long_description=read('README.rst'),
    packages=['elex'],
    license="Apache License 2.0",
    keywords='election race candidate democracy news associated press',
    install_requires=['cffi==1.3.0','greenlet==0.4.7','python-dateutil==2.4.2','readline==6.2.4.1','requests==2.8.1','six==1.10.0','wheel==0.24.0'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)