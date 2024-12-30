import express from 'express';
import { createServer } from 'vite';
import { ChatBackend } from './src/api/ChatBackend.js';
import { SummarizeContent } from './src/api/SummarizeContent.js';
import { ScenarioConfig } from './src/api/ScenarioConfig.js';
import { UploadImage } from './src/api/UploadImage.js';
import { login, logout, isAuthenticated } from './src/api/Authorization.js';

import cors from 'cors';
import session from 'express-session';
import bodyParser from 'body-parser';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();

app.use(session({
  secret: process.env.SESSION_SECRET || 'authorizeUserToAccessLearnEng',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // Set to true if using HTTPS
}));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors());

const port = 5137;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Serve static files from the 'public' directory
app.use('/public', express.static(path.join(__dirname, 'public')));

// Vite development server
async function startVite() {
  const vite = await createServer({
    server: { middlewareMode: true }, // Vite in middleware mode
  });

  // Define your API routes
  app.use(express.json()); // To parse JSON request bodies
  app.post('/api/ChatBackend', ChatBackend);
  app.get('/api/ChatBackend', ChatBackend);

  app.get('/api/SummarizeContent', SummarizeContent);
  app.post('/api/SummarizeContent', SummarizeContent);
  
  app.get('/api/ScenarioConfig', ScenarioConfig);
  app.post('/api/ScenarioConfig', ScenarioConfig);
  
  app.post('/api/UploadImage', UploadImage);

  app.post('/api/login', login);
  app.get('/api/logout', logout);

  app.use(vite.middlewares);

  // Apply authentication middleware before Vite middleware
  app.get('/editor_scenario_page.html', isAuthenticated, (req, res) => {
    res.sendFile(path.join(__dirname, 'editor_scenario_page.html'));
  });

  app.get('/scenario_configuration.html', isAuthenticated, (req, res) => {
    res.sendFile(path.join(__dirname, 'scenario_configuration.html'));
  });

  // Apply Vite middleware

  // Start the server
  console.log('Starting server...');
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
}

startVite();
