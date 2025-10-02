# Usa Node.js ufficiale
FROM node:18-alpine

# Imposta working dir
WORKDIR /app

# Copia prima i file di configurazione
COPY package.json package-lock.json* ./

# Installa dipendenze
RUN npm install

# Copia il resto del codice frontend
COPY . .

# Build app Next.js
RUN npm run build

# Espone porta Next.js
EXPOSE 3000

# Avvia in modalità produzione
CMD ["npm", "start"]
