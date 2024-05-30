FROM dockerhub.timeweb.cloud/library/python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY app /usr/local/app
RUN pip install --upgrade pip \
    && pip install -r /usr/local/app/req.txt

RUN chmod a+x /usr/local/app/entrypoint.sh
ENTRYPOINT ["/usr/local/app/entrypoint.sh"]
