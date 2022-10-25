from flask import Flask, render_template, request
import math

app = Flask(__name__)


@app.route('/')
def hello_world():
    title = "Raspberry Pi Ball Balancer"
    return render_template("main.html", title = title )

@app.route('/joints', methods=['GET', 'PUT'])
def joints( ):
    j1 = request.args['j1']
    j2 = request.args['j2']
    j3 = request.args['j3']
    j4 = request.args['j4']

    j1 = float(j1)/180.0 * math.pi 
    j2 = float(j2)/180.0 * math.pi 
    j3 = float(j3)/180.0 * math.pi 
    j4 = float(j4)/180.0 * math.pi 

    print(f"Setting joints: j1 = {j1/math.pi * 180.0}")
    print(f"Setting joints: j2 = {j2/math.pi * 180.0}")
    print(f"Setting joints: j3 = {j3/math.pi * 180.0}")
    print(f"Setting joints: j4 = {j4/math.pi * 180.0}")

    return f"Ok"

@app.route('/test/<param>', methods=['GET', 'POST'])
def test( param ):
    print("/test received param", param)
    return "ok"
    
def create_app():
    print("create_app")
    app.run( )

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=8080 )


