# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#RUN chmod 755 entrypoint.sh
# copy project
COPY . .
RUN chmod +x /usr/src/app/entrypoint.sh

# Expose the port
EXPOSE 8000

# Run Gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application", "--workers", "3","--timeout","120"]