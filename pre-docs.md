

1. `ztc project make_doc  . `: create the rst files into the docs folder
2. install https://github.com/codejamninja/sphinx-markdown-builder
3 `cd docs` and create a `conf.py` file
4. `sphinx-build -M markdown ./build` generates the md files starting from the rst files.
5. Copy the md generated files into the docs folder of the mkdocs documentation