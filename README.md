# KmlShpConvert

## Ing. Rosaura Rojas <rrojas@abae.gob.ve>
## Luis Acevedo  <laar@protonmail.com>

### Aplicación para convertir archivos con extensión .kml (Keyhole Markup Language) a .shp (Shapefile), y vice versa

Créditos para https://github.com/ManishSahu53 y https://github.com/tomtl   
Las funciones para convertir los archivos fueron adaptadas de sus   
repositorios

### Información técnica:

Desarrollado en python 3.7.3   
PyQt5 como librería gráfica.   
Distribuído bajo la GNU General Public License (GPLv3).   

### Contenido:

- *__README.md__* este archivo

- *__main.py__* ejecuta la aplicación
		
- *__window.ui__* interfaz gráfica

- *__requeriments.txt__* librerías a instalar

- *__LICENSE__* licencia GPLv3
		
- *__functions/functions.py__* funciones auxiliares
		
- *__functions/kmz_converter.py__* convierte de kml a shapefile https://github.com/tomtl/kmz-converter
		
- *__functions/shp2kml.py__* convierte de shapefile a kml https://github.com/ManishSahu53/geoconvert

### Uso:
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio iniciar un nuevo entorno virtual: __virtualenv --python=python3 .__   
3.- Instalar las librerías necesarias: __pip3 install -r requeriments.txt__   
4.- Ejecutar la aplicación: __python main.py__   
