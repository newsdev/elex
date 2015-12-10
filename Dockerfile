FROM python:3.5
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install --no-cache-dir ./
ENTRYPOINT ["/usr/local/bin/elex"]
