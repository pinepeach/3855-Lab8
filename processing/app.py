import connexion
from connexion import NoContent

import os
import yaml
import logging.config
import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def populate_stats():
    logger.info("start periodic processing")
    file = "./" + app_config["datastore"]["filename"]
    if os.path.exists(file):
        json_data = {
            "title": 0,
            "gcid": 0,
            "sale_product": 0,
            "return_product": 0,
            "timestamp": "2020-01-01T00:00:00Z"
        }


    else:
        data_file = open(file)
        file_data = data_file.read()
        json_data = json.loads(file_data)
        data_file.close()

    current_time = str(datetime.datetime.now())
    new_time = json_data["timestamp"]

    sales_query = requests.get(app_config["eventstore1"]["url"]+"?timestamp="+new_time)
    if sales_query.status_code == 200:
        logger.info("Completed sale events received: " + str(len(sales_query.json())))
    else:
        logger.error("Sorry there was an error. Response code: " + str(sales_query.status_code))
    returns_query = requests.get(app_config["eventstore2"]["url"]+"?timestamp="+new_time)
    if returns_query.status_code == 200:
        logger.info("Completed return events received: " + str(len(returns_query.json())))
    else:
        logger.error("Sorry there was an error. Response code: " + str(returns_query.status_code))

    json_data["title"] = json_data["title"] + len(sales_query.json()) + len(returns_query.json())
    json_data["gcid"] = json_data["gcid"] + len(sales_query.json()) + len(returns_query.json())
    json_data["sale_product"] = json_data["sale_product"] + len(sales_query.json())
    json_data["return_product"] = json_data["return_product"] + len(returns_query.json())
    json_data["timestamp"] = current_time

    with open(app_config["datastore"]["filename"], 'w') as f:
        f.write(json.dumps(json_data))
        f.close()

    logger.debug("Updated stats: " + json.dumps(json_data))
    logger.info("Periodic processing has ended")


def get_stats():
    logger.info("request has started")
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        string = "Statistics does not exist"
        return string, 404
    logger.debug(data)
    logger.info("request has completed")
    return data, 200


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("pinepeach-Retail_Store_POS_Tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
