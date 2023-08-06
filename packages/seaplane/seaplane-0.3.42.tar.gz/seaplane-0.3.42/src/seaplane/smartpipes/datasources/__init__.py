from .request_data_source import RequestDataSource
from .sql_executor import SqlExecutor
from typing import Dict
import os
from ...configuration import config
from ...api.sql_api import GlobalSQL
from ...model.sql import CreatedDatabase

import json 

requests_table = """
CREATE TABLE requests (
     id VARCHAR PRIMARY KEY,     
     batch_count INTEGER
);
"""

results_table = """
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR UNIQUE,
    original_order INTEGER,
    output JSONB
);

ALTER SEQUENCE results_id_seq START WITH 10 INCREMENT BY 1;
CREATE INDEX idx_request_id ON results(request_id);
"""


def create_schema(database: CreatedDatabase) -> None:
    sql = SqlExecutor.from_created_database(database)

    sql.execute(requests_table)
    sql.execute(results_table)


def tenant_database() -> CreatedDatabase:

    if os.path.exists(".seaplane"):                                
        with open(".seaplane", "r") as file:
            database = json.load(file)                  
            return CreatedDatabase(**database)
    else: 
        sql = GlobalSQL(config)
        new_database = sql.create_database()        

        with open(".seaplane", "w") as file:
            db_info = json.dumps(new_database._asdict())            
            file.write(db_info)

        create_schema(new_database)
          
        return CreatedDatabase(**new_database)
    

__all__ = ["RequestDataSource", "SqlExecutor"]