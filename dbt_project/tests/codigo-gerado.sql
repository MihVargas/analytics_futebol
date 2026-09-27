-- tests/no_duplicate_champions.sql
-- Não deve existir mais de um campeão por competição/temporada
SELECT competition, season, COUNT(*) AS n_champions
FROM {{ ref('stg_standings') }}
WHERE position = 1
GROUP BY competition, season
HAVING COUNT(*) > 1