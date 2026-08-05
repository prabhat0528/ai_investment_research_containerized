FROM node:18-alpine

WORKDIR /app

# Copy package configurations first to leverage Docker layer caching
COPY package*.json ./

# Install dependencies (including devDependencies if needed for build/start)
RUN npm install

# Copy backend source files
COPY . .

EXPOSE 5005

CMD ["npm", "start"]
