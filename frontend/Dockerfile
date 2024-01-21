FROM node:18.16.1-alpine

WORKDIR /frontend

COPY ./frontend/package*.json ./
RUN npm install

COPY ./frontend .

EXPOSE 3000

ENTRYPOINT ["npm", "start"] 