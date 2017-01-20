flask-file-uploader
===================

## Description
File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.

## Prerequesites
Any bucket that can be trashed to be used as the HEALTHCHECK_TEST_BUCKET.  It's only used as a preflight on credentials.

### CORS Bucket Restrictions
Theses are the CORS permissions that should be at the bucket
```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>http://54.191.47.109:9194</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedMethod>DELETE</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
    <CORSRule>
        <AllowedOrigin>http://*.sfblur.com</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedMethod>DELETE</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>

```
## Running on docker host

```
[root@ip-172-30-0-153 ec2-user]# docker run -it --name fup-prod \
    -e FUP_SETTINGS=/config/fup.py \
    -e AWS_ACCESS_KEY_ID=XXX \
    -e AWS_BUCKET=fup-prod \
    -e AWS_SECRET_ACCESS_KEY=XXX \
    -e FUP_PORT=9191 \
    -e BRANCH=master \
    -e HEALTHCHECK_TEST_BUCKET=some-bucket-that-can-be-trashed \
    fogcitymarathoner/flask-file-s3-uploader:latest /docker-entrypoint.sh
Using boto version 2.40.0
<Bucket: terraverde-fup>
Servicing S3 Bucket terraverde-fup Branch master
Uploading to S3 Folder upload
 * Running on http://0.0.0.0:9191/ (Press CTRL+C to quit)
 * Restarting with stat
Using boto version 2.40.0
<Bucket: terraverde-fup>
Servicing S3 Bucket terraverde-fup Branch s3-test
Uploading to S3 Folder upload-s3-test
 * Debugger is active!
 * Debugger pin code: 856-804-685
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
    -e BRANCH=master \
    -e HEALTHCHECK_TEST_BUCKET=some-bucket-that-can-be-trashed \
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
