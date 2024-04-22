# code of sunrise sunset algorithm develop by edwillin Almanac for Computers, 1990
# 	published by Nautical Almanac Office
# 	United States Naval Observatory
# 	Washington, DC 20392
import math
from math import floor


def sunrise_sunset(years, months, days, latitudes, longitudes, zeniths):
    # year = int(year)
    # month = int(month)
    # day = int(day)
    # latitude = float(latitude)
    # longitude = float(longitude)
    # zenith = float(zenith)

    # calculate day of year

    N1 = floor(275 * months / 9)
    N2 = floor((months + 9) / 12)
    N3 = (1 + floor((years - 4 * floor(years / 4) + 2) / 3))
    N = N1 - (N2 * N3) + days - 30
    # convert latitude and longitude in radina
    latirad = math.radians(latitudes)
    longirad = math.radians(longitudes)

    # convert longitude hour value and calculate an approximate time

    lng_hour = longitudes / 15
    t_rise = N + ((6 - lng_hour) / 24)
    t_set = N + ((18 - lng_hour) / 24)

    # sun's mean anomaly
    M_rise = (0.9856 * t_rise) - 3.289
    M_set = (0.9856 * t_set) - 3.289

    # calculate sun's true longitude
    L_rise = M_rise + (1.916 * math.sin(math.radians(M_rise))) + (0.020 * math.sin(math.radians(2 * M_rise))) + 282.634
    L_set = M_set + (1.916 * math.sin(math.radians(M_set))) + (0.020 * math.sin(math.radians(2 * M_set))) + 282.634

    # adjust longitude within the range [-180, 180]

    L_rise = L_rise % 360
    if L_rise > 180:
        L_rise -= 360

    L_set = L_set % 360
    if L_set > 180:
        L_set -= 360
    # calculate sun's right ascension
    RA_rise = math.degrees(math.atan(0.91764 * math.tan(math.radians(L_rise))))
    RA_set = math.degrees(math.atan(0.91764 * math.tan(math.radians(L_set))))

    # adjust right ascension value to be within range [0, 360]
    RA_rise = RA_rise % 360
    RA_set = RA_set % 360

    # right ascension value needs to be in the same quadrant as L
    Lquadrant_rise = (math.floor(L_rise / 90)) * 90
    Lquadrant_set = (math.floor(L_set / 90)) * 90
    RAquadrant_rise = (math.floor(RA_rise / 90)) * 90
    RAquadrant_set = (math.floor(RA_set / 90)) * 90
    RA_rise = RA_rise + (Lquadrant_rise - RAquadrant_rise)
    RA_set = RA_set + (Lquadrant_set - RAquadrant_set)

    # right ascension value needs to be converted into hours
    RA_rise = RA_rise / 15
    RA_set = RA_set / 15

    # sun declination
    sinDec_rise = 0.39782 * math.sin(math.radians(L_rise))
    sinDec_set = 0.39782 * math.sin(math.radians(L_set))

    cosDec_rise = math.cos(math.asin(sinDec_rise))
    cosDec_set = math.cos(math.asin(sinDec_set))

    # calculate sunrise and sunset times
    cos_H_rise = (math.sin(math.radians(zeniths)) - sinDec_rise * math.sin(latirad)) / (cosDec_rise * math.cos(latirad))
    cos_H_set = (math.sin(math.radians(zeniths)) - sinDec_set * math.sin(latirad)) / (cosDec_set * math.cos(latirad))

    # Ensure the argument is within the valid range [-1, 1]
    cos_H_rise = max(min(cos_H_rise, 1), -1)
    cos_H_set = max(min(cos_H_set, 1), -1)

    # calculate sunrise and sunset times
    H_rise = math.degrees(math.acos(cos_H_rise))
    H_set = math.degrees(math.acos(cos_H_set))

    H_rise /= 15
    H_set /= 15

    # calculate local mean time
    T_rise = H_rise + RA_rise - (0.0657 * t_rise) - 6.622
    T_set = H_set + RA_set - (0.0657 * t_set) - 6.622
    # adjust back to UTC
    UT_rise = T_rise - lng_hour
    UT_set = T_set - lng_hour

    # Adjust UT to range of (0, 24)
    UT_rise %= 24
    UT_set %= 24

    # format time as hour and minutes
    sunrise_hours = int(UT_rise)
    sunrise_minutes = int((UT_rise - sunrise_hours) * 60)
    sunset_hours = int(UT_set)
    sunset_minutes = int((UT_set - sunset_hours) * 60)

    return sunrise_hours, sunrise_minutes, sunset_hours, sunset_minutes


year = 2024
month = 4
day = 18
latitude = 37.7749  # San Francisco latitude
longitude = -122.4194  # San Francisco longitude
zenith = 90.8333  # Civil twilight zenith angle

sunrise_hour, sunrise_minute, sunset_hour, sunset_minute = sunrise_sunset(year, month, day, latitude, longitude, zenith)

print("Sunrise:", sunrise_hour, ":", sunrise_minute)
print("Sunset:", sunset_hour, ":", sunset_minute)

