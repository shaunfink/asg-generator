# A whole load of imports for stuff to work
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import json
import logging

# Setup some logging for more info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('INFO')

# Instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, expose_headers='Authorization')

# TODO: Plug this into some kind of session DB (SQLAlchemy?) instead of using a list/array
# Instantiate the ASG JSON Array
ASGS = []


# TODO: Classes for simplifying working with ASG Objects
# Some useful info:
# - https://www.makeuseof.com/tag/json-python-parsing-simple-guide/
# - https://linuxconfig.org/how-to-parse-data-from-json-into-python
class ASGObjects:
    def __init__(self, description, destination, log, ports, protocol):
        self.id = uuid.uuid4().hex
        self.description = description
        self.destination = destination
        self.log = log
        self.ports = ports
        self.protocol = protocol

    def __str__(self):
        return '{"id" = "{0}", \
                 "description" = "{1}", \
                 "destination" = "{2}", \
                 "log" = {3}, \
                 "ports" = {4}, \
                 "protocol" = "{5}"}' \
            .format(
            self.id,
            self.destination,
            self.destination,
            self.log,
            self.ports,
            self.protocol
        )


# TODO: json object creator to simplify it all
# Some useful info here:
# - https://www.makeuseof.com/tag/json-python-parsing-simple-guide/
# def obj_creator(obj):
#     return ASGObjects(
#         obj[obj.get('description')],
#         obj[obj.get('destination')],
#         obj[obj.get('log')],
#         obj[obj.get('ports')],
#         obj[obj.get('protocol')]
#     )
#     # return ASGObjects(
#     #     obj[post_data.get('description')],
#     #     obj[post_data.get('destination')],
#     #     obj[post_data.get('log')],
#     #     obj[post_data.get('ports')],
#     #     obj[post_data.get('protocol')]
#     # )


def remove_asg(asg_id):  # Something for Removing ASG's
    logger.info("Entering remove_asg function")
    logger.debug(asg_id)
    # Loop through asgs until we get the one with the ID we want, then remove it.
    for asg in ASGS:
        if asg['id'] == asg_id:
            logger.debug(asg)
            ASGS.remove(asg)
            return True
    return False


@app.route('/ping', methods=['GET'])
def ping_pong():  # sanity checking route
    response_object = {'ping': 'pong!'}
    logger.debug(response_object)
    return jsonify(response_object)


@app.route('/api/asgs', methods=['GET'])
def all_asgs():
    response_object = {'status': 'success', 'asgs': ASGS}
    logger.debug(response_object)
    return jsonify(response_object)


@app.route('/api/add', methods=['POST'])
def add_asg():  # Add an ASG
    # TODO: Make this use my JSON Object Creator
    response_object = {'status': 'success'}
    # Get the post data, and then append it to ASGS in the format we want
    post_data = request.get_json()
    ASGS.append({
        'id': uuid.uuid4().hex,
        'description': post_data.get('description'),
        'destination': post_data.get('destination'),
        'log': post_data.get('log'),
        'ports': post_data.get('ports'),
        'protocol': post_data.get('protocol')
    })
    response_object['message'] = 'ASG added!'
    logger.debug(response_object)
    return jsonify(response_object)


@app.route('/api/asgs/<asg_id>', methods=['PUT', 'DELETE', 'GET'])
def single_asg(asg_id):  # Adding/Editing single ASG's
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # Loop through asgs until we get the one with the ID we want, and then display it
        for asg in ASGS:
            if asg['id'] == asg_id:
                response_object = {'status': 'success', 'asg': asg}
    if request.method == 'PUT':
        # TODO: Make this use my JSON Object Creator
        post_data = request.get_json()
        logger.debug(post_data)
        logger.debug(asg_id)
        # Loop through asgs until we get the one with the ID we want, then update it with the post data.
        for asg in ASGS:
            if asg['id'] == asg_id:
                asg.update(post_data)
        response_object['message'] = 'ASG updated!'
    if request.method == 'DELETE':
        # call the remove asg function
        remove_asg(asg_id)
        response_object['message'] = 'ASG removed!'
    logger.debug(response_object)
    return jsonify(response_object)


@app.route('/api/upload', methods=['POST'])
def import_json():  # Import an existing ASG JSON file into our table
    # TODO: Make this use my JSON Object Creator
    response_object = {'status': 'success'}
    if request.method == 'POST':
        # Load the uploaded json, then loop through each object, and append to ASGS
        file = request.files['file']
        data = json.load(file)
        for obj in data:
            ASGS.append(obj)
        response_object['message'] = 'JSON added!'
    else:
        response_object['asgs'] = ASGS
    logger.debug(response_object)
    return jsonify(response_object)


@app.route('/api/generate-json', methods=['GET'])
def generate_json():  # Generate the ASG JSON files
    JSON_EXPORT=[]
    for asg in ASGS:
        JSON_EXPORT.append({
            'description': str(asg.get('description')),
            'destination': str(asg.get('destination')),
            'log': str(asg.get('log')),
            'ports': str(asg.get('ports')),
            'protocol': str(asg.get('protocol'))
        })
    logger.debug(JSON_EXPORT)
    return jsonify(JSON_EXPORT)


if __name__ == '__main__':  # Make the magic happen
    app.secret_key = os.urandom(24)
    app.run(debug=False)
