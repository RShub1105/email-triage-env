FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "email_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]