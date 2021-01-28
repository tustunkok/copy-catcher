FROM python:3.8-buster

ARG CC_USER="copycat"
ARG CC_UID="1000"
ARG CC_GID="1000"

EXPOSE 8000

USER root

RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

COPY . /copy_catcher/

RUN chmod a+x /copy_catcher/start.sh && mkdir /copy_catcher/persist/
RUN pip install --no-cache-dir -r /copy_catcher/requirements.txt

RUN groupadd -g $CC_GID $CC_USER && \
    useradd -M -u $CC_UID -g $CC_GID -s /sbin/nologin $CC_USER && \
    chown -R $CC_USER:$CC_USER /copy_catcher/

WORKDIR /copy_catcher/

USER $CC_USER
CMD /bin/sh start.sh