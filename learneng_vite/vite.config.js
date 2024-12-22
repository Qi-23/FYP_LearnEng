import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import express from 'express';


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    middlewareMode: true,
    configureServer: ({ app }) => {
        const api = express();

        api.use(express.json());

        api.post('/api/ChatBackend', (req, res) => {
            const { message } = req.body;
            res.json({ response: `Received: ${message}` });
        });

        api.post('/api/SummarizeContent', (req, res) => {
            const { data } = req.body;
            res.json({ response: `Received: ${data}` });
        });

        api.post('/api/ScenarioConfig', (req, res) => {
            const { data } = req.body;
            res.json({ response: `Received: ${data}` });
        });

        // Use express as middleware in the Vite dev server
        app.use('/api', api);
    },
},
})
