from __future__ import annotations

import json
import time

import click
import requests

from .config import BASE_DIR, TOKEN_PATH


def parse_url(url: str) -> str:
    parsed_url = requests.models.parse_url(url)
    assert parsed_url.path is None or parsed_url.path == "/"
    assert parsed_url.query is None
    assert parsed_url.fragment is None
    return parsed_url.url.rstrip("/")


def post_login(
    base_url: str, username: str, password: str, api_version: str | None = None
) -> str:
    version = (api_version or "").strip().lower() or None
    if version == "v2":
        login_url = f"{base_url}/api/v2/auth/login"
    else:
        login_url = f"{base_url}/api/auth/login"
    response = requests.post(
        login_url,
        json={"username": username, "password": password},
    )
    response.raise_for_status()
    return response.content.decode()


def store_token(token: str, url: str):
    """Stores a token securely in ~/.cache/authrx/token.json."""
    # Ensure the directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    # Store the token in a JSON file
    with TOKEN_PATH.open("w") as f:  # Open Path directly
        json.dump({"token": token, "url": url, "COD": str(time.time_ns())}, f)

    # Set file permissions to be readable only by the user
    TOKEN_PATH.chmod(0o600)


@click.command()
@click.argument("url", type=str)
@click.option("--username", prompt="Enter username", help="Your username")
@click.option(
    "--password",
    prompt="Enter password",
    hide_input=True,
    confirmation_prompt=True,
    help="Your password",
)
@click.option(
    "--api-version",
    type=click.Choice(["v2"]),
    default=None,
    help="API version (e.g. v2). Omit for unversioned (legacy) paths.",
)
def login(url, username, password, api_version):
    """Simple CLI to take a username and password securely."""
    click.echo(f"Username: {username}")
    click.echo("Password received securely!")

    base_url = parse_url(url)
    token = post_login(base_url, username, password, api_version=api_version)
    store_token(token, base_url)


@click.group()
@click.version_option(package_name="authentrics-client")
def cli():
    """AuthRX CLI - Authentrics Command Line Tool"""
    pass


cli.add_command(login)
