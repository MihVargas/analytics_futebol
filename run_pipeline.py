import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

ROOT = Path(__file__).parent
DBT = ROOT / "dbt_project"

load_dotenv(ROOT / ".env")

def main():
    subprocess.run(["python", "extraction.py"], cwd=ROOT, check=True)

    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(DBT)

    # Usa o MESMO hostname externo que o dlt usa (via POSTGRES_URL) — resolve o erro de SNI
    parsed = urlparse(os.environ["POSTGRES_URL"])
    env["PG_HOST"] = parsed.hostname

    subprocess.run(["dbt", "run"], cwd=DBT, check=True, env=env)
    subprocess.run(["dbt", "test"], cwd=DBT, check=True, env=env)

if __name__ == "__main__":
    main()