FROM python:3.9.16-alpine3.17

WORKDIR /app
COPY . .

RUN pip install -r requirements/prod.requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port 8000
