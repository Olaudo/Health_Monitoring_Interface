"""
VitalWatch — Alert Engine
Evaluates incoming vital readings against clinical thresholds
and generates alerts when values are out of range.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ThresholdRule:
    metric: str
    low_critical: Optional[float]
    low_warning: Optional[float]
    high_warning: Optional[float]
    high_critical: Optional[float]
    unit: str


# Clinical thresholds (customisable per patient in production)
THRESHOLDS: list[ThresholdRule] = [
    ThresholdRule("heart_rate",       40,  50,  120, 150, "bpm"),
    ThresholdRule("spo2",             85,  90,  None, None, "%"),
    ThresholdRule("systolic_bp",      70,  80,  160, 180, "mmHg"),
    ThresholdRule("diastolic_bp",     40,  50,  100, 120, "mmHg"),
    ThresholdRule("respiratory_rate",  6,  10,   25,  30, "/min"),
    ThresholdRule("temperature",      34, 35.5, 38.5, 39.5, "°C"),
]


def evaluate_vitals(vitals: dict) -> list[dict]:
    """
    Evaluate a vitals dict against thresholds.
    Returns a list of alert dicts for any breaches.

    Args:
        vitals: dict with keys matching ThresholdRule.metric

    Returns:
        List of alert payloads ready to be written to the DB.
    """
    alerts = []

    for rule in THRESHOLDS:
        value = vitals.get(rule.metric)
        if value is None:
            continue

        severity = None
        message = None

        if rule.low_critical is not None and value <= rule.low_critical:
            severity = "critical"
            message = f"{rule.metric.replace('_',' ').title()} critically low: {value} {rule.unit}"
        elif rule.high_critical is not None and value >= rule.high_critical:
            severity = "critical"
            message = f"{rule.metric.replace('_',' ').title()} critically high: {value} {rule.unit}"
        elif rule.low_warning is not None and value <= rule.low_warning:
            severity = "warning"
            message = f"{rule.metric.replace('_',' ').title()} below normal: {value} {rule.unit}"
        elif rule.high_warning is not None and value >= rule.high_warning:
            severity = "warning"
            message = f"{rule.metric.replace('_',' ').title()} above normal: {value} {rule.unit}"

        if severity:
            alerts.append({
                "metric": rule.metric,
                "severity": severity,
                "message": message,
                "value": value,
                "threshold": rule.low_critical or rule.high_critical or
                             rule.low_warning or rule.high_warning,
            })

    return alerts


def get_patient_status(vitals: dict) -> str:
    """Derive overall patient status from current vitals."""
    alerts = evaluate_vitals(vitals)
    if any(a["severity"] == "critical" for a in alerts):
        return "critical"
    if any(a["severity"] == "warning" for a in alerts):
        return "warning"
    return "stable"
