# VitalWatch — API Reference

Base URL: `http://localhost:8000`  
Interactive docs (Swagger): `http://localhost:8000/docs`  
ReDoc: `http://localhost:8000/redoc`

---

## Authentication

All endpoints (except `/health`) require a JWT bearer token.

```
Authorization: Bearer <token>
```

Obtain a token via `POST /auth/login` with your credentials.

---

## Patients

### `GET /api/patients`
List all patients. Optional query params:
- `ward` — filter by ward name (e.g. `ICU-A`)
- `status` — filter by `stable`, `warning`, or `critical`

**Response**
```json
[
  {
    "id": 1,
    "mrn": "MRN10001",
    "first_name": "James",
    "last_name": "Harlow",
    "date_of_birth": "1957-03-14T00:00:00",
    "gender": "M",
    "bed_number": "Bed 1",
    "ward": "ICU-A",
    "status": "critical",
    "attending_physician": "Dr. Chen",
    "admitted_at": "2026-03-10T08:22:00"
  }
]
```

---

### `GET /api/patients/{id}`
Get a single patient record by ID.

---

### `POST /api/patients`
Admit a new patient.

**Request body**
```json
{
  "mrn": "MRN10013",
  "first_name": "Anna",
  "last_name": "Fischer",
  "date_of_birth": "1979-06-15",
  "gender": "F",
  "bed_number": "Bed 13",
  "ward": "ICU-A",
  "attending_physician": "Dr. Patel"
}
```

---

### `PUT /api/patients/{id}`
Update a patient record (transfer wards, update notes, etc.)

---

### `DELETE /api/patients/{id}`
Discharge a patient (soft delete — record is retained).

---

## Vitals

### `GET /api/vitals/{patient_id}`
Retrieve vitals history for a patient.

Query params:
- `hours` — lookback window in hours (default: 24)
- `limit` — max readings to return (default: 500)

**Response**
```json
[
  {
    "id": 1,
    "patient_id": 1,
    "recorded_at": "2026-03-17T08:00:00",
    "heart_rate": 128,
    "spo2": 88.0,
    "systolic_bp": 162,
    "diastolic_bp": 98,
    "respiratory_rate": 26,
    "temperature": 38.9,
    "recorded_by": "device-monitor-1"
  }
]
```

---

### `POST /api/vitals`
Submit a new vitals reading. Automatically triggers the alert engine.

**Request body**
```json
{
  "patient_id": 4,
  "heart_rate": 68,
  "spo2": 98.0,
  "systolic_bp": 112,
  "diastolic_bp": 70,
  "respiratory_rate": 14,
  "temperature": 36.5,
  "recorded_by": "nurse-station-2"
}
```

---

## Alerts

### `GET /api/alerts`
List alerts. Query params:
- `patient_id` — filter to one patient
- `severity` — `info`, `warning`, or `critical`
- `acknowledged` — `true` or `false` (default: `false`)

**Response**
```json
[
  {
    "id": 12,
    "patient_id": 1,
    "severity": "critical",
    "metric": "heart_rate",
    "message": "Heart Rate critically high: 128 bpm",
    "value": 128,
    "threshold": 120,
    "triggered_at": "2026-03-17T08:00:05",
    "acknowledged": false
  }
]
```

---

### `PUT /api/alerts/{id}/acknowledge`
Acknowledge an alert. Pass `acknowledged_by` as a query param.

```
PUT /api/alerts/12/acknowledge?acknowledged_by=Dr.Chen
```

---

## WebSocket

### `WS /ws/vitals/{patient_id}`
Real-time vitals stream. Pushes a reading every 2 seconds.

**Connect**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/vitals/4');
ws.onmessage = (e) => {
  const vitals = JSON.parse(e.data);
  console.log(vitals.heart_rate);
};
```

**Message format**
```json
{
  "patient_id": "4",
  "timestamp": 1742198400.0,
  "heart_rate": 69,
  "spo2": 97.8,
  "systolic_bp": 113,
  "diastolic_bp": 71,
  "respiratory_rate": 14,
  "temperature": 36.6
}
```

---

## Health Check

### `GET /health`
Returns API status. No auth required.

```json
{ "status": "ok", "version": "1.0.0" }
```
