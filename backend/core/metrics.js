import client from 'prom-client';

// Collect default Node.js system and runtime metrics (memory heap, CPU, event loop lag, GC)
client.collectDefaultMetrics({
  prefix: 'investment_agent_',
  timeout: 5000
});

// Custom Metric 1: HTTP Request Duration in Seconds (Histogram)
export const httpRequestDurationSeconds = new client.Histogram({
  name: 'investment_agent_http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
});

// Custom Metric 2: Total HTTP Requests Processed (Counter)
export const httpRequestsTotal = new client.Counter({
  name: 'investment_agent_http_requests_total',
  help: 'Total number of HTTP requests processed by endpoint and status',
  labelNames: ['method', 'route', 'status_code']
});

// Custom Metric 3: Active AI Research Audits (Gauge)
export const activeResearchAudits = new client.Gauge({
  name: 'investment_agent_active_research_audits',
  help: 'Current number of active AI investment research audit pipelines running'
});

// Custom Metric 4: AI Model API Calls (Counter)
export const aiApiCallsTotal = new client.Counter({
  name: 'investment_agent_ai_api_calls_total',
  help: 'Total number of LLM API calls executed (Gemini / Groq)',
  labelNames: ['provider', 'model', 'status']
});

export default client;
