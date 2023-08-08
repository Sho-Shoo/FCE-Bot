# Use an official Python runtime as a parent image
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code

EXPOSE 80

# RUN python -c "from fce_bot.db.fce_data_transform import transform_main; transform_main()"

ENTRYPOINT [ "gunicorn" ]

CMD ["-b", ":80", "-w", "4", "fce_bot.main:server"]