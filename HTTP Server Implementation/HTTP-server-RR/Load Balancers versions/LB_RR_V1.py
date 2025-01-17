from flask import Flask, redirect, request
import itertools

app = Flask(__name__)

servers = [
    "http://127.0.0.1:5001",  #server1
    "http://127.0.0.1:5002",  #server2
]

#RR
server_iterator = itertools.cycle(servers)

@app.route('/')
def load_balancer():
    target_server = next(server_iterator)
    return redirect(target_server)    #eg: redirect(http://127.0.0.1:5001)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

#run instead --> gunicorn -w 4 -b 127.0.0.1:5000 load_balancer:app
