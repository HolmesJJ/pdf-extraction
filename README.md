# PDF Extraction

* [Layout Parser](https://github.com/Layout-Parser/layout-parser?tab=readme-ov-file)
* [Layout Parser's Documentation](https://layout-parser.readthedocs.io/en/latest/)
* [Layout Parser Model Training](https://www.kaggle.com/code/ammarnassanalhajali/layout-parser-model-training)

## Quick Start

### Python

1. Install Anaconda following the [link](https://docs.anaconda.com/anaconda/install/index.html).

2. Create and activate environment using the following commands.
```
# Create Python environment
conda create --name pdf-extraction python=3.10.10

# Check Python environment
conda info --envs

# Activate environment
conda activate pdf-extraction

# Deactivate environment
conda deactivate

# Remove environment
conda remove -n pdf-extraction --all
```

3. Install `requirements.txt`.
```
pip install -r /path/to/requirements.txt
```

4. Bugs Resolved.
* https://pypi.org/project/pdf2image/
* https://github.com/orgs/Homebrew/discussions/5373
* https://github.com/facebookresearch/detectron2/issues/5216
* https://github.com/facebookresearch/detectron2/issues/5010
* https://github.com/Layout-Parser/layout-parser/issues/168
