# Where the Light Fails to Fall

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | osint |
| **Solves** | 516 |

## Overview

The brief is a photo of a pigeon — Sir Marcus Skuttlebanks, apparently well travelled — with two annotations: a red arrow pointing north, and the pigeon's shadow falling to its right. The observation is timestamped `2026-06-20 · 19:55 · UTC+02:00`. The question is the city.

There is only one hard piece of evidence in the image: the direction of the shadow relative to north. Everything else is scenery. A shadow points exactly away from the sun, and the sun's azimuth at a given instant is a function of latitude and longitude, so the photo is not a photo problem but a solar-geometry problem with a unique answer.

## Solve

The red arrow defines the frame, so the shadow's direction can be measured directly in the image plane. Overlay a protractor with its baseline on the arrow — an on-screen one such as `onlineprotractortool.org` is enough — and read clockwise from north:

```
shadow bearing ≈ 109°
```

A shadow is the anti-solar direction, so the sun was at:

```
sun azimuth = shadow bearing + 180° = 289°
```

That is a north-west evening sun, which matches the timestamp.

`2026-06-20 19:55 UTC+02:00` is `17:55 UTC`. On 20 June at that hour the sun is still up across western and central Europe, so daylight alone is not a discriminator. The offset in the timestamp is: the clock was running CEST, which puts the location in the UTC+2 belt and removes London, a UTC+1 city. What remains among the major cities with the sun still up is essentially Paris and Amsterdam.

Entering the date, the time and the CEST timezone into `suncalc.org`, then clicking each candidate and reading the azimuth from the info panel:

| City | Sun azimuth | Implied shadow bearing |
|---|---|---|
| Paris | 284° | 104° |
| Amsterdam | 289° | **109°** |

Amsterdam matches the photo exactly, Paris is five degrees off. Five degrees is small, which is why the angle has to be measured rather than estimated by eye, and why the timezone filter is worth doing first: it turns "any city in Europe" into a two-item shortlist before the protractor comes out.

The north arrow is what makes the image solvable at all: it converts a picture into a bearing, and a bearing plus a timestamp intersects a point on the globe.

The city is **Amsterdam**.