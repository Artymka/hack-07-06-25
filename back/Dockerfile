FROM python:3.13.2-alpine3.21

WORKDIR /workdir

COPY ./app/app.py /workdir
COPY requirements.txt /workdir

RUN pip install -r requirements.txt

ENTRYPOINT [ "uvicorn",  "app:app" ]
CMD [ "--host", "0.0.0.0", "--port", "8000" ]