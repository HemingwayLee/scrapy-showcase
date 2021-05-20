import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException

def get_all_clickable_tags(driver, visited):
    time.sleep(7)

    print(driver.current_url)
    if driver.current_url not in visited:
        visited.add(driver.current_url)

        # for btn in driver.find_elements_by_tag_name('button'):
        #     print(f"try {btn.tag_name}")
        #     btn.click()
        #     get_all_clickable_tags(driver, visited)
        #     driver.back()

        # for a in driver.find_elements_by_css_selector('a[href]'):
        #     print(f"try {a.tag_name}")
        #     a.click()
        #     get_all_clickable_tags(driver, visited)
        #     driver.back()
        
        divs = driver.find_elements_by_css_selector("div[onclick]")
        for i in range(len(divs)):
            try:
                print(f"try {divs[i].tag_name}")
                divs[i].click()
                get_all_clickable_tags(driver, visited)
                driver.back()
                divs = driver.find_elements_by_css_selector("div[onclick]")
            except ElementNotVisibleException:
                print("tag is not visible, skip")
                continue
            except StaleElementReferenceException:
                print("tag is a stale element, skip")
                continue
    else:
        print(f"{driver.current_url} visited, skip...")



try:
    urls = [ "http://ec2-54-238-101-61.ap-northeast-1.compute.amazonaws.com/" ]
    visited = set()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options) 
    
    driver.get(urls[0])
    get_all_clickable_tags(driver, visited)   

    print("!!!!!!DONE!!!!!")
    print(visited)
except:
    print(traceback.format_exc())

driver.quit()

