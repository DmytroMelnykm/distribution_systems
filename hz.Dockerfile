# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.11.1-alpine

ENTRYPOINT ["./opt/hazelcast/register_node.sh"]

CMD ["hz start"]