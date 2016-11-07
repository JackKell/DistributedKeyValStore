# Distributed Key Value Store Project

## Install Instructions

### General Setup
```
cd path/DistributedKeyValStore
make setup
source env/bin/activate
```
#### Sever Setup
```
python server.py "port"
```

#### Client Setup
```
python client.py "server ip address" "port number"
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
python client.py n03 5555
```

### Additional Notes
For the purposes of project 2 testing I have made it so the servers should be run on server nodes "n03", "n04", "n05", "n06", and "n07" and the client can be run on any of the nodes that are not also running a server. Additionally, if you want to change the the servers that are used in the cluster simply go into the `server.py` file and change the servers list `keyValServer.servers = ["n03", "n04", "n05", "n06", "n07"]` to be only the server nodes that you want. By doing this you can change the servers that are used and or the number of servers used.

