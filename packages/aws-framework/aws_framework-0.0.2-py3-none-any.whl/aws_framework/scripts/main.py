#!env/bin/python3
import os
import subprocess

import click

CONTAINERS_PATH = "./scripts/containers"
CONTAINERS = ["fastapi", "flask", "express", "codeserver", "react", "vue", "php"]


@click.group()
def main():
    pass


@main.command()
def build():
    for container in CONTAINERS:
        pwd = os.getcwd()
        os.chdir(f"{CONTAINERS_PATH}/{container}")
        print(f"Building {container} container...")
        subprocess.run(["docker", "build", "-t", f"{container}:latest", "."])
        os.chdir(pwd)


@main.command()
def prune():
    for path in [
        "/etc/nginx/conf.d",
        "/etc/nginx/sites-enabled",
        "/etc/nginx/sites-available",
    ]:
        subprocess.run(["rm", "-rf", path])
    subprocess.run(["docker", "system", "prune", "-a", "-f"])
