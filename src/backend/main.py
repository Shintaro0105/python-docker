"""Black-Scholes option pricing API."""

from typing import Literal

import numpy as np
import scipy.stats as st
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scipy.optimize import newton

app = FastAPI(title="Black-Scholes API")


# -------------------- 入力モデル --------------------
class PriceInput(BaseModel):
    """オプション価格計算の入力モデル."""

    S_list: list[float] | None = None
    K_list: list[float] | None = None
    T: float
    r: float
    sigma: float | None = None
    q: float = 0.0
    option_type: Literal["call", "put"]


class IVInput(BaseModel):
    """インプライドボラティリティ計算の入力モデル."""

    S_list: list[float] | None = None
    K_list: list[float] | None = None
    T: float
    r: float
    price_list: list[float]
    q: float = 0.0
    option_type: Literal["call", "put"]


# -------------------- ブラック=ショールズ計算 --------------------
def black_scholes_price(  # noqa: PLR0913
    S: float,  # noqa: N803
    K: float,  # noqa: N803
    T: float,  # noqa: N803
    r: float,
    sigma: float,
    option_type: Literal["call", "put"] = "call",
    q: float = 0.0,
) -> float:
    """Black-Scholesモデルでオプション価格を計算.

    Args:
        S: 株価
        K: 権利行使価格
        T: 残存期間(年)
        r: 無リスク金利
        sigma: ボラティリティ
        option_type: オプション種別(call or put)
        q: 配当利回り

    Returns:
        オプション価格

    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * np.exp(-q * T) * st.norm.cdf(d1) - K * np.exp(-r * T) * st.norm.cdf(
            d2
        )
    return K * np.exp(-r * T) * st.norm.cdf(-d2) - S * np.exp(-q * T) * st.norm.cdf(-d1)


# -------------------- インプライドボラティリティ計算 --------------------
def implied_vol(  # noqa: PLR0913
    price: float,
    S: float,  # noqa: N803
    K: float,  # noqa: N803
    T: float,  # noqa: N803
    r: float,
    option_type: Literal["call", "put"] = "call",
    q: float = 0.0,
    tol: float = 1e-6,
    max_iter: int = 50,
) -> float | None:
    """インプライドボラティリティを計算.

    Args:
        price: オプション市場価格
        S: 株価
        K: 権利行使価格
        T: 残存期間(年)
        r: 無リスク金利
        option_type: オプション種別(call or put)
        q: 配当利回り
        tol: 収束判定の許容誤差
        max_iter: 最大反復回数

    Returns:
        インプライドボラティリティ(収束しない場合はNone)

    """

    def objective(sigma: float) -> float:
        return black_scholes_price(S, K, T, r, sigma, option_type, q) - price

    try:
        return newton(objective, x0=0.2, tol=tol, maxiter=max_iter)
    except RuntimeError:
        return None


# -------------------- 価格計算 API --------------------
@app.post("/calculate_prices")
def calculate_prices(data: PriceInput) -> dict:
    """オプション価格を計算するAPIエンドポイント.

    Args:
        data: 価格計算の入力データ

    Returns:
        S_list, K_list, pricesを含む辞書

    """
    s_list = data.S_list or [100.0]
    k_list = data.K_list or [100.0]
    result = []

    for S in s_list:  # noqa: N806
        row = []
        for K in k_list:  # noqa: N806
            price = black_scholes_price(
                S,
                K,
                data.T,
                data.r,
                data.sigma,
                data.option_type,
                data.q,
            )
            row.append(price)
        result.append(row)

    return {"S_list": s_list, "K_list": k_list, "prices": result}


# -------------------- IV計算 API --------------------
@app.post("/calculate_ivs")
def calculate_ivs(data: IVInput) -> dict:
    """インプライドボラティリティを計算するAPIエンドポイント.

    Args:
        data: IV計算の入力データ

    Returns:
        S_list, K_list, ivsを含む辞書

    Raises:
        HTTPException: price_listの長さが不正な場合

    """
    s_list = data.S_list or [100.0]
    k_list = data.K_list or [100.0]
    price_list = data.price_list

    if len(s_list) * len(k_list) != len(price_list):
        msg = "価格リストの長さがS_list*K_listと一致しません"
        raise HTTPException(status_code=400, detail=msg)

    iv_result = []
    idx = 0

    for S in s_list:  # noqa: N806
        row = []
        for K in k_list:  # noqa: N806
            price = price_list[idx]
            idx += 1
            iv = implied_vol(price, S, K, data.T, data.r, data.option_type, data.q)
            row.append(iv)
        iv_result.append(row)

    return {"S_list": s_list, "K_list": k_list, "ivs": iv_result}
