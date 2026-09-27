-- Dimensão: um time = uma linha (deduplicado, sem competition_code ambíguo)
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY competition_code) AS rn
    FROM {{ ref('stg_teams') }}
)

SELECT
    team_id,
    team_name,
    short_name,
    tla,
    crest,
    venue,
    founded,
    country
FROM ranked
WHERE rn = 1