import subprocess
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent
DBT = ROOT / "dbt_project"

load_dotenv(ROOT / ".env")

def main():
    subprocess.run(["python", "extraction.py"], cwd=ROOT, check=True)
    subprocess.run(["dbt", "run"], cwd=DBT, check=True)
    subprocess.run(["dbt", "test"], cwd=DBT, check=True)

if __name__ == "__main__":
    main()
