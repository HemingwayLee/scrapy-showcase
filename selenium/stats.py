import time
import json
import traceback
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import hashlib


# def _translate(lemma, words):
#     links = []
#     nodes = [{"name": lemma, "color": "red", "type": "url"}]
#     idx = 1
#     for ws in words:
#         currIdx = idx

#         nodes.append({"name": ws["synset"], "color": "blue", "type": "synset"})
#         links.append({"source": 0, "target": idx, "weight": 1})
#         newWords = wrapper.getSenseWithWord(ws["synset"], lemma)
#         idx = idx + 1
#         for nws in newWords:
#             nodes.append({"name": nws["lemma"], "color": "red", "type": "word"})
#             links.append({"source": currIdx, "target": idx, "weight": 1})
#             idx = idx + 1
    
#     res = { "nodes": nodes, "links": links }
#     print(res)
#     return res

def get_md5(key):
    return hashlib.md5(key.encode()).hexdigest()

def get_all_clickable_tags(driver):
    div = driver.find_elements_by_css_selector("div[onclick]")
    a = driver.find_elements_by_css_selector('a[href]')
    btn = driver.find_elements_by_css_selector("button[onclick]")
    return div + a + btn

def write2file(driver, foldername):
    content = driver.page_source
    filename = get_md5(driver.current_url)
    path = f'{foldername}/{filename}.html'

    with open(path, 'w') as fp:
        fp.write(content)

    return path

def do_dfs(driver, visited, parentUrl, nodes, links, nodeDict, clickedTagKey, foldername):
    time.sleep(7)

    print(f"\n\nfrom: {parentUrl}")
    print(f"dfs: {driver.current_url}\n")
    if driver.current_url not in visited:
        visited.add(driver.current_url)
        path = write2file(driver, foldername)
        nodes.append({"name": driver.title, "path": path, "url": driver.current_url, "color": "red", "type": "url"})
        nodeDict[driver.current_url] = len(nodeDict)

        tags = get_all_clickable_tags(driver)
        print(tags)
        for i in range(len(tags)):
            try:
                print(f"i: {i} of {len(tags)}")
                print(f"try {tags[i].tag_name}")

                tagIdx = len(nodeDict)
                tagKey = get_md5(driver.current_url) + str(i)
                nodes.append({"name": tagKey, "color": "blue", "type": tags[i].tag_name, "url": driver.current_url, "i": i})
                links.append({"source": nodeDict[driver.current_url], "target": tagIdx, "weight": 1})
                nodeDict[tagKey] = tagIdx

                tmp = driver.current_url
                tags[i].click()

                doesSamePage = do_dfs(driver, visited, tmp, nodes, links, nodeDict, tagKey, foldername)
                if not doesSamePage:
                    driver.back()
                    time.sleep(7)
                    print(f"back to {driver.current_url}")

                tags = get_all_clickable_tags(driver)
                print(f" new tag length: {i} of {len(tags)}")

            except ElementNotVisibleException:
                print("tag is not visible, skip")
                continue
            except StaleElementReferenceException:
                print("tag is a stale element, skip")
                continue
    else:
        print(f"{driver.current_url} visited, skip...")

    if clickedTagKey is not None:
        links.append({"source": nodeDict[driver.current_url], "target": nodeDict[clickedTagKey], "weight": 1})
    
    if driver.current_url == parentUrl:
        print("end, it is same url")
        return True
    else:
        print("end, it is different url")
        return False

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options) 
    
    return driver

def create_folder():
    now = datetime.now()
    dtString = now.strftime("%Y-%m-%d-%H-%M-%S")
    foldername = f"./pages/{dtString}"
    os.mkdir(foldername)

    return foldername

try:
    url = "http://ec2-54-238-101-61.ap-northeast-1.compute.amazonaws.com/"
    visited = set()
    links = []
    nodes = []
    parentUrl = None
    nodeDict = {}
    clickedTagKey = None

    foldername = create_folder()

    driver = get_driver()
    driver.get(url)
    do_dfs(driver, visited, parentUrl, nodes, links, nodeDict, clickedTagKey, foldername)   

    print(nodes)
    print(links)
    res = { "nodes": nodes, "links": links }

    with open('data.json', 'w') as fp:
        json.dump(res, fp)
except:
    print(traceback.format_exc())

driver.quit()

