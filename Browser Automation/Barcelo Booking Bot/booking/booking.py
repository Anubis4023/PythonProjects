from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from booking.filter import BookingFilter
from datetime import datetime

from booking.report import BookingReport

import os
import time

#TODO: #8 make a filter class with filter functions and replace them in booking.py and refilter when a price for a hotel is retrieved in report.py

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r";C:\Users\pacow\Onedrive\Desktop\Selenium Drivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        os.environ['PATH'] += r";C:\Users\pacow\OneDrive\Desktop\Selenium Drivers"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(1) #Find element methods will wait x seconds
        self.maximize_window()

    def land_first_page(self):
        self.get("https://www.barcelo.com/en-us/hotels/")


        # time.sleep(10)
        # self.switch_to.window(self.driver.window_handles[0])
        # self.close()
        # self.switch_to.window(self.driver.window_handles[0])
        

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.teardown:
            #time.sleep(3)
            self.quit()    

    def report(self, adults, rooms):
        hotels = self.find_element(By.CSS_SELECTOR, 'div[class="result__list result__list-JS"]')
        results = BookingReport(self, hotels, adults, rooms)
        results.search()
        
    def apply_filters(self):
        filter = BookingFilter(driver=self)
        filter.accept_cookies()
        filter.sort_cheapest()
        filter.choose_location()
        filter.filter_brand()
        pass
    
    # #VOLARIS FUNCTIONS
    # def find_tickets(self, departDay, returnDay):
    #     #Open departure list to select departure location
    #     departLocation_element = self.find_element(By.CSS_SELECTOR, 'a[class="btnSearch radius-6"]')
    #     departLocation_element.click()
    #     #Type in location to depart from
    #     departLocation = self.find_element(By.ID, 'fnameOrigin')
    #     time.sleep(1) #Wait for location menu to pop up to input text
    #     locationText = "TIJ"
    #     departLocation.send_keys(locationText)
    #     #Select the target location from the list that results
    #     departList = self.find_elements(By.CSS_SELECTOR, 'li[class="row row-spec ng-star-inserted"]') #Get the list of possible locations after departure location is typed in
    #     for location in departList:
    #         if location.find_element(By.CSS_SELECTOR, 'div[class="col-2 right-align"]').get_attribute('innerHTML') == locationText:
    #             departure = location
    #             departure.click()
    #             break

    #     #Type in location to arrive to
    #     arriveLocation = self.find_element(By.ID, 'fnameDestination')
    #     locationText = "CUN"
    #     arriveLocation.send_keys(locationText)
    #     #Select the target location from the list that results
    #     #list_element = self.find_element(By.CSS_SELECTOR, 'ul[tabindex="1"]')
    #     arriveList = self.find_elements(By.CSS_SELECTOR, 'li[class="row row-spec ng-star-inserted"]') #Get the list of possible locations after departure location is typed in
    #     for location in arriveList:
    #         if location.find_element(By.CSS_SELECTOR, 'div[class="col-2 right-align"]').get_attribute('innerHTML') == locationText:
    #             arrival = location
    #             arrival.click()
    #             break

    #     #Select dates
    #     #TODO:For #10 testing, select weekday to weekday, weekday to weekend, weekend to weekday, weekend to weekend
        
    #     #firstDate = "24"
    #     #secondDate = "25"
    #     day1 = datetime(2022, 5, int(departDay))
    #     day2 = datetime(2022, 5, int(returnDay))
    #     if (day1.weekday() > 4): #Weekend
    #         #print("weekend")
    #         firstDate = 'td[class="weekend datecell-202205' + firstDate + ' customfare available"]'
    #     else: #Weekday
    #         #print("weekday")
    #         firstDate = 'td[class="datecell-202205' + firstDate + ' customfare available"]'

    #     if (day2.weekday() > 4): #Weekend
    #         secondDate = 'td[class="weekend datecell-202205' + secondDate + ' returnVisible returnCustomfare available"]'
    #     else: #Weekday
    #         secondDate = 'td[class="datecell-202205' + secondDate + ' returnVisible returnCustomfare available"]'
    #     time.sleep(3) #Giving time for calendar to load in
    #     try: #regular price
    #         departDate_element = self.find_element(By.CSS_SELECTOR, firstDate) 
    #     except Exception as e: #Low price, green text offer
    #         firstDate = firstDate.replace("customfare", "customLowFare")
    #         departDate_element = self.find_element(By.CSS_SELECTOR, firstDate)

    #     WebDriverWait(self, 5).until(EC.element_to_be_clickable(departDate_element)) #Let calendar load
    #     departDate_element.click()

    #     try: #regular price
    #         departDate_element = self.find_element(By.CSS_SELECTOR, secondDate)
    #     except: #Low price, green text offer
    #         firstDate = firstDate.replace("returnCustomfare", "returnCustomLowFare")
    #         departDate_element = self.find_element(By.CSS_SELECTOR, secondDate)
    #     WebDriverWait(self, 5).until(EC.element_to_be_clickable(departDate_element)) #Let calendar load 
    #     departDate_element.click()
    #     #Finalize the calendar selection
    #     done_button = self.find_element(By.CSS_SELECTOR, 'button[class="btn-calendar d-none d-md-block mat-flat-button mat-button-base mat-secondary"]')
    #     done_button.click()

    #     #Select number of adults
    #     passengerList_element = self.find_element(By.CSS_SELECTOR, 'mat-form-field[aria-label="Passengers"]') #Drop down list for passengers
    #     passengerList_element.click()
    #     minusButton = self.find_element(By.CSS_SELECTOR, 'button[class="quantity-left-minus enabled"]')
    #     while minusButton.is_enabled():
    #         minusButton.click()

    #     adults = 4 #replace this with user input later
    #     plusButton = self.find_element(By.CSS_SELECTOR, 'button[class="quantity-right-plus enabled"]')
    #     if adults > 9:
    #         print("Error: Cannot buy more than 9 adult tickets at a time")
    #         self.close()
    #         quit()
    #     for i in range(adults):
    #         plusButton.click()
    #     passengerList_element.click()
    #     #Click the 'search' button
    #     self.find_element(By.CSS_SELECTOR, 'button[class="btn btn-large col-12 search-btn mat-flat-button mat-button-base mat-primary"]').click()
        

    #     #NEXT SECTION: allow modifier to pick non-stop or if stops are allowed

    #     #Add filter to arrange the flights from cheapest to highest
    #     loading = True
    #     while loading:
    #         try:
    #             filterList_element = self.find_element(By.ID, 'mat-input-9')
    #             filterList_element.click()
    #             loading = False
    #         except:
    #             print("loading")
    #             loading = True

    #     filterList = filterList_element.find_element(By.CSS_SELECTOR, 'option[value="PriceLowToHigh"]')
    #     filterList.click()
    #     time.sleep(1) #Time to sort the flights
    #     Flights = [[], []]

    #     Flights[0] = self.pullFlightInfo()

    #     #Select the first option for flight so that the return flight list gets opened
    #     self.find_element(By.CSS_SELECTOR, 'a[class="panel-open ng-star-inserted"]').click()
    #     self.find_element(By.CSS_SELECTOR, 'mat-card[class="basic mat-card ng-star-inserted"]').click()
    #     time.sleep(5)
    #     Flights[1] = self.pullFlightInfo()

    #     print("Possible departures to Cancun: ")
    #     for flights in Flights[0]:
    #         flights.printDetails()

    #     print("Possible departures from Cancun: ")
    #     for flights in Flights[1]:
    #         flights.printDetails()

    # def pullFlightInfo(self):

    #     #Get a list that has all the flight elements
    #     flightsList_element = self.find_element(By.ID, 'Flightlists')
    #     flightsList = flightsList_element.find_elements(By.CSS_SELECTOR, 'div[class="flightItem ng-star-inserted"]')

    #     #Seperate the list to a list where stops are allowed and another where stops are not allowed
    #     NoStopsList = []
    #     StopsList = []
    #     flight:WebElement
    #     #time.sleep(5)
    #     self.implicitly_wait(0)
    #     for flight in flightsList:
    #         try:
    #             flight.find_element(By.CSS_SELECTOR, 'div[class="flightSegment stop-0"]') #Find out if this flight has stops
    #             #print("There are no stops on this flight")
    #             #Get the price of the departing flight
    #             price_text = flight.find_element(By.CSS_SELECTOR, 'span[class="price ng-star-inserted"]').get_attribute('innerHTML')
    #             price_textList = price_text.split('<', 1)
    #             price_text = price_textList[0]
    #             price_text = price_text.replace('$', '')
    #             price_text = price_text.strip()
    #             price = float(price_text)

    #             #Get the departure time of the flight
    #             depart = flight.find_element(By.CSS_SELECTOR, 'div[class="time timeDeparture"]').get_attribute('innerHTML')
    #             depart = depart.strip()

    #             #Get the arrival time of the flight
    #             arrival = flight.find_element(By.CSS_SELECTOR, 'div[class="time timeArrival"]').get_attribute('innerHTML')
    #             arrival = arrival.strip()

    #             #Get the total time it takes from departure to arrival
    #             total = flight.find_element(By.CSS_SELECTOR, 'div[class="flightDuration"]').get_attribute('innerHTML')
    #             total = total.strip()

    #             NoStopsList.append(Flight(depart, arrival, total, price))
    #             #print("got here")
    #         except NoSuchElementException:
    #             #print("There are stops on this flight")
    #             StopsList.append(flight)
    #     self.implicitly_wait(10)
    #     #print("Size of lsit: ", len(NoStopsList))
    #     return NoStopsList

        






        #COPY PASTE CODE FROM ABOVE: selection stuff for return flight
        #Get a list that has all the flight elements
        # flightsList_element = self.find_element(By.ID, 'Flightlists')
        # flightsList = flightsList_element.find_elements(By.CSS_SELECTOR, 'div[class="flightItem ng-star-inserted"]')

        #Seperate the list to a list where stops are allowed and another where stops are not allowed
        # NoStopsList2 = []
        # StopsList2 = []
        # flight:WebElement
        # self.implicitly_wait(0)
        # time.sleep(5) #Give the webpage time to load
        # #Redefine flightsList
        # flightsList_element = self.find_element(By.ID, 'Flightlists')
        # flightsList = flightsList_element.find_elements(By.CSS_SELECTOR, 'div[class="flightItem ng-star-inserted"]')
        # for flight in flightsList:
        #     try:
        #         flight.find_element(By.CSS_SELECTOR, 'div[class="flightSegment stop-0"]') #Find out if this flight has stops
        #         #print("There are no stops on this flight pt2")
        #         #Get the price of the departing flight
        #         price_text = flight.find_element(By.CSS_SELECTOR, 'span[class="price ng-star-inserted"]').get_attribute('innerHTML')
        #         price_textList = price_text.split('<', 1)
        #         price_text = price_textList[0]
        #         price_text = price_text.replace('$', '')
        #         price_text = price_text.strip()
        #         price = float(price_text)

        #         #Get the departure time of the flight
        #         depart = flight.find_element(By.CSS_SELECTOR, 'div[class="time timeDeparture"]').get_attribute('innerHTML')
        #         depart = depart.strip()

        #         #Get the arrival time of the flight
        #         arrival = flight.find_element(By.CSS_SELECTOR, 'div[class="time timeArrival"]').get_attribute('innerHTML')
        #         arrival = arrival.strip()

        #         #Get the total time it takes from departure to arrival
        #         total = flight.find_element(By.CSS_SELECTOR, 'div[class="flightDuration"]').get_attribute('innerHTML')
        #         total = total.strip()

        #         NoStopsList2.append(Flight(depart, arrival, total, price))
        #     except NoSuchElementException:
        #         #print("There are stops on this flight")
        #         StopsList2.append(flight)
        # self.implicitly_wait(1)





