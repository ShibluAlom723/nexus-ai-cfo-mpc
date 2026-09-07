# NEXUS AI CFO — Binance Agentic MCP Edition

This is the web dashboard/scaffold for connecting NEXUS AI CFO with Binance's official Agentic MCP architecture.

## Important

Binance's Agentic MCP is an authenticated MCP service, not a normal REST API endpoint. The official documentation currently describes connecting it through supported AI clients/integrations and completing Binance authorization.

MCP endpoint:

`https://agent.binance.com/mcp/agentic`

Do not open the MCP endpoint directly in a browser and do not paste it into a generic chat.

## Current web app

The Streamlit app provides:

- NEXUS CFO dashboard
- live Binance public market snapshot
- risk-engine UI
- agent permission policy UI
- MCP architecture and safety guardrails

The app intentionally does not fake Binance MCP authentication or store user Binance credentials.

## Deploy

Upload this repository to GitHub and deploy `app.py` with Streamlit Community Cloud.

## Official MCP setup

For a supported AI client, follow Binance's current Agentic MCP documentation:

https://developers.binance.com/en/docs/agent-native/mcp-server/agentic

The current Binance documentation says the Agentic MCP can read market data and balances and, when authorized, perform Spot/Margin/Convert/Futures trades and transfers within the dedicated Agentic sub-account. Non-read actions require user confirmation and withdrawal scope is not available.

## Production note

For a public NEXUS web app to perform Binance Agentic MCP actions directly from its own UI, Binance must provide/approve the corresponding web-client authentication/integration path. Do not implement a homemade OAuth flow or collect Binance passwords/API secrets.
