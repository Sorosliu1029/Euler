FROM jupyter/minimal-notebook:703d8b2dcb88
LABEL author="Soros Liu"
RUN pip install beautifulsoup4 lxml
