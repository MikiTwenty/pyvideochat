from pyvideochat import Server

# initialize the server
server = Server()

# start the server
server.connect()

# start the videochat
server.start()

# close the server
server.close()