# Secure Login System

## Overview
Production-ready Flask web application with secure authentication, 2FA, and comprehensive security features.

## Features
- User registration with validation
- Bcrypt password hashing
- Rate limiting (5 attempts/5 min)
- Account lockout (15 min)
- Session management (30 min timeout)
- CSRF token protection
- 2FA with TOTP
- Secure session cookies
- SQL injection prevention

## Usage
```bash
python app.py
Visit: http://localhost:5000
```

## Test Credentials
- Username: testuser
- Password: TestPass@1234!

## Password Requirements
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Security Features
- HTTPOnly cookies
- Secure flag (HTTPS-ready)
- SameSite=Lax CSRF protection
- Parameterized queries (ORM)
- XSS protection (auto-escaping)

## Database
- SQLite (development)
- PostgreSQL (production)
- User model with security fields
