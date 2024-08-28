FROM docker.io/archlinux/archlinux

RUN pacman --noconfirm -Syu git base-devel unzip zip wget curl sudo less python nodejs bash-completion gdal

RUN useradd -m -s /bin/bash dev

RUN echo "dev ALL=(ALL) NOPASSWD: /usr/bin/pacman" > /etc/sudoers.d/dev

USER dev
WORKDIR /home/dev

RUN curl -s "https://get.sdkman.io" | bash

RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install java 21.0.2-tem"