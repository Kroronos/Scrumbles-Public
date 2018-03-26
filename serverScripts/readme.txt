Installation instructions

The scripts in this folder are to be installed and executed on the remote server.
The code in this folder will listen to port 3306, capture incoming packets, and listen to socket on port 5005.  If there is a packet that has a keyword that indicates a change is in progress on the database, a message will be sent to all connected clients on port 5005.

place msqlportListen.sh in /etc/init.d
place sqlport folder in /usr/bin/

run the following

sudo update-rc.d mysqlportListen.sh defaults
sudo /etc/init.d/msqlportLisen.sh start
