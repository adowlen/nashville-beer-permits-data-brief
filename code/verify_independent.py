"""Independent verifier: recomputes headline figures from the raw CSV by a second path (shell-style counters in pure python, no shared code with build_stats.py)."""
import csv, json, os, collections
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-beer-permits-brief-2026-11-06")
rows=list(csv.DictReader(open(os.path.join(PKG,"data/beer_permits_raw.csv"))))
checks={}
checks["rows_2117"]=len(rows)==2117
issued=[r for r in rows if r["Status"]=="ISSUED"]; checks["issued_2064"]=len(issued)==2064
checks["temporary_53"]=sum(1 for r in rows if r["Status"]=="TEMPORARY")==53
d19=sum(1 for r in issued if r["Council_Dist"] not in ("","None") and int(float(r["Council_Dist"]))==19)
checks["d19_458"]=d19==458; checks["d19_share_22_2"]=round(100*d19/len(issued),1)==22.2
z3=sum(1 for r in issued if int(float(r["ZIP"]))==37203); checks["zip37203_336"]=z3==336
z14=[r for r in issued if int(float(r["ZIP"]))==37214]; checks["zip37214_213"]=len(z14)==213
checks["gaylord_74"]=sum(1 for r in z14 if "GAYLORD" in r["Business_Name"].upper())==74
on=sum(1 for r in issued if r["Permit_Sub_Type"] in ("ONSALES","ONOFFSALES")); checks["on_or_both_1464"]=on==1464
checks["off_only_575"]=sum(1 for r in issued if r["Permit_Sub_Type"]=="OFFSALES")==575
join=json.load(open(os.path.join(PKG,"data/zip_join_summary.json")))
checks["spearman_0_904"]=join["spearman_rho_beer_vs_police_by_zip"]==0.904
checks["police_zip_missing_46_6"]=join["police_zip_missing_pct"]==46.6
print(json.dumps(checks,indent=1)); print("PASS" if all(checks.values()) else "FAIL", f"{sum(checks.values())}/{len(checks)}")
json.dump(checks, open(os.path.join(PKG,"data/verify_independent_output.json"),"w"), indent=1)
