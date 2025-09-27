FROM python:3.12

WORKDIR /usr/src/app

RUN pip install jupyterlab

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./data ./data
COPY med-chatbot.ipynb .