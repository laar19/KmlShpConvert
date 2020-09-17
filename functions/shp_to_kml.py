import ogr
import os

# ----------------------------------------------------------------------------
# define the mainline method
# ----------------------------------------------------------------------------

def shp2kml_(shpfile, number):
    shpFile = shpfile
    kmlFile = shpFile.replace('.shp', '_'+str(number)+'.kml')
    kmlFile.replace('-', '_')
        
    maxRecords = 0
    
    shp2kml(shpFile, kmlFile, maxRecords)

def shp2kml(shpFile, kmlFile, maxRecords):    
    #Open files
    shpDs=ogr.Open(shpFile)
    shpLayer=shpDs.GetLayer()
    
    kmlDs = ogr.GetDriverByName('KML').CreateDataSource(kmlFile)
    kmlLayer = kmlDs.CreateLayer(os.path.splitext(os.path.basename(kmlFile))[0])
    
    #Get field names
    shpDfn=shpLayer.GetLayerDefn()
    nfields=shpDfn.GetFieldCount()
    headers=[]
    for i in range(nfields):
        headers.append(shpDfn.GetFieldDefn(i).GetName())
        field = shpDfn.GetFieldDefn(i).GetName()
        field_def = ogr.FieldDefn(field)
        kmlLayer.CreateField(field_def)
    headers.append('kmlgeometry')
   
    # Write attributes and kml out to csv
    rows = 0
    for shpFeat in shpLayer:
        attributes=shpFeat.items()
        shpGeom=shpFeat.GetGeometryRef()
        attributes['kmlgeometry']=shpGeom.ExportToKML()
        # print (attributes)
        kmlFeat = ogr.Feature(kmlLayer.GetLayerDefn())
        for field in headers[:-1]: #skip kmlgeometry (assumed to be in last column)
            kmlFeat.SetField(field, attributes[field])
        kmlFeat.SetGeometry(ogr.CreateGeometryFromGML(attributes['kmlgeometry']))
        kmlLayer.CreateFeature(kmlFeat)
        rows += 1
        if rows % 1000 == 0:
            print ("Rows: {:,}".format(rows))
        if maxRecords > 0 and rows >= maxRecords:
            break
    
    #clean up
    del shpLayer,shpDs,kmlLayer,kmlDs

    print ("------------")
    print ("Rows: {:,}".format(rows))
    print ("")