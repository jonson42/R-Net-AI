# Backend v2.0 - Quick Reference Card

## 🚀 Quick Start

```bash
# Start backend
cd r-net-backend
python3 main.py

# Backend URL: http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
```

## 📍 Endpoints

| Endpoint | Method | Auth Required | Purpose |
|----------|--------|---------------|---------|
| `/` | GET | No | Service info |
| `/health` | GET | No | Health check |
| `/generate` | POST | Yes* | Generate code |
| `/metrics` | GET | Yes | Performance metrics |
| `/cache/stats` | GET | Yes | Cache statistics |
| `/cache/clear` | POST | Yes | Clear cache |

*Auth required if `REQUIRE_API_KEY=True`

## 🔑 Authentication

```bash
# Add API key to requests
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8000/generate
```

## ⚙️ Configuration (.env)

### Essential Settings
```bash
OPENAI_API_KEY=sk-...          # Required
HOST=127.0.0.1
PORT=8000
DEBUG=False                     # Set False in production
```

### Rate Limiting
```bash
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=5        # Max 5 generations/min
```

### Caching
```bash
CACHE_ENABLED=True
CACHE_TTL_SECONDS=3600         # 1 hour
CACHE_MAX_SIZE=100             # 100 items
```

### Security
```bash
REQUIRE_API_KEY=True           # Enable in production
API_KEYS=key1,key2,key3        # Comma-separated
```

## 📊 Rate Limits (Default)

| Endpoint | Limit | Burst |
|----------|-------|-------|
| `/generate` | 5/min | 2 |
| `/health` | 60/min | 10 |
| Others | 30/min | 5 |

## 🎯 Error Codes

| Code | Meaning |
|------|---------|
| `ERR_4000` | Invalid input |
| `ERR_4001` | Invalid image |
| `ERR_4100` | Missing API key |
| `ERR_4101` | Invalid API key |
| `ERR_4290` | Rate limit exceeded |
| `ERR_5000` | OpenAI connection failed |
| `ERR_5100` | Generation failed |

## 📈 Key Metrics

```bash
# View metrics
curl http://localhost:8000/metrics

# Key metrics to watch:
# - cache.hit_rate_percent (target: >40%)
# - errors.error_rate_percent (target: <5%)
# - openai.success_rate_percent (target: >95%)
```

## 🧪 Quick Tests

### Test Health
```bash
curl http://localhost:8000/health
```

### Test Generation (with auth)
```bash
curl -X POST http://localhost:8000/generate \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "data:image/png;base64,...",
    "description": "Todo list app",
    "tech_stack": {
      "frontend": "React",
      "backend": "FastAPI",
      "database": "PostgreSQL"
    },
    "project_name": "todo-app"
  }'
```

### Test Rate Limiting
```bash
# Make 6 requests (limit is 5/min)
for i in {1..6}; do
  curl http://localhost:8000/health
done
# 6th should return 429
```

## 🔒 Security Checklist

### Development
- [ ] `DEBUG=True`
- [ ] `REQUIRE_API_KEY=False`
- [ ] Use default API key

### Production
- [ ] `DEBUG=False`
- [ ] `REQUIRE_API_KEY=True`
- [ ] Set strong `API_KEYS`
- [ ] Use HTTPS
- [ ] Configure CORS properly
- [ ] Monitor `/metrics` daily

## 💡 Performance Tips

### Optimize Cache Hit Rate
1. Increase `CACHE_TTL_SECONDS` to 7200 (2 hours)
2. Increase `CACHE_MAX_SIZE` to 500
3. Monitor with `/cache/stats`

### Reduce API Costs
1. Enable caching (saves 40-50%)
2. Adjust rate limits to control usage
3. Monitor `openai.estimated_cost_usd` in `/metrics`

### Improve Response Times
1. Cache hit: ~50ms (vs 3500ms)
2. Optimize prompts for shorter responses
3. Monitor `performance.avg_response_time_ms`

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
lsof -ti :8000 | xargs kill -9

# Check logs
tail -f logs/app.log
```

### Rate limited
```bash
# Wait for Retry-After seconds
# Or increase RATE_LIMIT_PER_MINUTE
```

### Cache not working
```bash
# Check cache stats
curl http://localhost:8000/cache/stats

# Verify CACHE_ENABLED=True in .env
# Check if requests are identical (same image + description)
```

### High error rate
```bash
# Check metrics
curl http://localhost:8000/metrics

# Review logs
tail -100 logs/app.log | grep ERROR

# Common issues:
# - Invalid OpenAI API key
# - Rate limit on OpenAI side
# - Invalid image format
```

## 📞 Support

### Documentation
- Full docs: `/BACKEND_ENHANCEMENTS_v2.0.md`
- API docs: `http://localhost:8000/docs`
- Modular prompts: `/MODULAR_PROMPT_QUICKSTART.md`

### Logs
```bash
# View live logs
tail -f r-net-backend/logs/app.log

# Search for errors
grep ERROR r-net-backend/logs/app.log
```

### Health Check
```bash
# Quick health check
curl http://localhost:8000/health | python3 -m json.tool

# Detailed health
curl http://localhost:8000/metrics | python3 -m json.tool
```

---

**Version**: 2.0.0  
**Last Updated**: November 8, 2025  
**Status**: ✅ Production Ready
