from flask import jsonify

response_code = {
    '200': 'SUCCESS',
    '500': 'SERVER ERROR',
    '404': 'NOT FOUND',
    '403': 'FORBIDDEN'
}


class Response():
    def __init__(self, result):
        self.result = None
        if result is not None:
            self.code = 200
        else:
            self.code = 404           
        if isinstance(result, list) and len(result) > 1:
            self.result = []
            for result_obj in result:
                try:
                    dictret = dict(result_obj.__dict__)
                    dictret.pop('_sa_instance_state', None) 
                    self.result.append(dictret)
                except AttributeError:
                    self.result.append(result_obj[0])
        elif result is not None:
            dictret = dict(result.__dict__)
            dictret.pop('_sa_instance_state', None) 
            self.result = dictret         
    
    @property
    def status_message(self):
        return response_code[str    (self.code)]

    def json_response(self):
        return jsonify({'code': self.code, 'result': self.result, 'message': self.status_message})