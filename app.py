
import math
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts


# =========================================================
# 投資分析ダッシュボード
# - 短期: チャート分析 / 出来高急増 / ニュース・イベント
# - 中長期: 企業分析 / 財務分析 / マクロ経済 / 技術動向
# =========================================================

st.set_page_config(
    page_title="投資分析ダッシュボード",
    page_icon="📈",
    layout="wide",
)

# -----------------------------
# Style
# -----------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
    .main-title {
        font-size: 2.0rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #667085;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        border: 1px solid #EAECF0;
        border-radius: 18px;
        padding: 18px 20px;
        background: #FFFFFF;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.06);
    }
    .section-card {
        border: 1px solid #EAECF0;
        border-radius: 18px;
        padding: 16px 18px;
        background: #FFFFFF;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05);
        margin-bottom: 14px;
    }
    .pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        border: 1px solid #D0D5DD;
        color: #344054;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .pill-pos {
        border-color: #A6F4C5;
        color: #027A48;
        background: #ECFDF3;
    }
    .pill-neg {
        border-color: #FECDCA;
        color: #B42318;
        background: #FEF3F2;
    }
    .pill-neutral {
        border-color: #FEDF89;
        color: #B54708;
        background: #FFFAEB;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #EAECF0;
        padding: 14px 16px;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Dummy data
# -----------------------------
@st.cache_data
def load_dummy_data():
    random.seed(7)
    np.random.seed(7)

    companies = pd.DataFrame(
        [
            {
                "code": "7203",
                "name": "トヨタ自動車",
                "sector": "自動車",
                "theme": "EV / 自動運転",
                "price": 3180,
                "market_cap": 520000,
                "per": 10.8,
                "pbr": 1.25,
                "roe": 11.2,
                "op_margin": 10.1,
                "sales_growth": 8.5,
                "eps_growth": 12.0,
                "equity_ratio": 38.0,
                "fcf": 2450,
                "dividend_yield": 2.4,
            },
            {
                "code": "6758",
                "name": "ソニーグループ",
                "sector": "電機",
                "theme": "エンタメ / 半導体",
                "price": 14250,
                "market_cap": 178000,
                "per": 18.5,
                "pbr": 2.15,
                "roe": 13.8,
                "op_margin": 11.4,
                "sales_growth": 6.4,
                "eps_growth": 7.2,
                "equity_ratio": 45.0,
                "fcf": 980,
                "dividend_yield": 0.7,
            },
            {
                "code": "8035",
                "name": "東京エレクトロン",
                "sector": "半導体製造装置",
                "theme": "AI半導体 / HBM",
                "price": 36500,
                "market_cap": 172000,
                "per": 31.2,
                "pbr": 8.9,
                "roe": 26.3,
                "op_margin": 28.0,
                "sales_growth": 18.2,
                "eps_growth": 24.0,
                "equity_ratio": 66.0,
                "fcf": 1520,
                "dividend_yield": 1.1,
            },
            {
                "code": "6857",
                "name": "アドバンテスト",
                "sector": "半導体試験装置",
                "theme": "AI半導体 / テスター",
                "price": 6150,
                "market_cap": 95000,
                "per": 38.0,
                "pbr": 9.2,
                "roe": 24.8,
                "op_margin": 25.0,
                "sales_growth": 22.0,
                "eps_growth": 29.0,
                "equity_ratio": 60.0,
                "fcf": 730,
                "dividend_yield": 0.8,
            },
            {
                "code": "7011",
                "name": "三菱重工業",
                "sector": "機械 / 防衛",
                "theme": "防衛 / エネルギー",
                "price": 1840,
                "market_cap": 62000,
                "per": 21.0,
                "pbr": 3.1,
                "roe": 15.1,
                "op_margin": 7.9,
                "sales_growth": 11.0,
                "eps_growth": 18.0,
                "equity_ratio": 32.0,
                "fcf": 420,
                "dividend_yield": 1.5,
            },
            {
                "code": "9984",
                "name": "ソフトバンクグループ",
                "sector": "投資会社",
                "theme": "AI / 半導体投資",
                "price": 8950,
                "market_cap": 132000,
                "per": 0.0,
                "pbr": 1.35,
                "roe": -3.0,
                "op_margin": 0.0,
                "sales_growth": 2.0,
                "eps_growth": -8.0,
                "equity_ratio": 22.0,
                "fcf": -620,
                "dividend_yield": 0.5,
            },
            {
                "code": "6098",
                "name": "リクルートHD",
                "sector": "サービス",
                "theme": "HR Tech / AI",
                "price": 7720,
                "market_cap": 121000,
                "per": 29.5,
                "pbr": 5.7,
                "roe": 19.2,
                "op_margin": 18.5,
                "sales_growth": 7.5,
                "eps_growth": 10.0,
                "equity_ratio": 58.0,
                "fcf": 1050,
                "dividend_yield": 0.3,
            },
        ]
    )

    # Score design
    companies["financial_score"] = (
        companies["roe"].clip(0, 30) / 30 * 25
        + companies["op_margin"].clip(0, 30) / 30 * 25
        + companies["sales_growth"].clip(0, 25) / 25 * 25
        + companies["equity_ratio"].clip(0, 70) / 70 * 25
    ).round(1)

    companies["long_term_score"] = (
        companies["financial_score"] * 0.45
        + companies["eps_growth"].clip(-10, 30).add(10) / 40 * 20
        + companies["fcf"].clip(-700, 2500).add(700) / 3200 * 20
        + companies["dividend_yield"].clip(0, 3.5) / 3.5 * 15
    ).round(1)

    companies["volume_ratio"] = [1.6, 2.1, 3.8, 4.4, 3.2, 2.6, 1.4]
    companies["price_change_pct"] = [1.2, -0.8, 5.6, 7.2, 4.1, -3.4, 0.9]
    companies["news_score"] = [28, 5, 82, 78, 64, -48, 12]
    companies["chart_score"] = [62, 51, 85, 88, 77, 41, 59]
    companies["short_term_score"] = (
        companies["chart_score"] * 0.35
        + companies["volume_ratio"].clip(0, 5) / 5 * 30
        + companies["news_score"].add(100) / 200 * 35
    ).round(1)
    companies["total_score"] = (companies["short_term_score"] * 0.45 + companies["long_term_score"] * 0.55).round(1)

    news = pd.DataFrame(
        [
            ["2026-05-06 15:30", "8035", "東京エレクトロン", "TDnet", "決算 / 上方修正", "通期業績予想を上方修正、AI半導体向け需要が想定超", "Positive", 88, 70],
            ["2026-05-06 14:10", "6857", "アドバンテスト", "株探", "好材料", "半導体テスター関連として物色、出来高が急増", "Positive", 80, 62],
            ["2026-05-06 13:20", "7011", "三菱重工業", "日経", "政策 / 防衛", "防衛関連予算への期待で関連銘柄に買い", "Positive", 65, 68],
            ["2026-05-06 12:00", "9984", "ソフトバンクグループ", "EDINET", "大量保有 / 変更報告", "主要ファンドの保有比率変化を確認", "Neutral", 35, 45],
            ["2026-05-06 11:15", "6098", "リクルートHD", "みんかぶ", "個別株ニュース", "AI活用によるHR領域の効率化に注目", "Positive", 55, 60],
            ["2026-05-06 10:50", "6758", "ソニーグループ", "TDnet", "資本政策", "自己株式取得に関する開示", "Positive", 62, 54],
            ["2026-05-06 10:10", "7203", "トヨタ自動車", "JPX", "市場情報", "売買代金ランキング上位、輸出株に買い", "Neutral", 42, 52],
            ["2026-05-06 09:20", "9984", "ソフトバンクグループ", "M&A Online", "M&A / 投資", "AI関連投資先の評価変動に関心", "Neutral", 40, 50],
            ["2026-05-05 16:00", "7011", "三菱重工業", "TDnet", "特別損失", "一部プロジェクトで追加費用を計上", "Negative", -60, -35],
        ],
        columns=[
            "datetime",
            "code",
            "name",
            "source",
            "event_type",
            "title",
            "sentiment",
            "short_impact",
            "long_impact",
        ],
    )

    # Price history
    dates = pd.date_range(end=pd.Timestamp("2026-05-06"), periods=80, freq="B")
    rows = []
    for _, row in companies.iterrows():
        base_price = row["price"] * 0.85
        trend = row["price"] / base_price
        values = []
        last = base_price
        for i, d in enumerate(dates):
            drift = (trend ** (1 / len(dates)) - 1)
            noise = np.random.normal(0, 0.015)
            close = last * (1 + drift + noise)
            open_ = last * (1 + np.random.normal(0, 0.006))
            high = max(open_, close) * (1 + abs(np.random.normal(0.008, 0.006)))
            low = min(open_, close) * (1 - abs(np.random.normal(0.008, 0.006)))
            volume = int(np.random.normal(900000, 180000) * row["volume_ratio"] * (1 + i / 220))
            rows.append([d, row["code"], row["name"], round(open_, 1), round(close, 1), round(low, 1), round(high, 1), max(volume, 10000)])
            last = close

    prices = pd.DataFrame(rows, columns=["date", "code", "name", "open", "close", "low", "high", "volume"])

    macro = pd.DataFrame(
        [
            ["政策金利", "米国", 5.25, "グロース株には逆風。金利低下局面ではPER上昇余地"],
            ["政策金利", "日本", 0.10, "銀行・保険には追い風、輸出株は為替に注意"],
            ["為替", "USD/JPY", 154.0, "円安は輸出企業にプラス、輸入企業にはコスト増"],
            ["原油", "WTI", 78.0, "エネルギー企業にプラス、運輸・化学にはコスト増"],
            ["半導体市況", "AI/HBM", 82.0, "AI投資・データセンター需要が半導体装置に追い風"],
        ],
        columns=["indicator", "region", "value", "comment"],
    )

    return companies, news, prices, macro


companies, news, prices, macro = load_dummy_data()


# -----------------------------
# ECharts helper functions
# -----------------------------
def score_bar_option(df, score_col, title):
    data = df.sort_values(score_col, ascending=False)
    return {
        "title": {"text": title, "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 80, "right": 25, "top": 55, "bottom": 40},
        "xAxis": {"type": "value", "max": 100},
        "yAxis": {"type": "category", "data": (data["code"] + " " + data["name"]).tolist(), "axisLabel": {"fontSize": 11}},
        "series": [
            {
                "type": "bar",
                "data": data[score_col].round(1).tolist(),
                "label": {"show": True, "position": "right"},
                "barWidth": 16,
            }
        ],
    }


def scatter_option(df):
    return {
        "title": {"text": "短期スコア × 中長期スコア", "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}<br/>短期: {@[0]}<br/>中長期: {@[1]}<br/>出来高倍率: {@[2]}x",
        },
        "grid": {"left": 45, "right": 35, "top": 60, "bottom": 45},
        "xAxis": {"name": "短期スコア", "min": 30, "max": 100},
        "yAxis": {"name": "中長期スコア", "min": 30, "max": 100},
        "series": [
            {
                "type": "scatter",
                "symbolSize": [max(12, v * 8) for v in df["volume_ratio"]],
                "data": [
                    {
                        "name": f"{r.code} {r.name}",
                        "value": [round(r.short_term_score, 1), round(r.long_term_score, 1), round(r.volume_ratio, 1)],
                    }
                    for r in df.itertuples()
                ],
                "label": {"show": True, "formatter": "{b}", "position": "top", "fontSize": 10},
            }
        ],
    }


def candlestick_option(price_df, selected_name):
    d = price_df.sort_values("date").copy()
    d["date_str"] = d["date"].dt.strftime("%m/%d")
    ma5 = d["close"].rolling(5).mean().round(1)
    ma25 = d["close"].rolling(25).mean().round(1)

    return {
        "title": {"text": f"{selected_name} ローソク足 + 移動平均", "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
        "legend": {"top": 28, "data": ["日足", "MA5", "MA25"]},
        "grid": [{"left": 50, "right": 35, "top": 70, "height": "58%"}, {"left": 50, "right": 35, "top": "78%", "height": "14%"}],
        "xAxis": [
            {"type": "category", "data": d["date_str"].tolist(), "scale": True, "boundaryGap": False, "axisLine": {"onZero": False}},
            {"type": "category", "gridIndex": 1, "data": d["date_str"].tolist(), "axisLabel": {"show": False}},
        ],
        "yAxis": [{"scale": True}, {"gridIndex": 1, "scale": True, "axisLabel": {"show": False}}],
        "dataZoom": [{"type": "inside", "xAxisIndex": [0, 1], "start": 45, "end": 100}, {"show": True, "xAxisIndex": [0, 1], "type": "slider", "top": "94%", "start": 45, "end": 100}],
        "series": [
            {
                "name": "日足",
                "type": "candlestick",
                "data": d[["open", "close", "low", "high"]].values.tolist(),
            },
            {"name": "MA5", "type": "line", "data": ma5.replace({np.nan: None}).tolist(), "smooth": True, "showSymbol": False},
            {"name": "MA25", "type": "line", "data": ma25.replace({np.nan: None}).tolist(), "smooth": True, "showSymbol": False},
            {"name": "出来高", "type": "bar", "xAxisIndex": 1, "yAxisIndex": 1, "data": d["volume"].tolist(), "barWidth": "60%"},
        ],
    }


def volume_option(df):
    data = df.sort_values("volume_ratio", ascending=False)
    return {
        "title": {"text": "出来高急増ランキング（25日平均比）", "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 70, "right": 30, "top": 55, "bottom": 40},
        "xAxis": {"type": "category", "data": data["code"].tolist()},
        "yAxis": {"type": "value", "name": "倍率"},
        "series": [
            {
                "type": "bar",
                "data": data["volume_ratio"].round(1).tolist(),
                "label": {"show": True, "position": "top", "formatter": "{c}x"},
            }
        ],
    }


def event_pie_option(df):
    counts = df["event_type"].str.split(" / ").str[0].value_counts()
    return {
        "title": {"text": "イベント分類", "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {"trigger": "item"},
        "legend": {"bottom": 0},
        "series": [
            {
                "type": "pie",
                "radius": ["35%", "65%"],
                "avoidLabelOverlap": True,
                "data": [{"name": k, "value": int(v)} for k, v in counts.items()],
            }
        ],
    }


def radar_option(selected_row):
    indicators = [
        {"name": "売上成長", "max": 25},
        {"name": "営業利益率", "max": 30},
        {"name": "ROE", "max": 30},
        {"name": "財務安全性", "max": 70},
        {"name": "EPS成長", "max": 30},
    ]
    values = [
        max(0, selected_row["sales_growth"]),
        max(0, selected_row["op_margin"]),
        max(0, selected_row["roe"]),
        max(0, selected_row["equity_ratio"]),
        max(0, selected_row["eps_growth"]),
    ]
    return {
        "title": {"text": f"{selected_row['name']} 中長期ファンダメンタル", "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {},
        "radar": {"indicator": indicators, "radius": "65%"},
        "series": [{"type": "radar", "data": [{"value": values, "name": selected_row["name"]}]}],
    }


def macro_option(macro_df):
    return {
        "title": {"text": "マクロ・技術テーマ温度感", "left": "center", "textStyle": {"fontSize": 15}},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 60, "right": 25, "top": 55, "bottom": 40},
        "xAxis": {"type": "category", "data": (macro_df["indicator"] + " " + macro_df["region"]).tolist(), "axisLabel": {"rotate": 25}},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar", "data": macro_df["value"].tolist(), "label": {"show": True, "position": "top"}}],
    }


def news_badge(sentiment):
    if sentiment == "Positive":
        return "🟢 Positive"
    if sentiment == "Negative":
        return "🔴 Negative"
    return "🟡 Neutral"


def classify_action(row):
    if row["short_term_score"] >= 75 and row["long_term_score"] >= 65:
        return "短期も中長期も有力"
    if row["short_term_score"] >= 75:
        return "短期注目"
    if row["long_term_score"] >= 70:
        return "中長期候補"
    if row["news_score"] < -40:
        return "注意"
    return "監視"


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("📌 フィルター")
    sectors = ["すべて"] + sorted(companies["sector"].unique().tolist())
    selected_sector = st.selectbox("Sector", sectors)
    min_total_score = st.slider("総合スコア下限", 0, 100, 50, 5)
    selected_sources = st.multiselect(
        "ニュースソース",
        ["JPX", "TDnet", "EDINET", "M&A Online", "日経", "みんかぶ", "株探"],
        default=["JPX", "TDnet", "EDINET", "M&A Online", "日経", "みんかぶ", "株探"],
    )

    st.divider()
    st.caption("情報ソースの役割")
    st.markdown(
        """
        - **TDnet / EDINET / JPX**: 公式・一次情報
        - **株探 / みんかぶ / 日経**: 速報・市場反応
        - **M&A Online**: M&A・TOB・資本政策
        """
    )
    st.warning("このサンプルはダミーデータです。実投資判断には必ず一次情報を確認してください。")


filtered = companies.copy()
if selected_sector != "すべて":
    filtered = filtered[filtered["sector"] == selected_sector]
filtered = filtered[filtered["total_score"] >= min_total_score]

filtered_news = news[news["source"].isin(selected_sources)].copy()

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">投資分析ダッシュボード</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">短期は「チャート・出来高・ニュース」、中長期は「企業・財務・マクロ・技術動向」で銘柄選定する設計です。</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# KPI
# -----------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("監視銘柄数", len(filtered), delta=f"{len(companies)}銘柄中")
with k2:
    st.metric("短期注目", int((filtered["short_term_score"] >= 75).sum()))
with k3:
    st.metric("出来高3倍超", int((filtered["volume_ratio"] >= 3).sum()))
with k4:
    st.metric("重要ニュース", int((filtered_news["short_impact"].abs() >= 60).sum()))

# -----------------------------
# Tabs
# -----------------------------
tab0, tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Dashboard", "⚡ 短期分析", "📰 ニュース・イベント", "🏢 中長期分析", "🔍 銘柄比較"]
)

with tab0:
    c1, c2 = st.columns([1.15, 1])
    with c1:
        st_echarts(scatter_option(filtered), height="430px", key="scatter_total")
    with c2:
        st_echarts(score_bar_option(filtered, "total_score", "総合スコアランキング"), height="430px", key="total_score_bar")

    st.subheader("本日の銘柄候補")
    summary = filtered.copy()
    summary["判断"] = summary.apply(classify_action, axis=1)
    st.dataframe(
        summary[
            [
                "code",
                "name",
                "sector",
                "theme",
                "price_change_pct",
                "volume_ratio",
                "short_term_score",
                "long_term_score",
                "total_score",
                "判断",
            ]
        ].sort_values("total_score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with tab1:
    st.subheader("短期分析：チャート・出来高・材料")
    select_code = st.selectbox(
        "チャート表示銘柄",
        companies["code"] + " " + companies["name"],
        index=2,
        key="chart_select",
    )
    code = select_code.split(" ")[0]
    selected_company = companies[companies["code"] == code].iloc[0]
    price_df = prices[prices["code"] == code]

    a, b = st.columns([1.45, 1])
    with a:
        st_echarts(candlestick_option(price_df, select_code), height="520px", key="candlestick")
    with b:
        st_echarts(volume_option(filtered), height="250px", key="volume_ranking")
        st_echarts(score_bar_option(filtered, "short_term_score", "短期スコア"), height="250px", key="short_score_bar")

    st.markdown("#### 短期判断ルール")
    st.markdown(
        """
        **短期注目** = ニュース材料あり + 出来高急増 + チャート上昇  
        **注意** = 株価下落 + 出来高急増 + 悪材料ニュース
        """
    )

with tab2:
    st.subheader("ニュース・イベント分析")
    left, right = st.columns([1.35, 1])
    with left:
        show_news = filtered_news.sort_values("datetime", ascending=False).copy()
        show_news["判定"] = show_news["sentiment"].map(news_badge)
        st.dataframe(
            show_news[
                [
                    "datetime",
                    "code",
                    "name",
                    "source",
                    "event_type",
                    "title",
                    "判定",
                    "short_impact",
                    "long_impact",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    with right:
        st_echarts(event_pie_option(filtered_news), height="360px", key="event_pie")

    st.markdown("#### 情報ソース設計")
    source_design = pd.DataFrame(
        [
            ["JPX", "公式・市場情報", "売買停止、注意喚起、信用規制、売買代金など", "一次確認"],
            ["TDnet", "公式・適時開示", "決算、業績修正、自社株買い、増配、M&Aなど", "最重要"],
            ["EDINET", "公式・法定開示", "大量保有、臨時報告書、有価証券報告書、公開買付届出書", "最重要"],
            ["M&A Online", "M&A専門情報", "TOB、MBO、資本提携、業界再編", "深掘り"],
            ["日経", "企業・マクロニュース", "企業ニュース、業界、政策、金利、為替", "背景理解"],
            ["みんかぶ", "市場心理・個別株", "個別株ニュース、投資家予想、ランキング", "補助"],
            ["株探", "速報・材料株", "決算速報、好悪材料、人気ニュース、活況銘柄", "短期確認"],
        ],
        columns=["Source", "分類", "見る内容", "役割"],
    )
    st.dataframe(source_design, use_container_width=True, hide_index=True)

    st.markdown("#### イベント・スコア例")
    event_score = pd.DataFrame(
        [
            ["TOB / MBO", 95, "株価への直接影響が大きい"],
            ["上方修正", 85, "利益期待が上がる"],
            ["自社株買い", 75, "需給改善・株主還元"],
            ["増配", 70, "還元姿勢を評価"],
            ["大型受注", 70, "将来売上への期待"],
            ["下方修正", -85, "利益期待が下がる"],
            ["減配", -75, "投資家心理が悪化"],
            ["不祥事", -90, "信頼低下・売り材料"],
            ["売買停止", -95, "流動性・重大イベントリスク"],
        ],
        columns=["イベント", "スコア", "意味"],
    )
    st.dataframe(event_score, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("中長期分析：企業・財務・マクロ・技術")
    select_code2 = st.selectbox(
        "ファンダメンタル表示銘柄",
        companies["code"] + " " + companies["name"],
        index=2,
        key="fund_select",
    )
    code2 = select_code2.split(" ")[0]
    selected_row = companies[companies["code"] == code2].iloc[0]

    c1, c2 = st.columns([1, 1])
    with c1:
        st_echarts(radar_option(selected_row), height="420px", key="radar_fundamental")
    with c2:
        st_echarts(macro_option(macro), height="420px", key="macro_bar")

    st.markdown("#### 財務・企業指標")
    st.dataframe(
        companies[
            [
                "code",
                "name",
                "sector",
                "theme",
                "per",
                "pbr",
                "roe",
                "op_margin",
                "sales_growth",
                "eps_growth",
                "equity_ratio",
                "dividend_yield",
                "long_term_score",
            ]
        ].sort_values("long_term_score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with tab4:
    st.subheader("銘柄比較")
    compare_codes = st.multiselect(
        "比較する銘柄",
        companies["code"] + " " + companies["name"],
        default=[
            "8035 東京エレクトロン",
            "6857 アドバンテスト",
            "7011 三菱重工業",
        ],
    )
    compare_code_only = [x.split(" ")[0] for x in compare_codes]
    compare_df = companies[companies["code"].isin(compare_code_only)].copy()

    if len(compare_df) > 0:
        metric_options = ["short_term_score", "long_term_score", "total_score", "roe", "op_margin", "sales_growth", "volume_ratio"]
        selected_metric = st.selectbox("比較指標", metric_options, index=2)

        st_echarts(score_bar_option(compare_df, selected_metric, f"{selected_metric} 比較"), height="420px", key="compare_bar")
        st.dataframe(
            compare_df[
                [
                    "code",
                    "name",
                    "sector",
                    "theme",
                    "price",
                    "per",
                    "pbr",
                    "roe",
                    "op_margin",
                    "sales_growth",
                    "volume_ratio",
                    "short_term_score",
                    "long_term_score",
                    "total_score",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("比較する銘柄を選択してください。")

st.caption("Sample dashboard. Data is dummy and for UI design only.")

