from flask import Flask, request
from flask_restful import Api, Resource
from numpy import genfromtxt
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

DEFAULT_DATE = datetime.strptime("21 June, 2000", "%d %B, %Y")
DEFAULT_NUM_NODES = -1

app = Flask(__name__)
api = Api(app)

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', converters={1: lambda s: str(s)[1:]})
    data[0][0] = 1
    return data.tolist()

Base = declarative_base()

class BatchRecordModel(Base):
    __tablename__ = 'Batch_Records'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    date =  Column(DateTime)
    nodes = Column(Integer)

 #Create the database
 #Extra arguments in create_engine() allows client to send mutliple requests to the same API endpoint
engine = create_engine('sqlite:///csv_data.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.create_all(engine)

#Create the session
session = sessionmaker()
session.configure(bind=engine)
s = session()

try:
    file_name = "example_batch_records.csv" 
    data = Load_Data(file_name) 

    for i in data:
        dateTimeObject = DEFAULT_DATE
        numberOfNodes = DEFAULT_NUM_NODES

        #Checks if date value is not missing
        if i[1] != "''":
            dateTimeObject = datetime.strptime(i[1], "'%Y-%m-%dT%H:%M:%S+00:00'") 

        #Checks if number of nodes value is not missing (val is NaN if it is)
        if i[2] == i[2]:
            numberOfNodes = i[2]

        record = BatchRecordModel(**{
            'id': i[0],
            'date' : dateTimeObject,
            'nodes' : numberOfNodes
        })

        s.add(record) 

    s.commit()
except:
    s.rollback()


class BatchRecord(Resource):
    def get(self):
        submitted_after = None
        submitted_before = None
        min_nodes = None
        max_nodes = None

        url = request.url
        url = url.replace('%5B','[')
        url = url.replace('%5D',']')

        args = request.args
        
        for arg in args:
            if arg == 'filter[submitted_before]':
                submitted_before = datetime.strptime(args[arg], "'%Y-%m-%dT%H:%M:%S 00:00'")
            if arg == 'filter[submitted_after]':
                submitted_after = datetime.strptime(args[arg], "'%Y-%m-%dT%H:%M:%S 00:00'")
            if arg == 'filter[min_nodes]':
                min_nodes = int(args[arg])
            if arg == 'filter[max_nodes]':
                max_nodes = int(args[arg])

        res = s.query(BatchRecordModel.id, BatchRecordModel.date, BatchRecordModel.nodes)
        if min_nodes is not None:
            res = res.filter(BatchRecordModel.nodes >= min_nodes)
        if max_nodes is not None:
            res = res.filter(BatchRecordModel.nodes <= max_nodes)
        if submitted_after is not None:
            res = res.filter(BatchRecordModel.date >= submitted_after)
        if submitted_before is not None:
            res = res.filter(BatchRecordModel.date <= submitted_before)
    
        res = res.all()
        response = {"links": {
            "self": url},
            "data": []
        }

        id = 1
        for row in res:
            batch_record = {
                "type": "batch_jobs",
                "id": str(id),
                "attributes" : {
                    "batch_number": row.id,
                    "submitted_at": row.date.isoformat(),
                    "nodes_used": row.nodes 
                }
            }
            id+=1
            response['data'].append(batch_record)

        return response

api.add_resource(BatchRecord,'/batch_jobs', endpoint='batch_jobs')

if __name__ == "__main__":
    app.run(debug=True)
