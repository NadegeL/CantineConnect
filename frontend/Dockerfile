# Utilisez une image de base Node.js
FROM node:20-alpine

# Définissez le répertoire de travail
WORKDIR /app

# Copiez le fichier package.json et yarn.lock
COPY package.json yarn.lock ./

# Installez les dépendances de base
RUN yarn install

# Installer tailwindcss, @tailwindcss/vite, ky et le plugin Vue
RUN yarn add tailwindcss @tailwindcss/vite ky
RUN yarn add @vitejs/plugin-vue --dev

# Copiez le reste des fichiers de l'application
COPY . .

# Exposez le port sur lequel l'application va tourner
EXPOSE 5173

# Commande pour démarrer l'application
CMD ["yarn", "dev"]
