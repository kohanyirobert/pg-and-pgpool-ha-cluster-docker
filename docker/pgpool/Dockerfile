FROM bitnami/pgpool
USER root
RUN apt-get update && apt-get install -y iproute2 arping iputils-ping net-tools
RUN echo 'pgpool ALL = (root) NOPASSWD: /sbin/ip' >> /etc/sudoers
RUN echo 'pgpool ALL = (root) NOPASSWD: /usr/sbin/arping' >> /etc/sudoers
