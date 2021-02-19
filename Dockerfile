FROM python:3.9.1-alpine3.13

RUN apk update && \
    apk upgrade && \
    apk add --no-cache gcc \
                    libc-dev
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "-m", "main.py"]