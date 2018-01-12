import time
import sys
import json

import paho.mqtt.client as mqtt

from watertank import Watertank


def broadcastMqtt(client, server, port, prefix, postfix, data):
  # Publishing the results to MQTT
  mqttc = mqtt.Client(client)
  mqttc.connect(server, port)

  topic = prefix + "/" + postfix

  print "MQTT Publish", topic, data
  mqttc.publish(topic, data)

  mqttc.loop(2)

def main(argv):

  print "Starting"

  configuration = json.load(open('configuration.json'))
  #f configuration.has_key("mqtt-client") is False:
  configuration["mqtt-client"] = "Watertank-Mqtt"

  if configuration.has_key("mqtt-server") is False:
    configuration["mqtt-server"] = "127.0.0.1"

  if configuration.has_key("mqtt-port") is False:
    configuration["mqtt-port"] = 1883

  #if configuration.has_key("mqtt-prefix") is False:
  configuration["mqtt-prefix"] = "watertank"

  print "Configuration:"
  print "MQTT Client:   ", configuration["mqtt-client"]
  print "MQTT Server:   ", configuration["mqtt-server"]
  print "MQTT Port:     ", configuration["mqtt-port"]
  print "MQTT Prefix   :", configuration["mqtt-prefix"]

  watertank = Watertank()

  watertank.clean()
  watertank.setup()

  level = 0.0
  for i in range(0,20):
    level = level + watertank.measure()
    time.sleep(1)

  level = level / 20.0
  print "Level = {} %".format(level)

  watertank.clean()

  watertank = {}
  watertank["level"] = level
  watertank["level_alert_min"] = 30.0
  if level < watertank["level_alert_min"]:
    watertank["level_status"] = "level_too_low"
  else:
    watertank["level_status"] = "level_good"

  sensorId = "1"

  broadcastMqtt(
    configuration["mqtt-client"], 
    configuration["mqtt-server"], 
    configuration["mqtt-port"], 
    configuration["mqtt-prefix"], 
    sensorId + "/update",
    json.dumps(watertank))

if __name__ == "__main__":
  main(sys.argv)