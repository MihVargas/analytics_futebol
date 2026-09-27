
    

    create  table
      "football"."analytics_marts"."fct_matches__dbt_tmp"
  
    
    as (
      -- Fato: uma linha por partida, com métricas de gols e resultado
SELECT
    match_id,
    competition_code,
    match_date,
    matchday,
    stage,
    season_id,
    home_team_id,
    home_team_name,
    away_team_id,
    away_team_name,
    home_goals,
    away_goals,
    home_goals_ht,
    away_goals_ht,
    winner,
    (home_goals + away_goals) AS total_goals,
    CASE
        WHEN home_goals > away_goals THEN 'HOME_WIN'
        WHEN away_goals > home_goals THEN 'AWAY_WIN'
        ELSE 'DRAW'
    END AS result
FROM "football"."analytics_staging"."stg_matches"
    );
    
  