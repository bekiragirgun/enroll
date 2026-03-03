FROM ubuntu:22.04

# Temel paketler
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    sudo \
    bash-completion \
    coreutils \
    grep \
    sed \
    gawk \
    findutils \
    tree \
    vim \
    nano \
    man-db \
    manpages \
    curl \
    wget \
    iproute2 \
    iputils-ping \
    net-tools \
    htop \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Öğrenci kullanıcısı oluştur
RUN useradd -m -s /bin/bash -p $(openssl passwd -1 ogrenci) ogrenci

# Öğretmen kullanıcısı oluştur (sudo yetkili)
RUN useradd -m -s /bin/bash -p $(openssl passwd -1 ogretmen123) ogretmen && \
    usermod -aG sudo ogretmen

# Çalışma dizinleri
RUN mkdir -p /home/ogrenci/{egitim,pratik,testler,loglar} && \
    chown -R ogrenci:ogrenci /home/ogrenci

# Öğretmen için de dizin oluştur
RUN mkdir -p /home/ogretmen/{dersler,ogrenci-calisma} && \
    chown -R ogretmen:ogretmen /home/ogretmen

# Bash yapılandırması (öğrenci için)
RUN echo 'export PS1="\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "' >> /home/ogrenci/.bashrc && \
    echo 'alias ll="ls -la"' >> /home/ogrenci/.bashrc && \
    echo 'alias ..="cd .."' >> /home/ogrenci/.bashrc

# Bash yapılandırması (öğretmen için)
RUN echo 'export PS1="\[\033[01;31m\]ÖĞRETMEN@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "' >> /home/ogretmen/.bashrc && \
    echo 'alias ll="ls -la"' >> /home/ogretmen/.bashrc

WORKDIR /home/ogrenci

CMD ["/bin/bash"]
