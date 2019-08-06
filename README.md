# systemp
Simple Python flask app for Linux system temperature monitoring

## Install

- clone the repository to `/srv/`:
```
    git clone https://github.com/vladak/weather.git /srv/weather
```
- install Python and Flask
```
sudo apt-get -y install python3-venv
python3 -m venv install venv
. ./venv/bin/activate
pip install flask
```
- copy `systemp.service` file to `/etc/systemd/system/systemp.service`:
```
sudo cp systemp.service /etc/systemd/system/systemp.service
```
- enable the service:
```
sudo systemctl enable systemp
```
- if the file `/etc/systemd/system/systemp.service` changes, run:
```
sudo systemctl daemon-reload
```
- to start the service:
```
sudo systemctl start systemp
sudo systemctl status systemp
```

## Use
```
$ curl http://localhost:5000/
{"cpu":57.452}
```
