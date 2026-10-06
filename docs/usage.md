# Usage

## Generating documents

```python
from dovi.document_generator import DocumentGenerator
from dovi.datamodel.base_models import DocumentType, OutputFormat
from dovi.datamodel.pipeline_options import GenerationOptions

options = GenerationOptions(
    document_type=DocumentType.INVOICE,
    language="es",
    num_pages=1,
    output_format=OutputFormat.PDF,
    seed=42,
)
generator = DocumentGenerator(options)
result = generator.generate(
    "Factura de un estudio de arquitectura a una constructora, IVA 21%",
    output_dir="out/",
)

print(result.status)
print(result.document.export_to_markdown())
```

Generate many documents in one go with `generate_all`:

```python
prompts = [
    "Receipt from a Lisbon bakery, 4 items, paid by card",
    "Receipt from a hardware store in Lyon, 9 items, paid in cash",
]
for result in generator.generate_all(prompts, output_dir="out/receipts/"):
    print(result.document.name, result.status)
```

## Replicating documents

```python
from dovi.document_replicator import DocumentReplicator
from dovi.datamodel.pipeline_options import ContentStrategy, ReplicationOptions

options = ReplicationOptions(
    num_variants=50,
    content_strategy=ContentStrategy.SYNTHETIC,
    preserve_layout=True,
    layout_jitter=0.1,
    seed=7,
)
replicator = DocumentReplicator(options)
result = replicator.replicate("samples/invoice.pdf", output_dir="out/variants/")
```

### Content strategies

| Strategy    | Description                                                            |
| ----------- | ---------------------------------------------------------------------- |
| `synthetic` | Replace all content with new, consistent values from a language model. |
| `perturb`   | Keep the content but change entities, amounts and dates.               |
| `preserve`  | Keep the content and only vary layout and rendering.                   |

## Working with results

Every pipeline returns a result with a `status`, the produced `DoviDocument`(s), the rendered
`artifacts` and any `errors`:

```python
doc = result.document
doc.export_to_markdown()
doc.export_to_dict()
doc.save_as_json("invoice.json")
```
