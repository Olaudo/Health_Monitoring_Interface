"""
VitalWatch — Synthetic Data Generator
Generates realistic patient vitals for demos and testing.
"""

import random
import json
from datetime import datetime, timedelta
from pathlib import Path


FIRST_NAMES = ["James","Maria","Robert","Aisha","David","Helen","Thomas","Sofia",
               "William","Priya","Carlos","Mei","Fatima","Liam","Emma","Noah"]
LAST_NAMES  = ["Harlow","Santos","Chen","Okonkwo","Reyes","Park","Wright","Andersen",
               "Johnson","Patel","Rivera","Zhang","Al-Rashid","Murphy","Fischer","Kim"]
PHYSICIANS  = ["Dr. Chen","Dr. Patel","Dr. Morrison","Dr. Obi","Dr. Larsson"]
WARDS       = ["ICU-A","ICU-B","General-A","Step-Down"]


def random_patient(bed_num: int) -> dict:
    age = random.randint(28, 88)
    dob = datetime.now() - timedelta(days=age * 365)
    return {
        "mrn": f"MRN{10000 + bed_num:04d}",
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES),
        "date_of_birth": dob.isoformat(),
        "gender": random.choice(["M", "F"]),
        "bed_number": f"Bed {bed_num}",
        "ward": random.choice(WARDS),
        "attending_physician": random.choice(PHYSICIANS),
        "admitted_at": (datetime.now() - timedelta(days=random.randint(1, 14))).isoformat(),
    }


def random_vitals(patient_id: int, baseline: dict, jitter: float = 1.0) -> dict:
    """Generate a single vitals reading with Gaussian noise around a baseline."""
    def g(val, std): return round(val + random.gauss(0, std) * jitter, 1)

    return {
        "patient_id": patient_id,
        "heart_rate":       max(30, min(220, round(g(baseline["hr"],   5)))),
        "spo2":             max(70, min(100, round(g(baseline["spo2"], 1), 1))),
        "systolic_bp":      max(60, min(220, round(g(baseline["sbp"],  8)))),
        "diastolic_bp":     max(40, min(140, round(g(baseline["dbp"],  5)))),
        "respiratory_rate": max(4,  min(40,  round(g(baseline["rr"],   2)))),
        "temperature":      max(33, min(42,  round(g(baseline["temp"], 0.3), 1))),
        "recorded_at": datetime.now().isoformat(),
    }


# Baseline profiles for different patient conditions
BASELINES = {
    "healthy":  {"hr": 72,  "spo2": 98, "sbp": 118, "dbp": 76, "rr": 15, "temp": 36.7},
    "hypert":   {"hr": 82,  "spo2": 96, "sbp": 155, "dbp": 95, "rr": 17, "temp": 37.0},
    "hypoxic":  {"hr": 110, "spo2": 88, "sbp": 130, "dbp": 82, "rr": 24, "temp": 37.5},
    "critical": {"hr": 135, "spo2": 85, "sbp": 170, "dbp": 105,"rr": 28, "temp": 39.1},
    "brady":    {"hr": 48,  "spo2": 94, "sbp": 100, "dbp": 65, "rr": 12, "temp": 36.4},
}


def generate_history(patient_id: int, baseline_key: str = "healthy",
                     hours: int = 24, interval_minutes: int = 5) -> list[dict]:
    """Generate `hours` of vitals history at `interval_minutes` resolution."""
    baseline = BASELINES[baseline_key]
    readings = []
    points = (hours * 60) // interval_minutes
    for i in range(points):
        # Gradually worsen then improve to simulate a clinical event
        jitter = 1.0 + 0.5 * abs((i / points) - 0.5)
        r = random_vitals(patient_id, baseline, jitter)
        r["recorded_at"] = (
            datetime.now() - timedelta(minutes=(points - i) * interval_minutes)
        ).isoformat()
        readings.append(r)
    return readings


def seed_demo_data(n_patients: int = 12):
    """Seed the database with demo patients and vitals (called on startup)."""
    # In production: use SQLAlchemy session. Here we just log intent.
    print(f"[DataGenerator] Seeding {n_patients} demo patients...")
    profiles = ["healthy", "hypert", "hypoxic", "critical", "brady",
                "healthy", "healthy", "hypert", "healthy", "hypoxic", "healthy", "critical"]
    for i in range(n_patients):
        p = random_patient(i + 1)
        v = random_vitals(i + 1, BASELINES[profiles[i % len(profiles)]])
        print(f"  Patient {i+1}: {p['first_name']} {p['last_name']} — HR {v['heart_rate']}, SpO₂ {v['spo2']}%")
    print("[DataGenerator] Done.")


if __name__ == "__main__":
    # Save sample data to JSON for the repo
    patients = [random_patient(i+1) for i in range(12)]
    out = Path(__file__).parent.parent / "data" / "sample_patients.json"
    out.write_text(json.dumps(patients, indent=2))
    print(f"Wrote {len(patients)} patients to {out}")
