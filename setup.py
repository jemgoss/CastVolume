from setuptools import setup

setup(
    name="castvolume",
    version="0.0.1",
    author="Jeremy Goss",
    author_email="jem@goss-family.net",
    description="Simple Chromecast Audio volume control",
    url="https://github.com/jemgoss/CastVolume",
    #packages=setuptools.find_packages(),
    #packages=["castvolume"],
    install_requires=["PyChromecast"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
