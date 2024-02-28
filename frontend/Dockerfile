FROM node:latest

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "serve", "--bind", "0.0.0.0:3000"]