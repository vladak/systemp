from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    mydict = {}

    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp = float(f.read()) / 1000
        mydict['cpu'] = temp

    return mydict


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    print(index())
