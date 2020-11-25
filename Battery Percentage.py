import threading
import winsound
import psutil
import ctypes
import time
import sys

if psutil.sensors_battery() is None:
    ctypes.windll.user32.MessageBoxW(0, "This Computer may not have a battery or may be damaged.", "Battery Status", 0)
    sys.exit()


def batery_check():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    if not plugged:
        plugged = "Not Plugged In"
    else:
        plugged = "Plugged In"

    return percent, plugged


def beep():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 2000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)


def messagebox():
    ctypes.windll.user32.MessageBoxW(0, "Unplug Charger now to avoid battery damage!", "Battery Status", 0)


def check():
    flag = True
    messageflag = False

    while flag:

        percent, plugged = batery_check()
        sys.stdout.flush()
        sys.stdout.write('\rRunning program, battery at ' + str(percent) + "% " + plugged)
        sys.stdout.flush()

        if plugged == "Plugged In":
            if percent >= 95:

                beep()

                if not messageflag:
                    message = threading.Thread(target=messagebox)
                    message.start()
                    messageflag = True

        else:
            if percent <= 95:
                messageflag = False

        time.sleep(2)


t = threading.Thread(target=check)
t.start()