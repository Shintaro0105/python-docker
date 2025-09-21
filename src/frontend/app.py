import datetime

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Demo Web App", page_icon="🚀")

st.title("🚀 Python + Streamlit Demo")
st.write("これは uv + Ruff 環境で動作する簡単な Streamlit アプリです。")

# 入力フォーム
st.header("ユーザー入力")
name = st.text_input("名前を入力してください")
age = st.number_input("年齢を入力してください", min_value=0, max_value=120, step=1)

# タイムゾーン考慮した日付
today = datetime.datetime.now(datetime.UTC).date()
birthday = st.date_input("誕生日を選んでください", value=today)

if st.button("送信"):
    st.success(f"こんにちは {name} さん! 年齢は {age} 歳、誕生日は {birthday} ですね。")

# データ可視化の例
st.header("データ可視化")

rng = np.random.default_rng()
df = pd.DataFrame(rng.standard_normal((20, 3)), columns=["A", "B", "C"])

st.line_chart(df)
