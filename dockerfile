FROM python:3.10-alpine
# Create app directory
WORKDIR /root/app
# Bundle app source
COPY detect.py server.py requirements.txt utils ./
# Install Dependancy
RUN pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
# Run the app
CMD python3 server.py
