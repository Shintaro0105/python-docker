"""Black-Scholes option pricing Streamlit frontend."""

import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_PRICE_URL = "http://localhost:8000/calculate_prices"
API_IV_URL = "http://localhost:8000/calculate_ivs"

st.set_page_config(page_title="オプション計算ツール", layout="wide")
st.title("📈 オプション計算ツール (Black-Scholes)")

# ---------------- サイドバー ----------------
calculation_type = st.sidebar.selectbox(
    "計算タイプを選択",
    [
        "オプション価格計算",
        "インプライドボラティリティ計算",
    ],
)

# 共通パラメータ
S = st.sidebar.number_input("株価 (S)", value=100.0, step=1.0)
K_center = st.sidebar.number_input("権利行使価格 中央値 (K)", value=100.0, step=1.0)
K_range = st.sidebar.number_input("権利行使価格 範囲 (±)", value=20.0, step=1.0)
T = st.sidebar.number_input("残存期間 (年)", value=1.0, step=0.1)
r = st.sidebar.number_input("無リスク金利 (r)", value=0.05, step=0.01, format="%.2f")
q = st.sidebar.number_input("配当利回り (q)", value=0.0, step=0.01, format="%.2f")
option_type = st.sidebar.radio("オプション種別", ["call", "put"])

points = 21
K_min = K_center - K_range
K_max = K_center + K_range
K_list = list(np.linspace(K_min, K_max, points))

# ---------------- オプション価格計算 ----------------
if calculation_type == "オプション価格計算":
    sigma = st.sidebar.number_input(
        "ボラティリティ (sigma)",
        value=0.2,
        step=0.01,
        format="%.2f",
    )

    payload = {
        "S_list": [S],
        "K_list": K_list,
        "T": T,
        "r": r,
        "sigma": sigma,
        "q": q,
        "option_type": option_type,
    }

    try:
        response = requests.post(API_PRICE_URL, json=payload, timeout=10).json()

        # レスポンスの構造を確認
        if "prices" in response and "K_list" in response:
            # prices は [[price1, price2, ..., price21]] という形式
            # S_list=[100.0] なので、prices[0] が実際の価格リスト
            prices = response["prices"][0]  # 最初の行を取得

            df = pd.DataFrame({"K": response["K_list"], "オプション価格": prices})

            fig = px.line(
                df,
                x="K",
                y="オプション価格",
                title=(f"オプション価格の変化 (S={S:.2f}, sigma={sigma:.2f})"),
                markers=True,
            )
            st.plotly_chart(fig, use_container_width=True)

            # データテーブル表示
            with st.expander("データを表示"):
                st.dataframe(
                    df.style.format(
                        {
                            "K": "{:.2f}",
                            "オプション価格": "{:.4f}",
                        }
                    )
                )
        else:
            st.error("APIレスポンスの形式が不正です")
            st.json(response)

    except requests.exceptions.RequestException as e:
        st.error(f"API接続エラー: {e}")
    except (KeyError, IndexError, ValueError) as e:
        st.error(f"データ処理エラー: {e}")

# ---------------- インプライドボラティリティ計算 ----------------
elif calculation_type == "インプライドボラティリティ計算":
    market_price = st.sidebar.number_input("市場価格", value=10.0, step=0.1)

    payload = {
        "S_list": [S],
        "K_list": K_list,
        "T": T,
        "r": r,
        "price_list": [market_price] * len(K_list),
        "q": q,
        "option_type": option_type,
    }

    try:
        response = requests.post(API_IV_URL, json=payload, timeout=10).json()

        if "ivs" in response and "K_list" in response:
            # ivs は [[iv1, iv2, ..., iv21]] という形式
            # S_list=[S] なので、ivs[0] が実際のIVリスト
            ivs = response["ivs"][0]  # 最初の行を取得

            df = pd.DataFrame({"K": response["K_list"], "IV": ivs})

            # NaNを除外
            df_clean = df.dropna()

            if not df_clean.empty:
                fig = px.line(
                    df_clean,
                    x="K",
                    y="IV",
                    title=(
                        f"インプライドボラティリティの変化 "
                        f"(S={S:.2f}, "
                        f"市場価格={market_price:.2f})"
                    ),
                    markers=True,
                )
                st.plotly_chart(fig, use_container_width=True)

                # データテーブル表示
                with st.expander("データを表示"):
                    st.dataframe(df.style.format({"K": "{:.2f}", "IV": "{:.4f}"}))
            else:
                st.warning("有効なIV値が計算できませんでした")
        else:
            st.error("APIレスポンスの形式が不正です")
            st.json(response)

    except requests.exceptions.RequestException as e:
        st.error(f"API接続エラー: {e}")
    except (KeyError, IndexError, ValueError) as e:
        st.error(f"データ処理エラー: {e}")
