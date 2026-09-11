# 🚀 Deployment Guide - AI Stock Analysis Agent v1.0.0

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Monitoring & Logging](#monitoring--logging)
5. [Troubleshooting](#troubleshooting)

---

## Local Development

### Setup

```bash
# Clone repository
git clone https://github.com/dongsurya278-coder/stock-analysis-ai-agent.git
cd stock-analysis-ai-agent/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run migrations (if needed)
alembic upgrade head

# Start server
python -m uvicorn app.main:app --reload
```

Access:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Clone repository
git clone https://github.com/dongsurya278-coder/stock-analysis-ai-agent.git
cd stock-analysis-ai-agent

# Create .env file
cp backend/.env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t stock-agent:latest ./backend

# Run container
docker run -d \
  --name stock-agent \
  -p 8000:8000 \
  --env-file .env \
  stock-agent:latest

# View logs
docker logs -f stock-agent
```

---

## Production Deployment

### AWS EC2 Deployment

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone https://github.com/dongsurya278-coder/stock-analysis-ai-agent.git
cd stock-analysis-ai-agent
cp backend/.env.example .env
# Edit .env with production values

# Start services
docker-compose -f docker-compose.yml up -d
```

### Using Kubernetes

```bash
# Create namespace
kubectl create namespace stock-agent

# Create secrets
kubectl create secret generic stock-agent-secrets \
  --from-literal=anthropic-api-key=YOUR_KEY \
  --from-literal=iex-cloud-api-key=YOUR_KEY \
  -n stock-agent

# Deploy
kubectl apply -f k8s/deployment.yaml -n stock-agent
kubectl apply -f k8s/service.yaml -n stock-agent

# Check status
kubectl get pods -n stock-agent
kubectl get svc -n stock-agent
```

### Using Render.com

```yaml
# render.yaml
services:
  - type: web
    name: stock-agent-api
    runtime: docker
    dockerfilePath: ./backend/Dockerfile
    envVars:
      - key: DATABASE_URL
        value: postgresql://...
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: IEX_CLOUD_API_KEY
        sync: false
    healthCheckPath: /health
```

### Using Railway.app

```bash
# Install Railway CLI
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

## Monitoring & Logging

### Application Logs

```bash
# View logs
docker-compose logs -f backend

# Tail last 100 lines
docker-compose logs --tail=100 backend
```

### Database Monitoring

```bash
# Connect to PostgreSQL
psql -U stock_user -d stock_db -h localhost

# Check database size
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname))
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/api/v1/stocks
```

### Performance Monitoring

```bash
# CPU and Memory usage
docker stats stock-agent

# Application metrics
curl http://localhost:8000/metrics  # Prometheus format
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs backend

# Verify environment variables
docker-compose config | grep ANTHROPIC

# Check port availability
lsof -i :8000
```

### Database Connection Failed

```bash
# Check PostgreSQL container
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U stock_user -d stock_db -c "SELECT 1"

# Check DATABASE_URL format
echo $DATABASE_URL
```

### API Timeout Issues

```bash
# Check container logs for errors
docker-compose logs -f backend

# Increase timeout settings in .env
ANTHROPIC_TIMEOUT=60

# Restart service
docker-compose restart backend
```

### Memory Leaks

```bash
# Monitor memory usage
docker stats --no-stream

# Restart container if needed
docker-compose restart backend

# Check for connection leaks in logs
docker-compose logs backend | grep -i "connection"
```

---

## Performance Tuning

### Database Optimization

```sql
-- Create indexes for frequently queried fields
CREATE INDEX idx_stock_symbol ON stocks(symbol);
CREATE INDEX idx_signal_symbol ON buy_signals(symbol);
CREATE INDEX idx_price_timestamp ON stock_prices(timestamp);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM stock_prices WHERE symbol = 'AAPL';
```

### Application Tuning

```env
# Increase worker processes
WORKERS=8

# Enable connection pooling
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Set appropriate timeouts
REQUEST_TIMEOUT=30
DB_TIMEOUT=10
```

### Caching Strategy

```python
# Use Redis for caching
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

# Cache analysis results for 1 hour
redis_client.setex(f"analysis:{symbol}", 3600, json_result)
```

---

## Backup & Recovery

### Database Backup

```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U stock_user stock_db > backup.sql

# Restore from backup
cat backup.sql | docker-compose exec -T postgres psql -U stock_user stock_db
```

### Automated Backups

```bash
# Using cron job
0 2 * * * cd /path/to/stock-agent && docker-compose exec -T postgres pg_dump -U stock_user stock_db > /backups/stock_db_$(date +\%Y\%m\%d).sql
```

---

## Security Checklist

- [ ] Use environment variables for secrets
- [ ] Enable SSL/TLS for API
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Use strong database passwords
- [ ] Enable PostgreSQL authentication
- [ ] Rotate API keys regularly
- [ ] Use HTTPS in production
- [ ] Enable database encryption
- [ ] Set up firewall rules
- [ ] Monitor for suspicious activity
- [ ] Keep dependencies updated

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
      
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

### Vertical Scaling

```env
# Increase resources
WORKERS=16
DB_POOL_SIZE=50
DB_MAX_OVERFLOW=20
```

---

**Last Updated**: 2024
**Version**: 1.0.0
