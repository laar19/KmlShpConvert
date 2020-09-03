from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import shapefile
import sys

def create_reader(path):
    shp_fname = path
    dbf_fname = path
    
    dbf_fname = dbf_fname[:-4]
    dbf_fname += ".dbf"

    shp_file = open(shp_fname, 'rb')
    dbf_file = open(dbf_fname, 'rb')
    
    reader = shapefile.Reader(shp=shp_file, dbf=dbf_file)
    return reader

def create_kml_root():
    doc = KML.kml()
    return etree.SubElement(doc, 'Document')
    
def shp2kml(path):        
    reader = create_reader(path)
    doc = create_kml_root()    
    
    for shapeRec in reader.shapeRecords():
        name = shapeRec.record[1]

        points = shapeRec.shape.points
            
        doc.append(KML.Placemark(
            KML.name(name),
            KML.LineString(
                KML.coordinates(
                    ' '.join([str(item).strip('[]').replace(' ', '') for item in points])))))

    kml = etree.tostring(doc)
            
    return kml.decode("utf-8")

if __name__ == '__main__':
    sys.exit(main(sys.argv))