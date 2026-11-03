ARG BASE_IMAGE
FROM ${BASE_IMAGE}
ARG SOURCE_REVISION
LABEL org.opencontainers.image.revision=$SOURCE_REVISION
COPY nginx.conf /etc/nginx/showcase.conf.template
COPY 25-showcase-gateway.sh /docker-entrypoint.d/25-showcase-gateway.sh
RUN chmod 755 /docker-entrypoint.d/25-showcase-gateway.sh
