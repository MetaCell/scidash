# Dockerfile

# Use the offical haproxy base image
FROM haproxy:1.7

# Copy our haproxy configuration into the docker container
COPY ./haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# Copy our ssl certificate into the docker container
COPY ./spike.asu.edu.pem /private/spike.asu.edu.pem

# HAProxy requires a user & group named haproxy in order to run
RUN groupadd haproxy && useradd -g haproxy haproxy

# HAProxy also requires /var/lib/haproxy/run/haproxy/ to be created before it's run
RUN mkdir -p /var/lib/haproxy/run/haproxy/
