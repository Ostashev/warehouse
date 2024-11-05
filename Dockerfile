FROM python:3.10-slim

RUN apt-get update
COPY . /opt
WORKDIR /opt
RUN pip install -r requirements.txt
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8089", "--reload"]