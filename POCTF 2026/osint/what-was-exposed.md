# What Was Exposed

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | osint |
| **Solves** | 119 |

## Overview

The prompt separates the subject from the target. The subject is Janet Jackson — "singer, songwriter, actress, dancer. Super Bowl scapegoat" — but the task is framed as finding "someone that is looking for the subject." That someone is Reddit account `Legal-Yoghurt2423`, who posts in `r/janetjackson`, claims $17,000 is owed "for Robert Shepherd violations", and publishes a relative's home address "to discuss the matter." The address is what the poster exposed, and it is the pivot: the real question is a historical-imagery question about that property's backyard fence.

The work splits into three parts: recover the poster's Reddit activity, resolve the address to an exact parcel, and read the fence position from Google Earth's historical captures.

## Solve

Searching `r/janetjackson` for the account's distinctive phrasing returns two comments by `u/Legal-Yoghurt2423`. One, from 2024-04-29 in "What is Janet Jackson's fan mail address?", supplies "my Sister's townhouse at 4444 Victory Drive, Unit 14 Houston, Texas 77088" along with a gate code. A second, from 2024-05-30, supplies a mailbox address. The townhouse is the property in question.

"Unit 14" is not one of the four-digit condo units (1101–1319) at the same street number. Harris County's parcel layer disambiguates it. Querying the HCAD ArcGIS `Parcels` service for `site_str_num='4444'` and `site_str_name='VICTORY'` returns 63 records; unit 14 is account `1186140010014`, legal `LT 14 BLK 1 HUNTINGTON PARK PAR R/P` — 6,164 sqft, a 1,456 sqft one-story built in 2005. The parcel is the south-west corner of the townhouse block, and its backyard fence runs along the south boundary (E–F, ~20.1 m).

`GEHistoricalImagery` exposes 35 distinct z20 captures over the parcel between 2002 and 2026:

GEHistoricalImagery download --lower-left=29.86772,-95.47102 \
  --upper-right=29.86832,-95.47048 -z 20 -d 2015/08/01 \
  -o 2015-08-01.png --of=PNG

Overlaying the HCAD parcel ring on each capture and averaging a perpendicular brightness profile along E–F locates the fence: a sunlit band (the fence's south face) with a dark shadow band immediately north of it. Offsets are in metres, negative inside the lot:

| capture | fence face | shadow |
|---|---|---|
| 2011-03-11 | −0.60 | −1.30 |
| 2012-10-28 | −0.60 | −1.35 |
| 2013-08-08 | −1.25 | −1.95 |
| 2014-04-09 | −1.45 | −2.15 |
| 2015-06-01 | −2.15 | −2.85 |
| 2015-08-01 | −2.15 | −2.85 |

In 2011 the fence sits on the parcel line. The face and its shadow then move north together and progressively, reaching ~2 m inside the lot by 2015, which leaves a strip of open ground between the fence and the private drive. Because the bright face and the dark shadow move in lockstep, this is the fence itself moving, not a shifted camera.

The captures after 2020 are a trap. From 2024 the same measurement jumps around by ±1–2 m (2024-02-20 reads +1.8 m, 2026-02-27 reads −1.2 m, 2026-10-06 reads +0.9 m). That is parallax of a 1.5–2 m tall fence viewed from different capture angles, not a second move. The only monotonic change in the whole sequence is the 2011→2015 setback, which is why no adjacent-year pair works: the two usable bracket years are not consecutive.

The fence in the backyard was moved between 2011 and 2015.