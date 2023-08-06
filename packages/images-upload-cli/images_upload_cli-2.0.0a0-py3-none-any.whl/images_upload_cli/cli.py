#!/usr/bin/env python
"""Entrypoint for cli."""

import asyncio
from collections.abc import Callable
from pathlib import Path

import click
from dotenv import load_dotenv
from httpx import AsyncClient
from pyperclip import copy

from images_upload_cli.upload import HOSTINGS, UPLOAD
from images_upload_cli.util import get_config_path, make_thumbnail, notify_send


@click.command(context_settings={"show_default": True})
@click.argument(
    "images",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("-h", "--hosting", type=click.Choice(HOSTINGS), default="imgur")
@click.option("-b", "--bbcode", is_flag=True, help="Add bbcode tags.")
@click.option("-t", "--thumbnail", is_flag=True, help="Add caption thumbnail and bbcode tags.")
@click.option(
    "-n/-N",
    "--notify/--no-notify",
    is_flag=True,
    default=False,
    help="Send desktop notifications via libnotify.",
)
@click.option(
    "-c/-C",
    "--clipboard/--no-clipboard",
    is_flag=True,
    default=True,
    help="Copy result to clipboard.",
)
@click.version_option()
def cli(
    images: tuple[Path],
    hosting: str,
    bbcode: bool,
    thumbnail: bool,
    notify: bool,
    clipboard: bool,
) -> None:
    """Upload images via APIs."""
    # loading .env variables
    load_dotenv(dotenv_path=get_config_path())

    # images upload
    links = asyncio.run(
        upload_images(
            upload_func=UPLOAD[hosting],
            images=images,
            bbcode=bbcode,
            thumbnail=thumbnail,
        )
    )

    # out
    links_str = " ".join(links)
    click.echo(links_str)
    if clipboard:
        copy(links_str)
    if notify:
        notify_send(links_str)


async def upload_images(
    upload_func: Callable,
    images: tuple[Path],
    bbcode: bool,
    thumbnail: bool,
) -> list[str]:
    """Upload images."""
    links = []

    async with AsyncClient() as client:
        for img_path in images:
            img = img_path.read_bytes()

            if not thumbnail:
                img_link = await upload_func(client, img)
                link = f"[img]{img_link}[/img]" if bbcode else img_link
            else:
                img_link = await upload_func(client, img)
                thumb_link = await upload_func(client, make_thumbnail(img))
                link = f"[url={img_link}][img]{thumb_link}[/img][/url]"

            links.append(link)

    return links
