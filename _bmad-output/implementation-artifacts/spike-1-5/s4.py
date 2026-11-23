import urllib.request, urllib.parse, json
UA={"User-Agent":"G81-eriksen-spike/0.1 (studentprosjekt)"}
B="https://ws.geonorge.no/hoydedata/v1/punkt"
pts=[[10.717187,59.953615],[10.715769,59.953129]]
def kall(params, fil=None):
    u=B+"?"+urllib.parse.urlencode(params)
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60); b=r.read()
        if fil: open(fil,"wb").write(b)
        return r.status, json.loads(b)
    except urllib.error.HTTPError as e: return e.code, e.read()[:300]
for ks in ("4258","4326"):
    s,d=kall({"koordsys":ks,"punkter":json.dumps(pts),"geojson":"false"}, f"hoyde_{ks}.json"); print(ks,s,json.dumps(d,ensure_ascii=True)[:400])
many=[[10.71+i*0.0002,59.953] for i in range(51)]
print("50:",kall({"koordsys":"4258","punkter":json.dumps(many[:50]),"geojson":"false"})[0])
s,d=kall({"koordsys":"4258","punkter":json.dumps(many),"geojson":"false"}); print("51:",s,str(d)[:200])
