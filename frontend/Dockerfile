# Use the official Node.js image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /frontend

# Copy the package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . /frontend

# Expose the port where the app will run
EXPOSE 3000

# Command to serve the app
CMD ["npm", "start"]
