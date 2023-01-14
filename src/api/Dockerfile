FROM python:3.9-slim-buster

RUN pip install fastapi==0.88.0 spacy==3.4.3
RUN python -m spacy download en_core_web_sm

COPY . /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]