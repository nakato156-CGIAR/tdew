#!/usr/bin/env python3
"""Regenerate ZENML_STORE_URL in .env from ZENML_DB_PASSWORD.

Run this after editing MYSQL_ROOT_PASSWORD or ZENML_DB_PASSWORD in .env,
before `docker compose up`. It URL-encodes the password so special
characters (@, :, /, [, ], etc.) don't break the mysql:// connection
string that zenml-server parses on startup.
"""
from pathlib import Path
from urllib.parse import quote

ENV_PATH = Path(__file__).parent / ".env"


def _unquote_dotenv_value(value: str) -> str:
    """Strip one layer of surrounding quotes, same as docker compose's .env parser."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def main() -> None:
    lines = ENV_PATH.read_text().splitlines()
    values = {}
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            values[key.strip()] = _unquote_dotenv_value(value)

    password = quote(values["ZENML_DB_PASSWORD"], safe="")
    store_url = f"mysql://zenml:{password}@mysql:3306/zenml"

    new_lines = [line for line in lines if not line.startswith("ZENML_STORE_URL=")]
    new_lines.append(f"ZENML_STORE_URL={store_url}")
    ENV_PATH.write_text("\n".join(new_lines) + "\n")
    print("Updated ZENML_STORE_URL in .env")


if __name__ == "__main__":
    main()
