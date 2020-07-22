from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find(url)
        if site:
            return site.json()
        return {'message': 'Site not found.'}, 404

    def post(self, url):
        if SiteModel.find(url):
            return {"message": "The site '{}' already exists.".format(url)}, 400
        site = SiteModel(url)
        try:
            site.save()
        except:
            return {'message': 'An internal error occurred trying to create a new site.'}, 500
        return site.json()

    def delete(self, url):
        site = SiteModel.find(url)
        if site:
            site.delete()
            return {'message': 'Site deleted.'}
        return {'message': 'Site not found.'}, 404
