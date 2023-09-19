# pull official base image
FROM python:3.11.1-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# applicatin port
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]



