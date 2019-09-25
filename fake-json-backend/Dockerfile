FROM node

RUN mkdir /code
WORKDIR /code

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3333

ENTRYPOINT [ "node", "index.js" ]