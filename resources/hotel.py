from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params, query_with_city, query_without_city
from models.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3 

#path -> /hoteis?city=Rio de Janeiro&rating_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('rating_min', type=float)
path_params.add_argument('rating_max', type=float)
path_params.add_argument('dailyvalue_min', type=float)
path_params.add_argument('dailyvalue_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        data = path_params.parse_args()
        data_valid = {key: data[key] for key in data if data[key] is not None }
        parameters = normalize_path_params(**data_valid)
        
        if not parameters.get('city'):
            query_tuple = tuple([parameters[key] for key in parameters])
            result = cursor.execute(query_without_city, query_tuple)
        else:
            query_tuple = tuple([parameters[key] for key in parameters])
            result = cursor.execute(query_with_city, query_tuple)
        hoteis = []
        for linha in result:
            hoteis.append(
                {
                    'hotel_id': linha[0],
                    'name': linha[1],
                    'rating': linha[2],
                    'dailyvalue': linha[3],
                    'city': linha[4],
                    'site_id': linha[5]
                }
            )
        return { 'hoteis': hoteis }

class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type=str, required=True, help="The field name cannot be left  empty")
    arguments.add_argument('rating', type=float, required=True, help="The field rating cannot be left  empty")
    arguments.add_argument('dailyvalue')
    arguments.add_argument('city')
    arguments.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site")
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 # not found
    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists" .format(hotel_id)}, 400
        
        dados = Hotel.arguments.parse_args()
        object_hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': "The hotel must be associated to a valid site id"}, 400
        try:
            object_hotel.save_hotel()
        except:
            return {'message': 'Internal Server Error ocurred trying to save hotel'}, 500
        return object_hotel.json(), 200

    @jwt_required
    def put(self, hotel_id):

        dados = Hotel.arguments.parse_args()

        hotel_by_find = HotelModel.find_hotel(hotel_id)
        if hotel_by_find:
            hotel_by_find.update_hotel(**dados)
            hotel_by_find.save_hotel()
            return hotel_by_find.json(), 200 # OK
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Internal Server Error ocurred trying to save hotel'}, 500
        return hotel.json(), 201 # created
    
    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Internal Server Error ocurred trying to delete hotel'}, 500
            return {'message': 'Hotel deleted!'}
        return {'message': 'Hotel not found'}
    