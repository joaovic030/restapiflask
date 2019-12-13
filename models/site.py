from sql_alchemy_import import database

class SiteModel(database.Model):
    __tablename__ = 'sites'

    site_id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.String(80))
    hoteis = database.relationship('HotelModel')

    def __init__(self, url):
        self.url = url
    
    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }
    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first() # SELECT * FROM hoteis WHERE url = $url
        if site:
            return site
        return None
    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    def save_site(self):
        database.session.add(self)
        database.session.commit()
    # def update_hotel(self, name, rating, dailyvalue, city):
    #     self.name = name
    #     self.rating = rating
    #     self.dailyvalue = dailyvalue
    #     self.city = city

    def delete_site(self):
        # deletando todos os hoteis associados ao site deletado
        [hotel.delete_hotel() for hotel in self.hoteis]
        database.session.delete(self)
        database.session.commit()