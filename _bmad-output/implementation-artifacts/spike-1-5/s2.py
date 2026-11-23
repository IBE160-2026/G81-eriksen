import urllib.request, urllib.parse, sys, xml.etree.ElementTree as ET
UA={"User-Agent":"G81-eriksen-spike/0.1 (studentprosjekt)"}
APP="http://skjema.geonorge.no/SOSI/produktspesifikasjon/TurOgFriluftsruter/20171210"
base="https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter"
def hent(nr, fil):
    filt=(f'<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0" xmlns:app="{APP}">'
          f'<fes:PropertyIsEqualTo><fes:ValueReference>app:fotruteInfo/app:FotruteInfo/app:rutenummer</fes:ValueReference>'
          f'<fes:Literal>{nr}</fes:Literal></fes:PropertyIsEqualTo></fes:Filter>')
    q={"service":"WFS","version":"2.0.0","request":"GetFeature","typeNames":"app:Fotrute",
       "srsName":"EPSG:4326","namespaces":f"xmlns(app,{APP})","filter":filt}
    u=base+"?"+urllib.parse.urlencode(q)
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90); b=r.read()
    except urllib.error.HTTPError as e:
        print(nr,"HTTP",e.code,e.read()[:600]); return
    open(fil,"wb").write(b)
    root=ET.fromstring(b); ns={"app":APP,"gml":"http://www.opengis.net/gml/3.2"}
    ms=root.findall(".//app:Fotrute",ns)
    print(nr,"status",r.status,"bytes",len(b),"features",len(ms))
    for m in ms:
        pl=m.find(".//gml:posList",ns).text.split(); n=len(pl)//2
        print("  ", m.findtext("app:rutenavn",namespaces=ns), "| punkter",n,"| start",pl[0:2],"| slutt",pl[-2:])
for nr in sys.argv[1:]: hent(nr, f"wfs_{nr}.xml")
