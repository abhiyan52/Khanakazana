from flask import Blueprint, session, request, g, jsonify
from .functions.khanacore import KhanaAPI
from .functions.Response import Response
from flask_login import login_required
from .functions.Users import UserAPI


user = UserAPI()
khana = KhanaAPI()
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/restaurants', methods=['GET', 'POST'])
def restaurant_crud():
    if request.method == 'GET':
        return Response(khana.show_restaurants()).json_response()
    elif request.method == 'POST' and request.form.operation == 'post':
        khana.super_add_restaurants(request.form, 1)
        return {'status': 200, 'message': 'Restaurant added sucessfully'}
    elif request.method == 'POST' and request.form.operation == 'delete':
        rest_id = request.form['id']
        khana.super_delete_restaurant(rest_id)
        return {'status': 200, 'message': 'Restaurant delete sucessfully'}
    elif request.method == 'POST' and request.form.operation == 'put':
        rest_id = request.form['id'] 
        khana.super_update_restaurant(request.form, rest_id)
        return {'status': 200, 'message': 'Restaurant updates sucessfully'}
    else:
        return {'status': 405, 'message': 'Operation Not Supported'}


@api_blueprint.route('/restaurant/<int:rest_id>', methods=['GET'])
def get_restaurant(rest_id):
    return Response(khana.display_restaurant(rest_id)).json_response()


@api_blueprint.route('/items/<int:rest_id>')
def restaurant_items(rest_id):
    return Response(khana.show_items(rest_id)).json_response()


@api_blueprint.route('/items', methods=['POST'])
def items():
    item_id = request.form['id'] 
    if request.form.get('operation') == 'delete':
        if khana.owner_delete_item(item_id):
            return jsonify({'code': 200, 'status': 'Deletion done'})
        return jsonify({'code': 404, 'status': 'Not Found'})
    elif request.form.get('operation') == 'post':
        khana.owner_add_items(request.form)
        return jsonify({'code': 200, 'status': 'Sucessfullt Created'}) 
    elif request.form.get('operation') == 'put':
        flag = khana.super_update_restaurant(request.form, item_id)
        if flag:
            return jsonify({'code': 200, 'status': 'Update done'})
        else:
            return jsonify({'code': 404, 'status': 'Not Found'})
    else:
        return jsonify({'code': 405, 'status': 'Method Not Found'})


@api_blueprint.route('/categories/<int:rest_id>')
def rest_categories(rest_id):
    return Response(khana.show_categories(1, rest_id=rest_id)).json_response() 


@api_blueprint.route('/categories', methods=['GET'])
def categories():
    return Response(khana.show_categories()).json_response() 


@api_blueprint.route('/users', methods=['GET'])
def show_all_users(): 
    return Response(user.list_all_users()).json_response()


@api_blueprint.route('/owners', methods=['GET'])
def show_all_owners(): 
    return Response(user.list_all_owners).json_response()






