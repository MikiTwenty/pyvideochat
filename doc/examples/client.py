from pyvideochat import Client

# initialize the client
client = Client()

# connect to the server
client.connect()

# start the videochat
client.start()

# close the client
client.close()