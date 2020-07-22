from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            'id': self.id,
            'login': self.login
        }

    @classmethod
    def find(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        return user or None

    @classmethod
    def find_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        return user or None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()
