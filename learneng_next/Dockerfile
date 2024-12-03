# Use Node.js image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json yarn.lock ./

RUN yarn install

# Copy Next.js app code
COPY . .

# Expose port 3000 for the Next.js app
EXPOSE 3000

# Run the Next.js app
CMD ["yarn", "dev"]