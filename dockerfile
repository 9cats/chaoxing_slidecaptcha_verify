FROM python:3.10.6-bullseye
# Create app directory
WORKDIR /root/app
# Bundle app source
COPY run.sh detect.py models.py server.py chaoxing_slidecaptcha_verify.cfg requirements.txt ./
COPY utils ./utils
# open port 3000
EXPOSE 8888
# Run the app
CMD bash run.sh
