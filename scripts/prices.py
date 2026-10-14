import json, datetime, yfinance as yf
h = yf.Ticker("TQQQ").history(start="2010-01-01", interval="1d", auto_adjust=False, actions=False)
c = h["Close"].dropna()
c.index = c.index.tz_localize(None)
monthly = {}
for d, v in c.items():
    monthly[d.strftime("%Y-%m")] = (d.strftime("%Y-%m-%d"), round(float(v), 4))
last_d, last_v = c.index[-1].strftime("%Y-%m-%d"), round(float(c.iloc[-1]), 4)
m = [{"date": d, "close": v} for _, (d, v) in sorted(monthly.items())]
out = {"symbol": "TQQQ", "note": "unadjusted Close (Yahoo Finance via yfinance); last trading day of each month; current month = latest close",
       "monthly": m, "last": {"date": last_d, "close": last_v}}
old = None
try: old = json.load(open("prices.json"))
except Exception: pass
if old and old.get("monthly") == out["monthly"] and old.get("last") == out["last"]:
    print("unchanged")
else:
    json.dump(out, open("prices.json", "w"), separators=(",", ":"))
    print("written", len(m), out["last"])
