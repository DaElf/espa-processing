
# ==========+ Source Code dependencies +==========
FROM jbrinkmann/lagoon-water-dragon:devel-2.3.0.0 as application

RUN useradd espadev
RUN mkdir -p /var/log/uwsgi /home/espadev/espa-processing \
    && chown -R espadev:espadev /var/log/uwsgi \
    && chown -R espadev:espadev /home/espadev/espa-processing

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
FROM python:2.7-slim  as tester
RUN apt-get update && apt-get install -y gcc git

WORKDIR /home/espadev/espa-processing
COPY --from=application /home/espadev/espa-processing /home/espadev/espa-processing/
COPY --from=application /usr/lib/python2.7/site-packages /usr/lib/python2.7/site-packages
COPY --from=application  /usr/lib64/python2.7/site-packages  /usr/lib64/python2.7/site-packages

RUN pip install --no-cache-dir --process-dependency-links -e .[test]
COPY ./test/ ./test/
#    pylint --rcfile=.pylintrc api -f parseable -r n && \
#    mypy --silent-imports api && \
#    pycodestyle api --max-line-length=120 && \
#    pydocstyle api
ENTRYPOINT ["pytest", "--cov=./"]
