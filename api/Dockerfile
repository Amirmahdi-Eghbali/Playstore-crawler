FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=handler.settings

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]