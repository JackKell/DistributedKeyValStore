# Distributed Key Value Store Project

## Install Instructions

### General Setup
```
make setup
source env/bin/activate
```
#### Sever Setup
```
python server.py "port"
```

#### Client Setup
```
python server.py "server ip address" "port number"
```
### Example
#### On Server Nodes
```
make setup
source env/bin/activate
python server.py 5555
```
#### On Client Nodes
```
make setup
source env/bin/activate
python server.py 5555
```
