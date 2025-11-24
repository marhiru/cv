# Python OpenCV lab repository
- I made this repository with the intention of using as my personal laboratory.

**This repository will contain several projects using computer-vision models**

## Stack
### Language
- [Python 3.14](https://python.org/)

### Project manager 
- [uv](https://docs.astral.sh/uv/) (Python package and project manager)

### Packages 
- [OpenCV](https://opencv.org/)


**Attention** For every python project that you will work with, use this lsp configuration below to active pyright LSP.


`(pyrightconfig.json)`
```json
{
    "venvPath": ".",
    "venv": ".venv",
    "pythonVersion": "3.13",
    "include": [
        "."
    ],
    "executionEnviroments": [
        {
            "pythonPath": ".venv/bin/python",
            "strictListInference": true,
            "reportUnusedVariable": "warning",
            "typeCheckingMode": "basic",
            "reportUnusedFunction": "warning"
        }
    ],
    "exclude": [
        "**/__pycache__",
        ".venv"
    ]
}
```
