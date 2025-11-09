FROM python:3.14.0-trixie 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./mysite/manage.py", "runserver", "0.0.0.0:8000"]
