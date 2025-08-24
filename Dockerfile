# Use official Nginx image as base
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy your static files into Nginx folder
COPY . /usr/share/nginx/html

# Expose port 80 to the outside
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
