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


def post_login(base_url: str, username: str, password: str) -> str:
    response = requests.post(
        base_url + "/api/auth/login",
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
def login(url, username, password):
    """Simple CLI to take a username and password securely."""
    click.echo(f"Username: {username}")
    click.echo("Password received securely!")

    base_url = parse_url(url)
    token = post_login(base_url, username, password)
    store_token(token, base_url)


@click.group()
@click.version_option(package_name="authentrics-client")
def cli():
    """AuthRX CLI - Authentrics Command Line Tool"""
    pass


cli.add_command(login)
