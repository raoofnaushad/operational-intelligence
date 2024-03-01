# Stage 1: Build the React application
FROM node:latest as build

# Accept build arguments
ARG REACT_APP_API_URL
ARG REACT_APP_TRANSCRIPT_URL

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Set environment variables
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
ENV REACT_APP_TRANSCRIPT_URL=${REACT_APP_TRANSCRIPT_URL}

# Build the app
RUN npm run build

# Stage 2: Serve the app using Nginx
FROM nginx:alpine

# Copy the build from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 9090
EXPOSE 9090

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
