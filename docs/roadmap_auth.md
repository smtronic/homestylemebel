# 🔐 Phase 4: Authentication & Security (JWT + Hardening)

**Goal:** Secure user authentication and protect access to sensitive endpoints (admin, orders, etc).

---

## 🔑 Basic Authentication

- **Endpoints:**

  - `POST /api/v1/auth/register/` - User registration
  - `POST /api/v1/auth/login/` - User login
  - `POST /api/v1/auth/refresh/` - Refresh JWT tokens
  - `POST /api/v1/auth/verify/` - Verify JWT tokens
  - `GET /api/v1/users/me/` - Fetch user profile
  - `PATCH /api/v1/users/me/` - Update user profile

- **Features:**

  - JWT authentication using `djangorestframework-simplejwt`
  - Protected API route access with JWT

- **Testing:**
  - Comprehensive tests for all endpoints

---

## 🛡 Security Hardening

- **Password Policy:**

  - Minimum length: **10+ characters**
  - Optional: Enforce digit, uppercase, and symbol requirements

- **Brute-Force Protection:**

  - Use `django-axes` to block repeated failed login attempts

- **Rate Limiting:**

  - Configure DRF throttling:
    - `AnonRateThrottle`
    - `UserRateThrottle`

- **CAPTCHA:**

  - Add CAPTCHA (e.g., `django-simple-captcha`) for multiple failed login attempts

- **Two-Factor Authentication (2FA):**

  - Use `django-two-factor-auth`
  - Enable for:
    - Admin panel
    - User login

- **Admin Access Restrictions:**

  - Require `is_staff` for `/admin/`
  - Restrict access by IP using NGINX or middleware
  - Enforce 2FA for staff users

- **Security Testing:**
  - Test cases for:
    - Failed logins
    - Blocked sessions
    - IP lockouts

---
