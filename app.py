import streamlit as st
import requests

st.set_page_config(page_title="NEXUS AI CFO", page_icon="₿", layout="wide")

BINANCE_MCP = "https://agent.binance.com/mcp/agentic"

# Binance provides multiple REST hostnames. We try them in order so a
# temporary regional/network issue does not make every market card fail.
BINANCE_HOSTS = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api4.binance.com",
    "https://data-api.binance.vision",
]

def get_24hr(symbol):
    last_error = None
    for host in BINANCE_HOSTS:
        try:
            r = requests.get(
                f"{host}/api/v3/ticker/24hr",
                params={"symbol": symbol},
                timeout=8,
                headers={"User-Agent": "NEXUS-AI-CFO/1.0"},
            )
            r.raise_for_status()
            data = r.json()
            if "lastPrice" in data:
                return data
            last_error = f"Unexpected response from {host}"
        except Exception as e:
            last_error = f"{host}: {e}"
    raise RuntimeError(last_error or "All Binance market endpoints failed")

@st.cache_data(ttl=15)
def market_snapshot(symbol):
    return get_24hr(symbol)

def price_text(value):
    value = float(value)
    if value >= 100:
        return f"${value:,.2f}"
    if value >= 1:
        return f"${value:,.4f}"
    return f"${value:,.6f}"

st.title("₿ NEXUS AI CFO")
st.caption("Binance Agentic MCP-ready crypto CFO dashboard")

with st.sidebar:
    st.header("Binance Agentic MCP")
    st.success("MCP endpoint configured")
    st.code(BINANCE_MCP, language="text")
    st.caption("MCP authentication is completed through Binance-supported client/integration flows.")
    st.divider()
    st.subheader("Safety Policy")
    st.write("✓ Market-data reads")
    st.write("✓ Confirmation before write actions")
    st.write("✗ Withdrawals")
    st.write("✗ Automatic trading in this build")

st.info(
    "Binance Agentic MCP is an authenticated MCP service, not a normal REST URL. "
    "This dashboard does not collect Binance passwords or API secrets."
)

st.subheader("Live Market Snapshot")

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
cols = st.columns(4)
market_errors = []

for col, symbol in zip(cols, symbols):
    with col:
        try:
            d = market_snapshot(symbol)
            last = float(d["lastPrice"])
            change = float(d["priceChangePercent"])
            col.metric(symbol, price_text(last), f"{change:+.2f}%")
        except Exception as e:
            market_errors.append(f"{symbol}: {e}")
            col.metric(symbol, "Unavailable")

if market_errors:
    with st.expander("Market-data diagnostics"):
        for err in market_errors:
            st.write("• " + err)
else:
    st.success("Binance public market data connected.")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("NEXUS Risk Engine")
    st.write("Portfolio intelligence checks:")
    for item in [
        "Portfolio concentration",
        "Market volatility",
        "Stablecoin / cash buffer",
        "Position and leverage risk",
        "Suggested risk controls",
    ]:
        st.write("• " + item)

    risk = st.slider("Demo portfolio risk score", 0, 100, 42)
    if risk < 35:
        st.success("LOW — risk appears controlled")
    elif risk < 65:
        st.warning("MEDIUM — review concentration and volatility")
    else:
        st.error("HIGH — review exposure before taking additional risk")

with right:
    st.subheader("Agent Action Policy")
    st.checkbox("Allow market-data reads", value=True, disabled=True)
    st.checkbox("Allow account reads", value=False)
    st.checkbox("Allow trading", value=False)
    st.checkbox("Allow wallet transfers", value=False)
    st.checkbox("Require confirmation before every write action", value=True, disabled=True)

    st.info(
        "Keep trading and transfers disabled for the first deployment. "
        "Enable only after the official Binance Agentic MCP connection is verified."
    )

st.divider()
st.subheader("NEXUS Agent Flow")
st.code(
"""User
  ↓
NEXUS AI CFO Web UI
  ↓
Risk / Decision Engine
  ↓
Binance Agentic MCP
  ↓
Binance Agentic Sub-account
  ↓
Read → Analyze → Confirm → Execute (only when authorized)
""",
language="text",
)

st.caption("NEXUS AI CFO • Binance Agentic MCP edition • Read-first deployment")
