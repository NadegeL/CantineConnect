# Use a base Node.js image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Update and upgrade the package list and installed packages
RUN apk update && apk upgrade

# Copy the package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install the dependencies with Yarn (puisque vous semblez préférer Yarn)
RUN yarn install
# Ajout des icônes Iconify
RUN yarn add -D @unocss/preset-icons @iconify-json/mdi @iconify-json/carbon
# Ajout de gsap
RUN yarn add gsap

# Copy the rest of the application files
COPY . .

# Expose the port on which the application will run
EXPOSE 5173

# Command to start the application
CMD ["yarn", "dev", "--host"]