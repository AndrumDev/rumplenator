FROM python:3.9.1-alpine3.13

ARG TMI_TOKEN
ARG CLIENT_ID
ENV TMI_TOKEN=$TMI_TOKEN
ENV CLIENT_ID=$CLIENT_ID

RUN apk update && \
    apk upgrade && \
    apk add --no-cache gcc \
                    libc-dev
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Running on Elastic Beanstalk requires that we expose a port because
# it expects to host a web server application.
# We should move away from Beanstalk but it's a lot of faff to configure
# the EC2 instance & run the application instance manually
EXPOSE 9000

CMD ["python", "-m", "main.py"]
