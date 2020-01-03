from khanakazana.api.functions.Database import Database
from celery import Celery
from khanakazana.api.functions.Models import Restaurants, Items
from khanakazana.elastic_search import create_index
import csv, os
import pdfkit, time 

app = Celery('celery_tasks', broker='amqp://localhost//')


@app.task(name='app.import')
def upload_file(filename, rest_id=None):
    d = Database()
    database_rows = d.load_csv_to_mysql(file_name=filename, rest_id=rest_id)
    if database_rows.flag:
        create_index(database_rows.restaurants)
    return 'The files are uploaded and the indices are also updated'    


@app.task(name='app.export')
def export_file(rest_id):
    d = Database()
    d.session.commit()
    restaurant_information = d.session.query(Restaurants).get(rest_id)
    items_in_restaurant = d.session.query(Items).filter(Items.rest_id == rest_id).distinct(Items.name).order_by(Items.price).all()
    DIRECTORY_PATH = os.path.join(os.getcwd(), 'khanakazana', 'views', 'static', 'user_files')
    file_name = str(rest_id)+'_'+restaurant_information.name
    html_file_name = file_name + '.html'
    pdf_file_name = file_name + '.pdf'
    HTML_FILE_PATH = os.path.join(DIRECTORY_PATH, html_file_name)
    PDF_FILE_PATH = os.path.join(DIRECTORY_PATH, pdf_file_name)
    file_pointer = open(HTML_FILE_PATH, 'w')         
    html_string = f'''<html><head><link href='https://fonts.googleapis.com/css?family=Londrina+Shadow' rel='stylesheet' type='text/css'><link rel="stylesheet" href="menu.css"></head><body><h1>{restaurant_information.name}</h1><h2>Opens From: {restaurant_information.opening_time} to {restaurant_information.closing_time} </h2> <h2> Call us @ {restaurant_information.contact}</h2>    '''
    for item in items_in_restaurant:
        item_html_string = f'''<div class="first">
        <p>{item.name} <span class="price"> @ Rs.{item.price}</span>
        <br /><small>{item.category}</small></p></div> '''
        html_string = html_string + item_html_string
    file_pointer.write(html_string)
    file_pointer.close()
    pdfkit.from_file(HTML_FILE_PATH, PDF_FILE_PATH)
    return 'TASK COMPLETED'