import os
import dlt
from dlt.destinations import postgres
from dataclasses import dataclass, field
from dotenv import load_dotenv
from dlt.sources.helpers import requests as dlt_requests

load_dotenv()

FOOTBALL_BASE = "https://api.football-data.org/v4"


@dataclass
class FootballConfig:
    """Configuração do pipeline de futebol."""

    competitions: list = field(
        default_factory=lambda: ["CL", "PD", "BSA"]
    )  # CL, PD, BSA
    base_url: str = FOOTBALL_BASE

@dlt.resource(name="football_teams", write_disposition="replace", primary_key="id")
def football_teams(api_token: str, competitions: list):
    """Times de cada competição — subresource /competitions/{code}/teams."""
    headers = {"X-Auth-Token": api_token}
    for code in competitions:
        print(f"{FOOTBALL_BASE}/competitions/{code}/teams")
        resp = dlt_requests.get(
            f"{FOOTBALL_BASE}/competitions/{code}/teams",
            headers=headers,
        )
        resp.raise_for_status()
        for team in resp.json().get("teams", []):
            team["competition_code"] = code
            yield team



@dlt.resource(name="football_matches", write_disposition="replace", primary_key="id")
def football_matches(api_token: str, competitions: list):
    headers = {"X-Auth-Token": api_token}
    for code in competitions:
        resp = dlt_requests.get(
            f"{FOOTBALL_BASE}/competitions/{code}/matches",
            headers=headers,
        )
        resp.raise_for_status()
        for match in resp.json().get("matches", []):
            match["competition_code"] = code
            yield match


@dlt.resource(name="football_standings", write_disposition="replace")
def football_standings(api_token: str, competitions: list):
    headers = {"X-Auth-Token": api_token}
    for code in competitions:
        resp = dlt_requests.get(
            f"{FOOTBALL_BASE}/competitions/{code}/standings",
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()
        for standing in data.get("standings", []):
            for row in standing.get("table", []):
                yield {
                    "competition": code,
                    "season": data.get("season", {}).get("id"),
                    "stage": standing.get("stage"),
                    "type": standing.get("type"),
                    **row,
                }


if __name__ == "__main__":
    config = FootballConfig()

    prod_postgres = postgres(credentials=os.environ['POSTGRES_URL'])

    pipeline = dlt.pipeline(
        pipeline_name="football",
        destination=prod_postgres,
        dataset_name="football_raw",
    )
    token = os.environ["FOOTBALL_API_TOKEN"]
    load_info = pipeline.run(
        [
            football_teams(token, config.competitions),
            football_matches(token, config.competitions),
            football_standings(token, config.competitions),
        ]
    )
    print(load_info)
