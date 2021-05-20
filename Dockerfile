FROM python:3.7-slim

EXPOSE 5000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["gunicorn", "--worker-class", "gevent", "--workers", "4", "--bind", "0.0.0.0:5000", "wsgi:app", "--max-requests", "10000", "--timeout", "5", "--keep-alive", "5", "--log-level", "info"]
