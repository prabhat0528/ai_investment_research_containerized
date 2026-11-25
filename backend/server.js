import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { initDb } from './core/db.js';
import client, { httpRequestDurationSeconds, httpRequestsTotal } from './core/metrics.js';
import authRouter from './routes/auth.js';
import researchRouter from './services/auditor/routes/research.js';
import bookmarksRouter from './services/auditor/routes/bookmarks.js';
import notificationsRouter from './services/auditor/routes/notifications.js';
import chatRouter from './services/chat/routes/chat.js';
import { startNotificationScheduler } from './services/auditor/utils/notificationScheduler.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Prometheus HTTP Request Telemetry Middleware
app.use((req, res, next) => {
  if (req.path === '/metrics') return next();
  const start = process.hrtime();
  res.on('finish', () => {
    const diff = process.hrtime(start);
    const durationInSeconds = diff[0] + diff[1] / 1e9;
    const rawRoute = req.route ? req.route.path : req.path;
    const cleanRoute = (req.baseUrl || '') + (rawRoute || '').replace(/\/[0-9a-fA-F-]{10,}/g, '/:id').replace(/\/\d+/g, '/:id');
    httpRequestDurationSeconds.observe(
      { method: req.method, route: cleanRoute || req.path, status_code: res.statusCode },
      durationInSeconds
    );
    httpRequestsTotal.inc(
      { method: req.method, route: cleanRoute || req.path, status_code: res.statusCode }
    );
  });
  next();
});

// API Routes
app.use('/api/auth', authRouter);
app.use('/api', researchRouter);
app.use('/api', bookmarksRouter);
app.use('/api', notificationsRouter);
app.use('/api', chatRouter);

// Basic health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'AI Investment Research API is healthy' });
});

// Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', client.register.contentType);
    res.end(await client.register.metrics());
  } catch (err) {
    res.status(500).send(err.message);
  }
});

// Initialize database and start server
const startServer = async () => {
  try {
    // Initialize PostgreSQL tables
    try {
      await initDb();
    } catch (dbError) {
      console.error('[Database] Warning: Failed to connect to database or initialize tables. Database features (auth, bookmarks, reports) may fail, but server is starting:', dbError.message || dbError);
    }

    // Start server
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
      // Start background news polling scheduler
      try {
        startNotificationScheduler();
      } catch (schedError) {
        console.error('Failed to start background scheduler:', schedError);
      }
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
};

startServer();
