# Architecture

dovi is organized around two pipelines that share a common document model and render backends.

```
              ┌──────────────┐   ┌────────────────────┐   ┌──────────────┐
 prompt ───▶  │ LayoutPlanner│──▶│ ContentSynthesizer │──▶│ RenderBackend│──▶ PDF / DOCX / HTML
              └──────────────┘   └────────────────────┘   └──────────────┘

              ┌──────────────┐   ┌────────────────────┐   ┌──────────────┐
 source ───▶  │LayoutAnalyzer│──▶│   VariantSampler   │──▶│ RenderBackend│──▶ PDF / DOCX / HTML
              └──────────────┘   └────────────────────┘   └──────────────┘
```

## Components

- **`DocumentGenerator` / `DocumentReplicator`**: the public entry points. They hold the
  options and dispatch work to a pipeline.
- **Pipelines** (`dovi.pipeline`): orchestrate the components, record timings and collect errors.
- **Models** (`dovi.models`): planning, content synthesis, layout analysis and variant sampling.
- **Backends** (`dovi.backend`): turn a `DoviDocument` into a concrete file format. Custom
  backends can be added with `register_render_backend`.
