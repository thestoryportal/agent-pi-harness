# ArhuGula

Portable Pi-orchestrated agent development environment.

## Quickstart

```bash
just cldii        # Bootstrap: claude --init "/install"
just prime        # Load project context
```

## Architecture

Four-layer architecture: Skill -> Subagent -> Command -> Justfile recipe.

Run `just --list` to see all available recipes.
