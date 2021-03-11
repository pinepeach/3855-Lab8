import connexion
from connexion import NoContent

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import yaml
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from base import Base
from sale import Sale
from returns import Return
import logging.config
import datetime

# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

# DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore']['db'])
# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

MAX_EVENTS = 10
EVENT_FILE = "events.json"


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "record_completed_sales":  # Change this to your event type
            record_completed_sales(payload)
        elif msg["type"] == "record_completed_returns":  # Change this to your event type
            record_completed_returns(payload)
    # Store the event2 (i.e., the payload) to the DB
    # Commit the new message as being read
    consumer.commit_offsets()

def record_completed_sales(body):
    """Creates a list of recent posted sales and stores them in a json file"""
    session = DB_SESSION()

    sale = Sale(body['title'],
                body['gcid']['store'],
                body['gcid']['till_number'],
                body['gcid']['transaction_number'],
                body['gcid']['date'],
                body['sale_product']['sku'],
                body['sale_product']['name'],
                body['sale_product']['price'])

    session.add(sale)
    session.commit()
    session.close()

    logger.debug("Received event new sales request with a unique id of " + str(body["title"]))

    return NoContent, 201


def record_completed_returns(body):
    """Creates a list of recent posted return and stores them in a json file"""
    session = DB_SESSION()

    returns = Return(body['title'],
                   body['gcid']['store'],
                   body['gcid']['till_number'],
                   body['gcid']['transaction_number'],
                   body['gcid']['date'],
                   body['return_product']['sku'],
                   body['return_product']['name'],
                   body['return_product']['reason'])

    session.add(returns)
    session.commit()
    session.close()

    logger.debug("Received event new returns request with a unique id of " + str(body["title"]))

    return NoContent, 201

def get_completed_sales(timestamp):
    session = DB_SESSION()
    readings = session.query(Sale).filter(Sale.date_created >= timestamp)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for completed sale changes after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


def get_completed_returns(timestamp):
    session = DB_SESSION()
    readings = session.query(Return).filter(Return.date_created >= timestamp)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for completed return changes after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("pinepeach-Retail_Store_POS_Tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

logger.info('connecting to db hostname=%s port=%s' % (app_config['datastore']['hostname'], app_config['datastore']['port']))

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
