from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import csv
import time
import datetime

# Set chrome webdriver headless option
options = Options()
options.headless = True

def append_string_as_row(file_name, datetime_string, speed_string, units_string):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        speed_writer = csv.writer(write_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        # Add string params as last row in the csv file
        speed_writer.writerow([datetime_string, speed_string, units_string])

def measure_speed():
    driver = webdriver.Chrome(options=options)
    driver.get("https://fast.com")
    wait = WebDriverWait(driver, 60)

    try:
        speed_progress_indicator_circle_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".speed-progress-indicator.circle.succeeded"))
        )
        print("Successfully calculated speed")
    except:
        print("An exception occured loading speed calculation (Err:1)")

    speed_message_element = driver.find_element_by_id('your-speed-message')
    if speed_message_element.text == "Your Internet speed is":
        speed_value_element = driver.find_element_by_id("speed-value")
        speed_units_element = driver.find_element_by_id("speed-units")
        datetime_string = (datetime.datetime.now().strftime("%b %d %Y - %H:%M:%S"))
        speed_string = speed_value_element.text
        units_string = speed_units_element.text
        print(datetime_string + " " + speed_string + " " + units_string)
        append_string_as_row('speed_log.csv', datetime_string, speed_string, units_string)
    else:
        print("An error occured loading speed calculation (Err:2)")

    driver.close()

def loopthrough(value):
    while True:
        measure_speed()
        time.sleep(60 * value) # sleep for sys.argv[1] minutes

no_of_minutes = -1

try:
    no_of_minutes = float(sys.argv[1])
except Exception as e: 
    print("Error processing minute value")
    print("USAGE: python netspeed.py [minutes]")
    sys.exit(1)

if (no_of_minutes > 0):
    print("looping every " + str(no_of_minutes) + " minutes")
    loopthrough(no_of_minutes)
else:
    print("USAGE: python netspeed.py [minutes]\n[minutes] must be greater than 0")
