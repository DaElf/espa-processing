
# ==========+ Source Code dependencies +==========
FROM jbrinkmann/lagoon-water-dragon:devel-2.3.0.0 as application

RUN useradd espadev
WORKDIR /home/espadev/espa-processing
COPY setup.py version.txt README.md /home/espadev/espa-processing/
RUN pip install --trusted-host=pypi.python.org --no-cache-dir --upgrade pip \
    && pip install --trusted-host=pypi.python.org --no-cache-dir -e .

COPY ./processing/ /home/espadev/espa-processing/processing/
COPY ./run/ /home/espadev/espa-processing/run/

RUN mkdir -p /var/log/uwsgi \
    && chown -R espadev:espadev /var/log/uwsgi
ENV ESPA_PROCESSING_CONFIG_PATH=/home/espadev/espa-processing/run/config.ini \
    ESPA_PROCESSING_ENV="dev"

USER espadev
EXPOSE 8303 8304 8305
ENTRYPOINT ["uwsgi", "run/uwsgi.ini"]

# ==========+ Unit testing dependencies +==========
FROM python:3.6-slim  as tester

WORKDIR /home/espadev/espa-processing
COPY --from=application /home/espadev/espa-processing /home/espadev/espa-processing/
COPY --from=application /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

RUN pip install --trusted-host=pypi.python.org -e .[test]
COPY ./test/ ./test/
#    pylint --rcfile=.pylintrc api -f parseable -r n && \
#    mypy --silent-imports api && \
#    pycodestyle api --max-line-length=120 && \
#    pydocstyle api
ENTRYPOINT ["pytest", "--cov=./"]
