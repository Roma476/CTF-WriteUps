# Measurements

All values used in the final calculation. The flag is not included.

## Artifact

- Archive: `following-the-money.zip`
- SHA-256: `864cbc23a8756ed94d793f6f81259b47857b71d16268ca3ad0d2ca7f9cd6b90a`
- Contents: 30 RGBA PNG fragments with torn alpha masks.

## Bill

- Serial: `E10093751B`
- Series: 2017
- Signatory: Jovita Carranza
- Federal Reserve district: E (Richmond)
- Serial locations: top right and bottom left.

## Where's George

- Challenge token: `b:Fuzhs8rJ7u`
- Report URL: `https://www.wheresgeorge.com/report.php?b=Fuzhs8rJ7u`
- Relevant content: the report note
- Blog URL: `https://pointeroverflowctf.com/challenges/following-the-money/astroblog/`

## Blog

- Post: #137, "The viaduct, finally clear"
- Capture UTC: `2024-10-12T21:18:38Z`
- Image size: 1080 x 1620 px
- Vertical FOV: 45.9°
- Pixel scale: `45.9 / 1620 = 0.028333°/px`
- Horizon row: `y = 1443`
- EXIF timestamp on the edited image: `2024:10:12 22:44:26` (not used)

## Astrometry

- Solver: Astrometry.net
- CRVAL1 (RA): `9.5355366203°`
- CRVAL2 (Dec): `31.2660622861°`
- CRPIX1: `63.2815876007`
- CRPIX2: `660.067301432`

## Derived

- Altitude: `(1443 - 660.067301432) * 45.9 / 1620 = 22.1831°`
- GST at capture: `341.595636°`
- Longitude: `GST - RA = 341.595636 - 9.535537 = 332.060099° -> -27.939901°`

## Candidate viaducts

| Candidate | Latitude | Longitude | Verdict |
|---|---:|---:|---|
| Ribblehead | 54.2104 | -2.3702 | ~11 km north of the target latitude |
| Clapham / Wenning | 54.1041 | -2.4085 | wrong arch count and curve |
| Skipton & Wennington (unnamed) | 54.1066 | -2.4494 | wrong perspective |
| Helwith Bridge group | 54.1235 | -2.2909 | too far east |
| Bentham line | 54.1125 | -2.4911 | wrong viaduct |
