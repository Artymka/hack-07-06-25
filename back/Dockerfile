FROM python:3.13.2-alpine3.21

WORKDIR /workdir

COPY app.py /workdir
COPY requirements.txt /workdir

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "uvicorn",  "app:app" ]
CMD [ "--host", "0.0.0.0", "--port", "8080" ]