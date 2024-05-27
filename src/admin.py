import os
from flask_admin import Admin
from models import db, User, Characters, Planets,Vehicles, CharactersFavorites, PlanetsFavorites, VehiclesFavorites
from flask_admin.contrib.sqla import ModelView


#Esta función se encarga de configurar el admin de la aplicación
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Superteclas Admin', template_mode='bootstrap3')
#Esta clase se encarga de mostrar los datos de la tabla CharactersFavorites en el admin de la aplicación
    class MyFavoriteViewCharacters(ModelView):
        column_list = ( 'character_id', 'user_id',)
        form_columns = ('character_id', 'user_id',)
    class MyFavoriteViewPlanets(ModelView):
        column_list = ( 'planet_id', 'user_id',)
        form_columns = ('planet_id', 'user_id',)

    class MyFavoriteViewVehicles(ModelView):
        column_list = ( 'vehicle_id', 'user_id',)
        form_columns = ('vehicle_id', 'user_id',)

    # Esta función se encarga de agregar las tablas al admin de la aplicación
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(MyFavoriteViewCharacters(CharactersFavorites, db.session))  # Fix: Added closing parenthesis
    admin.add_view(MyFavoriteViewPlanets(PlanetsFavorites, db.session))
    admin.add_view(MyFavoriteViewVehicles(VehiclesFavorites, db.session))
    

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session)) 