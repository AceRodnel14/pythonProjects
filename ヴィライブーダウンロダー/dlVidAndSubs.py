# 02-03-2021
from selenium import webdriver
import os
import sys
import time

website = "website link"

with open(str(sys.argv[1])) as oFile:
    lnkList = [line.rstrip() for line in oFile]
    
for lnkElem in lnkList:
    driver = webdriver.Chrome (executable_path="./chromedriver")
    driver.get(str(lnkElem))
    vliveLnk = driver.find_element_by_xpath("//meta[@name='twitter:url']").get_attribute("content")
    driver.get(website)
    urlBox = driver.find_element_by_id("vlive_url")
    urlBox.send_keys(str(vliveLnk))
    vliveBtn = driver.find_element_by_id("vlive_find_submit")
    vliveBtn.click()
    vidTitle = driver.find_element_by_name("twitter:title")
    vidTitle = str(vidTitle.get_attribute("content"))
    pubDate = str(driver.find_element_by_class_name("onair").text)
    
    infoFile = open('info.txt', 'a')
    infoFile.write("Source: " + vidTitle + "\n\n")
    infoFile.write("Title: " + vidTitle + "\n")
    infoFile.write("Uploaded on: " + pubDate + "\n")

    hrefs=driver.find_elements_by_tag_name("a")
    links = []
    subInfo = []
    for lnk in hrefs:
        links.append(str(lnk.get_attribute("href")))
        subInfo.append(str(lnk.get_attribute("onclick")))

    index = [links.index(i) for i in links if "res=" in i]
    vidId = str(links[int(index[0])]).split("/")[-2]
    infoFile.write("File Name: " + vidId + ".mp4\n")
    reso = str(links[int(index[0])]).split("?")[-1].split("=")[-1]
    infoFile.write("Resolution: " + reso + "\n")
    
    vidLink = str(links[int(index[0])+1])
    os.system("wget -O " + vidId + ".mp4 " + vidLink) 

    subIndex = [subInfo.index(i) for i in subInfo if "subtitles-srt-" in i]
    for subs in subIndex:
        lang = subInfo[subs].split('"')[1].split("-")[-1]
        subLink = str(links[subs])
        if lang == "English":
            os.system("wget -O " + vidId + "." + lang + ".srt " + subLink)
            #time.sleep(30)

    dirName = pubDate[:10] + "_" + vidId
    os.system("mkdir -p " + dirName)
    os.system("mv info.txt " + dirName)
    os.system("mv " + vidId + ".* " + dirName)
    driver.close()
    time.sleep(60)










