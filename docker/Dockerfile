FROM ubuntu:20.04

COPY files/requirements.txt /tmp/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3.8 \
       python3-pip \
       libcairo2 \
       libcairo-gobject2 \
       libpango-1.0-0 \
       libpangocairo-1.0-0 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --config python \
    && pip3 install -r /tmp/requirements.txt \
    && pip3 install gunicorn \
    && adduser --system --group --home /web dummy

COPY files/web/ /web

USER dummy
WORKDIR /web
#RUN flask db upgrade
EXPOSE 5000

ENTRYPOINT ["gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "server:app"]
