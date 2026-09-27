-- Times com dados cadastrais limpos
WITH raw AS (
    SELECT * FROM {{ source('football_raw', 'football_teams') }}
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