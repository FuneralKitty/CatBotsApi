FROM python:3.12
WORKDIR /app
COPY requirements.txt /app
RUN sudo apt install gunicorn
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app