# Week 5 — Custom MCP Server: Data Explorer

## 1. Project Overview

I implemented a custom Model Context Protocol (MCP) server in Python using FastMCP. The server connects to the open `mledoze/countries` dataset hosted on GitHub and exposes two tools to an AI agent through the STDIO transport.

The two tools are:

- `search_countries(query, limit)`: Searches countries by name and returns their names, capitals, regions, and subregions.
- `get_country_details(name)`: Retrieves a country's currencies, languages, neighboring country codes, and flag URL.

I registered the server with Gemini CLI 0.65.0 and successfully tested both tools through the AI agent.

## 2. Agent–Tool Interaction Transcript

### Tool Call 1 — Search for Italy

**Prompt submitted to Gemini CLI:**

> Use the data-explorer MCP tool `search_countries` to search for countries containing "Italy" with a limit of 5. Show me the tool result.

**Tool:** `search_countries`

**Arguments:**
```json
{
  "query": "Italy",
  "limit": 5
}
```

**Result returned by Gemini CLI:**
```json
[
  {
    "name": "Italy",
    "capital": "Rome",
    "region": "Europe",
    "subregion": "Southern Europe"
  }
]
```

**Observation:** Gemini successfully accessed the MCP server and retrieved structured information about Italy.

### Tool Call 2 — Retrieve Germany's Details

**Prompt submitted to Gemini CLI:**

> Use the data-explorer MCP tool `get_country_details` to retrieve detailed information about Germany. Show the complete tool result, including currencies, languages, borders, and flag URL.

**Tool:** `get_country_details`

**Arguments:**
```json
{
  "name": "Germany"
}
```

**Result returned by Gemini CLI:**
```json
{
  "name": "Germany",
  "currencies": {
    "EUR": {
      "name": "Euro",
      "symbol": "€"
    }
  },
  "languages": {
    "deu": "German"
  },
  "borders": [
    "AUT",
    "BEL",
    "CZE",
    "DNK",
    "FRA",
    "LUX",
    "NLD",
    "POL",
    "CHE"
  ],
  "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/DEU.svg"
}
```

**Observation:** Gemini successfully called the second MCP tool and received detailed country information in a structured format.

*The transcripts above reproduce the observed Gemini responses, with the first result formatted as a JSON array to reflect the tool's return type.*

## 3. Error Handling and Validation

I tested the server's behavior with both valid and invalid inputs.

| Test | Expected behavior | Observed result |
|---|---|---|
| Search for Italy | Return country information | Passed |
| Get details for Germany | Return detailed country data | Passed |
| Search with limit = -1 | Reject invalid limit | Passed |
| Request details for Atlantis | Return country-not-found error | Passed |
| Request details with an empty name | Reject empty input | Passed |
| Simulated HTTP timeout | Return an upstream error message | Passed |

**Example: Invalid country name**

```python
get_country_details("Atlantis")
```

Result:
```json
{
  "error": "country not found: Atlantis"
}
```

**Example: Empty country name**

```python
get_country_details("")
```

Result:
```json
{
  "error": "name must be a non-empty string"
}
```

**Example: Invalid search limit**

```python
search_countries("Germany", -1)
```

Result:
```json
[
  {
    "error": "limit must be a positive integer"
  }
]
```

**Example: Simulated network timeout**

Using `unittest.mock.patch`, I simulated an `httpx.TimeoutException` during data loading.

Result:
```json
[
  {
    "error": "upstream request failed: Connection timed out"
  }
]
```

These tests demonstrate that the tools return understandable error messages instead of terminating unexpectedly for the tested failure scenarios.

## 4. MCP Server Registration

I registered the Data Explorer server with Gemini CLI using STDIO transport and user-level configuration.

The connection was verified with:

```bash
gemini mcp list
```

Gemini CLI reported:

```text
data-explorer (stdio) - Connected
```

Both registered tools were then successfully invoked through Gemini CLI.

## 5. Reflection — Context Access Through MCP

Without MCP, an AI agent may rely on information already present in its conversation or learned during training, which may be incomplete or outdated. MCP allows the agent to request external information through clearly defined tools rather than requiring the entire dataset to be included in the prompt. In this project, Gemini CLI accessed country information on demand through my Python server and received structured responses that were easy to interpret. This separation between the agent and the data source makes the system more extensible and allows validation and error handling to be managed by the server.