FROM python:3.7

RUN apt-get update \
    && apt-get install -y \
        postgresql-client \
        libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN pip install --upgrade pip
# Install Django
RUN pip install django
RUN pip install djangorestframework
RUN pip install pygments
RUN pip install django-cors-headers
RUN pip install --upgrade git+https://github.com/seungjinhan/python_jimmy_util.git

# Install additional libraries
RUN pip install numpy
RUN pip install pandas
RUN pip install sklearn

WORKDIR /usr/src/app

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]