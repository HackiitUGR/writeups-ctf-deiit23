FROM ubuntu:22.04
RUN apt update && apt install -y socat
RUN adduser --disabled-password challenge
COPY challenge/ /challenge/

EXPOSE 31337
USER challenge
CMD cd /challenge && ./start.sh