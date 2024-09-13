# Configuraciones principales

import secrets

# Generar clave secreta
class Config:
    SECRET_KEY = secrets.token_hex(50)
