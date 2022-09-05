FROM node:alpine3.16

WORKDIR /usr/src/client

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["sh", "entrypoint.sh"]