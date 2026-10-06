# Document model

`DoviDocument` is the format-agnostic representation produced by every pipeline.

| Field      | Description                                                    |
| ---------- | -------------------------------------------------------------- |
| `name`     | Identifier used for file names.                                |
| `metadata` | Document type, language, source document and random seed.     |
| `pages`    | Page numbers and sizes (points).                               |
| `items`    | Ordered content items: `TextItem`, `TableItem`, `PictureItem`. |

Each item carries the page it belongs to and an optional `BoundingBox`, which makes the
document directly usable as ground truth for layout and extraction tasks.

```python
for item in doc.iterate_items(page_no=1):
    print(item.kind, item.bbox)
```
