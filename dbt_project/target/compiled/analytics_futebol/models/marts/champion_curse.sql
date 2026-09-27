-- "Maldição do campeão": posição do campeão da temporada N na temporada N+1
WITH season_map AS (
    -- O season id da API não é o ano; deriva o ano real dos jogos
    SELECT
        competition_code,
        season_id,
        MIN(EXTRACT(YEAR FROM match_date))::BIGINT AS season_year
    FROM "football"."analytics_staging"."stg_matches"
    GROUP BY 1, 2
),
champions AS (
    SELECT
        s.competition,
        sm.season_year,
        s.team_name AS champion
    FROM "football"."analytics_staging"."stg_standings" s
    LEFT JOIN season_map sm
        ON sm.competition_code = s.competition
        AND sm.season_id = s.season
    WHERE s.position = 1
),
next_season AS (
    SELECT
        s.competition,
        sm.season_year,
        s.team_name,
        s.position,
        s.points
    FROM "football"."analytics_staging"."stg_standings" s
    LEFT JOIN season_map sm
        ON sm.competition_code = s.competition
        AND sm.season_id = s.season
)

SELECT
    c.competition,
    c.season_year AS season_champion,
    c.champion,
    n.season_year AS season_following,
    n.position AS position_following,
    n.points AS points_following,
    CASE
        WHEN n.position = 1 THEN 'bicampeão'
        WHEN n.position <= 4 THEN 'manteve top 4'
        WHEN n.position <= 10 THEN 'meio da tabela'
        ELSE 'caiu de rendimento'
    END AS outcome
FROM champions c
LEFT JOIN next_season n
    ON c.competition = n.competition
    AND n.season_year = c.season_year + 1
    AND n.team_name = c.champion
ORDER BY c.competition, c.season_year