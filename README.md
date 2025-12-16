# CastVolume

A simple Chromecast Audio volume control written in python.

## TODO:
Needs a proper installation and setup.

## Building

```shell
$ python -m venv ~/venv
$ ~/venv/bin/pip wheel -w dist --no-deps .
```

## Installing

It's best to use my cleaned up pychromecast lib.

Choose one of the following method:
```shell
$ ~/venv/bin/pip install -e ~/PyChromecast
$ ~/venv/bin/pip install -e .

$ ~/venv/bin/pip install ~/PyChromecast/dist/pychromecast*
$ ~/venv/bin/pip install dist/castvolume*

$ ~/venv/bin/pip install /mnt/Public/repo/python/pychromecast*
$ ~/venv/bin/pip install /mnt/Public/repo/python/castvolume*

$ ~/venv/bin/pip install https://github.com/jemgoss/pychromecast/releases/download/14.0.9/pychromecast-14.0.9-py2.py3-none-any.whl
$ ~/venv/bin/pip install https://github.com/jemgoss/CastVolume/releases/download/v0.0.2/castvolume-0.0.2-py3-none-any.whl
```

Optionally:
```shell
$ mkdir -p ~/.local/share/applications/
$ cp castvolume.desktop ~/.local/share/applications/
```

## Running
```shell
$ ~/venv/bin/python -m castvolume
```
