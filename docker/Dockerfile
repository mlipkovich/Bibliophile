FROM ubuntu:16.04

RUN apt install -y python3=3.5.* \
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

# Configure script for running the gunicorn
WORKDIR /srv/app
ADD ./start.sh /srv/start.sh
RUN chmod +x /srv/start.sh

ENTRYPOINT ["/bin/bash", "/srv/start.sh"]