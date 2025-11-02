FROM python:3.9-slim

WORKDIR /app

COPY main.py .

RUN pip install flask

RUN pip install flask_cors

EXPOSE 8000

CMD ["python", "main.py"]
