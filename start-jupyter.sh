#!/bin/bash
docker run -d --rm -p 8888:8888 -v $(pwd):/home/jovyan \
  ghcr.io/sorosliu1029/euler \
  start-notebook.sh --NotebookApp.password='sha1:34147a04de8e:28b0c1d0c034adf65f78074e69253c7f83e18144'