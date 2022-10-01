from dotenv import load_dotenv
from Core import app


load_dotenv()
app.config.from_prefixed_env()
