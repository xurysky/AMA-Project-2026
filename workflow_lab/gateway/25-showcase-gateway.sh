#!/bin/sh
set -eu
: "${SHOWCASE_GATEWAY_KEY:?Private upstream gateway key is required}"
: "${AMA_WORKFLOW_FUNCTION_KEY:?Workflow key is required}"
envsubst '${SHOWCASE_GATEWAY_KEY} ${AMA_WORKFLOW_FUNCTION_KEY}' < /etc/nginx/showcase.conf.template > /etc/nginx/nginx.conf
