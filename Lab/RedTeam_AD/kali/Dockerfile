FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
        nmap netcat-openbsd dnsutils ldap-utils smbclient krb5-user \
        python3 python3-pip pipx git john wordlists \
        impacket-scripts responder enum4linux-ng netexec \
        iproute2 iputils-ping curl wget vim less jq \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install bloodhound

RUN command -v kerbrute >/dev/null 2>&1 || { \
        curl -fsSL -o /usr/local/bin/kerbrute \
          https://github.com/ropnop/kerbrute/releases/latest/download/kerbrute_linux_amd64 && \
        chmod +x /usr/local/bin/kerbrute ; }

COPY krb5.conf /etc/krb5.conf

WORKDIR /root
CMD ["/bin/bash"]
