# Installation

dovi requires Python 3.10 or newer.

```bash
pip install dovi
```

## Optional extras

| Extra  | Enables                                   | Install                    |
| ------ | ----------------------------------------- | -------------------------- |
| `pdf`  | PDF rendering through WeasyPrint          | `pip install "dovi[pdf]"`  |
| `docx` | DOCX rendering through python-docx        | `pip install "dovi[docx]"` |
| `llm`  | Remote and local language model providers | `pip install "dovi[llm]"`  |
| `all`  | Everything above                          | `pip install "dovi[all]"`  |

!!! note "WeasyPrint system libraries"
    WeasyPrint depends on Pango. On macOS install it with `brew install pango`; on Debian/Ubuntu
    with `apt install libpango-1.0-0 libpangoft2-1.0-0`.

## From source

```bash
git clone https://github.com/maxhormazabal/dovi.git
cd dovi
uv sync --all-extras
```
