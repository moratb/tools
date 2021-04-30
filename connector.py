from gi_creds import creds
import requests
from requests.auth import HTTPBasicAuth
import tempfile
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
import time as t
import re

import psycopg2
import time
import json
import pymysql



#main_connector
conn_params = {
    'dbtest':  {"host": '',
            "port": ,
            "user":  '',
            "password": '',
            "database": ''},
    
    'dbtest2': {"host": '', 
            "port": ,
            "user": '',
            "password": '',
            "database": ''},
    
    'dbtest3':{"host": "", 
            "port": ,
            "user": '',
            "password": '',
            "database": ''}
}


def sql_query(db,query):
    
    start = t.time()
    tmp = re.search(r'from[ ]{0,3}[a-z_]{0,20}\.[a-z_-]{0,20}', query, flags=re.IGNORECASE) 
    print('Downloading ' + (tmp.group() if tmp is not None else 'unknown source') + ' started at ' + dt.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S'))
    
    pg_db = {'dbtest'}
    msql_db= {'dbtest2'}
    ch_db= {'dbtest3'}
    
    if db in pg_db:
        con = psycopg2.connect(**conn_params[db])
        df = pd.read_sql(query, con=con)
        con.close()       
    
    elif db in msql_db:
        con = pymysql.connect(**conn_params[db])
        df = pd.read_sql(query, con=con)
        con.close()            
    
    elif db in ch_db:           
        query += ' FORMAT CSVWithNames'
        file_res = tempfile.TemporaryFile()
        r = requests.post('http://%s:8123/?' % conn_params[db]['host'], data = query, auth=HTTPBasicAuth(conn_params[db]['user'], 
                                                                                                               conn_params[db]['password']))    

        file_res.write(r.content)
        file_res.seek(0)
        df = pd.read_csv(file_res)        
   
    print('Downloading finished at ' + dt.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S') + \
                             ', elapsed time: ' + str(round(((t.time() - start) / 60), 2)) + ' min', 'Data shape:' + str(df.shape[0]) + '\n')    
   
    return df


class FullConnectorPostgres(object):
    def __init__(self, server):
        self._server = server
        
             
    def _get_connection(self):
        import psycopg2
        connection = conn_params
        conn = psycopg2.connect(**connection[self._server])
        return conn
    
    
    def drop_table(self, tablename):
        conn = self._get_connection()
        cursor = conn.cursor() 
        cursor.execute('drop table if exists public.%s' % tablename)
        conn.commit()
        conn.close()
        
        
    def exec_sql(self, sql):
        conn = self._get_connection()
        cursor = conn.cursor() 
        cursor.execute(sql)
        conn.commit()
        conn.close()    
    
    
    def upload_data(self, tablename, df, timestamp_field=None):
        def to_str(row):
            return ('(' + ','.join([str(val) if type(val) in (type(1), type(1.0)) 
                                             else "'%s'" % val for val in row.values]) + ')')
        
        type_map = {'object': 'varchar(255)',
                    'int64': 'bigint',
                    'float64': 'double precision'}

        cols = df.dtypes.reset_index()
        cols.columns = ['name', 'dtype']
        cols['pg_type'] = cols['dtype'].apply(lambda s: type_map[str(s)])
        columns = 'id bigserial, ' + ', '.join(['%s %s' % (name, pg_type) 
                                      for idx, (name, pg_type) in cols[['name', 'pg_type']].iterrows()])

        conn = self._get_connection()
        cursor = conn.cursor()

        sql = """create table if not exists public.%(TABLENAME)s (%(COLUMNS)s)
            """ % {'TABLENAME': tablename,
                   'COLUMNS': columns}
        cursor.execute(sql)

        if (not timestamp_field is None) and (timestamp_field in df.columns):
            min_ts = df[timestamp_field].min()
            max_ts = df[timestamp_field].max()
            
            sql = """
                delete
                from public.%(TABLENAME)s
                where
                    %(TS_NAME)s >= %(MIN_TS)s
                    and %(TS_NAME)s <= %(MAX_TS)s
            """ % {'TABLENAME': tablename,
                   'TS_NAME': timestamp_field,
                   'MIN_TS': min_ts,
                   'MAX_TS': max_ts}
            cursor.execute(sql)
            
        data_vals = ','.join(df.apply(to_str, axis=1))
        sql = """insert into public.%(TABLENAME)s (%(COLNAMES)s)
                 values %(VALUES)s""" % {'TABLENAME': tablename,
                                         'COLNAMES': ','.join(df.columns),
                                         'VALUES': data_vals}
        cursor.execute(sql)
            
        conn.commit()
        conn.close()  
        
    def test_table(self, tablename):
        pass

    
test = FullConnectorPostgres('dbtest')
