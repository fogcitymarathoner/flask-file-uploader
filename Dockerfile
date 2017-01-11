FROM fogcitymarathoner/dockerfile-php5.6.22-python2.7.11

ENV PYTHONUNBUFFERED 1
ENV TERM=xterm

RUN apt-get update

# install flask
ADD requirements.txt .
RUN /usr/local/bin/pip install -r ./requirements.txt

# a couple of mount points to link volumes
RUN mkdir /php-apps
RUN mkdir /python-apps
RUN mkdir /sql
RUN mkdir /backups
# check python version
RUN which python
RUN python --version
RUN pip freeze
