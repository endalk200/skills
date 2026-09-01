# Agent Skills Repository

This repository contains agent skills I use in my daily work. Some are original; others are adapted to fit my workflows and use cases.

## Skills

The collection currently contains 30 published skills under [`skills/`](skills/). See the [skills catalog](skills/README.md) for their purposes and invocation modes.

## Validation

Run `python3 scripts/validate-skills.py` after adding, removing, or changing skill metadata. The validator keeps the active skill directories, catalog, Claude plugin manifest, Codex metadata, and invocation policies synchronized.

## Attribution

Some of the skills in this repo are adopted from [Matt Pocock's skills](https://github.com/mattpocock/skills) and have been customized for my use cases and also adopted to work with other coding agent. Matt's skills are too dependent on claude code specific things.
