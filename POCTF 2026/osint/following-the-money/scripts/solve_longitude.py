#!/usr/bin/env python3
"""Recompute the Following the Money longitude from the public measurements.

The solution is the literal meridian relation:

    longitude = GST - RA

where RA is the right ascension of the WCS reference star (the star at
CRPIX, not the star at the image centre) and GST is the Greenwich sidereal
time at the blog caption's capture time.

Run with:

    python3 scripts/solve_longitude.py
"""
from __future__ import annotations

from datetime import datetime, timezone

CAPTURE = datetime(2024, 10, 12, 21, 18, 38, tzinfo=timezone.utc)
IMAGE_HEIGHT = 1620.0
VFOV_DEG = 45.9
HORIZON_ROW = 1443.0
REFERENCE_ROW = 660.067301432
RA_DEG = 9.5355366203
LATITUDE_DEG = 54.1116


def gmst_deg(dt: datetime) -> float:
    """Greenwich mean sidereal time in degrees (IAU 1982)."""
    j2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    days = (dt - j2000).total_seconds() / 86400.0
    return (280.46061837 + 360.98564736629 * days) % 360.0


def main() -> None:
    altitude = (HORIZON_ROW - REFERENCE_ROW) * VFOV_DEG / IMAGE_HEIGHT
    gst = gmst_deg(CAPTURE)
    longitude = (gst - RA_DEG + 180.0) % 360.0 - 180.0

    print(f"altitude  = {altitude:.4f} deg")
    print(f"GST       = {gst:.6f} deg")
    print(f"longitude = {longitude:.6f} deg")
    print(f"latitude  = {LATITUDE_DEG:.4f} deg (given)")

    assert abs(altitude - 22.1831) < 0.001
    assert abs(gst - 341.595636) < 0.0001
    assert abs(longitude - (-27.939901)) < 0.0001


if __name__ == "__main__":
    main()
