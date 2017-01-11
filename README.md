flask-file-uploader
===================

## Description
File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.


## Setup

Install system package. See the `system_package.txt` file

Create virtual env and install python packages

```
$ sudo pip install virtualenv
$ cd flask-file-uploader/
$ virtualenv flask
$ flask/bin/pip install -r requirements.txt
```

Now you can run application by command `./app.py`

Running locally built container

```
[root@ip-172-30-0-153 flask-file-uploader]# docker run --rm -it fup /bin/bash
 * Running on http://127.0.0.1:9191/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 289-535-189
```

