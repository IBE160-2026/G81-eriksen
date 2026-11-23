import sys, math, xml.etree.ElementTree as ET
from collections import defaultdict
APP="http://skjema.geonorge.no/SOSI/produktspesifikasjon/TurOgFriluftsruter/20171210"
ns={"app":APP,"gml":"http://www.opengis.net/gml/3.2"}
def hav(a,b):
    R=6371008.8; lo1,la1=map(math.radians,a); lo2,la2=map(math.radians,b)
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
f=sys.argv[1]; root=ET.parse(f).getroot()
seg=[]
for m in root.findall(".//app:Fotrute",ns):
    v=list(map(float,m.find(".//gml:posList",ns).text.split())); p=list(zip(v[0::2],v[1::2]))
    info=m.find("app:fotruteInfo/app:FotruteInfo",ns)
    seg.append((p, info.findtext("app:rutenavn",namespaces=ns), m.findtext("app:merking",namespaces=ns)))
print("segmenter",len(seg),"navn",{ascii(s[1]) for s in seg},"merking",{s[2] for s in seg})
L=sum(hav(p[i],p[i+1]) for p,_,_ in seg for i in range(len(p)-1)); print("sum lengde m",round(L))
for tol in (0.0,1.0,5.0):
    nodes=[]; 
    def node(pt):
        for i,n in enumerate(nodes):
            if hav(n,pt)<=tol: return i
        nodes.append(pt); return len(nodes)-1
    deg=defaultdict(int); edges=[]
    for p,_,_ in seg:
        a,b=node(p[0]),node(p[-1]); deg[a]+=1; deg[b]+=1; edges.append((a,b))
    d1=[n for n,d in deg.items() if d==1]; d3=[n for n,d in deg.items() if d>=3]
    # components
    par=list(range(len(nodes)))
    def fnd(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b in edges: par[fnd(a)]=fnd(b)
    comps=len({fnd(n) for n in deg})
    print(f"tol {tol} m: noder {len(nodes)}, ender(grad1) {len(d1)}, forgreininger(grad>=3) {len(d3)}, komponenter {comps}")
# punktavstand
ds=[hav(p[i],p[i+1]) for p,_,_ in seg for i in range(len(p)-1)]
ds.sort(); print("punktavstand median",round(ds[len(ds)//2],1),"maks",round(ds[-1],1))
