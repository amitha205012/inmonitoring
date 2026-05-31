# Production Deployment Guide

## Pre-Deployment Checklist

### Security
- [ ] Change SECRET_KEY to strong random value
- [ ] Set FLASK_DEBUG = False
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure secure session cookies
- [ ] Implement rate limiting at reverse proxy
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable CORS only if needed
- [ ] Review all environment variables

### Database
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Enable database encryption
- [ ] Create database indices

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Configure performance monitoring
- [ ] Set up security alerts
- [ ] Configure log aggregation

## Deployment Options

### Option 1: Heroku
```bash
# Install Heroku CLI
# heroku login
# heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

### Option 2: Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Option 3: Linux VPS
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv nginx gunicorn postgresql

# Create application user
sudo useradd -m -s /bin/bash security-app

# Deploy application
sudo -u security-app git clone <repo> /opt/security-app
cd /opt/security-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Configure nginx reverse proxy
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Option 4: AWS
```bash
# Using AWS Elastic Beanstalk
eb init
eb create security-app-env
eb deploy

# Using EC2
# Launch Ubuntu 20.04 LTS instance
# Follow Linux VPS steps above
```

## Production Environment Variables
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/securitytoolkit
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict
PERMANENT_SESSION_LIFETIME=1800
SERVER_NAME=yourdomain.com
```

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Monitoring & Maintenance

### Health Check
```bash
curl -I https://yourdomain.com/
# Should return 200 OK
```

### Backup
```bash
# Daily database backup
0 2 * * * pg_dump securitytoolkit > /backups/db-$(date +\%Y-\%m-\%d).sql
```

### Logs
```bash
# View application logs
journalctl -u gunicorn -f

# View nginx logs
tail -f /var/log/nginx/error.log
```

## Performance Optimization

### Database Optimization
- Enable connection pooling
- Create appropriate indices
- Use query caching
- Regular VACUUM and ANALYZE

### Application Optimization
- Enable gzip compression
- Use CDN for static files
- Implement caching headers
- Use sessions wisely

## Security Hardening

### System Level
- Keep OS updated
- Use firewall (ufw)
- Configure fail2ban
- Disable unnecessary services

### Application Level
- Use HTTPS only
- Enable HSTS header
- Configure CSP headers
- Implement rate limiting
- Use security headers

## Rollback Procedure
```bash
git revert <commit-hash>
git push production main
sudo systemctl restart gunicorn
```
