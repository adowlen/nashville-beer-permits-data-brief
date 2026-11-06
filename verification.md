# Verification - Nashville Beer Permits brief (2026-11-06)

## Pre-flight audit

The audit script sits in code/audit_section10.py and ran BEFORE the final charts and prose were written. Full output: data/audit_output.txt. Summary of each gate:

- **Zero/null sentinel handling, "unknown" excluded from rate denominators:** Status carries exactly two values (ISSUED 2,064; TEMPORARY 53); there is no "unknown" status. Council_Dist is missing on 8 of 2,117 records (0.4 percent) - those records count in register totals and are excluded from district-share denominators' numerators only; the missing-district sample (4 on-site, 3 off-site, 1 on-and-off; 7 issued, 1 temporary) shows no systematic subtype skew at that size. ZIP is present on all records; Census_Tract missing on 7; Date_Issued missing on 52 (all TEMPORARY except one TEMPORARY record that carries an issued date). Business_Owner is missing on 1,084 records (51.2 percent), so no owner-concentration figure is published.
- **Matched-vs-excluded sample for sentinel-based filters:** the district filter sample above; the ZIP join matches 2,063 of 2,064 issued beer permits (99.95 percent) into a ZIP present in both registers.
- **Numerator/denominator unit agreement:** every share inside the beer register is permits / permits from the same snapshot. The police comparison is a share-vs-share comparison across two registers, labeled as such in the brief and on the chart; it is never printed as a rate.
- **Counter of all unique values for every column used in a hardcoded categorical filter:** Status, Permit_Type (BBPERMIT only, 2,117), Permit_Sub_Type (ONSALES 1,259; OFFSALES 580; ONOFFSALES 244; WHOLESALES 24; SPECIAL 10), and Permit_Subtype_Description are printed in full in data/audit_output.txt.
- **Join hygiene:** no spatial join is used; council district, ZIP, and census tract are register-supplied fields, so no street-name snapping check applies. Physical scale is reported alongside counts: permits are outlets, not venues - 2,064 issued permits at 1,933 distinct addresses, and one resort complex holds 74 permits in ZIP 37214.
- **Internal control group:** with all Gaylord-named permits removed, District 15 falls from 201 to 127 issued permits and remains the #2 district - the concentration shape is not a single-property artifact, while District 15's raw count does overstate its distinct venues. Recorded in the audit output.
- **Lag polarity check:** 2,065 records carry both dates; 1 gap is negative (-350 days, Joy Market, entered 1999-12-30, issued 1999-01-14) and 71 exceed 5 years (maximum 8,058 days). Long gaps pair old entered dates with recent issued dates in batches (the Gaylord group: entered 2012-09-20, issued 2023-01-12; 76 of the 230 permits issued in 2025 were entered before 2025), so Date_Issued behaves in part as a last-issuance stamp. The headline wait figure uses the entered-2023+ cohort (median 96 days); all-years medians carry the warning in the brief text and on the chart itself.

## Methods checklist (Brief-Writing Standards section 3)

- **Base rates and exposure:** all findings are shares of the register itself; no population or exposure denominator is claimed. Council districts are not population-normalized in this brief, and the brief does not claim they are equal-population units. The police join states its exposure limit (46.6 percent of records without a numeric ZIP) wherever it is used, and implies no causal pattern.
- **Direction of causality considered:** the brief makes no causal claim; the one interpretive section names land use and zoning as the strongest alternative explanation.
- **Category and definition changes over the time window:** the register is a current-status snapshot, not a time series; subtype definitions are the register's current ones. No trend claim is made from issued-date years, because Date_Issued is partly a re-issuance stamp (audit above).
- **Exact date range:** register snapshot 2026-11-06; entered dates span 1993-06-08 to 2026-11-03, issued dates 1994-02-01 to 2026-10-30. The police layer snapshot for the join is 2026-11-06 (all years served).
- **Match rate for every dataset join:** ZIP join - 33 of 34 beer-register ZIPs are present in the police register; 2,063 of 2,064 issued permits (99.95 percent) sit in a matched ZIP. On the police side, only 53.4 percent of records carry a numeric ZIP; the unmatched police records may differ systematically (records practice varies by report type, per the 2026-11-05 brief), and the brief prints this limit with the finding.
- **Small counts:** percentages are printed with their underlying counts throughout; the wholesale (24) and special-events (10 register-wide, 1 issued) groups are flagged by their counts wherever they appear, and no group comparison rests on a group under 30 without its count printed.
- **Official definitions:** permit types and subtypes use the register's own Permit_Subtype_Description values (BB - On Site Sales, BB - Off Site Sales, BB - On & Off Site Sales, BB - Wholesale Distributor, BB - Special Events). "Issued" and "Temporary" are the register's own Status values.

## Sync gate

- The repo README's dependency list (Python 3, pandas-free standard library plus matplotlib and Pillow for charts and the hero composite; the pull and audit use the standard library only) matches the imports in code/.
- Every number in brief-draft.md was cross-checked against stats.json after the final stats run; the independent verifier (code/verify_independent.py, a second code path over the raw CSV) passes 12/12 headline checks (data/verify_independent_output.json).

## Spot checks against primary sources (morning QA, 2026-11-06)

1. District 19 count and share recomputed from the raw pull by the independent verifier: 458 of 2,064 = 22.2 percent. Confirmed.
2. ZIP 37214 Gaylord count recomputed independently: 74 of 213. Confirmed; the same removal drops District 15 from 201 to 127 in the control run.
3. Police ZIP completeness re-pulled live on 2026-11-06 by grouped query: 946,569 served, 505,773 numeric-ZIP, 46.6 percent without a numeric ZIP. Confirmed against the join panel (data/police_incidents_by_zip.csv).
