"""
Deployment Guide for Production
"""

# Production Deployment Guide for MR & ASM Reporting App Backend

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security dependencies updated
- [ ] SSL certificates obtained
- [ ] Database backups configured

## Environment Variables for Production

Create a .env file with:

```
# Database
DATABASE_URL=postgresql://prod_user:secure_password@prod_db_host:5432/mr_reporting_db
DATABASE_ECHO=False

# Security
SECRET_KEY=generate-secure-random-key-here
DEBUG=False

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

## Using Gunicorn (Recommended)

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

## Using Docker

Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t mr-asm-backend .
docker run -p 8000:8000 --env-file .env mr-asm-backend
```

## Using Nginx as Reverse Proxy

nginx.conf:
```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

## Monitoring and Logging

Setup log rotation:
```
/var/log/mr-asm-backend/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

## Database Backups

Automated daily backup:
```bash
# Add to crontab
0 2 * * * pg_dump -U postgres mr_reporting_db | gzip > /backups/mr_reporting_db_$(date +\%Y\%m\%d).sql.gz
```

## Health Checks

Setup periodic health checks:
```bash
curl -f http://localhost:8000/health || systemctl restart mr-asm-backend
```

Add to crontab:
```
*/5 * * * * /usr/local/bin/health_check.sh
```

## Performance Tuning

- Increase database connection pool
- Enable database query caching
- Use CDN for static files
- Implement rate limiting
- Setup load balancing for multiple instances

## Security Hardening

- Change default SECRET_KEY
- Update ALLOWED_ORIGINS
- Enable HTTPS only
- Setup firewall rules
- Keep dependencies updated
- Implement API rate limiting
- Add request validation
- Setup DDoS protection
