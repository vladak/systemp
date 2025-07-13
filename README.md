# systemp

Simple Python app for Linux system temperature monitoring to be consumed
by Prometheus.

## Install

- clone the repository to `/srv/`:
```
which git || sudo apt-get install -y git
sudo mkdir -p /srv/systemp
sudo chown $USER /srv/systemp
git clone https://github.com/vladak/systemp.git /srv/systemp
```
- install requirements:
```
python3 -m venv env
. ./env/bin/activate
python3 -m pip install -r requirements.txt
```

## Setup

Create `/srv/systemp/environment` file with the arguments:
```
cat << EOF >/srv/systemp/environment
ARGS=--mqtt_hostname example.com --mqtt_topic foo/bar
EOF
```

## Start

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

Setup MQTT Prometheus exporter (see https://github.com/vladak/weather),
add the following snippet to `/etc/prometheus/mqtt-exporter.yaml` under the
`metrics`:
```yml
  -
    # The name of the metric in prometheus
    prom_name: sys_temperature
    # The name of the metric in a MQTT JSON message
    mqtt_name: sys_temperature
    # The prometheus help text for this metric
    help: temperature reading
    # The prometheus type for this metric. Valid values are: "gauge" and "counter"
    type: gauge
    # A map of string to string for constant labels. This labels will be attached to every prometheus metric
    #const_labels:
    #  sensor_type: dht22
```

Assumes labeling done in Prometheus config `/etc/prometheus/prometheus.yml`:

```yml
  - job_name: mqtt
    # If prometheus-mqtt-exporter is installed, grab metrics from external sensors.
    static_configs:
      - targets: ['localhost:9641']
    # The MQTT based sensor publish the data only now and then.
    scrape_interval: 1m
    # Add the location as a tag.
    metric_relabel_configs:
     - source_labels: [topic]
       target_label: location
       regex: 'devices/([[:alnum:]]*)/[[:alnum:]]*'
       action: replace
       replacement: "$1"
     - source_labels: [topic]
       target_label: name
       regex: 'devices/[[:alnum:]]*/([[:alnum:]]*)'
       action: replace
       replacement: "$1"
```

## Links

- https://betterstack.com/community/guides/monitoring/prometheus-relabeling/

