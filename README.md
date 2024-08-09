## Nombre del equipo: EcoWeb Devs
## Nombre de la plataforma: Verde Nica


**VerdeNica** es un sistema web diseñado para promover la conciencia social sobre el cambio climático, permitiendo a los usuarios crear campañas, participar en foros, y realizar denuncias sobre violaciones ambientales. Este proyecto está construido con Python, Flask y utiliza MySQL como sistema de gestión de bases de datos.

## Características

- **Conciencia Climática**: Proporciona información sobre el cambio climático, sus causas, efectos y como vivir de manera sostenible.
- **Biodiversidad**: Proporciona contenido sobre la biodiversidad de Nicaragua y permite a los usuarios subir contenido o hacer nuevas publicaciones sobre la biovidersidad o el medio ambiente en Nicaragua.
- **Campañas**: Permite a los usuarios crear y participar en campañas ambientales.
- **Foros**: Espacios de discusión donde la comunidad puede compartir ideas y debatir sobre temas relacionados con el medio ambiente.
- **Denuncias**: Los usuarios pueden reportar violaciones ambientales para crear un registro y tomar acción.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- **Python 3.12**
- **MySQL**

## Instalación

Sigue los pasos a continuación para instalar y ejecutar el proyecto en tu máquina local.

### Paso 1: Clonar el Repositorio

Clona el repositorio desde GitHub en tu máquina local utilizando el siguiente comando:


`git clone https://github.com/elmerurbina/EcoWeb_Devs`

## Paso 2: Installar dependencias

Accede al directorio del proyecto y procede a instalar las dependencias necesarias especificadas en el archivo requirements.txt. Puedes hacerlo con el siguiente comando:

`pip install -r requirements.txt`

## Paso 3: Crear y activar un entorno virtual
Es recomendable crear un entorno virtual para aislar las dependencias del proyecto. Puedes crear y activar un entorno virtual utilizando los siguientes comandos:

### Crear entorno virtual
`python -m venv env`

### Activar el entorno virtual en Windows
`.\env\Scripts\activate`

## Paso 4: configurar la Base de Datos
1. Abre tu terminal de MySQL o tu gestor de base de datos favorito.

2. Copia y pega el contenido del archivo **schema.sql** en la terminal para crear la base de datos y las tablas necesarias.

Puedes hacerlo manual o utilizando el siguiente comando:

`mysql -u tu_usuario -p < schema.sql`

3. Asegúrate de actualizar las credenciales de la base de datos en el archivo `db.py` con tu propia contraseña.
```
 connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='tu contraseña',
            database='VerdeNica'
        ) 
```
## Paso 5: Ejecutar la aplicacion
Ejecuta el archivo `app.py` para iniciar el servidor de Flask.

## Paso 6: Accede a la aplicacion
Una vez que el servidor esté en funcionamiento, abre tu navegador web favorito y navega a la siguiente URL:
`http://127.0.0.1:5000/verdeNica`

¡Enhorabuena! Ahora tienes el sistema VerdeNica instalado y funcionando en tu máquina local. Puedes empezar a explorar todas las funcionalidades que ofrece.
