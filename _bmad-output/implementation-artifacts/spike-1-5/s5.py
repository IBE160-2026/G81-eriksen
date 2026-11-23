import urllib.request, urllib.parse, json, math, xml.etree.ElementTree as ET
UA={"User-Agent":"G81-eriksen-spike/0.1 (studentprosjekt)"}
APP="http://skjema.geonorge.no/SOSI/produktspesifikasjon/TurOgFriluftsruter/20171210"; ns={"app":APP,"gml":"http://www.opengis.net/gml/3.2"}
def hav(a,b):
    R=6371008.8; lo1,la1=map(math.radians,a); lo2,la2=map(math.radians,b)
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2; return 2*R*math.asin(math.sqrt(h))
r=ET.parse("wfs_F_01812_03.xml").getroot()
segs=[[tuple(map(float,x)) for x in zip(*[iter(m.find(".//gml:posList",ns).text.split())]*2)] for m in r.findall(".//app:Fotrute",ns)]
# kjede: 61-, 25(rev?)... ta lengste segmentkjede manuelt: bruk de 3 lengste segmentene som henger sammen? enklere: lengste segment
seg=max(segs,key=len); L=sum(hav(seg[i],seg[i+1]) for i in range(len(seg)-1)); print("segment punkter",len(seg),"lengde",round(L))
def resample(p,step):
    out=[p[0]]; acc=0.0
    for a,b in zip(p,p[1:]):
        d=hav(a,b); t=step-acc
        while t<=d:
            f=t/d; out.append((a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f)); t+=step
        acc=(acc+d)%step
    if out[-1]!=p[-1]: out.append(p[-1])
    return out
def hoyder(pts):
    z=[]
    for i in range(0,len(pts),50):
        u="https://ws.geonorge.no/hoydedata/v1/punkt?"+urllib.parse.urlencode({"koordsys":"4258","punkter":json.dumps([list(p) for p in pts[i:i+50]]),"geojson":"false"})
        z+= [q["z"] for q in json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read())["punkter"]]
    return z
def opp_ned(z,ter):
    opp=ned=0.0; ref=z[0]
    for h in z[1:]:
        d=h-ref
        if abs(d)>=ter: (opp:=opp+d) if d>0 else None; ned+= -d if d<0 else 0; ref=h
    return round(opp),round(ned)
res={}
for step in (10,25):
    pts=resample(seg,step); z=hoyder(pts); res[step]=z
    print(f"steg {step} m: punkter {len(pts)}, min {min(z)} maks {max(z)}, netto {round(z[-1]-z[0],1)}")
    for ter in (0,2,5,10): print(f"   terskel {ter} m -> opp/ned {opp_ned(z,ter)}")
json.dump(res,open("hoyder_resample.json","w"))
