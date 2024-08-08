FROM python:3.12
WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["gunicorn", "main", "--w", "1", "--b", "0.0.0.0:8000"]

EXPOSE 8000
