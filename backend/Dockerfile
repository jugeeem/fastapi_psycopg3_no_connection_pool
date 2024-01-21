# Dockerfile
FROM python:3.12.1

WORKDIR /backend

COPY ./requirements.txt /backend
RUN pip install -r requirements.txt

COPY . /backend

WORKDIR /backend/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]