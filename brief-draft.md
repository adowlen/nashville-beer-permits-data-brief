# Nashville's beer permits are a downtown register

**One-line summary:** Of the 2,064 issued beer permits in Metro Nashville's register on November 6, 2026, 458 (22.2 percent) sit in a single Metro Council district, District 19, which covers downtown, while the median council district holds 40.

Start with one property. The resort and convention complex on the Cumberland River in ZIP 37214 holds 74 beer permits by itself, one for each of its bars, restaurants, and venues. It is the extreme case of the pattern this brief measures: in Nashville's beer permit register, the permits pile up where visitors gather, and a single district downtown holds more of them than the 17 smallest districts combined.

Machine Readable pulled the full Nashville Beer Permit Locations register (2,117 records, snapshot November 6, 2026) from Metro Nashville's open data service. The register is the Metro Beer Permit Board's current-status list: 2,064 records carry status ISSUED and 53 carry status TEMPORARY. Permits that lapsed or were surrendered before the snapshot are not in the register, so every figure below describes the permits in force on the snapshot date, not every permit ever issued.

## Where the permits sit

- District 19 (downtown) holds 458 issued permits, 22.2 percent of the register. The next district, District 15, holds 201 (9.7 percent), and District 17 holds 101 (4.9 percent). The top three districts together hold 36.8 percent of all issued permits.
- The median council district holds 40 issued permits. District 19 holds 11.4 times the median, and more than the 17 smallest districts combined (424; derived from the district panel in this brief's data folder). The smallest counts are District 8 with 13 and District 12 with 14.
- By ZIP code, 37203 (downtown) holds 336 issued permits (16.3 percent) and 37214 holds 213 (10.3 percent). No other ZIP holds more than 8.3 percent.
- District 19's permits are mostly on-site: 344 on-site, 81 on-and-off-site, 28 off-site only, and 5 wholesale. Across the whole register, 1,464 of 2,064 issued permits (70.9 percent) allow on-site sales (on-site or on-and-off-site), 575 (27.9 percent) are off-site only, 24 are wholesale, and 1 is a special-events permit.

## One resort complex is 74 of the permits in ZIP 37214

Permit counts are counts of permits, not counts of venues. In ZIP 37214, 74 of the 213 issued permits (34.7 percent) carry "Gaylord" in the business name, the resort and convention complex on the Cumberland River. District 15, which contains that ZIP, holds 201 issued permits. Removing every Gaylord-named permit drops District 15 to 127 issued permits, which is still the second-highest district count in the register. The district ranking therefore does not rest on the resort alone, but its raw count overstates the number of distinct venues there.

The same distinction applies register-wide: the 2,064 issued permits sit at 1,933 distinct addresses and carry 1,869 distinct business names. The largest single business name is Walgreens, with 24 permits, all off-site. Business-owner names are recorded for only 48.8 percent of records (1,033 of 2,117), so owner-level concentration is not reported in this brief.

## The register against the police incident ledger

This brief joins the beer register to the Metro Nashville Police Department incident layer published in the November 5, 2026 Machine Readable brief, by ZIP code. Two scope limits apply and are printed wherever the join is used:

- 46.6 percent of the incident records served on November 6, 2026 (440,796 of 946,569) carry no numeric ZIP code. The join uses only the 505,773 records with a numeric ZIP, for both the numerator and the denominator of every police share.
- The comparison is a comparison of shares of two different registers, not a rate, and it implies no causal pattern in either direction.

On that basis: across the 33 ZIP codes present in both registers, the rank order of beer-permit share and police-record share is similar (Spearman rank correlation 0.90). The shares diverge most at the top. ZIP 37203 holds 16.3 percent of issued beer permits and 6.3 percent of ZIP-coded incident records, a ratio of 2.6. ZIP 37207 holds 10.0 percent of ZIP-coded incident records and 4.2 percent of beer permits (ratio 0.42), and ZIP 37013 holds 10.6 percent of ZIP-coded incident records and 4.8 percent of beer permits (ratio 0.46).

## How long permits take in the register, and a warning about the dates

The register carries a Date_Entered and a Date_Issued for each permit. The gap between them is not a clean application wait, for a reason visible in the data itself: 76 of the 230 permits with a 2025 issued date were entered before 2025, one group of Gaylord permits shares an entered date of September 20, 2012 and an issued date of January 12, 2023, and the single largest gap is 8,058 days. Date_Issued behaves in part as a last-issuance stamp that updates over a permit's life.

With that warning printed, the register's gaps measure as follows:

- For permits entered in 2023 or later, the cohort least affected by later re-stamping, the median gap is 96 days (735 permits with both dates).
- By entered cohort, the median gap is 37 days for 1993-2009 entries, 48 days for 2010-2019 entries, 94 days for 2020-2022 entries, and 96 days for 2023-2026 entries.
- Across all years, off-site permits carry a median gap of 49 days, on-site permits 85 days, on-and-off-site permits 93.5 days, and wholesale permits 90.5 days. These all-years medians include the re-stamping described above and are printed for the register's shape, not as measured application waits.
- One record carries an issued date 350 days before its entered date; it is counted in the register totals and excluded from no figure except the gap medians, where negative gaps are excluded (2,064 of 2,065 dated records have a non-negative gap).

## The temporary side is small and recent

All 53 TEMPORARY permits were entered between March 13, 2025 and November 3, 2026, and 52 of the 53 carry no issued date. The register shows no older temporary permits. Because the register is a current-status list, a temporary permit that was never issued and was later removed would not appear here; the 53 records are the temporary permits in force on the snapshot date, not a complete history of pending applications.

## The Denver comparison, with both scopes labeled

Denver's liquor register, published in the October 24, 2026 Machine Readable brief, carried 1,965 active licenses across all liquor license classes (hotels, taverns, stores, beer and wine, and others), of which 1,498 (76.2 percent) were on-premises classes. Nashville's register in this brief is beer permits only, issued by a different board under a different licensing system: 2,064 issued permits, 70.9 percent allowing on-site sales. The two registers are compared as footprints, not as like-for-like license universes.

The concentration shapes differ. Denver's largest neighborhood share was Five Points with 174 of 1,965 active licenses (8.9 percent, neighborhood geography). Nashville's largest share is District 19 with 458 of 2,064 issued permits (22.2 percent, council district geography). The geographies are different units, so the two percentages describe each register's own internal concentration and are not a head-to-head measure of the two cities.

## What this might mean

One possible reading is that Nashville's beer-permit footprint follows its visitor and entertainment geography more than its residential geography: the two largest concentrations are downtown and a resort complex, and the ZIP codes with the largest shares of police incident records hold proportionally fewer permits. The strongest alternative explanation is simpler: both patterns may mostly track where commercial floor space and late-night businesses are permitted to operate, in which case the register is measuring zoning and land use as much as demand. The data in this brief cannot separate those two readings.

## Who can act

- **Metro Beer Permit Board (permit administration).** The lever is the register itself: publishing a permit history (original issuance separate from later re-issuance) would make application waits measurable from the public data. Cost class: low-cost operational change. Outcome measure: the share of register records whose Date_Issued is their original issuance, checkable in this same dataset on a future snapshot.
- **Metro Council (district-level review).** The lever is district-level permitting and land-use review in District 19 and District 15. Cost class: budget decision if staff review capacity is added; no figure is estimated here. Outcome measure: the district share distribution in this register on a future snapshot, computed the same way as the district panel in this brief's data folder.
- **Metro Nashville Police Department and the Beer Permit Board (shared geography).** The lever is the 46.6 percent of incident records with no numeric ZIP: raising ZIP completeness would make every ZIP-level join against city registers more reliable. Cost class: low-cost operational change (records practice). Outcome measure: the ZIP-coded share of incident records, checkable in the incident layer on a future snapshot.

## Methods in brief

Snapshot of the full served register on November 6, 2026 (2,117 records; the live count on November 5 was 2,115, so the register updates daily). Council district is missing on 8 records (0.4 percent); those records are counted in register totals and excluded from district shares. ZIP code is present on all 2,117 records. The police join and its match rates are documented in verification.md, along with the pre-flight audit. This brief measures permits in force, not alcohol sales, consumption, or venue counts.

Data, code, charts, and the full audit: https://github.com/adowlen/nashville-beer-permits-data-brief

*Machine Readable is a public-good civic data project. Figures are drawn from the sources in the repository's sources.md; corrections are welcome and will be recorded in the repository.*
