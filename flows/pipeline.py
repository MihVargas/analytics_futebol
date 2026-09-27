# flows/pipeline.py
from pathlib import Path
import subprocess

from prefect import flow, task

PROJECT_DIR = Path("/Users/michelevargas/projetos-dev/analytics_futebol")
DBT_DIR = PROJECT_DIR / "dbt_project"


@task
def extract():
    """1º Extração via dlt."""
    subprocess.run(["python", "extraction.py"], cwd=PROJECT_DIR, check=True)


@task
def dbt_run():
    """2º Staging + marts."""
    subprocess.run(["dbt", "run"], cwd=DBT_DIR, check=True)


# @task
# def dbt_test():
#     """3º Testes de qualidade."""
#     subprocess.run(["dbt", "test"], cwd=DBT_DIR, check=True)


@flow
def football_pipeline():
    extract()
    dbt_run()
    # dbt_test()
    print("Pipeline concluído com sucesso!")


if __name__ == "__main__":
    football_pipeline()