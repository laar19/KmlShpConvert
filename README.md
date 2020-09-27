# KmlShpConvert

## Aplicación para convertir archivos con extensión .kml (Keyhole Markup Language) a .shp (Shapefile), y vice versa

## Luis Acevedo  <laar@protonmail.com>
## Ing. Rosaura Rojas <rrojas@abae.gob.ve>

Créditos para https://github.com/ManishSahu53 y https://github.com/tomtl   
Las funciones para convertir los archivos fueron adaptadas de sus   
repositorios

## Información técnica:

Desarrollado en python 3.5   
PyQt5 como librería gráfica.   
Distribuído bajo la GNU General Public License (GPLv3).   

## Source:

- *__main.py__* ejecuta la aplicación
		
- *__ui/window.ui__* interfaz gráfica

- *__functions/functions.py__* funciones auxiliares
		
- *__functions/kmz_converter.py__* contiene las funciones para convertir de kml a shapefile https://github.com/tomtl/kmz-converter

- *__functions/geoconvert.py__* contiene las funciones para convertir de shapefile a kml https://github.com/ManishSahu53/geoconvert
		
- *__functions/shp2kml.py__* convierte de shapefile a kml https://github.com/ManishSahu53/geoconvert

## Uso:
### Anaconda (recomendado)
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio crear un nuevo entorno virtual: __conda env create -n nombre_entorno -f environment.yml__   
3.- Ejecutar la aplicación: __python main.py__   

### Virtualenv
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio crear un nuevo entorno virtual: __virtualenv --python=python3.5 .__   
3.- Instalar las librerías necesarias: __pip install -r requeriments.txt__   
4.- Ejecutar la aplicación: __python main.py__   
