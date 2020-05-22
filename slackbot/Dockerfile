FROM python:3.8-slim
WORKDIR /slackbot
COPY requirements.txt /slackbot
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD . /slackbot
CMD ["python", "slackbot.py"]
