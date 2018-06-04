
# ==========+ Source Code dependencies +==========
FROM usgseros/espa-dockerfiles:docker-devel-3.0rc1.dev1 as application

RUN useradd espadev
RUN mkdir -p /var/log/uwsgi /home/espadev/espa-processing \
    && chown -R espadev:espadev /var/log/uwsgi

WORKDIR /home/espadev/espa-processing
COPY setup.py version.txt README.md /home/espadev/espa-processing/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --process-dependency-links -e .

ENV ESPA_PROC_CFG_FILENAME=/home/espadev/espa-processing/run/config.ini \
    ESPA_PROC_ENV="dev"

USER espadev
EXPOSE 8303 8304 8305

COPY ./run/ /home/espadev/espa-processing/run/
COPY ./processing/ /home/espadev/espa-processing/processing/

ENTRYPOINT ["uwsgi", "run/uwsgi.ini"]

# ==========+ Unit testing dependencies +==========
FROM application  as tester
USER root
RUN pip install -U --no-cache-dir -e .[test]

COPY ./test/ ./test/
ENTRYPOINT ["pytest", "--cov=./"]
