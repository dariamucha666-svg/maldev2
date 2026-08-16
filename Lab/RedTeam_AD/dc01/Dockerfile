FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        samba samba-ad-provision samba-dsdb-modules samba-ad-dc \
        smbclient winbind dnsutils ldb-tools acl attr ca-certificates tini \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 53/udp 53 88 135 139 389 445 464 636 3268 3269
ENTRYPOINT ["tini", "--", "/usr/local/bin/entrypoint.sh"]
