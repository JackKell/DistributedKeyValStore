# Distributed Key Value Store Project

## Install Instructions

### General Setup
```
make setup
```
```
source env/bin/activate
```
### Sever Setup
```
python server.py "tcp port" "udp port" "rpc port"
```
### Client Setup
Where transmission method must equal, tcp, udp, or rpc
```
python server.py "server ip address" "port number" "transmission method"
```
