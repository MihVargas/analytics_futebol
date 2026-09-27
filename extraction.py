import os
import dlt
from dlt.destinations import postgres

pipeline = dlt.pipeline(
    pipeline_name="football",
    destination=postgres(credentials=os.environ["POSTGRES_URL"]),  # antes: duckdb
    dataset_name="football_raw",
)