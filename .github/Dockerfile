FROM docker.io/archlinux/archlinux

LABEL org.opencontainers.image.description="Ephemaral build image for one github action run" \
      org.opencontainers.image.authors="Finn Petersen <fp7@posteo.net>" \
      org.opencontainers.image.documentation="" \
      org.opencontainers.image.licenses="" \
      org.opencontainers.image.revision="" \
      org.opencontainers.image.source="" \
      org.opencontainers.image.title="woregnets build image" \
      org.opencontainers.image.url="" \
      org.opencontainers.image.version=""

RUN pacman --noconfirm -Syu make git gcc python nodejs gdal

RUN corepack enable

COPY /requirements.txt /requirements.txt
RUN python -m venv /opt/python \
 && source /opt/python/bin/activate \
 && pip install -r /requirements.txt \
 && rm /requirements.txt