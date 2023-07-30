# Use an official Python runtime as a parent image
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code

EXPOSE 8080

ENTRYPOINT [ "gunicorn" ]

CMD ["-b", "0.0.0.0:8080", "fce_bot.main:server"]