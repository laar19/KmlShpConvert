# KmlShpConvert

## Ing. Rosaura Rojas <rrojas@abae.gob.ve>
## Luis Acevedo  <laar@protonmail.com>

## Aplicación para convertir archivos con extensión .kml (Keyhole Markup Language) a .shp (Shapefile), y vice versa

Créditos para https://github.com/ManishSahu53 y https://github.com/tomtl   
Las funciones para convertir los archivos fueron adaptadas de sus   
repositorios

## Información técnica:

Desarrollado en python 3.5   
PyQt5 como librería gráfica.   
Distribuído bajo la GNU General Public License (GPLv3).   

## Source:

- *__main.py__* ejecuta la aplicación
		
- *__window.ui__* interfaz gráfica

- *__functions/functions.py__* funciones auxiliares
		
- *__functions/kmz_converter.py__* convierte de kml a shapefile https://github.com/tomtl/kmz-converter
		
- *__functions/shp2kml.py__* convierte de shapefile a kml https://github.com/ManishSahu53/geoconvert

## Uso:
### Virtualenv
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio crear un nuevo entorno virtual: __virtualenv --python=python3.5 .__   
3.- Instalar las librerías necesarias: __pip install -r requeriments.txt__   
4.- Ejecutar la aplicación: __python main.py__   

### Anaconda
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio crear un nuevo entorno virtual: __conda env create -n nombre_entorno -f environment.yml__   
3.- Ejecutar la aplicación: __python main.py__   
