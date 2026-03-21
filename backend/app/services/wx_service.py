import os
from typing import Optional

import httpx

WX_APP_ID = os.getenv("WX_APP_ID", "")
WX_APP_SECRET = os.getenv("WX_APP_SECRET", "")
WX_LOGIN_URL = "https://api.weixin.qq.com/sns/jscode2session"


async def code_to_openid(code: str) -> Optional[str]:
    """
    Exchange a WeChat login code for an openid via jscode2session API.
    Returns openid on success, None on failure.
    """
    if not WX_APP_ID or not WX_APP_SECRET:
        raise ValueError("WeChat login not configured: WX_APP_ID or WX_APP_SECRET missing")

    params = {
        "appid": WX_APP_ID,
        "secret": WX_APP_SECRET,
        "js_code": code,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(WX_LOGIN_URL, params=params)
        response.raise_for_status()
        data = response.json()

    if "openid" not in data:
        # WeChat API returned an error (errcode + errmsg)
        return None

    return data["openid"]
