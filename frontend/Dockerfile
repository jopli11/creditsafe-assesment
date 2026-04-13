# Dev-server image for the assessment: Vite on 0.0.0.0 so the host browser can reach
# the container. VITE_API_BASE_URL is set in Compose (browser → localhost:8000).

FROM node:22-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
