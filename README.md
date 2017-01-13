flask-file-uploader
===================

## Description
File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.


## Running on docker host

```
[root@ip-172-30-0-153 ec2-user]# docker run -it --name fup-prod \
    -e FUP_SETTINGS=/config/fup.py \
    -e AWS_ACCESS_KEY_ID=XXX \
    -e AWS_BUCKET=fup-prod \
    -e AWS_SECRET_ACCESS_KEY=XXX \
    -e FUP_PORT=9194 \
    fogcitymarathoner/flask-file-s3-uploader:latest /docker-entrypoint.sh
 * Running on http://0.0.0.0:9194/ (Press CTRL+C to quit)
 * Restarting with stat

 * Debugger is active!
 * Debugger pin code: 169-850-938
```

### reusing stopped named container `fup-prod` 
```
[root@ip-172-30-0-153 ec2-user]# docker start fup-prod
fup-prod
[root@ip-172-30-0-153 ec2-user]# docker attach fup-prod
```

## Running locally built reusable container `fup-dev `
### as shell
```
docker run -it --name fup-dev \
    -e FUP_SETTINGS=/config/cors.py \
    -e AWS_ACCESS_KEY_ID=XXXXX \
    -e AWS_BUCKET=fup-cors \
    -e AWS_SECRET_ACCESS_KEY=XXX \
    -e FUP_PORT=9194 
    fogcitymarathoner/flask-file-s3-uploader:cors /bin/bash
root@775030dbe30f:/# python app.py
 * Running on http://0.0.0.0:9194/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 169-850-938
```
### reusing stopped named container `fup-dev` with development in progress
```
[root@ip-172-30-0-153 ec2-user]# docker start fup-dev
fup-dev
[root@ip-172-30-0-153 ec2-user]# docker attach fup-dev
root@775030dbe30f:/# 
