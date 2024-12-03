import express from 'express';
import { createServer } from 'vite';
import { chatBackend } from './src/api/ChatBackend.js';

const app = express();
const port = 5137;

// Vite development server
async function startVite() {
  const vite = await createServer({
    server: { middlewareMode: true }, // Vite in middleware mode
  });

  // Define your API route
  app.use(express.json()); // To parse JSON request bodies
  app.post('/api/ChatBackend', chatBackend);
  app.get('/api/ChatBackend', chatBackend);


  // Use Vite's middleware to serve the frontend
  app.use(vite.middlewares);

  // Start the server
  console.log('Starting server...');
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
}

startVite();
