import streamlit as st
import requests

st.set_page_config(page_title="NEXUS AI CFO • Binance MCP", page_icon="₿", layout="wide")

BINANCE_MCP = "https://agent.binance.com/mcp/agentic"
BINANCE_API = "https://api.binance.com"

@st.cache_data(ttl=15)
def ticker(symbol):
    r = requests.get(f"{BINANCE_API}/api/v3/ticker/24hr", params={"symbol": symbol}, timeout=10)
    r.raise_for_status()
    return r.json()

def fmt_price(x):
    return f"${float(x):,.2f}"

st.title("₿ NEXUS AI CFO")
st.caption("Binance Agentic MCP-ready crypto CFO dashboard")

st.sidebar.header("Binance Agentic MCP")
st.sidebar.success("MCP endpoint configured")
st.sidebar.code(BINANCE_MCP, language="text")
st.sidebar.markdown(
    "This app is **MCP-ready**. Binance authentication/consent must be completed "
    "through a supported AI client or Binance-supported integration flow."
)

st.warning(
    "Important: Binance's Agentic MCP is not a normal public REST endpoint. "
    "Do not paste the MCP URL into a browser or into a generic chat. "
    "Connect it through a supported AI client/integration and complete Binance consent."
)

st.subheader("Live Market Snapshot")
cols = st.columns(4)
for col, symbol in zip(cols, ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]):
    try:
        d = ticker(symbol)
        change = float(d["priceChangePercent"])
        col.metric(symbol, fmt_price(d["lastPrice"]), f"{change:+.2f}%")
    except Exception:
        col.metric(symbol, "Unavailable")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("NEXUS Risk Engine")
    st.write("Use the CFO engine to evaluate:")
    st.write("• Portfolio concentration")
    st.write("• Market volatility")
    st.write("• Stablecoin/cash buffer")
    st.write("• Position and leverage risk")
    st.write("• Suggested risk controls")

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
        "For the first deployment, keep Account/Trade/Transfer disabled until "
        "the Binance Agentic MCP connection is verified."
    )

st.divider()
st.subheader("How the final agent flow works")

st.code(
"""User
  ↓
NEXUS AI CFO Web UI
  ↓
NEXUS Decision / Risk Engine
  ↓
Binance Agentic MCP
  ↓
Binance Agentic Sub-account
  ↓
Read data → analyze → ask confirmation → execute (only if authorized)
""",
language="text",
)

st.markdown(
    "**Safety:** This web build does not place Binance orders by itself. "
    "Binance's Agentic MCP is designed so non-read actions require user confirmation, "
    "and there is no withdrawal scope."
)

st.caption("NEXUS AI CFO • MCP integration scaffold • Read-first deployment")
