# dark_enhanced_dirtree

## install mkdocs

```bash
python -m pip install mkdocs

# to upgrade
python -m pip install --upgrade mkdocs
```

## install theme

```bash
pip install mkdocs-dark-enhanced-dirtree
```

### Manual installation

```bash
# first, download the archive
pip install mkdocs-dark_enhanced_dirtree-1.2.0.tar.gz
```

## setup

```bash
python -m mkdocs new proj1
code proj1/
nano mkdocs.yml
```

```yml
site_name: My Docs
theme:
  name: dark_enhanced_dirtree
```

```bash
python -m mkdocs serve
```
