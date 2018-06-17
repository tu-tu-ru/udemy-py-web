# To run the application
from src.app import app

app.run(DEBUG=app.config['DEBUG'], port=4990)