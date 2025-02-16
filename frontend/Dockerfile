# Use a base Node.js image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Update and upgrade the package list and installed packages
RUN apk update && apk upgrade

# Copy the package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install the base dependencies
RUN yarn install

# Copy the rest of the application files
COPY . .

# Expose the port on which the application will run
EXPOSE 5173

# Command to start the application
CMD ["yarn", "dev", "--host"]
