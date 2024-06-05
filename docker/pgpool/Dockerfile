FROM bitnami/pgpool:4.5.2
USER root
RUN apt-get update && apt-get install -y iproute2 arping iputils-ping net-tools sudo
RUN useradd --no-create-home --uid 1001 --gid 0 pgpool
RUN echo 'pgpool ALL = (ALL) NOPASSWD: /sbin/ip' >> /etc/sudoers
RUN echo 'pgpool ALL = (ALL) NOPASSWD: /usr/sbin/arping' >> /etc/sudoers
USER 1001
