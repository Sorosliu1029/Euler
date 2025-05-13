FROM quay.io/jupyter/minimal-notebook:latest
LABEL author="Soros Liu"
RUN pip install beautifulsoup4 lxml Jinja2 nbconvert
