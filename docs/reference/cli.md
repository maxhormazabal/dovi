# CLI reference

```
dovi [--version] [-v] COMMAND [ARGS]...
```

## `dovi generate`

Generate a new document from a natural-language description.

| Option          | Default       | Description                                    |
| --------------- | ------------- | ---------------------------------------------- |
| `--type`, `-t`  | `generic`     | Document type (`invoice`, `receipt`, `form`…). |
| `--pages`, `-p` | `1`           | Number of pages.                               |
| `--lang`, `-l`  | `en`          | Language of the content.                       |
| `--to`          | `pdf`         | Output format.                                 |
| `--output`,`-o` | `.`           | Output directory.                              |
| `--provider`    | `openai`      | Model provider.                                |
| `--model`       | `gpt-4o-mini` | Model identifier.                              |
| `--seed`        |               | Random seed.                                   |

## `dovi replicate`

Create variants of an existing document.

| Option             | Default     | Description                                  |
| ------------------ | ----------- | -------------------------------------------- |
| `--variants`, `-n` | `1`         | Number of variants.                          |
| `--strategy`       | `synthetic` | `synthetic`, `perturb` or `preserve`.        |
| `--to`             | `pdf`       | Output format.                               |
| `--output`, `-o`   | `.`         | Output directory.                            |
| `--seed`           |             | Random seed.                                 |
