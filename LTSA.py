import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

op = webdriver.ChromeOptions()
op.add_argument('headless')
url = "https://my.lifetime.life/login.html"

def checkLoaded(driver:webdriver.Chrome):
    return driver.current_url != url

def logIn(driver:webdriver.Chrome, username, password):
    longInName = driver.find_element(By.ID, "account-username")
    longInName.send_keys(username)
    logInPassWord = driver.find_element(By.ID, "account-password")
    logInPassWord.send_keys(password)
    action = ActionChains(driver)
    submitButton = driver.find_element(By.ID, "login-btn")
    action.click(submitButton)
    action.perform()

def selectperson(driver:webdriver.Chrome, action:ActionChains, name:str):
    personList = driver.find_elements(By.CLASS_NAME, "form-group m-b-0")[1].find_elements(By.TAG_NAME, "label")
    person
    for p in personList:
        if p.get_dom_attribute("innerText") == name: person = p
    action.click(person)
    action.perform()

def selectSpot(driver:webdriver.Chrome, action:ActionChains, spotNumber:int):
    #NOTE: ONLY FOR JOHNNY KESTS CLASS
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="spotAvailable"]')), "CANT FIND BUTTON")
    spots = driver.find_elements(By.CSS_SELECTOR, '[data-testid="spotAvailable"]')
    chosenSpot = None
    position = f"{spotNumber}"
    for s in spots:
        if s.text == position: 
            chosenSpot = s
    
    if chosenSpot == None:
        chosenSpot = spots[0]

    action.click(chosenSpot)
    action.perform()

    time.sleep(3)

    tos = driver.find_element(By.CSS_SELECTOR, 'label[data-testid="acceptWaiver"]')
    action.click(tos)
    action.perform()

    finishButton = driver.find_element(By.CSS_SELECTOR, '[data-testid="finishBtn"]')
    action.click(finishButton)
    action.perform()


def main():
    #NOTE Replace time sleep with web driver wait
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    position = input("Enter Class position: ")
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    logIn(driver, username, password)
    WebDriverWait(driver, 10).until(checkLoaded, "NOT LOADED ;d or logged in")
    print(driver.current_url)

    action = ActionChains(driver)
    schedule = driver.find_element(By.PARTIAL_LINK_TEXT, "Schedules")
    action.click(schedule)
    action.perform()

    link = driver.find_element(By.LINK_TEXT,"Studio, Yoga & Indoor Cycle")
    action = ActionChains(driver)
    action.click(link)
    action.perform()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "button.btn.planner-date-btn.planner-date-btn-next")), "CANT FIND BUTTON")
    nextWeek = driver.find_element(By.CSS_SELECTOR, "button.btn.planner-date-btn.planner-date-btn-next")
    action.click(nextWeek)
    action.perform()

    time.sleep(1)
    #Select Day, heated flow
    flowDate = driver.find_elements(By.CLASS_NAME, "day")[2].find_elements(By.PARTIAL_LINK_TEXT, "FLOW (Heated)")[0]
    action.click(flowDate)
    action.perform()
    #Select person
    
    #Reserve Button
    time.sleep(3)
    reserveButton = driver.find_elements(By.CSS_SELECTOR, '[data-testid="reserveButton"]')[1]
    action.click(reserveButton)
    action.perform()

    selectSpot(driver, action, position)
    print("Reservation complete")
    time.sleep(6)
main()
