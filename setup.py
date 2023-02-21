from setuptools import setup

setup(
    name="EnergyTrendsDataDownloader",
    version="1.0.1",
    description="A demo package to automate the downloading and cleaning trend data from the UK Government's website",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/muyiwao/PetroineosSolution",
    author="Muyiwa O",
    author_email="muyirays@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["EnergyTrendsDataDownloader"],
    include_package_data=True,
    python_requires=">=3.0",
)
