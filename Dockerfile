FROM python:slim-bullseye

LABEL version="1.0"

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
COPY . /opt/app

CMD ["python3", "/opt/app/get.py"]
