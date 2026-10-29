# Data Explorer — Custom MCP Server

## Overview

Data Explorer is a Python MCP server built using FastMCP. It provides an AI agent with access to structured country information from the open [mledoze/countries](https://github.com/mledoze/countries) dataset hosted on GitHub.

The server communicates using the Model Context Protocol (MCP) over STDIO and exposes two tools:

- `search_countries(query, limit)`
- `get_country_details(name)`

The dataset requires no API key and is downloaded over HTTPS on the first request, then cached in memory.

## Requirements

- Python 3.10 or newer
- pip
- An MCP-compatible client, such as Gemini CLI
- Internet access for the initial dataset download

## Installation

Navigate to the project directory:

```bash
cd assignments/05-advanced-context-management/starter
```

Create and activate a Python virtual environment.

**Windows (Git Bash):**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Server

Start the MCP server:

```bash
python server.py
```

The server uses STDIO transport. It waits for MCP protocol messages from a client rather than providing an interactive terminal interface. Launching it directly is not a complete tool invocation.

## Registering with Gemini CLI

Register the server using an absolute path to the Python interpreter and `server.py`:

```bash
gemini mcp add --scope user data-explorer "/absolute/path/to/python" "/absolute/path/to/server.py"
```

Replace both paths with the actual paths on your computer.

Verify the registration:

```bash
gemini mcp list
```

A successful connection displays `data-explorer` with the status `Connected`.

Start Gemini CLI:

```bash
gemini
```

You can then ask Gemini to call either registered tool.

## Tool Reference

### Tool 1 — `search_countries(query, limit=5)`

Searches countries by their common or official names.

**Parameters:**

- `query` (string): Country name or partial name to search for.
- `limit` (integer, optional): Maximum number of results. Defaults to 5 and is capped at 50.

**Example input:**

```json
{
  "query": "Italy",
  "limit": 5
}
```

**Example output:**

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

If no countries match the query, the tool returns an empty list.

### Tool 2 — `get_country_details(name)`

Retrieves detailed information for a country by its common or official name, using case-insensitive exact matching.

**Parameter:**

- `name` (string): Country name.

**Example input:**

```json
{
  "name": "Germany"
}
```

**Example output:**

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

## Error Handling

The server validates input and handles common failure scenarios.

- Empty or invalid country names return descriptive error messages.
- Invalid search limits return an error instead of unexpected results.
- HTTP failures and network timeouts are caught and returned as error messages.
- Invalid JSON responses are handled through exception handling.
- Country searches without matches return an empty list.
- Detailed lookups for unknown countries return a `country not found` error.

**Example error response:**

```json
{
  "error": "country not found: Atlantis"
}
```

## Testing

The server was tested using Python 3.12.14 and Gemini CLI 0.65.0.

Both MCP tools were successfully invoked through Gemini CLI:

1. `search_countries("Italy", 5)`
2. `get_country_details("Germany")`

Additional tests covered invalid limits, empty names, unknown countries, and a simulated network timeout.

See [writeup.md](writeup.md) for the agent interaction transcript, validation results, and reflection.

## Data Source

[mledoze/countries — GitHub](https://github.com/mledoze/countries)

Country data is fetched from the repository's JSON dataset. Flag URLs are constructed from each country's three-letter `cca3` code.