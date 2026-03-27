FROM python:3.10

WORKDIR /app

COPY . .

# ✅ Install all required dependencies
RUN pip install fastapi uvicorn openenv

CMD ["uvicorn", "email_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
