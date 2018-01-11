# TODO: Do not run pip install on each docker run; use absolute paths

FROM ubuntu:16.04

RUN apt-get update -qq && \
    apt-get upgrade -qqy

RUN apt-get install -qqy python3=3.5.* \
    python3-dev=3.5.* \
    python3-pip \
    python-virtualenv \
    nginx=1.10.*

# Configure nginx
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default
ADD ./nginx/bibliophile /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/bibliophile /etc/nginx/sites-enabled
RUN service nginx reload

EXPOSE 5000

ADD ./start.sh /code/start.sh
WORKDIR /code
RUN chmod +x ./start.sh
ENTRYPOINT ["/bin/bash", "./start.sh"]
