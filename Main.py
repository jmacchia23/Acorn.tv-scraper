import time
from selenium.webdriver import Chrome
from selenium import webdriver
import random
import pandas as pd

urls = []
titles = []
nepisodes = []
nseasons = []
tipes = []
descriptions = []
trailers = []
images = []
totaldescription = []

#configure webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)

#Get all films url
driver.get('https://acorn.tv/')
time.sleep(random.randint(5,7))
driver.find_element_by_link_text("ver todo").click()
time.sleep(random.randint(1,5))
driver.find_element_by_xpath('.//a[@href="/browse/all/"]').click()
library = driver.find_elements_by_xpath('//div[@class="col-sm-6 col-md-6 col-lg-3"]')
for film in library:        
        urls.append(film.find_element_by_xpath('.//a[@itemprop="url"]').get_attribute('href'))

#Get all films data               
for link in urls:
        driver.get(link)
        time.sleep(random.randint(5,7))
        data = driver.find_elements_by_xpath('//div[@class="secondary-bg"]')
        
        titles.append(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/h4/span[2]').text)
        nepisodes.append(driver.find_element_by_xpath('.//meta[@itemprop="numberOfEpisodes"]').get_attribute('content'))
        nseasons.append(driver.find_element_by_xpath('.//meta[@itemprop="numberOfSeasons"]').get_attribute('content'))

        if nepisodes[-1] == '1' and nseasons[-1] == '1':
                tipes.append('Movie')
        else:
                tipes.append('Series')

        descriptions.append(driver.find_element_by_xpath('.//p[@itemprop="description"]').text)
        trailers.append(driver.find_element_by_xpath('.//a[@class="inline"]').get_attribute('href'))
        seasons = driver.find_elements_by_xpath('.//div[class="container episode"]')    
        images.append(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[1]/img').get_attribute('src'))

        ep = driver.find_elements_by_xpath('.//a[@itemprop="url"]')
        ep = [x.get_attribute('href') for x in ep]
        
        epdesc=[]
        '''
        cast = []
        rating = []
        '''
        #get all episodes data
        for x in ep:
                driver.get(x)
                time.sleep(random.randint(3,4))
                try:
                        epdesc.append(driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/p').text)
                except:
                        epdesc.append('description no available')
                
                ''' Comentado por la baja cantidad de ep que contienen estos datos.
                try:
                        rating.append(driver.find_element_by_xpath('rating/html/body/div[3]/div[1]/div[2]/div[2]'))
                except:
                        rating.append('')

                try:
                        cast.append(driver.find_elements_by_xpath('span[@itemprop="name"]'))
                except:
                        cast.append('')
                '''
        totaldescription.append(epdesc)
        serie = pd.DataFrame({'Link Episode': ep,'Description': epdesc})
        titulo = titles[-1]
        
        #export ep data
        serie.to_csv(titulo.replace(':','')+'.csv', index = False)

#export library list data
df = pd.DataFrame({'Title': titles,'Url': urls,'Trailer': trailers, 'Description': descriptions,\
        'Tipe': tipes, 'Seasons': nseasons, 'Episodes': nepisodes, 'Image URL': images})

df.to_csv('testAaccorn.csv', index = False)

driver.quit()