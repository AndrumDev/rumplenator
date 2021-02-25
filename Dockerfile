FROM python:3.9.1-alpine3.13

RUN apk update && \
    apk upgrade && \
    apk add --no-cache gcc \
                    libc-dev
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Required by Elastic Beanstalk environment.
# A healthcheck endpoint is exposed at localhost:9000/health
EXPOSE 9000

ENTRYPOINT [ "python", "-m" ]
CMD ["main.py" ]
