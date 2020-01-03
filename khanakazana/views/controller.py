'''
 Name: controllers.py
 Description: Main controller for all the views
 author: abhiyan timilsina              '''

from flask import Blueprint, jsonify, session, request, render_template, flash, g, redirect
from .forms import Users, Restaurants, Items, BookRestaurant
import requests
import random
from khanakazana.api.functions.khanacore import KhanaAPI
from khanakazana.auth.routes import validate_unique_username
from flask_login import current_user, login_required
from flask import current_app as app
from os import urandom
from khanakazana.celery_tasks import upload_file, export_file
from khanakazana.elastic_search import search_elastic

views_blueprint = Blueprint('view', __name__, static_folder='static', static_url_path='/static/view', template_folder='templates')
khana = KhanaAPI()


@views_blueprint.before_app_request
def checklogin():
    if g.user_type == 0 and 'cart_count' not in session:
        session['cart_count'] = 0
        session['cart_items'] = ''
        g.cart_count = session['cart_count']
    elif 'cart_count' in session:
        g.cart_count = session['cart_count']


# Route for the Home Page
@views_blueprint.route('/')
def index():
    categories_images = ['image_chinese.jpg', 'image_bbq.jpg', 'image_drinks.jpeg', 'image_nepalese.jpg']
    random_number = [random.randint(0, len(categories_images)) for i in range(0,len(categories_images))]
    return render_template('index.html', user_type=g.user_type, user=g.user, cat_images=categories_images, random_number = random_number)

''' -----------------------  USER INTERACTION ROUTES ----------------------------'''


@views_blueprint.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    operation_type = request.form.get('operation_id')
    item_id = request.form.get('item_id')
    cart_items_array = session['cart_items'].split(',')
    if int(operation_type) == 0:
        session['cart_count'] = int(session['cart_count']) + 1
        cart_items_array.append(str(item_id))
    else:
        session['cart_count'] = int(session['cart_count']) - 1
        cart_items_array.remove(str(item_id))
    session['cart_items'] = ','.join(cart_items_array)
    g.cart_count = session['cart_count']
    return jsonify({'count': g.cart_count})    


@views_blueprint.route('/checkout')
def checkout():
    items_added = session['cart_items']
    items_added = items_added.split(',')[1:]
    items = []
    cart_total = 0
    for item in items_added:
        item_obj = khana.get_item(item)
        cart_total = int(item_obj.price) + cart_total
        items.append(item_obj)
    return render_template('checkout.html', items=items, total = cart_total)


@views_blueprint.route('/book/<int:rest_id>', methods=['GET', 'POST'])
@login_required 
def book_restaurant(rest_id):
    form = BookRestaurant()
    title = 'Book a Table'
    action = request.url 
    if form.validate_on_submit():
        khana.owner_add_items(form_values)
        for record in form:
            record = ""
        flash({'type': 'ok', 'message': 'Your Response has been recorded'})
        return redirect('/')
    elif not form.validate_on_submit() and request.method == 'POST':
        flash({'type': 'fail', 'message': 'Forms are not filled correctly please review'})
    return render_template('forms.html', form=form, title=title, action=action)    


@views_blueprint.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    response = search_elastic(query)
    return render_template('search.html', result=response)


@views_blueprint.route('/signup', methods=['GET', 'POST'])
def sign_up():
    url_root = request.url_root
    form = Users()
    title = 'Add new user'
    action = '/signup'
    if request.method == 'POST' and validate_unique_username(request.form['username']) is True:
        if form.validate_on_submit():
            r = requests.post(url_root+'auth/register', request.form)
            for record in form:
                record.data = ""
            flash({'type': 'ok', 'message': 'Your Response has been recorded'})
        else:
            flash({'type': 'fail', 'message': 'Please choose a different username'})

    elif not form.validate_on_submit() and request.method == 'POST':
        flash({'type': 'fail', 'message': 'Forms are not filled correctly Please Review'})
    return render_template('forms.html', form=form, title=title, action= action)


@views_blueprint.route('/restaurant/<int:rest_id>')
def restaurant_detail(rest_id):
    restaurant = khana.display_restaurant(rest_id)
    items = khana.show_items(rest_id)
    return render_template('restaurant_detail.html', items=items, restaurant=restaurant)


''' ----------------------- END OF USER INTERACTION ROUTES ----------------------------'''


''' ----------------------- RESTAURANT OWNER  ROUTES ----------------------------'''


@views_blueprint.route('owner/export/<int:rest_id>')
@login_required
def export_menu(rest_id):
    export_file.delay(rest_id)
    flash({'type': 'ok', 'message': 'Menu is being generated...'})
    return redirect('/owner/restaurants')


@views_blueprint.route('/restaurants', methods=['GET'])
def show_restaurants():
    restaurants = khana.show_restaurants()
    return render_template('restaurant_list.html', restaurants=restaurants, title='Restaurants Available')


@views_blueprint.route('/items/<int:rest_id>', methods=['GET'])
def listItems(rest_id):
    items = khana.show_items(rest_id)
    return render_template('item_list.html', items=items)


@views_blueprint.route('/category/<category_name>')
def show_restaurant_with_category(category_name):
    restaurants = khana.display_restaurant_category(category_name)
    return render_template('restaurant_list.html', restaurants=[elements[0] for elements in restaurants], title='Restaurants For Category '+category_name)


@views_blueprint.route('/additem/<owner_username>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def add_item(owner_username, rest_id):
    if g.user_type != 1:
        return '403 You are forbidden to use this route as you are not the owner'
    form = Items()
    form.rest_id = rest_id
    title = 'Add new item'
    action = request.url 
    if form.validate_on_submit():
        form_values = {
            'name': request.form['name'],
            'description': request.form['name'],
            'price': request.form['price'],
            'category': request.form['category'],
            'rest_id': rest_id
        }
        khana.owner_add_items(form_values)
        for record in form:
            record = ""
        flash({'type': 'ok', 'message': 'Your Response has been recorded'})
        return redirect('/owner/restaurants')
    elif not form.validate_on_submit() and request.method == 'POST':
        flash({'type': 'fail', 'message': 'Forms are not filled correctly Please Review'})
    return render_template('forms.html', form=form, title=title, action= action)


@views_blueprint.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_items(item_id):
    if g.user_type != 1:
        return '403 You are forbidden to use this route as you are not the owner'
    item_to_update = khana.show_item(item_id)
    form = Items(name=item_to_update.name, description=item_to_update.description, price=item_to_update.price,category=item_to_update.category)
    if form.validate_on_submit():
        khana.owner_update_items(request.form, item_id)
        flash('The item has been updated')
        return redirect('/owner/restaurants')
    else:
        flash('The fields are invalid')
    return render_template('forms.html', form=form)    


@views_blueprint.route('/items/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_items(item_id):
    if g.user_type != 1:
        return '403 You are forbidden to use this route as you are not the owner'
    khana.owner_delete_item(item_id)
    return redirect('/owner/restaurants')


@views_blueprint.route('owner/upload/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def upload_items(rest_id):
    action = request.url
    rest_id = rest_id 
    if request.method == 'POST' and 'file' in request.files:
        filename = app.files.save(request.files['file'])
        upload_file.delay(filename, rest_id)
        flash({'type':'ok', 'message':'uploading process started'})
        return redirect('/owner/restaurants')
    return render_template('upload.html', action = action)


@views_blueprint.route('/owner/restaurants')
@login_required
def addItem():
    if g.user_type != 1:
        return '403 You are forbidden to use this route as you are not the owner'
    username = g.user
    restaurants = khana.owner_resturant(username)
    return render_template('tables/owner_table.html', restaurants = restaurants)    


''' ----------------------- END OF RESTAURANT OWNER  ROUTES ----------------------------'''


''' ----------------------- SITE ADMIN  ROUTES ----------------------------'''


@views_blueprint.route('/addrestaurant', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    if g.user_type != 2:
        return '403 You are forbidden to use this route as you are not the owner'
    form = Restaurants()
    title = 'Add new restaurant'
    action = '/addrestaurant'
    if form.validate_on_submit():
        khana.super_add_restaurants(request.form.to_dict(flat=True))
        for record in form:
            record.data = ""
            
        flash({'type': 'ok', 'message': 'Your Response has been recorded'})
        return redirect('/superadmin')
    elif not form.validate_on_submit() and request.method == 'POST':
        flash({'type': 'fail', 'message': 'Forms are not filled correctly Please Review'})
    return render_template('forms.html', form=form, title=title, action= action)


@views_blueprint.route('/superadmin')
@login_required
def super_admin():
    if g.user_type != 2:
        return '403 You are forbidden to use this route as you are not the owner'
    restaurants = khana.show_restaurants(type=1)
    return render_template('super_admin.html', restaurants=restaurants)


@views_blueprint.route('/superadmin/load')
@login_required
def super_admin_load():
    if g.user_type != 2:
        return redirect('You are forbidden to use this')
    khana.super_load()    
    flash({'type': 'ok', 'message': 'loading process started'})
    return redirect('/superadmin')


@views_blueprint.route('/super/owner/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def add_owner(rest_id):
    if g.user_type != 2:
        return redirect('You are forbidden to use this')
    users = khana.get_all_users()
    restaurant = khana.display_restaurant(rest_id)
    if request.method == 'POST':
        user_id = request.form.get('owner_id')
        khana.super_add_owner(rest_id, user_id)
        flash({'type': 'ok', 'message': 'Owner Added Successfully'})
        return redirect('/superadmin')
    return render_template('addowner.html', users=users, restaurant=restaurant)


''' ----------------------- END OF SITE ADMIN  ROUTES ----------------------------'''
