"""
Flask-Opsgenie
---------------

An easy to use Opsgenie extension for flask. Allows user
to raise an opsgenie alert on unwanted response status code,
increased response latency and on unhandled exception thrown
by routes.
With flask-opsgenie, you will no more have to add alerting
logic to your code manually, rather all you need to do is configure
this extension with different alert conditions and attributes.
"""

from setuptools import find_packages, setup

def get_dependencies():
  with open("requirements.txt") as req:
    lines = [line.strip() for line in req.readlines()]
    return lines

setup(
    name="Flask-Opsgenie",
    url="https://github.com/djmgit/flask-opsgenie",
    download_url="",
    license="",
    author="Deepjyoti Mondal",
    author_email="",
    description="Opsgenie extension for Flask",
    long_description=__doc__,
    zip_safe=False,
    platforms="any",
    packages=find_packages(),
    install_requires=get_dependencies(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: DevOps :: monitoring :: alerting :: Reliability',
    ],
    vcversioner={},
)
