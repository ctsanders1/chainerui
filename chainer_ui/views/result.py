''' result.py '''


from flask import jsonify, request
from flask.views import MethodView


from chainer_ui import DB_SESSION
from chainer_ui.models.result import Result


class ResultAPI(MethodView):
    ''' ResultAPI '''

    def get(self, id=None, project_id=None):
        ''' get '''

        if id is None:
            results = DB_SESSION.query(Result).\
                filter_by(project_id=project_id).\
                filter_by(is_unregistered=False).\
                all()

            return jsonify({
                'results': [result.serialize for result in results]
            })

        else:
            result = DB_SESSION.query(Result).\
                filter_by(id=id).\
                filter_by(project_id=project_id).\
                filter_by(is_unregistered=False).\
                first()

            if result is None:
                return jsonify({
                    'result': None,
                    'message': 'No interface defined for URL.'
                }), 404

            return jsonify({
                'result': result.serialize
            })

    def put(self, id, project_id=None):
        """ put """
        result = DB_SESSION.query(Result).filter_by(id=id).first()
        if result is None:
            response = jsonify({
                'result': None, 'message': 'No interface defined for URL.'
            })
            return response, 404

        request_json = request.get_json()
        request_result = request_json.get('result')

        name = request_result.get('name', None)
        if name is not None:
            result.name = name

        is_unregistered = request_result.get('isUnregistered', None)
        if is_unregistered is not None:
            result.is_unregistered = is_unregistered

        DB_SESSION.add(result)
        DB_SESSION.commit()

        return jsonify({'result': result.serialize})

    def delete(self, id, project_id=None):
        """ delete """
        result = DB_SESSION.query(Result).filter_by(id=id).first()
        if result is None:
            response = jsonify({
                'result': None, 'message': 'No interface defined for URL.'
            })
            return response, 404

        DB_SESSION.delete(result)
        DB_SESSION.commit()

        return jsonify({'result': result.serialize})
