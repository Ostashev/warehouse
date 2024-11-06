FROM python:3.10-slim

RUN apt-get update
COPY . /opt
RUN chmod +x opt/docker-entrypoint.sh
WORKDIR /opt
RUN pip install -r requirements.txt
ENTRYPOINT ["/opt/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8089", "--reload"]