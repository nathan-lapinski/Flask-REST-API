#!flask/bin/python
#Author: Nathan Lapinski and Louis Boudhhou
#email: n4t311@gmail.com
#all unit tests were performed using the curl command line utility
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
 
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'planet':
        return 'python'
    return None
 
#HTTP Error Code handling
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify( { 'error': 'Resource already exists' } ), 409)
 
#Sample record data structures
user_records = [
    {
        "first_name": u"Joe",
        "last_name": u"Smith",
        'userid': u"jsmith", 
        'groups': ["admins","users"]
    }
]

group_records = [
    {
        "group_name" : u"test_group",
        "members" : ["sample1","sample2"]
    }
]
#For handling response reports
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task

#Returns all user records
@app.route('/users/', methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify( { 'records': map(make_public_task, user_records) } )

#1 GET /users/<userid> Returns the matching user record or 404 if none exist  //////
@app.route('/users/<string:user_id>', methods = ['GET'])
@auth.login_required
def get_record(user_id):
    record = filter(lambda t: t['userid'] == user_id, user_records)
    if len(record) == 0:
        abort(404)
    return jsonify( { 'record': make_public_task(record[0]) } )

#2 POST /users/<userid> Creates a new user record. The body of the request should be a valid user
#record. POSTs to an existing user are treated as errors and flagged with HTTP status code 409 (Conflict)
@app.route('/users/<string:user_id>', methods = ['POST'])
@auth.login_required
def create_record(user_id):
    records = filter(lambda t: t['userid'] == user_id, user_records )
    if len(records) > 0:
        abort(409)
    if not request.json or not 'userid' in request.json or not 'first_name' in request.json or not 'last_name' in request.json or not 'groups' in request.json:
        abort(400)
    record = {
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
        'userid': request.json['userid'],
        'groups': request.json['groups']
    }
    update_groups_on_new_user(record['groups'],user_id)
    user_records.append(record)
    return jsonify( { 'record': make_public_task(record) } ), 201

#3 DELETE /users/<userid> Deletes a user record. Returns 404 if the user record doesn't exist.
@app.route('/users/<string:user_id>', methods = ['DELETE'])
@auth.login_required
def delete_record(user_id):
    record= filter(lambda t: t['userid'] == user_id, user_records)
    if len(task) == 0:
        abort(404)
    user_records.remove(record[0])
    #update groups
    update_groups_on_delete(user_id)
    return jsonify( { 'result': True } )

#4 PUT
@app.route('/users/<string:user_id>', methods = ['PUT'])
@auth.login_required
def update_task(user_id):
    task = filter(lambda t: t['userid'] == user_id, user_records)
    if len(user_id) == 0 or len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'first_name' in request.json and type(request.json['first_name']) != unicode:
        abort(400)
    if 'last_name' in request.json and type(request.json['last_name']) is not unicode:
        abort(400)
    if 'userid' in request.json and type(request.json['userid']) is not unicode:
        abort(400)
    task[0]['first_name'] = request.json.get('first_name', task[0]['first_name'])
    task[0]['last_name'] = request.json.get('last_name', task[0]['last_name'])
    task[0]['userid'] = request.json.get('userid', task[0]['userid'])
    task[0]['groups'] = request.json.get('groups', task[0]['groups'])
    
    verify_groups_exists(task[0]['groups'])
    update_user_record(task[0]['userid'],user_id,task[0]['groups'])

    return jsonify( { 'record': make_public_task(task[0]) } )

#5 GET /groups/<group name> Returns a JSON list of userids containing the members of that group. Should
#return a 404 if the group doesn't exist or has no members.
@app.route('/groups/<string:group_name>', methods = ['GET'])
@auth.login_required
def get_group(group_name):
    records = filter(lambda t:t['group_name'] == group_name, group_records)
    if len(records) == 0:
        abort(404)
    users = records[0]['members']
    if len(users) == 0:
        abort(404)
    return jsonify( {'record': users})

#6 POST a new group
@app.route('/groups/<string:group_name>', methods = ['POST'])
@auth.login_required
def create_group(group_name):
    if not request.json or not 'group_name' in request.json:
        abort(400)
    records = filter(lambda t: t['group_name'] == group_name, group_records)
    if len(records) > 0:
        abort(409)
    group = {
        'group_name': request.json['group_name'],
        'members': []
    }
    group_records.append(group)
    return jsonify( { 'record': make_public_task(group) } ), 201

#7 PUT /groups/
@app.route('/groups/<string:group_name>', methods = ['PUT'])
@auth.login_required
def update_group(group_name):
    task = filter(lambda t: t['group_name'] == group_name, group_records)
    if len(group_name) == 0 or len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['members'] = request.json.get('members', task[0]['members'])
    #update user_records
    update_user_group_put(task[0]['members'],group_name)
    return jsonify( { 'record': make_public_task(task[0]) } )

#8 DELETE /groups/
@app.route('/groups/<string:group_name>', methods = ['DELETE'])
@auth.login_required
def delete_group(group_name):
    task = filter(lambda t: t['group_name'] == group_name, group_records)
    if len(task) == 0:
        abort(404)
    #update user records
    delete_group_from_users(task[0]['members'],group_name)
    group_records.remove(task[0])
    return jsonify( { 'result': True } )

#Helper functions. In a production implementation, we would use some sort of database 
#To handle the mapping between users and groups - which would be more effecient and scalable
def delete_group_from_users(group_list,group_name):
    i = 0
    while i < len(group_list):
        j = 0
        while j < len(user_records):
            if group_list[i] == user_records[j]['userid']:
                user_records[j]['groups'].remove(group_name)
            j = j + 1
        i = i + 1
def update_user_group_put(group_list,group_name):
    i = 0
    j = 0
    while i < len(group_list):
        while j < len(user_records):
            if group_list[i] == user_records[j]['userid']:
                user_records[j]['groups'].append(group_name)
            elif group_name in user_records[j]['groups'] and user_records[j]['userid'] not in group_list:
                user_records[j]['groups'].remove(group_name)
            j = j + 1
        i = i + 1
def verify_groups_exists(group_list):
    j=0
    while j < len(group_list):
        i = 0
        found = False
        while i < len(group_records):
            if group_list[j] == group_records[i]['group_name']:
                found = True
            i = i + 1
        if not found:
            abort(404)
        j = j + 1
def update_user_record(new_id,user_id,groups):
    i = 0
    while i < len(group_records):
        if user_id in group_records[i]['members']:
            group_records[i]['members'].remove(user_id)
        if group_records[i]['group_name'] in groups:
            group_records[i]['members'].append(new_id)
        i = i + 1
def update_groups_on_delete(user_id):
    i=0
    while i < len(group_records):
            if user_id in group_records[i]['members']:
                group_records[i]['members'].remove(user_id)
            i = i + 1
def update_groups_on_new_user(mygroups,user_id):
    i=0
    j=0
    while i < len(mygroups):
        found = False
        while j < len(group_records):
            if mygroups[i] == group_records[j]['group_name']:
                if user_id not in group_records[j]['members']:
                    group_records[j]['members'].append(user_id)
                found = True
            j = j + 1
        if not found:
            abort(404)
        i = i + 1

if __name__ == '__main__':
    app.run(debug = True)