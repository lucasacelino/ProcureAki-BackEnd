from helpers.database import db
from helpers.application import app
from helpers.database import migrate
from helpers.cors import cors

from service.loja_service import loja_bp

app.config.from_object("config")

cors.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()
    print("Banco de dados e tabelas criados com sucesso!")

app.register_blueprint(loja_bp, url_prefix="/lojas")

if __name__ == "__main__":
    app.run(debug=True)
