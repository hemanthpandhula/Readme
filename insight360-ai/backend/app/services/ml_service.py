from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


class MLService:
    def run_anomaly(self) -> str:
        cmd = ["python", str(ROOT / "ml/anomaly_detection/run_anomaly.py")]
        out = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if out.returncode != 0:
            raise RuntimeError(out.stderr or out.stdout)
        return out.stdout.strip() or "Anomaly run complete"

    def run_forecast(self) -> str:
        cmd = ["python", str(ROOT / "ml/forecasting/run_forecast.py")]
        out = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if out.returncode != 0:
            raise RuntimeError(out.stderr or out.stdout)
        return out.stdout.strip() or "Forecast run complete"
