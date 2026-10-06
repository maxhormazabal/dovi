from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from dovi.datamodel.base_models import DocumentType, OutputFormat, TaskStatus
from dovi.datamodel.pipeline_options import (
    ContentStrategy,
    GenerationOptions,
    ModelOptions,
    ModelProvider,
    ReplicationOptions,
)
from dovi.version import __version__

app = typer.Typer(
    name="dovi",
    help="Generate and replicate documents for Document AI.",
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_enable=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"dovi {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],  # noqa: UP045
        typer.Option("--version", callback=_version_callback, is_eager=True),
    ] = None,
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
) -> None:
    level = logging.WARNING - 10 * min(verbose, 2)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


@app.command()
def generate(
    prompt: Annotated[str, typer.Argument(help="Description of the document to generate.")],
    document_type: Annotated[
        DocumentType, typer.Option("--type", "-t", help="Document type.")
    ] = DocumentType.GENERIC,
    num_pages: Annotated[int, typer.Option("--pages", "-p", min=1)] = 1,
    language: Annotated[str, typer.Option("--lang", "-l")] = "en",
    to: Annotated[OutputFormat, typer.Option("--to", help="Output format.")] = OutputFormat.PDF,
    output: Annotated[Path, typer.Option("--output", "-o")] = Path("."),
    provider: Annotated[ModelProvider, typer.Option()] = ModelProvider.OPENAI,
    model_id: Annotated[str, typer.Option("--model")] = "gpt-4o-mini",
    seed: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP045
) -> None:
    """Generate a new document from a natural-language description."""
    from dovi.document_generator import DocumentGenerator

    options = GenerationOptions(
        document_type=document_type,
        num_pages=num_pages,
        language=language,
        output_format=to,
        seed=seed,
        model=ModelOptions(provider=provider, model_id=model_id),
    )
    result = DocumentGenerator(options).generate(prompt, output_dir=output)
    for artifact in result.artifacts:
        typer.echo(f"wrote {artifact.path}")
    _report(result.status, [e.error_message for e in result.errors])


@app.command()
def replicate(
    source: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    num_variants: Annotated[int, typer.Option("--variants", "-n", min=1)] = 1,
    strategy: Annotated[ContentStrategy, typer.Option()] = ContentStrategy.SYNTHETIC,
    to: Annotated[OutputFormat, typer.Option("--to", help="Output format.")] = OutputFormat.PDF,
    output: Annotated[Path, typer.Option("--output", "-o")] = Path("."),
    seed: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP045
) -> None:
    """Create variants of an existing document that keep its layout and style."""
    from dovi.document_replicator import DocumentReplicator

    options = ReplicationOptions(
        num_variants=num_variants, content_strategy=strategy, output_format=to, seed=seed
    )
    result = DocumentReplicator(options).replicate(source, output_dir=output)
    for artifact in result.artifacts:
        typer.echo(f"wrote {artifact.path}")
    _report(result.status, [e.error_message for e in result.errors])


def _report(status: TaskStatus, errors: list[str]) -> None:
    for message in errors:
        typer.secho(f"error: {message}", fg=typer.colors.RED, err=True)
    if status is TaskStatus.FAILURE:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
