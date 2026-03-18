# VitalWatch — Setup Guide

## Local Development

### 1. Clone & configure
```bash
git clone https://github.com/YOUR_USERNAME/patient-monitor.git
cd patient-monitor
cp .env.example .env
```

Edit `.env` and set a strong `JWT_SECRET`.

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API will be live at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

### 3. Frontend
Open `frontend/index.html` directly in your browser.  
No build step required.

---

## Docker (Recommended)

```bash
docker-compose up -d
```

This starts:
- **API** on port 8000
- **PostgreSQL + TimescaleDB** on port 5432
- **Redis** on port 6379
- **Nginx** reverse proxy on port 80

Check logs:
```bash
docker-compose logs -f api
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./vitalwatch.db` | Postgres or SQLite connection string |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection string |
| `JWT_SECRET` | `changeme` | Secret key for JWT signing — **change this** |
| `JWT_EXPIRE_MINUTES` | `480` | Token expiry in minutes |
| `ALERT_POLL_INTERVAL` | `5` | Seconds between alert checks |

---

## Database Migrations

The app uses SQLAlchemy with auto-create on startup (suitable for dev).  
For production, use Alembic:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## Production Deployment

### Recommended stack
- **Server**: AWS EC2 t3.small or DigitalOcean Droplet (2GB RAM)
- **Database**: AWS RDS PostgreSQL or Supabase
- **Reverse proxy**: Nginx with SSL (Let's Encrypt / Certbot)
- **Process manager**: systemd or Docker Compose with restart policies

### SSL with Certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Hardening checklist
- [ ] Change `JWT_SECRET` to a 64-char random string
- [ ] Set `DATABASE_URL` to a production PostgreSQL instance
- [ ] Enable HTTPS only (redirect HTTP → HTTPS in Nginx)
- [ ] Restrict CORS origins to your frontend domain
- [ ] Set up database backups (daily minimum)
- [ ] Enable firewall — only expose ports 80 and 443 publicly
