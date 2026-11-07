from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


class ETLService:
    def run(self, mode: str = "full") -> str:
        cmd = ["python", str(ROOT / "etl/pipelines/run_etl.py"), "--mode", mode]
        out = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if out.returncode != 0:
            raise RuntimeError(out.stderr or out.stdout)
        return out.stdout.strip() or "ETL run complete"
