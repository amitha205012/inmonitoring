# Security Toolkit Architecture

## System Design

```
┌─────────────────────────────────────────────────────────┐
│              Security Toolkit Suite                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Password   │  │ Vulnerability│  │   Phishing   │ │
│  │   Analyzer   │  │   Scanner    │  │  Detection   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │        Secure Login System (Flask)              │  │
│  ├──────────────────────────────────────────────────┤  │
│  │ Authentication │ Session Mgmt │ 2FA │ CSRF      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Database Layer (SQLAlchemy)          │  │
│  │  User Model │ Session Store │ Auth Tokens       │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Component Overview

### Module 1: Password Strength Analyzer
```
Input: Password String
  │
  ├─→ Length Check
  ├─→ Complexity Analysis
  ├─→ Pattern Detection
  ├─→ Entropy Calculation
  ├─→ Breach Database Check
  │
Output: PasswordAnalysis Object
  ├─ score (0-100)
  ├─ strength_level
  ├─ entropy
  ├─ issues
  └─ suggestions
```

### Module 2: Vulnerability Scanner
```
Input: Target IP/Host + Port List
  │
  ├─→ Port Scanning
  ├─→ Service Detection
  ├─→ SSL/TLS Validation
  ├─→ Vulnerability Mapping
  ├─→ Severity Classification
  │
Output: ScanResult Object
  ├─ open_ports
  ├─ vulnerabilities
  ├─ services_detected
  └─ scan_time
```

### Module 3: Phishing Detection
```
Input: Email Text
  │
  ├─→ URL Extraction & Analysis
  ├─→ Keyword Extraction
  ├─→ Spelling Check
  ├─→ Domain Validation
  ├─→ Feature Vectorization (TF-IDF)
  ├─→ ML Model Prediction
  │
Output: Classification
  ├─ label (Phishing/Legitimate)
  ├─ confidence (0-1)
  └─ features_importance
```

### Module 4: Secure Login System
```
Request
  │
  ├─→ Rate Limiter
  ├─→ CSRF Validator
  ├─→ Input Validator
  ├─→ Database Query (ORM)
  ├─→ Password Verification (Bcrypt)
  ├─→ Session Creation
  │
Response
  ├─ Success: Session Cookie + Redirect
  └─ Failure: Error Message + Status Code
```

## Data Flow

### User Registration Flow
```
┌─ User Form ─┐
│ Username    │
│ Email       │
│ Password    │
└─────────────┘
      │
      ├─→ Input Validation
      ├─→ Email Format Check
      ├─→ Username Uniqueness
      ├─→ Password Strength Check
      │
      ├─→ Hash Password (Bcrypt)
      ├─→ Create User Record
      ├─→ Store in Database
      │
      └─→ Redirect to Login
```

### User Login Flow
```
┌─ Login Form ─┐
│ Username     │
│ Password     │
└──────────────┘
      │
      ├─→ Rate Limit Check
      ├─→ CSRF Token Validation
      ├─→ Retrieve User
      ├─→ Password Verification
      │
      ├─→ Success:
      │   ├─→ Generate Session ID
      │   ├─→ Create Session Cookie
      │   ├─→ Update Last Login
      │   └─→ Redirect to Dashboard
      │
      └─→ Failure:
          ├─→ Increment Failed Attempts
          ├─→ Check Account Lock
          └─→ Display Error
```

## Security Layers

```
┌─────────────────────────────────────────┐
│      Application Security Layer         │
│  Input Validation, Output Encoding      │
├─────────────────────────────────────────┤
│    Authentication & Authorization       │
│  Sessions, Permissions, 2FA             │
├─────────────────────────────────────────┤
│      Transport Security Layer           │
│  HTTPS, Secure Cookies, HSTS            │
├─────────────────────────────────────────┤
│    Infrastructure Security Layer        │
│  Firewall, WAF, DDoS Protection         │
└─────────────────────────────────────────┘
```

## Database Schema

```sql
-- Users Table
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NOW(),
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1,
    totp_secret VARCHAR(32),
    totp_enabled BOOLEAN DEFAULT 0,
    failed_attempts INTEGER DEFAULT 0,
    account_locked_until DATETIME
);

-- Indices
CREATE INDEX idx_username ON user(username);
CREATE INDEX idx_email ON user(email);
```

## Technology Stack

### Backend
- **Framework:** Flask 2.3.3
- **Database:** SQLite (dev), PostgreSQL (prod)
- **ORM:** SQLAlchemy 2.0.21
- **Authentication:** Flask-Login, Flask-WTF

### Security
- **Password Hashing:** bcrypt 4.0.1
- **Cryptography:** cryptography 41.0.4
- **2FA:** pyotp 2.9.0, qrcode 7.4.2

### Machine Learning
- **ML Library:** scikit-learn 1.3.2
- **Data Processing:** pandas 2.1.1, numpy 1.26.1
- **Visualization:** matplotlib 3.8.1, seaborn 0.13.0

### Network Scanning
- **Scanning:** socket (Python stdlib)
- **SSL/TLS:** ssl (Python stdlib)

## Scalability Considerations

### Horizontal Scaling
- Stateless application design
- Database connection pooling
- Session store in Redis
- Load balancing with nginx/HAProxy

### Vertical Scaling
- Database optimization
- Query caching
- Asynchronous task processing
- Memory optimization

## Performance Targets

| Operation | Target | Measured |
|-----------|--------|----------|
| Password Analysis | <10ms | ~5ms |
| Login | <250ms | ~200ms |
| 2FA Verification | <100ms | ~75ms |
| Port Scan | 100+ ports/sec | ~120 ports/sec |
| Email Classification | <50ms | ~40ms |
