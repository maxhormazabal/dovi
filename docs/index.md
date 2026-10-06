<p align="center">
  <img src="assets/logotipo.png" alt="dovi" width="420">
</p>

# dovi

**dovi** generates and replicates documents for Document AI.

- **Generate** new documents from a natural-language description.
- **Replicate** existing documents: keep their layout and style, replace their content.
- Get every result both as a rendered file (PDF, DOCX, HTML) and as a structured
  `DoviDocument` with text, tables, pictures and their positions on the page.

```python
from dovi.document_generator import DocumentGenerator

generator = DocumentGenerator()
result = generator.generate("Two-page quarterly report for a small solar energy cooperative")
print(result.document.export_to_markdown())
```

## Why dovi?

Document understanding models need large amounts of annotated documents, and real documents
are often private, scarce or expensive to label. dovi produces realistic documents together with
their ground truth, so datasets can be created, extended and rebalanced on demand.

<p align="center">
  <img src="assets/mascot.png" alt="dovi mascot" width="160">
</p>
