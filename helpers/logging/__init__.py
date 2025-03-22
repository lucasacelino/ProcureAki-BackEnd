import logging

logging.basicConfig(
    filename="app.log", 
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S"
)


logger = logging.getLogger("flask_app")
