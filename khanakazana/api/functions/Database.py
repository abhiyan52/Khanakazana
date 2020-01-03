from .Models import Restaurants, Items, Address, initialize_tables
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
from sqlalchemy.ext.declarative import declarative_base
import os


ROOT_CSV_DIR = os.path.join(os.getcwd(), 'restaurant_files')
database_engine_string = 'mysql+pymysql://khanakazana:test123@localhost/khanakazana'


class Database():
    def __init__(self):
        self.engine = create_engine(database_engine_string, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def load_csv_to_mysql(self, file_name='restaurant.csv', rest_id=None):
        absolute_file_path = os.path.join(os.path.join(os.getcwd(), 'static', 'files'), file_name)
        model_object = None
        restaurant_flag = False
        if file_name.find('restaurant') != -1:
            model_object = Restaurants
            restaurant_flag = True
        elif file_name.find('items') != -1:
            model_object = Items
        elif file_name.find('address') != -1:
            model_object = Address
        else:
            print("NOT FOUND")
            return
        try:
            with open(absolute_file_path) as file_contents:
                file_dict = csv.DictReader(file_contents)
                db_rows = []
                for row in file_dict:
                    values = [value for key, value in row.items()][1:]
                    if rest_id is not None:
                        values.append(rest_id)
                    db_rows.append(model_object(*values))
                self.session.add_all(db_rows)
                self.session.commit()
        except FileNotFoundError:
            print("FILE NOT FOUND")
        return {'flag':restaurant_flag, 'restaurants':db_rows}
