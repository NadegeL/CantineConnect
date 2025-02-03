FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache python3 make g++

COPY package*.json yarn.lock ./

RUN yarn install

RUN yarn add -D tailwindcss postcss autoprefixer

COPY . .

EXPOSE 5173

CMD ["yarn", "dev", "--host", "0.0.0.0"]