FROM python:3.9-slim-buster

RUN pip install fastapi==0.88.0 spacy==3.4.3 pymongo==4.3.3 transformers==4.25.1 tensorflow==2.11.0 torch==1.13.1 torchaudio==0.13.1 torchvision==0.14.1 sentencepiece==0.1.97 uvicorn==0.20.0 pyjwt==2.6.0 passlib==1.7.4 bcrypt==4.0.1 pytest==7.2.0 httpx==0.23.3
RUN python -m spacy download en_core_web_sm

COPY . /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
