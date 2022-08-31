FROM python:3.10.6-bullseye
# Create app directory
WORKDIR /root/app
# Bundle app source
COPY detect.py models.py server.py chaoxing_slidecaptcha_verify.cfg chaoxing_slidecaptcha_verify.pth requirements.txt ./
COPY utils ./utils
# Install Dependancy
# RUN pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
# open port 3000
EXPOSE 8888
# Run the app
CMD pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple && python3 server.py
