FROM alpine:latest

RUN apk add curl

WORKDIR /app

COPY requete.json .

CMD ["curl", "-X", "POST", "-H", "Content-Type: application/json", "-d", "@requete.json", "http://localhost:8000/apirest/api/"]
