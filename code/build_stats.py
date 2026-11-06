import csv, json, collections, statistics, datetime, os, urllib.request, urllib.parse
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-beer-permits-brief-2026-11-06")
rows=list(csv.DictReader(open(os.path.join(PKG,"data/beer_permits_raw.csv"))))
def dt(ms):
    return datetime.datetime.fromtimestamp(int(ms)/1000, datetime.timezone.utc).date() if ms not in (None,"","None") else None
for r in rows:
    r["_entered"]=dt(r["Date_Entered"]); r["_issued"]=dt(r["Date_Issued"])
    r["_lag"]=(r["_issued"]-r["_entered"]).days if r["_entered"] and r["_issued"] else None
    r["_dist"]=int(float(r["Council_Dist"])) if r["Council_Dist"] not in (None,"","None") else None
    r["_zip"]=str(int(float(r["ZIP"]))) if r["ZIP"] not in (None,"","None") else None
def med(xs): return statistics.median(xs) if xs else None
def pct(a,b): return round(100*a/b,1) if b else None
stats={}
stats["dataset"]="Nashville Beer Permit Locations (Beer_Permit_Locations_Feature_Layer_view layer 0, hubNashville / Metro Nashville open data)"
stats["snapshot_date"]="2026-11-06"; stats["rows"]=len(rows)
stats["unit"]="one row = one beer permit record in the served register (Permit__ is the permit number); the register is a current-status list, not a historical ledger of every permit ever issued - permits that lapsed or were surrendered before the snapshot are not in it"
stats["status_counter"]=dict(collections.Counter(r["Status"] for r in rows))
stats["subtype_counter"]=dict(collections.Counter(r["Permit_Sub_Type"] for r in rows))
stats["subtype_description_counter"]=dict(collections.Counter(r["Permit_Subtype_Description"] for r in rows))
stats["permit_type_counter"]=dict(collections.Counter(r["Permit_Type"] for r in rows))
# issued-only population
issued=[r for r in rows if r["Status"]=="ISSUED"]
stats["issued_rows"]=len(issued)
stats["issued_subtype_counter"]=dict(collections.Counter(r["Permit_Sub_Type"] for r in issued))
on=[r for r in issued if r["Permit_Sub_Type"] in ("ONSALES","ONOFFSALES")]
stats["issued_on_site_or_both"]=len(on); stats["issued_on_site_or_both_pct"]=pct(len(on),len(issued))
stats["issued_off_only"]=len([r for r in issued if r["Permit_Sub_Type"]=="OFFSALES"]); stats["issued_off_only_pct"]=pct(stats["issued_off_only"],len(issued))
# lag
lags=[r["_lag"] for r in rows if r["_lag"] is not None]
stats["lag"]={"n":len(lags),"median_days":med(lags),"mean_days":round(statistics.mean(lags),1),"p90_days":sorted(lags)[int(0.9*len(lags))],"max_days":max(lags),"min_days":min(lags),"negative_n":sum(1 for x in lags if x<0),"zero_n":sum(1 for x in lags if x==0)}
by={}
for st in sorted(set(r["Permit_Sub_Type"] for r in rows)):
    xs=[r["_lag"] for r in rows if r["Permit_Sub_Type"]==st and r["_lag"] is not None]
    by[st]={"n":len(xs),"median_days":med(xs),"p90_days":sorted(xs)[int(0.9*len(xs))] if xs else None,"max_days":max(xs) if xs else None}
stats["lag_by_subtype"]=by
# lag by entered era
eras={}
for label,lo,hi in [("1993-2009",1993,2009),("2010-2019",2010,2019),("2020-2022",2020,2022),("2023-2026",2023,2026)]:
    xs=[r["_lag"] for r in rows if r["_lag"] is not None and r["_entered"] and lo<=r["_entered"].year<=hi]
    eras[label]={"n":len(xs),"median_days":med(xs)}
stats["lag_by_entered_era"]=eras
# recent cohorts full lag distribution 2023-2025 entered
rec=[r for r in rows if r["_entered"] and r["_entered"].year>=2023]
stats["entered_2023_plus"]={"n":len(rec),"with_issued_date":sum(1 for r in rec if r["_issued"]),"status_counter":dict(collections.Counter(r["Status"] for r in rec))}
# issued by year
iy=collections.Counter(r["_issued"].year for r in rows if r["_issued"])
stats["issued_by_year"]=dict(sorted(iy.items()))
ey=collections.Counter(r["_entered"].year for r in rows if r["_entered"])
stats["entered_by_year"]=dict(sorted(ey.items()))
stats["issued_2021_2025_total"]=sum(iy[y] for y in range(2021,2026))
# district
dist=collections.Counter(r["_dist"] for r in issued if r["_dist"])
stats["district_top10_issued"]=[{"district":k,"permits":v,"share_pct":pct(v,len(issued))} for k,v in dist.most_common(10)]
stats["district19_share_pct"]=pct(dist[19],len(issued))
stats["districts_with_permits"]=len(dist); stats["issued_missing_district"]=sum(1 for r in issued if not r["_dist"])
d19=[r for r in issued if r["_dist"]==19]
stats["district19_subtypes"]=dict(collections.Counter(r["Permit_Sub_Type"] for r in d19))
stats["district19_on_share_pct"]=pct(len([r for r in d19 if r["Permit_Sub_Type"] in ("ONSALES","ONOFFSALES")]),len(d19))
stats["all_issued_on_share_pct"]=stats["issued_on_site_or_both_pct"]
# smallest districts
stats["district_bottom5_issued"]=[{"district":k,"permits":v} for k,v in dist.most_common()[-5:]]
stats["top3_district_share_pct"]=pct(sum(v for _,v in dist.most_common(3)),len(issued))
stats["top_district_to_median_ratio"]=round(dist.most_common(1)[0][1]/statistics.median(list(dist.values())),1)
stats["median_district_permits"]=statistics.median(list(dist.values()))
# ZIP
zc=collections.Counter(r["_zip"] for r in issued if r["_zip"])
stats["zip_top10_issued"]=[{"zip":k,"permits":v,"share_pct":pct(v,len(issued))} for k,v in zc.most_common(10)]
# business / owner concentration
bc=collections.Counter(r["Business_Name"].strip().upper() for r in issued if r["Business_Name"])
stats["distinct_business_names_issued"]=len(bc)
stats["businesses_with_2plus"]=sum(1 for v in bc.values() if v>=2); stats["max_permits_one_business_name"]=bc.most_common(5)
oc=collections.Counter(r["Business_Owner"].strip().upper() for r in issued if r["Business_Owner"])
stats["distinct_owners_issued"]=len(oc); stats["owner_top5"]=oc.most_common(5)
stats["permits_at_duplicate_addresses"]=None
ac=collections.Counter(" ".join(r["Address"].upper().split()) for r in issued if r["Address"])
stats["distinct_addresses_issued"]=len(ac); stats["addresses_with_2plus_permits"]=sum(1 for v in ac.values() if v>=2); stats["max_permits_one_address"]=ac.most_common(3)
pc=collections.Counter(r["Parcel"] for r in issued if r["Parcel"] not in (None,"","None"))
stats["distinct_parcels_issued"]=len(pc); stats["parcels_with_2plus"]=sum(1 for v in pc.values() if v>=2)
# temporary
temp=[r for r in rows if r["Status"]=="TEMPORARY"]
stats["temporary"]={"n":len(temp),"with_issued_date":sum(1 for r in temp if r["_issued"]),"entered_range":[str(min(r["_entered"] for r in temp)),str(max(r["_entered"] for r in temp))],"subtypes":dict(collections.Counter(r["Permit_Sub_Type"] for r in temp))}
stats["issued_status_without_issued_date"]=sum(1 for r in issued if not r["_issued"])
stats["nonissued_with_issued_date"]=sum(1 for r in rows if r["Status"]!="ISSUED" and r["_issued"])
# completeness
stats["completeness"]={"missing_council_district_all":sum(1 for r in rows if not r["_dist"]),"missing_zip_all":sum(1 for r in rows if not r["_zip"]),"missing_parcel_all":sum(1 for r in rows if r["Parcel"] in (None,"","None")),"missing_business_owner_all":sum(1 for r in rows if not r["Business_Owner"]),"missing_latlon_all":sum(1 for r in rows if r["Lat"] in (None,"","None") or r["Lon"] in (None,"","None"))}
# audit counters for every column used in a hardcoded filter
stats["audit_column_counters"]={col:dict(collections.Counter(str(r[col]) for r in rows)) for col in ["Status","Permit_Type","Permit_Sub_Type"]}
json.dump(stats, open(os.path.join(PKG,"stats.json"),"w"), indent=2, default=str)
# panels
with open(os.path.join(PKG,"data/district_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["district","issued_permits","on_or_both","off_only","wholesale","special","on_share_pct"])
    for k in sorted(dist):
        sub=[r for r in issued if r["_dist"]==k]; c=collections.Counter(r["Permit_Sub_Type"] for r in sub)
        w.writerow([k,len(sub),c["ONSALES"]+c["ONOFFSALES"],c["OFFSALES"],c["WHOLESALES"],c["SPECIAL"],pct(c["ONSALES"]+c["ONOFFSALES"],len(sub))])
with open(os.path.join(PKG,"data/zip_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["zip","issued_permits","share_pct"])
    for k,v in zc.most_common(): w.writerow([k,v,pct(v,len(issued))])
with open(os.path.join(PKG,"data/lag_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["subtype","n_with_dates","median_days","p90_days","max_days"])
    for k,v in by.items(): w.writerow([k,v["n"],v["median_days"],v["p90_days"],v["max_days"]])
print(json.dumps({k:stats[k] for k in ["rows","issued_rows","lag","district19_share_pct","top3_district_share_pct","temporary"]},indent=2,default=str))
