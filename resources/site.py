from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found with the especified url'}
    def post(self, url):
        site = SiteModel.find_site(url)
        if site:
            return {"message": "The site '{}' already exists".format(site.url)}, 400 # bad request
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'Interal Server Error'}, 500
        return site.json()

    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted'} 
        return {'message': 'Site not found'} #