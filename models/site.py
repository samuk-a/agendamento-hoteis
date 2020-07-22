from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find(cls, url):
        site = cls.query.filter_by(url=url).first()
        return site or None

    @classmethod
    def find_id(cls, site_id):
        site = cls.query.filter_by(id=site_id).first()
        return site or None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        [hotel.delete() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()
