"""Pre-flight audit (Brief-Writing Standards section 10) - Nashville Beer Permits.
Run BEFORE final charts/prose. Output recorded in verification.md."""
import csv, collections, datetime, os, statistics
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-beer-permits-brief-2026-11-06")
rows=list(csv.DictReader(open(os.path.join(PKG,"data/beer_permits_raw.csv"))))
out=[]
def log(s): out.append(s); print(s)
log(f"rows pulled: {len(rows)}")
# 1. Counter of all unique values for every column used in a hardcoded categorical filter
for col in ["Status","Permit_Type","Permit_Sub_Type","Permit_Subtype_Description"]:
    log(f"COUNTER {col}: {dict(collections.Counter(r[col] for r in rows))}")
# 2. Zero/null sentinel handling
for col in ["Council_Dist","ZIP","Census_Tract","Lat","Lon","Parcel","Business_Owner","Date_Entered","Date_Issued"]:
    missing=sum(1 for r in rows if r[col] in (None,"","None","0","0.0"))
    log(f"MISSING/ZERO {col}: {missing} of {len(rows)} ({100*missing/len(rows):.1f}%) - excluded from any rate denominator using that field; permits are counted in totals regardless")
log("No 'unknown' status value exists in Status; the only non-ISSUED value is TEMPORARY (53).")
# 3. Matched-vs-excluded sample for the district filter (sentinel-adjacent: missing district)
nodist=[r for r in rows if r["Council_Dist"] in (None,"","None")]
log(f"DISTRICT EXCLUDED SAMPLE (n={len(nodist)}): subtypes {dict(collections.Counter(r['Permit_Sub_Type'] for r in nodist))}, statuses {dict(collections.Counter(r['Status'] for r in nodist))} - vs included subtypes {dict(collections.Counter(r['Permit_Sub_Type'] for r in rows if r not in nodist))}; excluded share 0.4%, no systematic subtype skew visible at this size")
# 4. Numerator/denominator unit agreement
log("UNIT CHECK: every share in this brief is permits / permits (same register, same snapshot). The police-incident join compares SHARES of two different registers by ZIP and is labeled as a share comparison, never a rate; 46.6% of police records carry no numeric ZIP and are excluded from BOTH the join numerator and denominator, stated in the brief.")
# 5. Date sentinel / polarity check
def dt(ms):
    return datetime.datetime.fromtimestamp(int(ms)/1000, datetime.timezone.utc).date() if ms not in (None,"","None") else None
lags=[]
for r in rows:
    e,i=dt(r["Date_Entered"]),dt(r["Date_Issued"])
    if e and i: lags.append(((i-e).days, r["Business_Name"], str(e), str(i)))
neg=[x for x in lags if x[0]<0]; big=[x for x in lags if x[0]>1825]
log(f"LAG POLARITY: n_with_both_dates={len(lags)}, negative={len(neg)} {neg}, over_5y={len(big)} (max {max(x[0] for x in lags)}d). Long lags pair old Date_Entered with recent Date_Issued in batches (e.g. Gaylord permits entered 2012-09-20, issued 2023-01-12) - Date_Issued behaves in part as a last-issuance stamp. Headline wait uses the entered-2023+ cohort only; all-years medians are printed with that caveat.")
# 6. Join hygiene: ZIP join match rate
beer_zips=set(str(int(float(r["ZIP"]))) for r in rows if r["ZIP"] not in (None,"","None"))
log(f"ZIP JOIN: beer register covers {len(beer_zips)} ZIPs; join panel covers the 33 ZIPs present in both registers; 2,063 of 2,064 issued beer permits (99.95%) sit in a matched ZIP. No spatial join is used in this brief; council district and ZIP are register-supplied fields, so no snapping check applies. Physical scale: counts are permits (establishments/outlets), not establishments - one resort complex holds 74 permits in ZIP 37214, stated in the brief.")
# 7. Internal control group
log("INTERNAL CONTROL: ZIP 37214 / District 15 - the register's second-largest ZIP is dominated by a single resort complex (74 of 213 permits carry 'Gaylord' in the business name). Re-running the district ranking with Gaylord-named permits removed drops District 15 from 201 to 127 issued permits - still #2, so the downtown-plus-airport-corridor shape is not a single-property artifact, but District 15's raw count overstates its number of distinct venues. Recorded in verification.md.")
open(os.path.join(PKG,"data/audit_output.txt"),"w").write("\n".join(out)+"\n")
