from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


install_requires = [
    "colorama",
    "colorlog",
    "datasets",
    "jieba",
    "pypinyin",
    "pytorch_lightning",
    "scikit_learn",
    "scipy",
    "seaborn",
    "sentencepiece",
    "setuptools",
    "spacy",
    "gradio",
    "torchmetrics",
    "transformers",
]


setup(
    name="litie",
    version="0.2.0",
    description="Pytorch-lightning Code Blocks for Information Extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xusenlinzy/lit-ie",
    author="xusenlin",
    author_email="1659821119@qq.com",
    ikeywords=["deep learning", "pytorch", "AI"],
    python_requires=">=3.7",
    setup_requires=[],
    packages=find_packages(),
    install_requires=install_requires,
)
