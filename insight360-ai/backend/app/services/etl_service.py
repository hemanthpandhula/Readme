from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


class ETLService:
    def run(self, mode: str = "full") -> str:
        if mode == "full":
            cmd = ["python", str(ROOT / "etl/pipelines/run_etl.py"), "--mode", "full"]
        elif mode == "incremental":
            cmd = ["python", str(ROOT / "etl/pipelines/run_etl.py"), "--mode", "incremental"]
        else:
            raise ValueError("Unsupported ETL mode")
        out = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if out.returncode != 0:
            raise RuntimeError(out.stderr or out.stdout)
        return out.stdout.strip() or "ETL run complete"
