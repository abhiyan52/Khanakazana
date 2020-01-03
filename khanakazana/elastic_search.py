from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search
# from khanakazana.api.functions.Database import Database
# from khanakazana.api.functions.Models import Restaurants


elastic_search = Elasticsearch()
index_name = 'restaurants'

#add enum

def create_index(restaurants):
    # database_connection = Database()
    elastic_search.indices.delete(index_name, ignore=[404, 400])
    elastic_search.indices.create(index_name)
    # restaurants = database_connection.session.query(Restaurants).all()
    restaurant_jsons = []
    for restaurant in restaurants:
        restaurant_json = {
            '_index': index_name,
            '_type': 'restaurant',
            '_id': restaurant.id,
            'name': restaurant.name,
            'minimum_order': restaurant.minimum_order,
            'res_type': restaurant.res_type
        }
        restaurant_jsons.append(restaurant_json)
    res = helpers.bulk(elastic_search, restaurant_jsons, chunk_size=1000, request_timeout=200)
    return 'Sucessfully Created The Index'


def search_elastic(query_string):
    query_string = list(query_string)
    lower_case_string = map(lambda x: x.lower(), query_string)
    patterns = []
    string_patterns = ''.join([''.join(query_string[:3]), '.*'])
    patterns.extend([str(query_string[0])+'.*', ''.join(query_string), ''.join(lower_case_string), ''.join(query_string[:4]), ''.join(query_string[-3:]), string_patterns])
    patterns = '|'.join(patterns)
    print(patterns)
    elastic_search.indices.refresh()
    # s = Search(using=elastic_search, index=index_name).query('regexp',name=)
    res = elastic_search.search(index_name, body={
        "query": {
            "regexp": {
                "name": patterns
            }
        }
    })
    # bento|bento|bent|nto
    time_taken = res['took']
    total_items_found = res['hits']['total']
    restaurants_found = res['hits']['hits']
    restaurants_array = []
    for restaurant in restaurants_found:
        rest_id = restaurant['_id']
        restaurant_info = restaurant['_source']
        restaurant_info['id'] = rest_id
        restaurants_array.append(restaurant_info)

    return {'status':True, 'time_taken':time_taken, 'total_found':total_items_found, 'restaurants': restaurants_array}

# def add_to_index(restaurant):
#     res = elastic_search.create(index='restaurants', type='restaurant', id=restaurant.id)
#     return 'Created Successfuly'
    



