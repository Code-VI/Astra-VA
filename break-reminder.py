
import psutil
import datetime
import time
from plyer import notification

while True:
    def get_boot_time():
        boot_time_timestamp = psutil.boot_time()
        boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
        current_time = datetime.datetime.now()
        
        uptime = current_time -  boot_time
        return str(uptime)


    boot_time = get_boot_time()
    hours = boot_time.split(':')[0]

    if not int(hours)==0 and int(hours) % 2 == 0:
        notification.notify(
            title = 'Take a break!',
            message = "You've been working for more than 2 hours. Take a break and enjoy this beautiful day! 😊",
            app_name = 'break Reminder',
            timeout = 7
        )
        time.sleep(3600)

    elif int(hours) == 0:
        print('Good luck doing programming! 😊')
        notification.notify(
            title = 'Do your best!',
            message = 'Good luck doing programming! 😊',
            app_name = '',
            timeout = 7
        )
        time.sleep(3600)
    else:
        notification.notify(
            title = 'I LIKE YOUR SPIRIT!!',
            message = "Drink a glass of water and stay motivated 😊",
            app_name = 'Water Reminder',
            timeout = 7
        )
        time.sleep(3600)
