# app.py
from flask import request, g, session, make_response
from flask_restful import Resource

from config import app, db, api # This line will run the config.py file and initialize our app
from models._models import * 
from resources._resources import *

# All routes here!

# Dictionary where keys are the endpoints, and the values are the models.
endpoint_model_map = {}

def map_resource(resource, route, endpoint = None, model = None):
    print("Method called")
    if endpoint:
        api.add_resource(resource, route, endpoint=endpoint)
    else:
        api.add_resource(resource, route)
    if bool(model and endpoint):
        endpoint_model_map[endpoint] = model

@app.before_request
def get_record_by_id():
    if model := endpoint_model_map.get(request.endpoint):
        id = request.view_args.get('id') # Retrieve argument values from a CRUD method.
        if record := model.query.filter_by(id=id).first():
            g.record = record
        else:
            return make_response({'message': '404 Not Found'}, 404)


map_resource(Users, '/users')
map_resource(Users, '/users/<int:id>', 'user_by_id')
map_resource(Companies, '/companies')
map_resource(CompanyById, '/companies/<int:id>', 'company_by_id')
map_resource(Employees, '/employees')
map_resource(EmployeeById, '/employees/<int:id>', 'employee_by_id')
map_resource(Incidents, '/incidents')
map_resource(IncidentById, '/incidents/<int:id>', 'incident_by_id')
map_resource(NearMisses, '/near_misses')
map_resource(NearMissById, '/near_misses/<int:id>', 'near_miss_by_id')
print(endpoint_model_map)
print(api.endpoints)
if __name__ == '__main__':
    app.run(port=5000, debug=True)