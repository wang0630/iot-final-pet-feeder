# Iot-final-pet-feeder
The server and hx711 driver for TCSS 573 IOT final project

### How to run
`python3 start.py`
A thread will be used to deal with hx711 weight sensor, and a Flask server will handle InfluxDB communication and weight calculation. 

### How to embed Grafana into Node-red dashboard
Follow this guide: https://flows.nodered.org/flow/8e96b8630c4edc866aa0459354033c9b/in/u1hmO7pQPVSi
1. Change two flags in `/etc/grafana/grafana.ini`: `anonymous access enabled=true` and `allow_embedding=true`.
2. Click the panel you want to embed -> share -> in embed tab -> copy the url in iframe `src` attribute.
3. Create a template node containing an iframe and put the url in its src attribute.

### Database requirement
There must be a database named `final` in InfluxDB. Run `create database final` in influx command line to create it.