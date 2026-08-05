FROM node:18-alpine

WORKDIR /app

# Copy package configurations first to leverage Docker layer caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source files
COPY . .

EXPOSE 3001

CMD ["npm", "run", "dev"]
