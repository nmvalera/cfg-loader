FROM python:3.6-alpine

RUN mkdir -p /usr/src/app/boilerplate_python
WORKDIR /usr/src/app

# Install the project in editable mode
COPY setup.py setup.cfg /usr/src/app/

ARG DEV=0
ENV DEV $DEV

RUN if [ $DEV = 1 ]; then pip install --no-cache-dir --disable-pip-version-check --compile -e .[dev]; else pip install --no-cache-dir --disable-pip-version-check --compile -e .; fi

# Copy scripts
COPY . /usr/src/app