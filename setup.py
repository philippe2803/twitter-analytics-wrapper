import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="twitter-analytics",
    version="0.0.6",
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
    long_description=read('README')
)
