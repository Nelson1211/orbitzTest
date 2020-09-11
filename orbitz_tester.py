from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

browser = None
base_link = 'https://www.orbitz.com/'

def initialise():
    global browser
    chrome_driver = os.getcwd() + '/chromedriver'
    browser = webdriver.Chrome(chrome_driver)
    browser.maximize_window()

def execute_flight_search():
    global browser
    browser.get(base_link)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tab-flight-tab-hp"]')))
    browser.find_element_by_xpath('//*[@id="tab-flight-tab-hp"]').click()
    source = browser.find_element_by_xpath('//*[@id="flight-origin-hp-flight"]')
    source.send_keys('PHX')
    destination = browser.find_element_by_xpath('//*[@id="flight-destination-hp-flight"]')
    destination.send_keys('EWR')
    departure = browser.find_element_by_xpath('//*[@id="flight-departing-hp-flight"]')
    departure.send_keys('10/29/2020')
    returning = browser.find_element_by_xpath('//*[@id="flight-returning-hp-flight"]')
    for i in range(10):
        returning.send_keys(Keys.BACKSPACE)
    returning.send_keys('11/03/2020')
    returning.send_keys(Keys.RETURN)
    
    # Source and Destination Test
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'secondary-content no-wrap')]")))
    paths = browser.find_elements_by_xpath("//div[contains(@class,'secondary-content no-wrap')]")
    for path in paths:
        temp = path.text.strip().split('\n')
        if len(temp) == 1:
            if len(temp[0].split('-')) == 3:
                assert temp[0].split('-')[0].strip() == 'PHX' and temp[0].split('-')[2].strip() == 'EWR'
            elif len(temp[0].split('-')) == 2:
                assert temp[0].split('-')[0].strip() == 'PHX' and temp[0].split('-')[1].strip() == 'EWR'
        elif len(temp) == 2:
            if len(temp[1].split('-')) == 3:
                assert temp[1].split('-')[0].strip() == 'PHX' and temp[1].split('-')[2].strip() == 'EWR'
            elif len(temp[1].split('-')) == 2:
                assert temp[1].split('-')[0].strip() == 'PHX' and temp[1].split('-')[1].strip() == 'EWR'

    # Number of stops Test
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'Nonstop-stop-flights-checkbox')]")))
    nonstop = browser.find_element_by_xpath("//span[contains(@id,'Nonstop-stop-flights-checkbox')]")
    nonstop.find_element_by_xpath("..").click()
    try:
        browser.switch_to.window(browser.window_handles[1])
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except:
        pass
    time.sleep(2)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@class,'number-stops')]")))
    stops = browser.find_elements_by_xpath("//span[contains(@class,'number-stops')]")
    for stop in stops:
        assert stop.text.strip() == '(Nonstop)'
    nonstop.find_element_by_xpath("..").click()
    
    # Airline Test
    target_airline = browser.find_element_by_xpath("//input[contains(@id,'airlineRowContainer')]")
    target_airline.find_element_by_xpath("..").click()
    target_airline = target_airline.find_element_by_xpath("..").find_element_by_xpath('.//span').text.split()
    index = target_airline.index('flights')
    target = ''
    for i in range(1, index):
        target += target_airline[i] + ' '
    target = target.strip()
    time.sleep(2)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@class,'number-stops')]")))
    airlines = browser.find_elements_by_xpath("//span[contains(@data-test-id,'airline-name')]")
    for airline in airlines:
        assert airline.text.strip() == target

    browser.quit()

def main():
    initialise()
    execute_flight_search()

if __name__ == '__main__':
    main()
