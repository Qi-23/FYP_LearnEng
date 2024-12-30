import express from 'express';
import fs from 'fs';
import { createServer } from 'vite';
import { ChatBackend } from './src/api/ChatBackend.js';
import { SummarizeContent } from './src/api/SummarizeContent.js';
import { ScenarioConfig } from './src/api/ScenarioConfig.js';
import { login, logout, isAuthenticated, isNotAuthenticated } from './src/api/Authorization.js';

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
const port = 5137;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Vite development server
async function startVite() {
  const vite = await createServer({
    server: { middlewareMode: true }, // Vite in middleware mode
  });

  app.use(cors());

  // Define your API route
  app.use(express.json()); // To parse JSON request bodies
  app.post('/api/ChatBackend', ChatBackend);
  app.get('/api/ChatBackend', ChatBackend);

  app.get('/api/SummarizeContent', SummarizeContent);

  app.get('/api/ScenarioConfig', ScenarioConfig);
  app.post('/api/ScenarioConfig', ScenarioConfig);

  app.post('/api/login', login);
  app.get('/api/logout', logout);

  app.get('/editor_scenario_page.html', isAuthenticated, (req, res) => {
    res.sendFile('/editor_scenario_page.html', { root: __dirname });
  });

  app.get('/scenario_configuration.html', isAuthenticated, (req, res) => {
    vite.transformIndexHtml(req.url, fs.readFileSync(path.resolve(__dirname, 'scenario_configuration.html'), 'utf-8'))
    .then((transformedHtml) => {
      res.status(200).set({ 'Content-Type': 'text/html' }).send(transformedHtml);
    })
    .catch((err) => {
      console.error('Error during HTML transformation', err);
      res.status(500).send('Internal Server Error');
    });
  });

  app.get('/editor-login.html', isNotAuthenticated, (req, res) => {
    res.sendFile('/editor-login.html', { root: __dirname });
  });

  app.use(vite.middlewares);

  // Start the server
  console.log('Starting server...');
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
}

startVite();
