FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . /code
EXPOSE 8000
RUN chmod +x /code/start.sh
CMD ["sh", "/code/start.sh"]