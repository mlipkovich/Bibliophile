#!/usr/bin/env bash

cd ~
git clone https://github.com/mlipkovich/Bibliophile.git
cd Bibliophile/docker
sudo docker build -t bibliophile .
sudo docker run -v ~/Bibliophile/flask:/code/flask -p 5000:5000 --privileged --cap-add=ALL -t -d bibliophile /bin/bash