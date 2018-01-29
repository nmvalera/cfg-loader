FROM python:3.6-alpine

RUN mkdir -p /usr/src/app/boilerplate_python
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt setup.py /usr/src/app/
RUN pip install --no-cache-dir --disable-pip-version-check --compile -r requirements.txt

ARG DEV=0
ENV DEV $DEV

# Install the project as a package in editable mode
RUN if [ $DEV = 1 ]; then pip install --no-cache-dir --disable-pip-version-check --compile -e .[dev]; else pip install --no-cache-dir --disable-pip-version-check --compile -e .; fi

# Copy scripts
COPY . /usr/src/app