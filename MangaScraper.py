from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os



webPage = "https://manhuascan.com/manga-a-witchs-printing-office.html"



# Initialize Window
# Initialize Window Settings
WIDTH = 1920
HEIGHT = 2980
WINDOW_SIZE = str(WIDTH) + "," + str(HEIGHT)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
#Intialize Window
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

#Loading Web Page

print("Loading Web Page : " + webPage)
driver.get(webPage)
#driver.execute_script("document.body.style.zoom='zoom 80'") # Leaving this here as a comment just in case I need it later.
print("Web Page Loaded. Chapter List Loaded.")

items = driver.find_elements(By.XPATH, "//div[@id='list-chapters']/p/span/a")
# Make Directory with title
title = webPage.split("https://manhuascan.com/manga-", 1)[1].split(".html", 1)[0].replace("-", " ").title()
# Create manga directory if it doesn't exist
if not(os.path.exists(os.path.join("Manga", title))):
    os.mkdir(os.path.join("Manga", title))

chapter_List = []
for item in items:
    chapter_List.append(item.get_attribute('href'))
chapter_num = 32
for webPage in chapter_List:
    chapter_num -= 1
    # Use this if statement to rescan specific chapters.
    #if not (chapter_num == 1 or chapter_num == 4 or chapter_num == 6 or chapter_num == 12 or chapter_num == 13):
    #    continue
    chapter = webPage
    chapter = chapter.split("-chapter-", 1)[1].split(".html", 1)[0]
    # Create directory if it doesn't already exist.
    if not (os.path.join("Manga\\" + str(title), chapter)):
        os.mkdir(os.path.join("Manga\\" + str(title), chapter))
    # Load Chapter
    print("Loading Chapter : ", chapter, " at ", webPage)
    driver.get(webPage)
    # Scan chapter
    print("Scanning Chapter : ", chapter)
    # Ensures that all pages are scraped.
    found = True

    length = 1
    while (found):
        # Finds next image
        img = driver.find_elements(By.CLASS_NAME, "page" + str(length))
        # If there is no next image it leaves the loop
        if (len(img) == 0):
            found = False
            length -= 1
        else:
            if(img[1].size['width'] > WIDTH - 1000):
                driver.set_window_size(img[1].size['width'] + 1000, HEIGHT)
            if (img[1].size['height'] > HEIGHT - 1000):
                driver.set_window_size(WIDTH, img[1].size['height'] + 1000)
            # Scrolls to image, and then down a little so the navigation bar doesn't show
            driver.execute_script("arguments[0].scrollIntoView();", img[1])
            driver.execute_script("window.scrollBy(0,-100)")
            # Saves image
            with open(os.path.join("Manga\\" + str(title), chapter, 'page' + str(length) + '.png'), 'wb') as f:
                f.write(img[1].screenshot_as_png)
            # Increments length for next page
            length += 1

    print("Pages Scraped : " + str(length))

driver.quit()
