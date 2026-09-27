# dash.py  (na raiz do analytics_futebol)
import os
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from sqlalchemy import create_engine

load_dotenv(Path(__file__).parent / ".env")
engine = create_engine(os.environ["POSTGRES_URL"])


# DB_PATH = Path(os.getenv("FOOTBALL_DB", "/Users/michelevargas/projetos-dev/analytics_futebol/football.duckdb"))

st.set_page_config(page_title="Analytics Futebol", layout="wide")
st.title("⚽ Analytics Futebol — Champions League · La Liga · Brasileirão")

# @st.cache_resource
# def get_conn():
#     return duckdb.connect(str(DB_PATH), read_only=True)

# @st.cache_data(ttl=300)
# def load(sql: str) -> pd.DataFrame:
#     return get_conn().sql(sql).df()



@st.cache_data(ttl=300)
def load(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, engine)

# Lista as tabelas disponíveis no DuckDB (para diagnóstico amigável)
available = load("SELECT table_schema, table_name FROM information_schema.tables ORDER BY 1, 2")

if not available.empty:
    st.sidebar.success(f"{len(available)} tabelas encontradas")
else:
    st.sidebar.error("Nenhuma tabela. Rode `dbt run` antes.")
    st.stop()

# ---------- KPI gerais ----------
try:
    matches = load("SELECT * FROM analytics.fct_matches")
    curse = load("SELECT * FROM analytics.champion_curse")
    standings = load("SELECT * FROM analytics.stg_standings WHERE standing_type = 'TOTAL'")
except Exception as e:
    st.error(f"Não consegui carregar os marts: {e}\nRode `dbt run` e tente de novo.")
    st.stop()

st.subheader("Visão geral")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Partidas", f"{len(matches):,}")
k2.metric("Gols", f"{matches.home_goals.sum() + matches.away_goals.sum():,}")
k3.metric("Média de gols/jogo", f"{(matches.home_goals + matches.away_goals).mean():.2f}")
k4.metric("Competições", f"{matches.competition_code.nunique()}")

# ---------- Distribuição por competição ----------
st.subheader("Gols por partida e por competição")
by_comp = (
    matches.groupby("competition_code")
    .agg(partidas=("match_id", "count"), gols=("home_goals", "sum"))
    .assign(media_gols=lambda d: d.gols / d.partidas)
    .reset_index()
)
c1, c2 = st.columns(2)
c1.plotly_chart(
    px.bar(by_comp, x="competition_code", y="partidas", text="partidas", title="Partidas"),
    use_container_width=True,
)
c2.plotly_chart(
    px.bar(by_comp, x="competition_code", y="media_gols", text=by_comp["media_gols"].round(2), title="Média de gols/jogo"),
    use_container_width=True,
)

# ---------- A maldição do campeão ----------
st.subheader("👑 A maldição do campeão")
curse_plot = curse[["competition", "season_champion", "champion", "position_following", "outcome"]]
st.plotly_chart(
    px.bar(
        curse_plot,
        x="season_champion",
        y="position_following",
        color="competition",
        hover_data=["champion"],
        barmode="group",
        title="Posição do campeão na temporada seguinte (1 = título, pior = maior valor)",
    ),
    use_container_width=True,
)
st.dataframe(curse_plot, use_container_width=True, hide_index=True)

# ---------- Classificação por competição ----------
st.subheader("Classificação")
comp = st.selectbox("Competição", standings["competition"].unique())
season = st.selectbox("Temporada", sorted(standings.loc[standings["competition"] == comp, "season"].unique(), reverse=True))
st.dataframe(
    standings[(standings["competition"] == comp) & (standings["season"] == season)]
    .sort_values("position")[["position", "team_name", "played_games", "won", "draw", "lost", "points", "goal_difference"]],
    use_container_width=True,
    hide_index=True,
)
