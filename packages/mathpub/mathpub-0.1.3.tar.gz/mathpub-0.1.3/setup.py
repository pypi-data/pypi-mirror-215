from setuptools import setup

setup(
    name="mathpub",
    description="small library for quick formatting of math calculations",
    packages=["mathpub"],
    author_email="timur20041229@gmail.com",
    requires=["IPython", "ipywidgets"],
    zip_safe=False,
    version="0.1.3"
)
