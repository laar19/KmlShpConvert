# KmlShpConvert

## Rosaura Rojas <rosaurarojas1989@gmail.com>
## Luis Acevedo  <laar@protonmail.com>

### Aplicación para convertir archivos con extensión .kml (Keyhole Markup Language) a .shp (Shapefile), y vice versa

Créditos para https://github.com/cthrall y https://github.com/tomtl   
Las funciones para convertir los archivos fueron adaptadas de sus   
repositorios

### Información técnica:

Desarrollado en python 3.7.3   
PyQt5 como librería gráfica.   
Distribuído bajo la GNU General Public License (GPLv3).   

### Contenido:

- README.md                   este archivo

- main.py                     ejecuta la aplicación
		
- window.ui                   interfaz gráfica

- requeriments.txt            librerías a instalar

- LICENSE                     licencia GPLv3
		
- functions/functions.py      funciones auxiliares
		
- functions/kmz_converter.py  convierte de kml a shapefile https://github.com/tomtl/kmz-converter
		
- functions/shp2kml.py        convierte de shapefile a kml https://github.com/cthrall/shp2kml

### Uso:
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio iniciar un nuevo entorno virtual: __virtualenv --python=python3.7 .__   
3.- Instalar las librerías necesarias: __pip3 install -r requeriments.txt__   
4.- Ejecutar la aplicación: __python main.py__
