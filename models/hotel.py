from sql_alchemy_import import database

class HotelModel(database.Model):
    __tablename__ = 'hoteis'

    hotel_id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80))
    rating = database.Column(database.Float(precision=1))
    dailyvalue = database.Column(database.Float(precision=2))
    city = database.Column(database.String(40))

    def __init__(self, hotel_id, name, rating, dailyvalue, city):
        self.hotel_id = hotel_id
        self.name = name
        self.rating = rating
        self.dailyvalue = dailyvalue
        self.city = city
    
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'rating': self.rating,
            'dailyvalue': self.dailyvalue,
            'city': self.city
        }