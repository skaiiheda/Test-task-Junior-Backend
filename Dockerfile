FROM python:3.14

ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY backendTestTask .

CMD ["gunicorn", "backendTestTask.wsgi:application", "--bind", "0.0.0.0:8000"]
