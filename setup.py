import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="twitter-analytics",
    version="0.1",
    author="Philippe Oger",
    author_email="phil.oger@gmail.com",
    description=("A twitter analytics reports downloader. The only way to get tweet impressions data with Python"),
    license="MIT",
    keywords="twitter analytics reports downloader",
    url="https://github.com/philippe2803/twitter-analytics-wrapper",
    packages=['twitter_analytics'],
    install_requires=[
        'selenium',
        'python-dateutil',
        'pyvirtualdisplay'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
