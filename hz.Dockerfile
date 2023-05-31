# syntax=docker/dockerfile:1

# pull official base image
FROM hazelcast/hazelcast:latest

WORKDIR /opt/hazelcast/
COPY register_node.sh /opt/hazelcast/

ENTRYPOINT ["./register_node.sh"]