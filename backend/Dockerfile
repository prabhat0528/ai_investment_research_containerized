FROM node:18-alpine

WORKDIR /app

# Copy package configurations first to leverage Docker layer caching
COPY package*.json ./

# Install production dependencies
RUN npm install

# Copy backend source files
COPY . .

ENV PORT=5000
EXPOSE 5000

# Container Healthcheck using the native /health route
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:5000/health || exit 1

CMD ["npm", "start"]
