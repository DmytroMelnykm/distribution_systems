#!/usr/bin/env sh

SERVICE_NAME=$PROXY_SERVICE
SERVICE_ADDRESS=$PROXY_SERVICE
SERVICE_PORT=$PORT_SERVICE

SERVICE_DATA='{
  "Name": "'$SERVICE_NAME'",
  "Address": "'$SERVICE_ADDRESS'",
  "Port": '$SERVICE_PORT'
}'

curl -X PUT -d "$SERVICE_DATA" http://consul-service:8500/v1/agent/service/register

hz start