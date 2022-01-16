# systemp

Simple Python app for Linux system temperature monitoring to be consumed
by Prometheus.

## Install

- This needs Prometheus Python client API library:
```
sudo apt-get install -y python3-prometheus-client
```
- clone the repository to `/srv/`:
```
sudo mkdir -p /srv/systemp
sudo chown $USER /srv/systemp
git clone https://github.com/vladak/systemp.git /srv/systemp
```
- copy `systemp.service` file to `/etc/systemd/system/systemp.service`:
```
sudo cp /srv/systemp/systemp.service /etc/systemd/system/systemp.service
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
$ curl http://localhost:8222/

...

CPU_temp_teplota 58.913
```
