from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
screenshotDir = "Screenshots"
userDataDir = "C:\\Users\\lukas\\AppData\\Local\\Google\\Chrome\\User Data"

def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, By.ID, f"t3_{script.url.split('/')[6]}")
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, By.ID, f"t1_{commentFrame.commentId}")
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, method, handle):
    search = wait.until(EC.presence_of_element_located((method, handle)))
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def __setupDriver(url: str):
    options = webdriver.ChromeOptions()
    options.headless = False
    options.enable_mobile = False
    options.add_argument("user-data-dir=" + userDataDir)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    driver.maximize_window()
    driver.get(url)

    return driver, wait