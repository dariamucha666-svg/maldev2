FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
        nmap netcat-openbsd dnsutils ldap-utils smbclient krb5-user \
        python3 python3-pip pipx john wordlists \
        impacket-scripts responder enum4linux-ng \
        iproute2 iputils-ping curl wget vim less jq \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y netexec 2>/dev/null || pipx install netexec
RUN pip install --no-cache-dir bloodhound

RUN command -v kerbrute >/dev/null 2>&1 || { \
        curl -fsSL -o /usr/local/bin/kerbrute \
          https://github.com/ropnop/kerbrute/releases/latest/download/kerbrute_linux_amd64 && \
        chmod +x /usr/local/bin/kerbrute ; }

RUN echo "10.10.0.2 dc01.xmask.lab dc01" >> /etc/hosts
COPY krb5.conf /etc/krb5.conf

WORKDIR /root
CMD ["/bin/bash"]
