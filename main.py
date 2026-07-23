#Real life
day_total_seconds = 24 * 60*60 #Hours in a day * seconds in an hour
time_to_calculate = "23:39:00"
sunrise = "05:11:00"
sunset = "21:01:00"
sunrise_tomorrow = "05:12:00"
sunset_yesterday = "21:03:00"
moonphase = "Waxing Gibbous"

#Minecraft
minecraft_day_total_ticks = 24000
minecraft_sunrise_tick = 23000
minecraft_sunset_tick = 13000

#==========================================================================================

import datetime


def convert_to_time_object(string):
    """Function to convert strings into time objects"""

    #Format as 24hour:minute:second
    time_object = datetime.datetime.strptime(string, "%H:%M:%S")
    return time_object


def convert_to_seconds(time):
    """Function to convert times into total seconds"""
    hour = time.hour
    minute = time.minute
    second = time.second

    hour_as_seconds = hour*60*60
    minute_as_seconds = minute*60

    time_as_seconds = hour_as_seconds + minute_as_seconds + second
    return time_as_seconds


time_to_calculate = convert_to_seconds(convert_to_time_object(time_to_calculate))
sunrise = convert_to_seconds(convert_to_time_object(sunrise))
sunset = convert_to_seconds(convert_to_time_object(sunset))
sunrise_tomorrow = convert_to_seconds(convert_to_time_object(sunrise_tomorrow))
sunset_yesterday = convert_to_seconds(convert_to_time_object(sunset_yesterday))

minecraft_day_duration = (minecraft_sunset_tick - minecraft_sunrise_tick) % minecraft_day_total_ticks
minecraft_night_duration = minecraft_day_total_ticks - minecraft_day_duration


if moonphase == "New Moon":
    minecraft_moon_phase = 4

elif moonphase == "Waxing Crescent":
    minecraft_moon_phase = 5

elif moonphase == "First Quarter":
    minecraft_moon_phase = 6

elif moonphase == "Waxing Gibbous":
    minecraft_moon_phase = 7

elif moonphase == "Full Moon":
    minecraft_moon_phase = 0

elif moonphase == "Waning Gibbous":
    minecraft_moon_phase = 1

elif moonphase == "Last Quarter":
    minecraft_moon_phase = 2

elif moonphase == "Waning Crescent":
    minecraft_moon_phase = 3

minecraft_tick_addition = minecraft_moon_phase * minecraft_day_total_ticks


if sunrise <= time_to_calculate < sunset:
    day_duration = sunset - sunrise
    elapsed_time = time_to_calculate - sunrise
    progress = elapsed_time / day_duration
    
    minecraft_time = minecraft_sunrise_tick + (progress * minecraft_day_duration)

else:
    #Note that after midnight, the sunrise and sunset should be adjusted
    
    if time_to_calculate < sunrise: #After midnight
        sunset = sunset_yesterday
    
    else: #Before midnight
        sunrise = sunrise_tomorrow  
    
    #This is a reference to an old method that was used to calculate the night lenght
    #Think as a circle, where midnight is the origin. It takes the entire time from 0 to sunset.
    #What is left is a tiny slice of that circle, from sunset to midnight. We add the time untill sunrise to that.
    #night_duration = (day_total_seconds - sunset) + sunrise #Old way
    
    night_duration = (sunrise - sunset) % day_total_seconds
    elapsed_time = (time_to_calculate - sunset) % day_total_seconds
    progress = elapsed_time / night_duration
    
    minecraft_time = minecraft_sunset_tick + (progress * minecraft_night_duration)

minecraft_time = round((minecraft_time % minecraft_day_total_ticks) + minecraft_tick_addition)

print(minecraft_time)
