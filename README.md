# 🏥 VitalWatch

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=flat-square&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Multi-tenant](https://img.shields.io/badge/Architecture-Multi--tenant-purple?style=flat-square)

**Real-time multi-tenant patient monitoring for ICU and general wards.**

Any hospital can register, log in, and immediately start monitoring patients from any browser — no installation required. Patient admissions, vitals updates, and alerts broadcast instantly to every connected dashboard in the hospital via WebSocket.

---

## What it does

- **Any hospital can onboard in 30 seconds** — self-registration creates an isolated tenant with a full admin account
- **Live patient dashboard** — heart rate, SpO₂, blood pressure, respiratory rate, and temperature per bed, updating in real time
- **Instant admission broadcast** — when a nurse admits a patient, every screen in the hospital updates within 200ms, no refresh needed
- **Automated clinical alerts** — threshold-based alerts fire immediately when vitals go out of range, visible to all staff
- **Wearable device support** — connect any BLE heart rate monitor (Polar H10, Wahoo TICKR, Garmin HRM-Pro) directly from the browser via Web Bluetooth
- **Demo mode** — fully functional without any backend or hardware, for presentations and testing
- **Light / dark mode** — persists across sessions
- **Role-based access** — nurses, doctors, and admins each have scoped permissions
- **Fully isolated tenants** — hospitals share the server but never see each other's data

---

## Architecture

```
Browser (any hospital) ──HTTPS──► FastAPI Backend ──► PostgreSQL
                       ──WSS────►                 ──► Redis (pub/sub)
                                       │
                              JWT auth per tenant
                              hospital_id scopes all queries
```

Each hospital is a completely isolated tenant. `hospital_id` is enforced at the database query level on every table — patients, vitals, alerts, and staff.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vanilla HTML/CSS/JS — zero build step, single file |
| Backend | Python 3.11, FastAPI, WebSockets |
| Database | PostgreSQL + TimescaleDB (SQLite for local dev) |
| Auth | JWT (per-hospital tokens) |
| Device input | Web Bluetooth API (BLE Heart Rate Service) |
| Deployment | Docker Compose / Railway / Render |

---

## Getting Started

### Option A — Demo mode (no setup needed)

Open `frontend/index.html` in Chrome and click **"Skip login — use demo data"**. The full dashboard runs with simulated patients and a demo wearable mode.

### Option B — Run with the real backend

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/patient-monitor.git
cd patient-monitor
```

**2. Start the backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**3. Open the frontend**

Open `frontend/index.html` in Chrome. Enter `http://localhost:8000` as the API server, then register your hospital.

### Option C — Docker

```bash
docker-compose up -d
```

Starts the API, PostgreSQL, and Redis together.

---

## Hospital Onboarding

Any hospital can self-register at the login screen:

1. Click **Register Hospital**
2. Fill in hospital name, city, and admin credentials
3. Hit **Register & Sign In**

That's it. The hospital is live with a fully isolated tenant. To invite nurses and doctors:

```bash
POST /api/staff
{
  "email": "nurse@hospital.com",
  "password": "secure_password",
  "first_name": "Sarah",
  "last_name": "Jones",
  "role": "nurse"
}
```

---

## API Overview

Full interactive docs at `http://localhost:8000/docs` when running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/hospitals/register` | Register a new hospital (public) |
| `POST` | `/api/auth/login` | Staff login → returns JWT |
| `POST` | `/api/staff` | Invite a nurse or doctor (admin only) |
| `GET`  | `/api/patients` | List all active patients for this hospital |
| `POST` | `/api/patients` | Admit a patient → broadcasts to all dashboards |
| `DELETE` | `/api/patients/{id}` | Discharge a patient |
| `POST` | `/api/vitals` | Submit a vitals reading → triggers alert engine |
| `GET`  | `/api/vitals/{patient_id}` | Get vitals history (default 24h) |
| `GET`  | `/api/alerts` | List active alerts |
| `PUT`  | `/api/alerts/{id}/acknowledge` | Acknowledge an alert |
| `WS`   | `/ws/{hospital_id}?token=...` | Live event stream for a hospital |

---

## WebSocket Events

All connected dashboards in a hospital receive these events in real time:

| Event | Trigger | Payload |
|-------|---------|---------|
| `patient_admitted` | New patient admitted | Patient details + admitting staff name |
| `patient_discharged` | Patient discharged | `patient_id` |
| `vitals_update` | New vitals reading posted | Full vitals + new status + any alerts |
| `alert_acknowledged` | Alert acknowledged by staff | `alert_id` + staff name |

---

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Heart Rate | <60 or >100 bpm | <50 or >120 bpm |
| SpO₂ | <95% | <90% |
| Systolic BP | <90 or >140 mmHg | <80 or >160 mmHg |
| Temperature | >37.3°C | >38.5°C or <35°C |
| Respiratory Rate | <12 or >20 /min | <10 or >25 /min |

---

## Wearable Device Support

Click **Connect Device** in the dashboard to pair a Bluetooth heart rate monitor. Supported devices:

| Device | HR | RR Interval | Notes |
|--------|-----|-------------|-------|
| Polar H10 | ✅ | ✅ | Best accuracy, recommended |
| Wahoo TICKR | ✅ | ✅ | |
| Garmin HRM-Pro | ✅ | ✅ | |
| Any BLE HRS device | ✅ | ⚠️ | Standard heart rate service |
| Apple Watch | ❌ | ❌ | HR locked behind HealthKit |
| Fitbit | ❌ | ❌ | Proprietary protocol |

Requires **Chrome or Edge** on desktop or Android. Must be served over HTTPS or localhost.

---

## Deployment

### Recommended (Railway — free tier available)

```bash
# Push to GitHub, then connect repo to Railway
# Set environment variables:
DATABASE_URL=postgresql://...
JWT_SECRET=your_long_random_secret
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./vitalwatch.db` | Postgres recommended for production |
| `JWT_SECRET` | `change_me` | **Change this before deploying** |
| `JWT_EXPIRE_MINUTES` | `480` | Token lifetime in minutes |

---

## Project Structure

```
patient-monitor/
├── frontend/
│   └── index.html          # Entire frontend — single self-contained file
├── backend/
│   ├── main.py             # FastAPI app, all routes and WebSocket
│   ├── models.py           # SQLAlchemy multi-tenant models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── core/
│   │   ├── auth.py         # JWT creation and verification
│   │   ├── database.py     # DB engine and session
│   │   └── tenants.py      # WebSocket connection manager (per hospital)
│   ├── services/
│   │   └── alert_engine.py # Clinical threshold evaluation
│   └── requirements.txt
├── data/
│   ├── sample_patients.json
│   └── sample_vitals.csv
├── docs/
│   ├── API.md
│   └── SETUP.md
├── docker-compose.yml
├── .env.example
└── README.md
```
<img width="1055" height="540" alt="image" src="https://github.com/user-attachments/assets/1e771825-e973-4b4c-a8da-f2a3c0f8528a" />

---

## Disclaimer

This software is for **demonstration and educational purposes only**. It is not a certified medical device and must not be used for actual clinical patient care without proper regulatory validation and approval.

---

## License

MIT — see [LICENSE](LICENSE) for details.
