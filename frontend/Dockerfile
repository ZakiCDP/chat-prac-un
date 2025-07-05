FROM node:16-alpine

WORKDIR /app

# Кэшируем зависимости отдельным слоем
COPY package.json package-lock.json ./
RUN npm install --silent

COPY . .

CMD ["npm", "start"]