from setuptools import setup

def readme():
    with open("README.md") as f:
        README = f.read()
    return README

setup(
    name="EnergyTrendsDataDownloader",
    version="1.0.0",
    description="A demo package to automate the downloading and cleaning trend data from the UK Government's website",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    url="https://github.com/muyiwao/PetroineosSolution",
    author="muyiwa",
    author_email="muyirays@gmail.com"
)
