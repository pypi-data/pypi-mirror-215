import argparse
import psycopg2
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from psycopg2.extras import execute_batch
from miacag.configs.config import load_config
from miacag.utils.sql_utils import update_cols, getDataFromDatabase


parser = argparse.ArgumentParser(
    description='Define data inputs for transforming stenosis.')
parser.add_argument(
            '--query', type=str,
            help='query for retrieving data',
            required=True)
parser.add_argument(
            '--config', type=str,
            help='Path to the YAML config file',
            required=True)
parser.add_argument(
    '--database', type=str,
    help="database name")
parser.add_argument(
    '--username', type=str,
    help="username for database")
parser.add_argument(
    '--password', type=str,
    help="password for database")
parser.add_argument(
    '--host', type=str,
    help="host for database")
parser.add_argument(
    '--port', type=str,
    help="port for database")
parser.add_argument(
    '--table_name', type=str,
    help="table_name in database")


class transformMissingFloats():
    def __init__(self, sql_config, labels_config):
        self.sql_config = sql_config
        self.labels_config = labels_config
        self.df, self.connection = getDataFromDatabase(sql_config=sql_config)
        self.df = self.df[self.df['phase'] == 'test']
    def __call__(self):
        self.df = self.df[self.df[self.config["labels_names"]].notna()]
        self.df[config['labels_names']] = self.df[self.config["labels_names"]]
        self.df = self.df.replace({config['labels_names']: self.labels_config})

        update_cols(
                    self.df.to_dict('records'),
                    self.sql_config,
                    ['phase', config['labels_names']],)
if __name__ == '__main__':
    args = parser.parse_args()

    config = load_config(args.config)
    labels_config = config['labels_dict']
    sql_config = {'database':
                  args.database,
                  'username':
                  args.username,
                  'password':
                  args.password,
                  'host':
                  args.host,
                  'port':
                  args.port,
                  'table_name':
                  args.table_name,
                  'query':
                  args.query,
                  'TestSize':
                  args.TestSize
                  }

    mapper = labelsMap(sql_config, labels_config)
    mapper()
