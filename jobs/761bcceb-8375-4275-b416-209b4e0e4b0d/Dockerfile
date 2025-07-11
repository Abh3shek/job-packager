FROM python:3.10-slim

WORKDIR /app
COPY code/ /code
COPY data/ /data
COPY run.sh/ /run.sh

RUN chmod +x /run.sh

CMD ["sh", "/run.sh"]