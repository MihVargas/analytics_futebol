# Modelo de dados

## Fluxo

O `dlt` extrai recursos da API football-data.org e os grava no schema `football_raw`. O dbt organiza os dados em modelos staging (views) e marts (tabelas) no schema `analytics`.

## Camada raw

| Tabela | Conteúdo |
| --- | --- |
| `football_raw.football_matches` | Partidas retornadas por competição |
| `football_raw.football_standings` | Linhas de classificação por competição e temporada |
| `football_raw.football_teams` | Cadastro de equipes |

Os recursos consultam os códigos `CL` (Champions League), `PD` (La Liga) e `BSA` (Brasileirão). A extração atual usa `write_disposition="replace"` nos três recursos.

## Staging

| Modelo | Conteúdo |
| --- | --- |
| `analytics.stg_matches` | Partidas encerradas; nomes e tipos padronizados, com gols, equipes e datas |
| `analytics.stg_standings` | Classificação geral (`TOTAL`) com posição, pontos e estatísticas |
| `analytics.stg_teams` | Cadastro de equipes com país e competição de origem |

## Marts

| Modelo | Tipo | Conteúdo |
| --- | --- | --- |
| `analytics.fct_matches` | Fato | Uma linha por partida encerrada; gols totais e resultado (`HOME_WIN`, `AWAY_WIN`, `DRAW`) |
| `analytics.dim_teams` | Dimensão | Uma linha por equipe, deduplicada por `team_id` |
| `analytics.champion_curse` | Análise | Posição do campeão na temporada seguinte e faixa de desempenho |

## Dashboard

O Streamlit consulta `fct_matches` para partidas, gols e médias; `champion_curse` para a posição dos campeões; e `stg_standings` para a classificação selecionada. A atualização dos dados ocorre ao executar o pipeline.
