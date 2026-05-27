FROM node:18-alpine

WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Copy configuration metadata
COPY package.json ./

# 🛠️ THE CACHE-BUSTER FIX: Force clean download of packages directly from npm registry
RUN npm set progress=false && npm install

# Copy the source code matrix
COPY . .

# Run the build (Next is now guaranteed to be found)
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]