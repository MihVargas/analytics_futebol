-- Classificação geral (TOTAL) de cada competição/temporada
WITH raw AS (
    SELECT * FROM "football"."football_raw"."football_standings"
)

SELECT
    competition,
    season,
    stage,
    type AS standing_type,
    position,
    team__id AS team_id,
    team__name AS team_name,
    played_games,
    won,
    draw,
    lost,
    points,
    goals_for,
    goals_against,
    goal_difference,
    _dlt_load_id
FROM raw
WHERE type = 'TOTAL'