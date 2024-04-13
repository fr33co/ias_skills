FROM python:3.10.12-alpine3.17

WORKDIR /app

COPY src src

RUN cd /app/src && pip install -r requirements.txt

EXPOSE 8085

ENTRYPOINT [ "python", "src/app.py", "--host=0.0.0.0" ]