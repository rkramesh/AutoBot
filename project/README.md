# AutoBot
Simple python Script to Send and Receive Meessage in whatsapp with Dictionary amd Amazon Price scrapper mode Enabled


# Usage
After Completing the Yowsup Installation run the run.py and start send/receive messages


# How to Use

## About Yowsup
Yowsup is a python library that allows you to login and use the WhatsApp(TM) service and provides you with all capabilities of an official WhatsApp(TM) client, allowing you to create a full-fledged custom WhatsApp(TM) client. Yowsup also comes with a cross platform command-line frontend called yowsup-cli which allows you to jump into connecting and using WhatsApp(TM) service directly from command line.

## Installation

 - Requires python2.6+, or python3.0 +
 - Required python packages: python-dateutil,
 - Required python packages for end-to-end encryption: protobuf, pycrypto, python-axolotl-curve25519
 - Required python packages for yowsup-cli: argparse, readline (or pyreadline for windows), pillow (for sending images)

Install using setup.py to pull all python dependencies, or using pip:

```
pip install yowsup2
```

### Linux

You need to have installed python headers (from probably python-dev package) and ncurses-dev, then run
```
python setup.py install
```
Because of a bug with python-dateutil package you might get permission error for some dateutil file called requires.txt when you use yowsup (see [this bug report](https://bugs.launchpad.net/dateutil/+bug/1243202)) to fix you'll need to chmod 644 that file.

### FreeBSD (*BSD)
You need to have installed: py27-pip-7.1.2(+), py27-sqlite3-2.7.11_7(+), then run
```
pip install yowsup2
```

### Mac
```
python setup.py install
```
Administrators privileges might be required, if so then run with 'sudo'

### Windows

 - Install [mingw](http://www.mingw.org/) compiler
 - Add mingw to your PATH
 - In PYTHONPATH\Lib\distutils create a file called distutils.cfg and add these lines:

```
[build]
compiler=mingw32
```
 - Install gcc: ```mingw-get.exe install gcc```
 - Install [zlib](http://www.zlib.net/)
 - ```python setup.py install```

If pycrypto fails to install with some "chmod error". You can install it separately using something like
```easy_install http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe```


## Usage
run the run.py
eg: python run.py


