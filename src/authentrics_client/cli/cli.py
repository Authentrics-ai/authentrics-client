import os
import json
import time
from pathlib import Path

import click
import requests


class CliSession:
    BASE_DIR = Path.home() / ".authrx"
    TOKEN_PATH = BASE_DIR / "token.json"

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.username = username
        self.password = password

        parsed_url = requests.models.parse_url(base_url)
        assert parsed_url.path is None or parsed_url.path == "/"
        assert parsed_url.query is None
        assert parsed_url.fragment is None

        self.base_url = parsed_url.url.rstrip("/")
        self._session = requests.Session()
        self.token = self._login()
        self._store_token(self.token, self.base_url)
        os.environ["authrx_token"] = str(self.TOKEN_PATH)

    def _login(self) -> str:
        return self._post(
            "/api/auth/login",
            json={"username": self.username, "password": self.password},
        ).content.decode()

    def _post(self, route: str, **kwargs):
        response = self._session.post(self.base_url + route, **kwargs)
        response.raise_for_status()
        return response

    def _store_token(self, token: str, url: str):
        """Stores a token securely in ~/.authrx/token.json."""
        # Ensure the directory exists
        self.BASE_DIR.mkdir(parents=True, exist_ok=True)

        # Store the token in a JSON file
        with self.TOKEN_PATH.open("w") as f:  # Open Path directly
            json.dump({"token": token, "url": url, "COD": str(time.time_ns())}, f)

        # Set file permissions to be readable only by the user
        self.TOKEN_PATH.chmod(0o600)


@click.command()
@click.option("--env", default="dev")
@click.option("--username", prompt="Enter username", help="Your username")
@click.option(
    "--password",
    prompt="Enter password",
    hide_input=True,
    confirmation_prompt=True,
    help="Your password",
)
def login(env, username, password):
    environments = {
        "dev": "http://api.dev.authentrics.ai/",
        "uat": "http://api.uat.authentrics.ai/",
        "prod": "http://api.authentrics.ai/",
    }

    """Simple CLI to take a username and password securely."""
    click.echo(f"Username: {username}")
    click.echo("Password received securely!")

    if env in environments:
        url = environments[env]
        click.echo("login using env: " + env)
    else:
        click.echo("Provided env not found")
        raise ValueError

    CliSession(url, username, password)


@click.group()
@click.version_option(package_name="authentrics-client")
def cli():
    """AuthRX CLI - Authentrics Command Line Tool"""
    pass


cli.add_command(login)
