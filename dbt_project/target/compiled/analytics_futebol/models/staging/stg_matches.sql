-- Partidas encerradas, tipadas e com colunas renomeadas (flat da raw)
WITH raw AS (
    SELECT * FROM "football"."football_raw"."football_matches"
)

SELECT
    id AS match_id,
    competition_code,
    utc_date::DATE AS match_date,
    status,
    stage,
    matchday,
    season__id AS season_id,
    home_team__id AS home_team_id,
    home_team__name AS home_team_name,
    away_team__id AS away_team_id,
    away_team__name AS away_team_name,
    score__full_time__home AS home_goals,
    score__full_time__away AS away_goals,
    score__half_time__home AS home_goals_ht,
    score__half_time__away AS away_goals_ht,
    score__winner AS winner,
    _dlt_load_id
FROM raw
WHERE status = 'FINISHED'