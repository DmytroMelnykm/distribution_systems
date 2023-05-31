# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.11.1-alpine

ENTRYPOINT ["./register_node.sh"]