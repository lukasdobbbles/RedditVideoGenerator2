from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from sys import platform
import os
import time

class YouTubeUploader():
  def __init__(self, filePath, title, description, tags, userDataDir) -> None:
    self.filePath = os.path.abspath(filePath)
    self.title = title
    self.description = description
    self.tags = tags
    self.userDataDir = userDataDir
    pass

  def __setup_method(self):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=" + self.userDataDir)

    self.driver = webdriver.Chrome(options=options)
    self.wait = WebDriverWait(self.driver, 10)
    self.vars = {}
  
  def __teardown_method(self):
    self.driver.quit()
  
  def upload(self):
    self.__setup_method()
    
    self.driver.get("https://studio.youtube.com/channel/UCwkHnpBcQ_5_zZUcx2efLOQ")

    # click "create" button
    self.driver.find_element(By.XPATH, "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-button/div").click()
    time.sleep(1)
    # click "upload videos" button
    self.driver.find_element(By.XPATH, "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string").click()
    time.sleep(1)

    file_input = self.driver.find_element(By.CSS_SELECTOR, "#content > input[type=file]")
    file_input.send_keys(self.filePath)
    time.sleep(1)

    title_input = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div")))
    title_input.click()
    time.sleep(1)
    
    # remove any default title
    if platform == "darwin":
      title_input.send_keys(Keys.COMMAND, "a")
    else:
      title_input.send_keys(Keys.CONTROL, "a") 
    title_input.send_keys(self.title) 

    description_input = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div")))
    description_input.click()
    description_input.send_keys(self.description)  
    time.sleep(1)

    # click not made for kids
    self.driver.find_element(By.CSS_SELECTOR, ".ytkc-made-for-kids-select:nth-child(2) > #radioLabel > .style-scope").click()
    time.sleep(1)

    # click "SHOW MORE"
    self.driver.find_element(By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button").click()
    time.sleep(1)
    
    tags_input = self.driver.find_element(By.CSS_SELECTOR, "#text-input")
    ActionChains(self.driver).move_to_element(tags_input).perform()
    tags_input.click()
    for tag in self.tags:
      tags_input.send_keys(tag)
      tags_input.send_keys(",")
    time.sleep(1)

    self.driver.find_element(By.CSS_SELECTOR, "#next-button").click()
    self.driver.find_element(By.CSS_SELECTOR, "#next-button").click()
    self.driver.find_element(By.CSS_SELECTOR, "#next-button").click()
    # make video public
    make_video_public_button = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[2]")))
    make_video_public_button.click()
    self.driver.find_element(By.CSS_SELECTOR, "#done-button").click()
    time.sleep(1)

    upload_progress = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="dialog"]/div[2]/div/ytcp-video-upload-progress/span')))
    while not upload_progress.text.startswith("Upload complete"):
      print(upload_progress.text)
    self.driver.find_element(By.CSS_SELECTOR, "#close-button").click()
    self.__teardown_method()
