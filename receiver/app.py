import connexion
from connexion import NoContent

import datetime
import json
from pykafka import KafkaClient
import yaml
import requests
import logging
import logging.config

# MAX_EVENTS = 10
# EVENT_FILE = "events.json"

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def record_completed_sales(body):
    """Creates a list of recent posted sales and stores them in a json file"""
    # status_code = requests.post(app_config['eventstore1']['url'], json=body).status_code
    status_code = 201

    logger.info("Returned event sales request with a unique id of" + str(body["title"]))
    logger.info("Returned event sales response (Id:" + str(body["title"]) + ") with status " + str(status_code))

#    record_last_ten(body)

    client = KafkaClient(hosts="%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"]))
    topic = client.topics[str.encode(app_config["events"]['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "record_completed_sales",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201


def record_completed_returns(body):
    """Creates a list of recent posted return and stores them in a json file"""
#    record_last_ten(body)
    # status_code = requests.post(app_config['eventstore2']['url'], json=body).status_code
    status_code = 201

    logger.info("Returned event returns request with a unique id of" + str(body["title"]))
    logger.info("Returned event returns response (Id:" + str(body["title"]) + ") with status " + str(status_code))

    client = KafkaClient(hosts="%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"]))
    topic = client.topics[str.encode(app_config["events"]['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "record_completed_returns",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201



# def record_last_ten(body):
#     """Records the last ten posts into the json file"""
#     LIST = []
#     # Adds any existing content from the json file into the list
#     read_file = open(EVENT_FILE, "r")
#     read_lines = read_file.readlines()
#     for lines in read_lines:
#         LIST.append(lines.rstrip("\n"))
#     read_file.close()

#     # Makes sure the list does not exceed max number of events
#     while len(LIST) >= MAX_EVENTS:
#         LIST.pop(0)
#     LIST.append(body)

#     write_file = open(EVENT_FILE, "w")
#     for events in LIST:
#         write_file.write(str(events) + "\n")
#     write_file.close()
#     return NoContent, 201



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("pinepeach-Retail_Store_POS_Tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
