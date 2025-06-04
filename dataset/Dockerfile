FROM python:3.13.2-alpine3.21

WORKDIR /workdir

COPY . /workdir

RUN ls
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3",  "convert.py" ]