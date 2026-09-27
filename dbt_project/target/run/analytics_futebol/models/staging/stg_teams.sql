
  
  create view "football"."analytics_staging"."stg_teams__dbt_tmp" as (
    -- Times com dados cadastrais limpos
WITH raw AS (
    SELECT * FROM "football"."football_raw"."football_teams"
)

SELECT
    id AS team_id,
    name AS team_name,
    short_name,
    tla,
    crest,
    venue,
    founded,
    area__name AS country,
    competition_code,
    _dlt_load_id
FROM raw
  );
