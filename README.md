# Obtener datos climáticos de la API de OpenWeatherMap y almacenarlos en archivos CSV o Postgres

Este proyecto tiene como objetivo obtener datos climáticos de la API de OpenWeatherMap, en formato JSON, y luego convertirlos a archivos CSV organizando los archivos en rutas siguiendo una estructura específica (si se trata el clima actual). Añade a una base de datos PostgreSQL remota si se trata del pronostico.

Dada una lista de parametros, el código reconoce que si el parametro es el nombre de una ciudad consigue su longitud y latitud para ser procesados de forma uniforme con otros parametros pasados como longitud y latitud. Es decir, se puede pasar de forma arbitraria nombre de ciudades, latitudes y longitudes.

Los parámetros pueden ser suministrados en el módulo params.


## API de datos abiertos del clima

La API de OpenWeatherMap proporciona datos climáticos históricos o en tiempo real, como temperaturas, precipitaciones, vientos, etc.

## Comentarios en el código

El código proporcionado incluye comentarios (#) para facilitar la comprensión del mismo. Los comentarios explican la funcionalidad de cada parte del código y ayudan a entender qué hace cada sección.

## Usar el programa:


# 1: Instalar dependencias

pip install -r requirements.txt

# 2: Configurar variables de entorno

Por cuestiones de seguridad las claves son guardadas en variables de entorno. 

WHEATER_APP -> API Key
DB_PASS -> Contraseña de la base de datos

*En Windows (PowerShell):*

$env:WEATHER_APP = "654e73254585d3f8ea2ce898965c489e"

$env:DB_PASS = "XlxhNhoVFJKHp4cVTLef"

# 3: Obtener pronóstico a 5 días (opcional)

Para obtener el pronóstico del clima para los próximos 5 días, asegúrate de proporcionar el parámetro five_days=True al llamar al método make_requests() en el archivo config.py.

make_requests(five_days=True)

# 4: Ejecutar el proceso ETL
Antes de ejecutar el proceso ETL, asegúrate de configurar las variables de entorno como se indicó en el paso 2. Luego, ejecuta el archivo config.py para iniciar el proceso de extracción, transformación y carga de datos climáticos. Este proceso recuperará los datos de la API de OpenWeatherMap, los procesará y los almacenará en archivos CSV organizados en rutas específicas (para el clima actual) o los añadirá a una base de datos PostgreSQL remota (para el pronóstico).







