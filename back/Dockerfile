FROM python:3.13.2-alpine3.21

WORKDIR /workdir

COPY ./app/ /workdir/app/
COPY ./ml/ /workdir/ml/
COPY ./requirements.txt /workdir/

RUN pip install -r requirements.txt
# RUN ls && cd app && ls

ENTRYPOINT [ "uvicorn",  "app.app:app" ]
CMD [ "--host", "0.0.0.0", "--port", "8000" ]