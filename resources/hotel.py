from flask_restful import Resource, reqparse
from models.hotel import HotelModel
hoteis = [
    {
    'id': 'alpha',
    'nome': 'Alpha Hotel',
    'estrelas': 4.3,
    'diaria': 420.34,
    'cidade': 'Rio de Janeiro'
    },
    {
    'id': 'bravo',
    'nome': 'Bravo Hotel',
    'estrelas': 4.4,
    'diaria': 380.90,
    'cidade': 'São Paulo'
    },
    {
    'id': 'charlie',
    'nome': 'Charlie Hotel',
    'estrelas': 4.2,
    'diaria': 180.99,
    'cidade': 'Fortaleza'
    },
    {
    'id': 'delta',
    'nome': 'Delta Hotel',
    'estrelas': 3.4,
    'diaria': 120,
    'cidade': 'Rio de Janeiro'
    },
    {
    'id': 'echo',
    'nome': 'Echo Hotel',
    'estrelas': 4.8,
    'diaria': 520.25,
    'cidade': 'Uberlândia'
    },
    {
    'id': 'fox',
    'nome': 'Foxtrot Hotel',
    'estrelas': 4.1,
    'diaria': 485.62,
    'cidade': 'Santos'
    }
]
class Hoteis(Resource):
    def get(self):
        return {'hoteis':hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    @staticmethod
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados).json()
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados).json()
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel_id != hotel['id']]
        return {'message': 'Hotel deleted'}
