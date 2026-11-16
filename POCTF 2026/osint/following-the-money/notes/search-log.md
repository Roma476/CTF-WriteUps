# Search log — Following the Money

This is the cleaned-up version of the notes I kept during the solve. It is deliberately more detailed than the write-up: the dead ends are the point. Credentials, session cookies, the team key, and the flag are omitted.

## 0. The artifact

The challenge shipped a ZIP with thirty PNG fragments. The archive hash was:

```text
864cbc23a8756ed94d793f6f81259b47857b71d16268ca3ad0d2ca7f9cd6b90a
```

Each PNG is a torn piece with an alpha mask. The pieces are not a simple grid: the tears overlap and the edges are irregular.

## 1. The jigsaw (evening 1, ~1 h)

First attempt: sort by the alpha-mask bounding box and place the pieces on a 6x5 grid. This gets the general layout but leaves the engraved lines misaligned. The trick is to match the torn edges, not the rectangular bounding boxes: the alpha mask is the shape, and the engraved lines continue across the tear.

After reconstruction, the serial is visible in two places. The top-right crop is the cleanest:

```text
E10093751B
```

The bill is a 2017 series $1 with Jovita Carranza's signature. The `E` prefix is the Federal Reserve district letter for Richmond; the trailing `B` is the block letter.

## 2. Where's George (evening 1, ~1 h)

The challenge gives `b:Fuzhs8rJ7u`. The direct report URL is:

```text
https://www.wheresgeorge.com/report.php?b=Fuzhs8rJ7u
```

The direct URL opens the bill page, but the travel history is not visible without a lookup. The site's lookup form accepts a ZIP code and the serial; using a ZIP from the bill's history confirmed the serial existed. The history then shows the entries, including the Initial Entry. The note points to:

```text
https://pointeroverflowctf.com/challenges/following-the-money/astroblog/
```

We used the site's form once and did not add further entries. The note is the only part of the report used in the chain; the travel history itself is not.

## 3. The blog (evening 1, ~30 min)

The blog has one relevant post, #137, "The viaduct, finally clear". The caption gives:

```text
2024-10-12T21:18:38Z
```

The page states the image is 1620 px tall with a 45.9° vertical FOV. The post includes two images: the star field and a "horizon marked" version. The second image is a redaction joke: a purple `[REDACTED]` panel covers the lower half, a row of cartoon figures sits above it, and a black band labelled `HORIZON` marks row 1443. The horizon is not drawn as a line; the band is the marker.

There is a timestamp discrepancy: the edited image's EXIF says `2024:10:12 22:44:26`, but the blog caption says `21:18:38Z`. The caption is the value that produces the accepted longitude; the EXIF time is local/edited metadata and is not used.

Post #136, "Leonids over the back garden", mentions a streetlight on Harrow Road. We tried to use that to pin the town, but it did not resolve the longitude; it is flavour text, not a coordinate.

## 4. The viaduct detour (evening 2, ~6 h)

The latitude in the challenge is 54.1116 N. The obvious move is to identify the viaduct and use its coordinates. We tried:

| Candidate | Latitude | Longitude | Verdict |
|---|---:|---:|---|
| Ribblehead | 54.2104 | -2.3702 | visually close, ~11 km north of the target latitude |
| Clapham / Wenning | 54.1041 | -2.4085 | close in latitude, wrong arch count and curve |
| Skipton & Wennington (unnamed) | 54.1066 | -2.4494 | close in latitude, wrong perspective |
| Helwith Bridge group | 54.1235 | -2.2909 | too far east, wrong setting |
| Bentham line | 54.1125 | -2.4911 | close in latitude, wrong viaduct |

Ribblehead is the trap: it is the famous viaduct, it is in the right general area, and the star field looks plausible over it. But it is 0.0988° north of the stated latitude, about 11 km. The challenge never asks for the viaduct. It asks for the camera's longitude.

We also tested the moon hypothesis: the post mentions the moon coming over the fell, so the moon's position at the capture time might constrain the azimuth. It did not produce a unique longitude.

## 5. The API graveyard (evening 2, ~2 h)

To check the candidates we tried:

- Overpass API: 406 Not Acceptable with the default user agent, then timeouts on the larger queries.
- Wikidata SPARQL: 429 Too Many Requests after a few queries.
- Geograph API: 403 Forbidden.
- The challenge site's Flask session cookie went stale mid-solve; re-authenticating fixed it.

The useful data came from OSM tiles and Wikipedia, not from the APIs.

## 6. Astrometry (evening 2, ~2 h)

Astrometry.net solves the star field. The WCS reference star is at:

```text
CRVAL1 =   9.5355366203°   (RA)
CRVAL2 =  31.2660622861°   (Dec)
CRPIX1 =  63.2815876007
CRPIX2 = 660.067301432
```

The first mistake was to use the star at the image centre. The WCS reference star is not the centre; it is the star at `CRPIX`. The second mistake was to use the full spherical branch: with the altitude and the latitude, you can recover the hour angle and then the longitude, but the challenge hint reduces the problem to the meridian relation. The literal `GST - RA` using the WCS reference star is the accepted path.

## 7. The formula (evening 2, ~30 min)

The altitude:

```text
alt = (1443 - 660.067301432) * 45.9 / 1620
    = 22.1831°
```

The sidereal time:

```text
GST = 280.46061837 + 360.98564736629 * (t - J2000) / 86400  (mod 360)
    = 341.595636°
```

The longitude:

```text
longitude = GST - RA
          = 341.595636 - 9.535537
          = 332.060099°  ->  -27.939901°
```

Submitting `-27.939901` returned the flag. The flag is redacted in the public write-up.

## 8. Timeline

| Phase | Time |
|---|---:|
| Jigsaw | ~1 h |
| Where's George | ~1 h |
| Blog | ~0.5 h |
| Viaduct detour | ~6 h |
| API graveyard | ~2 h |
| Astrometry | ~2 h |
| Formula | ~0.5 h |
| **Total** | **~13 h** |

## 9. What I would do differently

1. Read the hint literally. `GST - RA` is the whole formula; the spherical branch is a distraction.
2. Use the WCS reference star, not the image centre.
3. Treat the viaduct as flavour, not as a coordinate source. The latitude is given; the longitude is the unknown.
4. Keep a search log from the first minute. The dead ends are the write-up.
