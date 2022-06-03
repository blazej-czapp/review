FROM alpine:3.16

COPY python_requirements.txt .

RUN apk update \
    && apk upgrade --available \
    && apk add --update python3 py3-pip sqlite \
    && pip install -r python_requirements.txt

COPY docker_entrypoint.sh /bin/
RUN chmod +x /bin/docker_entrypoint.sh

COPY init_dev.sh /bin/
RUN chmod +x /bin/init_dev.sh

WORKDIR /review

# usage for dev server (under review/docker workdir)
#
# build:
# docker build -t review .
#
# initial setup (database, superuser etc.):
# docker run --rm -it -v /path/to/review:/review review /bin/init_dev.sh
#
# run dev server:
# docker run --rm -it -v /path/to/review:/review -p 8000:8000 review

CMD ["/usr/bin/python3", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/bin/docker_entrypoint.sh"]
