FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir --disable-pip-version-check --compile -r requirements.txt

# Install package
COPY . /usr/src/app
RUN pip install --no-cache-dir --disable-pip-version-check --compile -e .
