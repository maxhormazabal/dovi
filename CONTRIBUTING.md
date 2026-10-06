# Contributing to dovi

Thanks for your interest in contributing!

## Development setup

We use [uv](https://docs.astral.sh/uv/) to manage the development environment.

```bash
git clone https://github.com/maxhormazabal/dovi.git
cd dovi
uv sync --all-extras
```

## Checks

Before opening a pull request, make sure the following pass:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy dovi
uv run pytest
```

## Pull requests

- Keep pull requests focused on a single change.
- Add or update tests for any behavior you change.
- Add an entry to `CHANGELOG.md` under an `Unreleased` section.
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
  (`feat:`, `fix:`, `docs:`, ...).

## Reporting issues

Please open an issue on [GitHub](https://github.com/maxhormazabal/dovi/issues) with a minimal
example that reproduces the problem, the dovi version (`dovi --version`) and your platform.
