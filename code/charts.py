import json, csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-beer-permits-brief-2026-11-06")
s=json.load(open(os.path.join(PKG,"stats.json")))
CHAR="#232323"; AMBER="#E8A33D"; TEAL="#2A9D8F"; GREY="#8A8A8A"
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":CHAR,"axes.edgecolor":GREY,"axes.labelcolor":CHAR,"xtick.color":CHAR,"ytick.color":CHAR})
def save(fig,name):
    fig.savefig(os.path.join(PKG,"charts",name), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print(name)
# 1 districts
top=s["district_top10_issued"][::-1]
fig,ax=plt.subplots(figsize=(7.2,4.6))
ax.barh([f"District {d['district']}" for d in top],[d["permits"] for d in top], color=[AMBER if d["district"]==19 else TEAL for d in top])
for i,d in enumerate(top): ax.text(d["permits"]+8,i,f"{d['permits']} ({d['share_pct']}%)",va="center",fontsize=9)
ax.set_xlabel("Issued beer permits in the register, snapshot 2026-11-06 (n=2,064 issued; 2,056 with a council district)")
ax.set_title("One council district holds 22.2% of Nashville's issued beer permits",fontsize=12,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); ax.set_xlim(0,540); save(fig,"chart_districts_top10.png")
# 2 subtype lag (all-years, caveated on the graphic)
order=["OFFSALES","ONSALES","ONOFFSALES","WHOLESALES"]
labels={"OFFSALES":"Off-site only\n(n=575 with dates)","ONSALES":"On-site\n(n=1,239)","ONOFFSALES":"On & off site\n(n=226)","WHOLESALES":"Wholesale\n(n=24)"}
fig,ax=plt.subplots(figsize=(7.2,4.2))
ax.bar([labels[o] for o in order],[s["lag_by_subtype"][o]["median_days"] for o in order], color=[TEAL,AMBER,TEAL,GREY])
for i,o in enumerate(order): ax.text(i,s["lag_by_subtype"][o]["median_days"]+3,f"{s['lag_by_subtype'][o]['median_days']} days",ha="center",fontsize=10,weight="bold")
ax.set_ylabel("Median days, Date_Entered to Date_Issued (all years in register)")
ax.set_title("Register lag by permit type - all-years medians\n(Date_Issued partly behaves as a last-issuance stamp; see brief)",fontsize=11,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); save(fig,"chart_lag_by_subtype.png")
# 3 ZIP join scatter
panel=list(csv.DictReader(open(os.path.join(PKG,"data/zip_join_panel.csv"))))
fig,ax=plt.subplots(figsize=(7.2,5.0))
for r in panel:
    x,y=float(r["police_share_pct"]),float(r["beer_share_pct"])
    ax.scatter(x,y,s=55,color=TEAL,edgecolor=CHAR,linewidth=0.5)
    if r["zip"] in ("37203","37207","37013","37214","37211"): ax.annotate(r["zip"],(x,y),textcoords="offset points",xytext=(6,5),fontsize=9,weight="bold")
lim=17
ax.plot([0,lim],[0,lim],color=GREY,ls="--",lw=1)
ax.text(11.5,13.2,"equal shares",rotation=38,color=GREY,fontsize=8)
ax.set_xlabel("Share of MNPD incident records with a numeric ZIP (%), all years served, n=505,773 of 946,569")
ax.set_ylabel("Share of issued beer permits (%), n=2,064")
ax.set_title("Beer permits and police incident records by ZIP - shares track,\nbut downtown (37203) holds 2.6x the permit share",fontsize=11,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False)
fig.text(0.01,-0.02,"46.6% of police incident records carry no numeric ZIP and are excluded from both shares. ZIPs with fewer than 30 permits in either register are plotted but not labeled.",fontsize=7.5,color=GREY)
save(fig,"chart_zip_join.png")
# 4 entered-era lag
eras=[("1993-2009",37.0),("2010-2019",48),("2020-2022",94),("2023-2026",96)]
fig,ax=plt.subplots(figsize=(7.2,4.2))
ax.bar([e[0] for e in eras],[e[1] for e in eras],color=[GREY,GREY,TEAL,AMBER])
for i,e in enumerate(eras): ax.text(i,e[1]+3,f"{int(e[1])} days",ha="center",fontsize=10,weight="bold")
ax.set_ylabel("Median days, Date_Entered to Date_Issued")
ax.set_title("The register's entered-to-issued gap has doubled since the 2010s\n(cohorts by Date_Entered; recent cohorts are the cleanest wait measure)",fontsize=11,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); save(fig,"chart_lag_by_era.png")
