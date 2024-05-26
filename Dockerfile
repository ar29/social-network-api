FROM python:alpine3.15

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apk add -u gcc musl-dev
RUN pip install -r requirements.txt


COPY . .
RUN python manage.py makemigrations users

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
