from flask_restful import Resource, reqparse
from models.hotel import HotelModel
hoteis = [
    {
        'hotel_id': 1,
        'name': 'AlphaVille',
        'rating': '4.3',
        'dailyvalue': 'R$380',
        'city': 'Cuiabá'
    },
    {
        'hotel_id': 2,
        'name': 'Budega do Zé',
        'rating': '1.2',
        'dailyvalue': 'R$25',
        'city': 'Varzea Grande'
    },
    {
        'hotel_id': 3,
        'name': 'Hostel Hallidad',
        'rating': '3.5',
        'dailyvalue': 'R$190',
        'city': 'Quebab'
    },
    {
        'hotel_id': 4,
        'name': 'Hotel from a Great Company',
        'rating': '5',
        'dailyvalue': 'R$800',
        'city': 'California'
    }
]

class Hoteis(Resource):
    def get(self):
        return { 'hoteis': hoteis }

class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name')
    arguments.add_argument('rating')
    arguments.add_argument('dailyvalue')
    arguments.add_argument('city')
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found'}, 404 # not found

    def post(self, hotel_id):
        
        dados = Hotel.arguments.parse_args()
        object_hotel = HotelModel(hotel_id, **dados)
        new_hotel = object_hotel.json()

        hoteis.append(new_hotel)
        return new_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.arguments.parse_args()
        object_hotel = HotelModel(hotel_id, **dados)
        new_hotel = object_hotel.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200 # OK
        hoteis.append(new_hotel)    
        return new_hotel, 201 # created

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id ]
        return {'message': 'Hotel deleted!'}