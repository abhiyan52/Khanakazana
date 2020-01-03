'''
Name: functions.py
Description: Contains all the functions for handling create,update,delete and read
author:abhiyan timilsina
'''
from .Database import Database
from .Models import Users, Restaurants, Items, Address, Recipes, Owner
from sqlalchemy.sql.functions import func
from sqlalchemy import and_


class KhanaAPI(Database):
    def __init__(self):
        super(KhanaAPI, self).__init__()
    
    def display_restaurant_category(self, category_name):
        restaurants = self.session.query(Restaurants, Items.category, func.count(Items.category)).filter(Items.rest_id == Restaurants.id, Items.category==str(category_name)).group_by(Items).distinct().all()
        return restaurants

    def super_add_owner(self, rest_id, user_id):
        owner = Owner(user_id=user_id, rest_id=rest_id)
        user = self.session.query(Users).get(user_id)
        user.user_type = 1
        self.session.add(owner)
        self.session.commit()
        return 'OK'

    def super_add_restaurants(self, restaurant_information, owner_id=0):
        name = restaurant_information['name']
        contact = restaurant_information['contact']
        minimum_order = restaurant_information['minimum_order']
        opening_time = restaurant_information['opening_time']
        closing_time = restaurant_information['closing_time']
        res_type = restaurant_information['res_type']
        restaurant = Restaurants(name, contact, res_type, opening_time, closing_time)
        self.session.add(restaurant)
        self.session.commit()

    def display_restaurant(self, rest_id):
        return self.session.query(Restaurants).get(rest_id)  

    def super_delete_restaurant(self, rest_id):
        restaurant = self.session.query(Restaurants).filter(Restaurants.id == rest_id).first()
        if restaurant is not None:
            self.session.delete(restaurant)
            self.session.commit()
    
    def super_update_restaurant(self, update_fields, rest_id):
        restaurant = self.session.query(Restaurants).filter(Restaurants.id == rest_id).first()
        if restaurant is not None:
            update_field = update_fields.to_dict(flat=True)
            for key, value in update_fields.items():
                if key != 'id':
                    setattr(restaurant, key, value)
            self.session.commit()
            return True
        return False

    def owner_add_items(self, item_information):
        name = item_information['name']
        category = item_information['category']
        description = item_information['description']
        price = item_information['price']
        rest_id = item_information['rest_id']
        item = Items(name, category, description, price, rest_id)
        self.session.add(item)
        self.session.commit()
    
    def owner_delete_item(self, item_id):
        item = self.session.query(Items).filter(Items.id == item_id).first()
        if item is not None:
            self.session.delete(item)
            self.session.commit()
            return True
        return False
    
    def owner_update_items(self, update_fields, item_id):
        item = self.session.query(Items).filter(Items.id == item_id).first()
        if item is not None:
            update_field = update_fields.to_dict(flat=True)
            for key, value in update_fields.items():
                setattr(item, key, value)
            self.session.commit()

    def show_restaurants(self, type=0):
        if type == 0:
            restaurants = self.session.query(Restaurants).all()
        elif type == 1:
            restaurants = self.session.query(Restaurants, Owner.user_id).outerjoin(Owner, Owner.rest_id==Restaurants.id).all()
        else:
            return 'Invalid Choice'
        return restaurants    

    def show_items(self, rest_id):
        restaurant = self.session.query(Restaurants).get(rest_id)
        if restaurant is not None:
            items = self.session.query(Items).filter(Items.rest_id == rest_id).all()
            return items

    def show_categories(self, get_type=0, rest_id=-1):
        if get_type == 0: 
            categories = self.session.query(Items.category).distinct(Items.category).all()
            return categories
        elif get_type == 1:
            restaurant = self.session.query(Restaurants).get(rest_id)
            if restaurant is not None:
                categories = self.session.query(Items.category).filter(and_(Restaurants.id == rest_id, Restaurants.id == Items.rest_id)).distinct(Items.category).all()       
                return categories

    def owner_resturant(self, username):
        self.session.commit()
        restaurants_data = self.session.query(Restaurants,Items).filter(and_(Owner.user_id==Users.id,Users.username==username,Restaurants.id==Owner.rest_id,Items.rest_id==Restaurants.id)).all()
        restaurants = {}
        restaurant = 0
        items = 1
        if len(restaurants_data):
            for restaurant_info in restaurants_data:
                if restaurant_info[restaurant].name not in restaurants:
                    restaurants[restaurant_info[restaurant].name] = {}
                    restaurants[restaurant_info[restaurant].name]['menu'] = []
                if 'rest_info' not in restaurants[restaurant_info[restaurant].name]:
                    restaurants[restaurant_info[restaurant].name]['rest_info'] = restaurant_info[restaurant]
                restaurants[restaurant_info[restaurant].name]['menu'].append(restaurant_info[items].__dict__)    
        else:
                restaurants_data = self.session.query(Restaurants).filter(and_(Owner.user_id==Users.id,Users.username==username,Restaurants.id==Owner.rest_id)).all()
                for restaurant_info in restaurants_data:
                    if restaurant_info.name not in restaurants:
                        restaurants[restaurant_info.name] = {}
                        restaurants[restaurant_info.name]['menu'] = []
                    if 'rest_info' not in restaurants[restaurant_info.name]:
                        restaurants[restaurant_info.name]['rest_info'] = restaurant_info
                 
        return restaurants
        
    def super_load(self):
        self.load_csv_to_mysql('items.csv')

    def show_item(self, item_id):
        item = self.session.query(Items).filter(Items.id == item_id).first()
        return item

    def get_all_users(self):
        return self.session.query(Users).all()

    def get_item(self, item_id):
        return self.session.query(Items).get(int(item_id))