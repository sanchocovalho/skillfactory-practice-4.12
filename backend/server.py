import os
import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import todos_db as dbase

session = dbase.create_session()

app = bottle.Bottle()

@enable_cors
@app.route('/', method=['GET', 'POST'])
def get_or_add_task():
    try:
        if bottle.request.method == 'GET':
            tasks = [dbase.task_to_dict(task) for task in dbase.get_all_tasks(session)]
            return {'tasks': tasks,
                    'total': len(tasks),
                    'uncompleted': dbase.get_uncompleted_tasks(session)}
        elif bottle.request.method == "POST":
            description = bottle.request.json['description']
            if len(description) > 0:
                uid = 1
                while 1:
                    task = dbase.get_task_by_id(session, uid)
                    if not task:
                        break
                    uid += 1
                dbase.add_task(session, uid, description)
            return 'The task is added successfully'
    except IndexError:
        return bottle.HTTPError(500, 'Internal server error')

@enable_cors
@app.route('/<uid:int>', method=['GET', 'PUT', 'DELETE'])
def modify_or_delete_task(uid):
    try:
        if bottle.request.method == 'GET':
            task = dbase.get_task_by_id(session, uid)
            return dbase.task_to_dict(task[0])
        elif bottle.request.method == 'DELETE':
            dbase.delete_task(session, uid)
            return 'The task is deleted successfully'
        elif bottle.request.method == 'PUT':
            is_completed = bottle.request.json.get('is_completed', False)
            dbase.make_task_completed(session, uid, is_completed)
            return 'The task is completed successfully'
    except IndexError:
        return bottle.HTTPError(404, f'No task with uid {uid}')

app.install(CorsPlugin(origins=['http://localhost:5000']))

if __name__ == "__main__":
	bottle.run(app, host='localhost', port=5000)
