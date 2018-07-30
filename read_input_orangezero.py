#!/usr/bin/env python3

from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from os import path
import OPi.GPIO as GPIO # to install "pip3 install --upgrade OPi.GPIO"
import sys
import os
import time
import yaml
import logging
import subprocess
GPIO.setmode(GPIO.BOARD)

# Change working dir to the same dir as this script
os.chdir(sys.path[0])

class DataCollector:
    def __init__(self, influx_client, inputspins_yaml):
        self.influx_client = influx_client
        self.inputspins_yaml = inputspins_yaml
        self.max_iterations = None  # run indefinitely by default
        self.inputspins = None
        gpioinputs = self.get_inputs()
        for gpio in gpioinputs:
            GPIO.setup(gpioinputs[gpio], GPIO.IN)

    def get_inputs(self):
        assert path.exists(self.inputspins_yaml), 'Inputs not found: %s' % self.inputspins_yaml
        if path.getmtime(self.inputspins_yaml) != self.inputspins_map_last_change:
            try:
                log.info('Reloading inputs as file changed')
                self.inputspins = yaml.load(open(self.inputspins_yaml))
                self.inputspins_map_last_change = path.getmtime(self.inputspins_yaml)
            except Exception as e:
                log.warning('Failed to re-load inputs, going on with the old one.')
                log.warning(e)
        return self.inputspins

    def collect_and_store(self):
        inputs = self.get_inputs()
        t_utc = datetime.utcnow()
        t_str = t_utc.isoformat() + 'Z'

        save = False
        datas = dict()

		## inicio while :
        while:
            start_time = time.time()

            for parameter in inputs:
                statusInput = !GPIO.input(inputs[parameter])
                if statusInput != datas[parameter]
                    datas[parameter] = statusInput
                    save = True
			
            datas['ReadTime'] =  time.time() - start_time

            if save:
                save = False
                json_body = [
                    {
                        'measurement': 'LocalInputsLog',
                        'tags': {
                            'id': inputs_id,
                        },
                        'time': t_str,
                        'fields': datas[inputs_id]
                    }
                    for inputs_id in datas
                ]
                if len(json_body) > 0:
                    try:
                        self.influx_client.write_points(json_body)
                        log.info(t_str + ' Data written for %d inputs.' % len(json_body))
                    except Exception as e:
                        log.error('Data not written!')
                        log.error(e)
                        raise
                else:
                    log.warning(t_str, 'No data sent.')
			## delay 10 ms between read inputs
            time.sleep(0.01)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--inputspins', default='inputspins.yml',
                        help='YAML file containing relation inputs, name, type etc. Default "inputspins.yml"')
    parser.add_argument('--log', default='CRITICAL',
                        help='Log levels, DEBUG, INFO, WARNING, ERROR or CRITICAL')
    parser.add_argument('--logfile', default='',
                        help='Specify log file, if not specified the log is streamed to console')
    args = parser.parse_args()
    loglevel = args.log.upper()
    logfile = args.logfile

    # Setup logging
    log = logging.getLogger('input-logger')
    log.setLevel(getattr(logging, loglevel))

    if logfile:
        loghandle = logging.FileHandler(logfile, 'w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        loghandle.setFormatter(formatter)
    else:
        loghandle = logging.StreamHandler()

    log.addHandler(loghandle)

    log.info('Started app')

    # Create the InfluxDB object
    influx_config = yaml.load(open('influx_config.yml'))
    client = InfluxDBClient(influx_config['host'],
                            influx_config['port'],
                            influx_config['user'],
                            influx_config['password'],
                            influx_config['dbname'])

    collector = DataCollector(influx_client=client,
                              inputspins_yaml=args.inputspins)

    collector.collect_and_store()
