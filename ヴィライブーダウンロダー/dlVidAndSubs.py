# 03-07-2021
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import time

website = "website link"
options = Options()
options.add_argument('--headless')
for fileNo in range(1, len(sys.argv)):
    
    print("===============================================================================")
    print("Created folder for videos under " + str(sys.argv[fileNo]))
    print("===============================================================================\n\n")
    os.system("mkdir -p " + str(sys.argv[fileNo])[0:6])
    
    with open(str(sys.argv[fileNo])) as oFile:
        lnkList = [line.rstrip() for line in oFile]
    
    for curr, lnkElem in enumerate(lnkList):
        print("===============================================================================")
        print("Idle for 1 minute. Please wait...")
        print("===============================================================================\n\n")
        time.sleep(60)
        driver = webdriver.Chrome(executable_path="./chromedriver", options=options
        driver.get(str(lnkElem))
        vliveLnk = driver.find_element_by_xpath("//meta[@name='twitter:url']").get_attribute("content")
        driver.get(website)
        urlBox = driver.find_element_by_id("vlive_url")
        urlBox.send_keys(str(vliveLnk))
        vliveBtn = driver.find_element_by_id("vlive_find_submit")
        vliveBtn.click()
        if driver.find_elements_by_name("twitter:title"):
            vidTitle = driver.find_element_by_name("twitter:title")
            vidTitle = str(vidTitle.get_attribute("content"))
            pubDate = str(driver.find_element_by_class_name("onair").text)
    
            infoFile = open('info.txt', 'a')
            infoFile.write("Source: " + vliveLnk + "\n\n")
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
        
            lnkIndex = curr + 1
            print("video # " + str(lnkIndex) + " out of " + str(len(lnkList)) + " from file " + str(sys.argv[fileNo]))
            print("saving " + vidId + ".mp4...")
            os.system('echo "=====' + vliveLnk + '=====" > logs.info')
        
            vidLink = str(links[int(index[0])+1])
            os.system("wget -O " + vidId + ".mp4 " + vidLink + " -a logs.info") 

            subIndex = [subInfo.index(i) for i in subInfo if "subtitles-srt-" in i]
            for subs in subIndex:
                lang = subInfo[subs].split('"')[1].split("-")[-1]
                subLink = str(links[subs])
                if lang == "English":
                    print("Found English subs. Downloading now...")
                    os.system("wget -O " + vidId + "." + lang + ".srt " + subLink + " -a logs.info")
            infoFile.close()
            dirName = pubDate[:10] + "_" + vidId
            os.system("mkdir -p " + dirName)
            os.system("mv info.txt " + dirName)
            os.system("mv " + vidId + ".* " + dirName)
        else:
            print("Video cannot be downloaded")
            errorFile = open('error.txt', 'a')
            errorFile.write(vliveLnk + "\n")
            errorFile.close()

        driver.close()
        driver.quit()
        print("\n")


    print("===============================================================================")
    print("Moved files inside " + str(sys.argv[fileNo])[0:6] + " folder")
    print("===============================================================================\n\n")
    os.system("mv " + str(sys.argv[fileNo])[2:6] + "* " + str(sys.argv[fileNo])[0:6])
