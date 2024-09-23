from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import eel

def Driver():
    cd_path = 'utilities/chromedriver.exe'
    crx_path = 'utilities/ublock.crx'
    blocker_path = 'utilities/blocker.crx'

    options = webdriver.ChromeOptions()

    options.add_extension(crx_path)
    options.add_argument('--start-maximized')
    options.add_argument('--headless=new')
    options.add_experimental_option('excludeSwitches', ['enable-automation']) 

    service = Service(cd_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@eel.expose
def get_Ind_Movie_quality_links(movie_name):
    driver = Driver()

    try:
        driver.get('https://topmovies.dad/')
        print('Navigated to website')
        eel.Wait_Text('Sending request..')

        search_box = driver.find_element(By.ID, 's')
        search_box.send_keys(movie_name, Keys.RETURN)
        print('Searched for movie')
        eel.Wait_Text('Searching for movie..')

        movie_page_element = driver.find_element(By.CLASS_NAME, 'post-cards')
        movie_page = movie_page_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if movie_page:
            driver.get(movie_page)

        print('Navigated to movie page')
        eel.Wait_Text('Generating Movie Meta Data..')
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, 1000)")
        temp_element = driver.find_element(By.CLASS_NAME, 'thecontent')

        elements = temp_element.find_elements(By.TAG_NAME, 'h3')
        quality_names = elements[2:]

        quality_names_list = []
        for element in quality_names:
            quality_names_list.append(element.text)
        eel.Wait_Text('Generating Quality-Options..')

        quality_links = []
        elements = temp_element.find_elements(By.CLASS_NAME, 'maxbutton-download-links')
        for element in elements:
            quality_links.append(element.get_attribute("href"))

        Final_Items = {}
        eel.Wait_Text('Fetching Quality-Links..')

        for i in range(len(quality_names_list)):
            Final_Items[quality_names_list[i]] = quality_links[i]

        return(Final_Items)

    finally:
        driver.quit()

@eel.expose
def get_Ind_Series_quality_links(movie_name,season_no):
    driver = Driver()

    try:
        driver.get('https://topmovies.dad/')
        print('Navigated to website')
        eel.Wait_Text('Sending request..')

        search_box = driver.find_element(By.ID, 's')
        search_box.send_keys(movie_name, Keys.RETURN)
        print('Searched for movie')
        eel.Wait_Text('Searching for movie..')

        movie_page_elements = driver.find_elements(By.CLASS_NAME, 'post-image')

        series_dict = {}
        for element in movie_page_elements:
            series_dict[element.get_attribute("title")] = element.get_attribute("href")
        
        #--------------------AI PART--------------

        link = Name_Checker(movie_name,series_dict,season_no)

        #--------------------AI PART--------------

        driver.get(link)
        print('Navigated to movie page')
        eel.Wait_Text('Generating Movie Meta Data..')
        time.sleep(3)

        temp_element = driver.find_element(By.CLASS_NAME, 'thecontent')

        elements = temp_element.find_elements(By.TAG_NAME, 'h3')
        quality_names = elements[2:]

        quality_names_list = []
        for element in quality_names:
            if ( f"Season {season_no}" in element.text):
                quality_names_list.append(element.text)

        eel.Wait_Text('Generating Quality-Options..')

        quality_links = []
        elements = temp_element.find_elements(By.CLASS_NAME, 'maxbutton-batch-zip')
        for element in elements:
            quality_links.append(element.get_attribute("href"))
        eel.Wait_Text('Fetching Quality-Links..')

        Final_Items = {}

        for i in range(len(quality_names_list)):
            Final_Items[quality_names_list[i]] = quality_links[i]

        return(Final_Items)

    finally:
        driver.quit()

@eel.expose
def get_NonInd_Movie_quality_links(movie_name):
    driver = Driver()

    try:
        driver.get('https://moviesmod.space/')
        print('Navigated to website')
        eel.Wait_Text('Sending request..')

        time.sleep(3)
        search_box = driver.find_element(By.ID, 's')
        search_box.send_keys(movie_name, Keys.RETURN)
        print('Searched for movie')
        eel.Wait_Text('Searching for movie..')

        movie_page_element = driver.find_element(By.TAG_NAME, 'article')
        movie_page = movie_page_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if movie_page:
            driver.get(movie_page)

        print('Navigated to movie page')
        eel.Wait_Text('Generating Movie Meta Data..')
        time.sleep(3)

        driver.execute_script('window.scrollBy(0, 1650);')
        driver.find_element(By.TAG_NAME, 'h4').click()

        # time.sleep(3)
        elements = driver.find_elements(By.TAG_NAME, 'a')

        quality_links = []
        for element in elements:
            if(element.text == "Download Links"):
                quality_links.append(element.get_attribute('href'))
        print('Got quality links')
        eel.Wait_Text("Generating Quality-Options..")

        quality_names = []
        elements = driver.find_elements(By.TAG_NAME, 'h4')

        for element in elements[1:-2]:
            quality_names.append(element.text)
        print("Got quality names")

        Final_Items = {}
        eel.Wait_Text("Fetching Quality-Links..")

        for i in range(len(quality_names)):
            Final_Items[quality_names[i]] = quality_links[i]

        return(Final_Items)

    finally:
        driver.quit()

@eel.expose
def get_NonInd_Series_quality_links(movie_name,season_no):

    driver = Driver()

    try:
        name = movie_name.replace(' ', '+')
        driver.get('https://moviesmod.space/')
        print('Navigated to website')

        search_box = driver.find_element(By.ID, 's')
        search_box.send_keys(movie_name, Keys.RETURN)
        print('Searched for movie')

        movie_page_elements = driver.find_elements(By.TAG_NAME, 'article')

        # for element in movie_page_elements:
        #     print("-----")
        #     print(element.text)
        #     print("-----")

        driver.get(movie_page_elements[0].find_element(By.TAG_NAME, 'a').get_attribute('href'))
        print('Navigated to movie page')


        driver.execute_script('window.scrollBy(0, 1650);')
        driver.find_element(By.TAG_NAME, 'h3').click()

        time.sleep(3)
        elements = driver.find_elements(By.TAG_NAME, 'a')
        quality_links = []
        for element in elements:
            if((element.text)=="Batch/Zip File"):
                quality_links.append(element.get_attribute('href'))

        print('Got quality links') 

        quality_names = []
        elements = driver.find_elements(By.TAG_NAME, 'h3')
        for element in elements[4:-3]:
            quality_names.append(element.text)
        print("Got quality names")

        Final_Items = {}
        for i in range(len(quality_names)):
            Final_Items[quality_names[i]] = quality_links[i]

        return(Final_Items)

    finally:
        driver.quit()

@eel.expose
def Download_link(link):
    driver = Driver()

    try:
        driver.get(link)
        time.sleep(4)
        link = ""
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            if element.get_attribute("href").startswith("https://tech.unblockedgames.world/"):
                link = element.get_attribute("href")
                break
        
        eel.Wait_Text_final('Configuring Driver...')

        driver.get(link)
        time.sleep(13)
        driver.find_element(By.TAG_NAME, 'H5').click()

        eel.Wait_Text_final('Fetching Link...')

        time.sleep(1)
        driver.find_element(By.ID, 'verify_button2').click()
        time.sleep(11)

        eel.Wait_Text_final('Verifying the Link...')

        driver.find_element(By.ID,'verify_button').click()
        time.sleep(9)

        eel.Wait_Text_final('Chechking the Security...')

        driver.find_element(By.ID,'two_steps_btn').click()
        time.sleep(7)
        
        links = driver.find_elements(By.TAG_NAME, 'a')
        return (links[6].get_attribute('href'))

    finally:
        driver.quit()

def Name_Checker(name,Dict,season):
    
    temp_name = name.split(" ")
    for i in Dict:
        s_name = i.split(" ")

        if s_name[1].endswith(":"):
            s_name[1] = s_name[1][:-1]
        
        if len(temp_name) == 1:
            if temp_name[0] in s_name:

                if "(Season 1-" in i:
                    temp = i[i.index("Season")+9]
                    if int(temp) >= int(season):
                        return(Dict[i])
                        break
                        
                
                elif ("(Season "+str(season)+")" in i):
                        return(Dict[i])

                        break
        else:
            var = True
            for j in temp_name:
                if j in s_name:
                    var = True
                else:
                    var = False
                    break
            if var == True:
                if "(Season 1-" in i:
                    temp = i[i.index("Season")+9]
                    if int(temp) >= int(season):
                        return(Dict[i])
                        break
                elif ("(Season "+str(season)+")" in i):
                    
                    return(Dict[i])
                    break

