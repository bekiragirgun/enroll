FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    python3 \
    python3-pip \
    gcc \
    g++ \
    make \
    nano \
    vim \
    git \
    curl \
    wget \
    net-tools \
    man-db \
    sudo \
    openssh-client \
    iputils-ping \
    tree \
    htop \
    less \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash -G sudo ogrenci && \
    echo "ogrenci:ogrenci" | chpasswd && \
    echo "ogrenci ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /home/ogrenci
USER ogrenci

CMD ["/bin/bash"]
