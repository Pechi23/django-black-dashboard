# FROM python:3.9

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY requirements.txt .
# # install python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # running migrations
# RUN python manage.py migrate

# # gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000

# runs the production server
# ENTRYPOINT ["python", "mysite/manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]