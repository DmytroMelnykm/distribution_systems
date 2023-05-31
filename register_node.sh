#!/usr/bin/env sh

# Замените значения переменных на соответствующие вашему сервису
SERVICE_NAME=$PORT_SERVICE
SERVICE_ADDRESS="localhost"
SERVICE_PORT=$PORT_SERVICE

# Определение данных для регистрации сервиса
SERVICE_DATA='{
  "Name": "'$SERVICE_NAME'",
  "Address": "'$SERVICE_ADDRESS'",
  "Port": '$SERVICE_PORT'
}'

# Выполнение запроса на регистрацию сервиса
curl -X PUT -d "$SERVICE_DATA" http://consul-service:8500/v1/agent/service/register

hz start