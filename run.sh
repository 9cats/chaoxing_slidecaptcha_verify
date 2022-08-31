#!/bin/bash

if [ -d "chaoxing_slidecaptcha_verify.pth" ]; then
  wget https://cdn.9cats.link/chaoxing_slidecaptcha_verify.pth
fi

pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
python3 server.py
