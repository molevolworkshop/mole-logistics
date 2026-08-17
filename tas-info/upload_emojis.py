#!/usr/bin/env python3
"""
Upload emojis dumped by `slackdump emoji` into a Discord guild, using the
naming convention that pR0Ps/slack-to-discord expects.

Run this BEFORE running slack-to-discord: the importer builds its emoji map
once at startup from the emojis already present in the guild.

Usage:
    python3 upload_emojis.py --source emojis.zip --guild "My Server" --token TOKEN
    python3 upload_emojis.py --source emojis/ --guild "My Server" --token TOKEN --dry-run

Requires: pip install discord.py
"""

import argparse
import asyncio
import io
import json
import os
import re
import sys
import zipfile

import discord


MAX_EMOJI_BYTES = 256 * 1024
ANIMATED_EXTS = {".gif"}
VALID_NAME = re.compile(r"^[A-Za-z0-9_]{2,32}$")


def discord_name(slack_name):
    """Apply the same transform slack-to-discord uses when looking emojis up.

    Dashes after the first character become underscores. Anything else that
    Discord rejects is stripped, but that breaks the importer's lookup, so we
    report it rather than silently mangling.
    """
    name = slack_name
    if len(name) > 1 and "-" in name[1:]:
        name = name[0] + name[1:].replace("-", "_")

    cleaned = re.sub(r"[^A-Za-z0-9_]", "", name)
    return cleaned, (cleaned != name or not VALID_NAME.match(cleaned))


class Source:
    """Reads emojis from either a directory or a zip produced by slackdump."""

    def __init__(self, path):
        self.path = path
        self._zip = zipfile.ZipFile(path) if zipfile.is_zipfile(path) else None

    def _names(self):
        if self._zip:
            return self._zip.namelist()
        out = []
        for root, _, files in os.walk(self.path):
            for f in files:
                full = os.path.join(root, f)
                out.append(os.path.relpath(full, self.path).replace(os.sep, "/"))
        return out

    def _read(self, name):
        if self._zip:
            return self._zip.read(name)
        with open(os.path.join(self.path, name), "rb") as fp:
            return fp.read()

    def aliases(self):
        """Map alias -> canonical name, from index.json if present."""
        try:
            index = json.loads(self._read("index.json"))
        except Exception:
            return {}
        out = {}
        for name, val in index.items():
            if isinstance(val, str) and val.startswith("alias:"):
                out[name] = val[len("alias:"):]
        return out

    def emojis(self):
        """Yield (slack_name, extension, bytes) for each downloaded image."""
        for entry in sorted(self._names()):
            if not entry.startswith("emojis/") or entry.endswith("/"):
                continue
            base = entry[len("emojis/"):]
            stem, ext = os.path.splitext(base)
            if not stem:
                continue
            yield stem, ext.lower(), self._read(entry)


class Uploader(discord.Client):

    def __init__(self, *args, source, guild_name, dry_run, **kwargs):
        self._source = source
        self._guild_name = guild_name
        self._dry_run = dry_run
        self.failed = 0
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        try:
            await self._run()
        finally:
            await self.close()

    async def _run(self):
        guild = discord.utils.get(self.guilds, name=self._guild_name)
        if guild is None:
            print(f"Bot is not in a guild named {self._guild_name!r}", file=sys.stderr)
            self.failed = 1
            return

        existing = {e.name for e in guild.emojis}
        limit = guild.emoji_limit
        used_static = sum(1 for e in guild.emojis if not e.animated)
        used_anim = sum(1 for e in guild.emojis if e.animated)
        print(f"{guild.name}: {used_static}/{limit} static, {used_anim}/{limit} animated in use")

        alias_map = self._source.aliases()
        if alias_map:
            print(f"{len(alias_map)} aliases in index.json (not uploaded - Discord has no aliases)")

        skipped, uploaded, renamed = [], 0, []

        for slack_name, ext, data in self._source.emojis():
            name, mangled = discord_name(slack_name)
            animated = ext in ANIMATED_EXTS

            if not VALID_NAME.match(name):
                skipped.append((slack_name, "unusable name after sanitising"))
                continue
            if mangled:
                renamed.append((slack_name, name))
            if name in existing:
                continue
            if len(data) > MAX_EMOJI_BYTES:
                skipped.append((slack_name, f"{len(data)//1024}KB exceeds 256KB"))
                continue

            used = used_anim if animated else used_static
            if used >= limit:
                pool = "animated" if animated else "static"
                skipped.append((slack_name, f"{pool} slots full"))
                continue

            if self._dry_run:
                print(f"  would upload {slack_name} -> :{name}:")
            else:
                try:
                    await guild.create_custom_emoji(
                        name=name,
                        image=data,
                        reason="Slack workspace migration",
                    )
                except discord.HTTPException as e:
                    skipped.append((slack_name, f"upload failed: {e}"))
                    continue
                print(f"  uploaded {slack_name} -> :{name}:")

            existing.add(name)
            uploaded += 1
            if animated:
                used_anim += 1
            else:
                used_static += 1
            await asyncio.sleep(1.5)

        print(f"\n{'Would upload' if self._dry_run else 'Uploaded'} {uploaded} emojis")

        if renamed:
            print(f"\n{len(renamed)} renamed to satisfy Discord's rules:")
            for old, new in renamed:
                flag = "" if VALID_NAME.match(old.replace("-", "_")) else "   <-- check this one"
                print(f"  {old} -> {new}{flag}")

        if skipped:
            print(f"\n{len(skipped)} skipped:")
            for name, why in skipped:
                print(f"  {name}: {why}")
            print("\nMessages using these will show up as literal :name: text.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", required=True, help="emoji zip or directory from `slackdump emoji`")
    ap.add_argument("--guild", required=True, help="Discord server name")
    ap.add_argument("--token", default=os.environ.get("DISCORD_TOKEN"),
                    help="bot token (or set DISCORD_TOKEN)")
    ap.add_argument("--dry-run", action="store_true", help="report without uploading")
    args = ap.parse_args()

    if not args.token:
        ap.error("no token provided (use --token or DISCORD_TOKEN)")

    client = Uploader(
        source=Source(args.source),
        guild_name=args.guild,
        dry_run=args.dry_run,
        intents=discord.Intents(guilds=True, emojis_and_stickers=True),
    )
    client.run(args.token, log_handler=None)
    sys.exit(client.failed)


if __name__ == "__main__":
    main()
