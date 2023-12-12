# base image  
FROM python:3.11.2 

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip  

WORKDIR /notes_service

RUN mkdir -p /notes_service

COPY . /notes_service

RUN pip install -r requirements.txt && python manage.py makemigrations && python manage.py migrate
EXPOSE 8000  

# start server  
# CMD python manage.py runserver 0.0.0.0:8000

# docker build . -t secret_service
# docker run -p 8000:8000 -d secret_service
# http://localhost:8000/

# docker-compose up --build 