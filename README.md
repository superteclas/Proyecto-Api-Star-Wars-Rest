Claro, aquí tienes un README para el proyecto "Proyecto-Starwars-Alvaro-Backend":

---

# Proyecto Star Wars - Backend

![Captura de Pantalla 2024-06-17 a las 10 10 56](https://github.com/superteclas/Proyecto-Starwars-Alvaro-Backend/assets/147168257/b53e7e49-26b0-43b4-90dd-1ca940da29d0)

![Captura de Pantalla 2024-06-17 a las 10 10 21](https://github.com/superteclas/Proyecto-Starwars-Alvaro-Backend/assets/147168257/216c9a8c-f07b-4c67-8de9-f0c0662eeab5)

![Captura de Pantalla 2024-06-17 a las 10 10 14](https://github.com/superteclas/Proyecto-Starwars-Alvaro-Backend/assets/147168257/4daf69b7-bdcc-41e7-843c-0191198c4d92)


Este proyecto es la parte backend de una aplicación basada en la saga de Star Wars. Fue desarrollado como parte del Bootcamp de Full Stack Developer en 4Geeks Academy.

## Descripción

La aplicación proporciona una API RESTful que permite gestionar datos relacionados con personajes, planetas, y vehículos de Star Wars. Utiliza Python y Flask para el desarrollo del backend y SQLAlchemy para la gestión de la base de datos.

## Tecnologías Utilizadas

- **Lenguaje**: Python
- **Framework**: Flask
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Herramientas**: Docker, Git

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/superteclas/Proyecto-Starwars-Alvaro-Backend.git
   cd Proyecto-Starwars-Alvaro-Backend
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en el directorio raíz del proyecto y agrega las siguientes variables:
   ```env
   FLASK_APP=src/app.py
   FLASK_DEBUG=True
   DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/starwars
   ```

5. Realiza las migraciones de la base de datos:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Ejecuta la aplicación:
   ```bash
   flask run
   ```

## Endpoints

- **/characters**: Devuelve una lista de personajes.
- **/planets**: Devuelve una lista de planetas.
- **/vehicles**: Devuelve una lista de vehículos.
- **/characters/<id>**: Devuelve información de un personaje específico.
- **/planets/<id>**: Devuelve información de un planeta específico.
- **/vehicles/<id>**: Devuelve información de un vehículo específico.

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:
1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz un commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Sube los cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre una solicitud de extracción.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo LICENSE.

## Contacto

Desarrollado por [Álvaro](https://github.com/superteclas). Si tienes alguna pregunta o sugerencia, no dudes en contactarnos.



### Contributors

This template was built as part of the 4Geeks Academy [Coding Bootcamp](https://4geeksacademy.com/us/coding-bootcamp) by [Alejandro Sanchez](https://twitter.com/alesanchezr) and many other contributors. Find out more about our [Full Stack Developer Course](https://4geeksacademy.com/us/coding-bootcamps/part-time-full-stack-developer), and [Data Science Bootcamp](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning).

You can find other templates and resources like this at the [school github page](https://github.com/4geeksacademy/).
