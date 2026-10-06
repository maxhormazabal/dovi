<p align="center">
  <img src="https://raw.githubusercontent.com/maxhormazabal/dovi/main/docs/assets/logotipo.png" alt="dovi" width="420">
</p>

<p align="center">
  <a href="https://pypi.org/project/dovi/"><img src="https://img.shields.io/pypi/v/dovi" alt="PyPI version"></a>
  <a href="https://pypi.org/project/dovi/"><img src="https://img.shields.io/pypi/pyversions/dovi" alt="Python versions"></a>
  <a href="https://github.com/maxhormazabal/dovi/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/code%20style-ruff-000000" alt="Ruff"></a>
</p>

# dovi

**dovi** generates and replicates documents for Document AI. Describe a document and get a
rendered PDF, DOCX or HTML file together with a structured representation of its content and
layout, or take an existing document and produce new variants that keep its look and structure.

It is built for teams that need realistic, annotated documents to train and evaluate document
understanding models: invoices, receipts, forms, letters, contracts, statements and more.

## Features

- 🧾 **Document generation** from a natural-language description, with typed templates for
  common business documents
- 🪞 **Document replication**: keep the layout and style of a source document while replacing its content
- 🧱 Unified `DoviDocument` representation with pages, text, tables, pictures and bounding boxes
- 📤 Export to PDF, DOCX, HTML, Markdown and lossless JSON
- 🔌 Works with any OpenAI-compatible endpoint, including local models served by Ollama or vLLM
- 💻 Simple and convenient CLI

### Coming soon

- 🖼️ Layout analysis for PDF and scanned image sources
- 🏷️ Ground-truth export for layout and key-value benchmarks (COCO, DocLayNet-style, FUNSD-style)
- 🎨 Visual augmentations: scanning noise, rotations, stamps and handwriting

## Installation

```bash
pip install dovi
```

Optional extras enable additional render backends and model providers:

```bash
pip install "dovi[pdf]"    # PDF rendering via WeasyPrint
pip install "dovi[docx]"   # DOCX rendering via python-docx
pip install "dovi[llm]"    # remote and local language models
pip install "dovi[all]"
```

Works on macOS, Linux and Windows, with Python 3.10 or newer.

## Getting started

### Generate a document

```python
from dovi.document_generator import DocumentGenerator
from dovi.datamodel.base_models import DocumentType

generator = DocumentGenerator(document_type=DocumentType.INVOICE)
result = generator.generate(
    "Invoice from a Barcelona design studio to a logistics company, six line items, VAT 21%",
    output_dir="out/",
)
print(result.document.export_to_markdown())
```

### Replicate a document

```python
from dovi.document_replicator import DocumentReplicator
from dovi.datamodel.pipeline_options import ReplicationOptions

replicator = DocumentReplicator(ReplicationOptions(num_variants=20, seed=7))
result = replicator.replicate("samples/invoice.pdf", output_dir="out/variants/")

for doc in result.documents:
    print(doc.name, doc.num_pages)
```

### CLI

```bash
dovi generate "Rental agreement for a two-bedroom flat in Madrid" --type contract --pages 3 --to pdf -o out/
dovi replicate samples/invoice.pdf --variants 20 -o out/variants/
```

Run `dovi --help` for the full list of options.

## Configuration

Model access is configured through `ModelOptions`:

```python
from dovi.datamodel.pipeline_options import GenerationOptions, ModelOptions, ModelProvider

options = GenerationOptions(
    language="es",
    model=ModelOptions(
        provider=ModelProvider.OLLAMA,
        model_id="qwen2.5:14b",
    ),
)
```

API keys are read from `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` when not set explicitly.

## Documentation

Full documentation lives in [`docs/`](https://github.com/maxhormazabal/dovi/tree/main/docs) and
can be served locally with `mkdocs serve`.

## Contributing

Contributions are welcome. Please read the
[contributing guidelines](https://github.com/maxhormazabal/dovi/blob/main/CONTRIBUTING.md)
before opening a pull request.

## License

dovi is released under the [Apache License 2.0](https://github.com/maxhormazabal/dovi/blob/main/LICENSE).
