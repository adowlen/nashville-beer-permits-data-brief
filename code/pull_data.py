import urllib.request, urllib.parse, json, csv, os, collections, statistics, datetime
base="https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Beer_Permit_Locations_Feature_Layer_view/FeatureServer/0/query"
outdir=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-beer-permits-brief-2026-11-06/data")
rows=[]
offset=0
while True:
    params={"where":"1=1","outFields":"*","returnGeometry":"false","f":"json","resultOffset":offset,"resultRecordCount":2000,"orderByFields":"ObjectId"}
    url=base+"?"+urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r: d=json.load(r)
    feats=d.get("features",[])
    for f in feats: rows.append(f["attributes"])
    print(offset, len(feats), d.get("exceededTransferLimit"))
    if not d.get("exceededTransferLimit"): break
    offset+=len(feats)
# save csv
fields=list(rows[0].keys())
with open(os.path.join(outdir,"beer_permits_raw.csv"),"w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
with open(os.path.join(outdir,"pull_log.json"),"w") as fh: json.dump({"rows":len(rows),"source":base,"snapshot_date":"2026-11-06"},fh,indent=2)
print("total",len(rows))
# counters
for col in ["Status","Permit_Type","Permit_Sub_Type","Permit_Subtype_Description","City","State"]:
    c=collections.Counter(str(r.get(col)) for r in rows)
    print("\n==",col); 
    for k,v in c.most_common(30): print(repr(k),v)
# dates
def ts(v):
    return datetime.datetime.utcfromtimestamp(v/1000).date().isoformat() if v else None
entered=[r["Date_Entered"] for r in rows if r.get("Date_Entered")]
issued=[r["Date_Issued"] for r in rows if r.get("Date_Issued")]
print("\nentered range", ts(min(entered)), ts(max(entered)), "n",len(entered))
print("issued range", ts(min(issued)), ts(max(issued)), "n",len(issued))
print("missing council", sum(1 for r in rows if r.get("Council_Dist") is None), "missing zip", sum(1 for r in rows if r.get("ZIP") is None), "missing latlon", sum(1 for r in rows if r.get("Lat") is None))
print("council counter", collections.Counter(r.get("Council_Dist") for r in rows).most_common())
