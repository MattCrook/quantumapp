FROM node:12

# WORKDIR /quantumadminapp
WORKDIR /usr/source/app/quantumadminapp

COPY package.json .

# RUN npm ci
RUN npm install

COPY . .

# ENV API_URL=http://localhost:8000

# EXPOSE 8000

CMD ["npm", "run", "watch"]
