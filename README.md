# KmlShpConvert

## Aplicación para convertir archivos con extensión .kml (Keyhole Markup Language) a .shp (Shapefile), y vice versa

## Luis Acevedo  <laar@protonmail.com>
## Ing. Rosaura Rojas <rrojas@abae.gob.ve>

## Información técnica:

Desarrollado en python 3.7.x   
PyQt5 como librería gráfica.   
Distribuído bajo la GNU General Public License (GPLv3).   

## Source:

- *__main.py__* ejecuta la aplicación
		
- *__ui/window.ui__* interfaz gráfica

- *__functions/functions.py__* funciones auxiliares
		
## Uso:
### Anaconda (recomendado)
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio crear un nuevo entorno virtual: __conda env create -n nombre_entorno -f environment.yml__   
3.- Ejecutar la aplicación: __python main.py__   

### Virtualenv
1.- Clonar o descargar este repositorio   
2.- Dentro de la carpeta del repositorio crear un nuevo entorno virtual: __virtualenv --python=python3.7 .__   
3.- Instalar las librerías necesarias: __pip install -r requeriments.txt__   
4.- Ejecutar la aplicación: __python main.py__   
