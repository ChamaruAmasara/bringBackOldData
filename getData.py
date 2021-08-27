from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# time for webpage to load
timeout = 10


#Initializing Selenium
opt = Options()
#opt.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)



#Opening file to append the data
file=open("text.txt",'a')


#Initializing mysql and creating db
if None:
    import mysql.connector

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
    )

    mycursor = mydb.cursor()

    mycursor.execute("DROP DATABASE mydatabase")
    mycursor.execute("CREATE DATABASE mydatabase")

    mycursor.execute("CREATE TABLE blogdata (dateandtime VARCHAR(size), heading VARCHAR(size), content VARCHAR(size), imageurla VARCHAR(size))")




count=0
for number in range(1,7):
    page_url = "https://web.archive.org/web/20180705230325/http://www.moraspirit.com/home?page="+str(number)

    driver.get(page_url)

    # loading page
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.views-row-1'))
        WebDriverWait(driver, timeout).until(element_present)
        try:
            headings = driver.find_elements_by_xpath("""//*[@id="block-system-main"]/div/div/div/div/div/div/div/div/div/h5/a""")
            
            count=len(headings)+count
            print(count)
            contents=driver.find_elements_by_xpath("""/html/body/div[4]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div/div[text()]""")
#            contents2=driver.find_elements_by_xpath("""/html/body/div[4]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div[3]/div/div[3]/div/div/div[text]""")
#            for elem in range(0,len(contents)):
#                if contents2[elem].text!="":
#                    contents=contents+contents2
            
            images=driver.find_elements_by_xpath("""/html/body/div[4]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/a/img""")
            datestimes=driver.find_elements_by_xpath("""/html/body/div[4]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[2]/div/div""")
            if not(len(contents)==len(images)==len(datestimes)==len(datestimes)):
                print(len(contents),len(images),len(datestimes),len(datestimes))


                print("I'm really dead")

            print(contents[0])
            for elem in range(0,len(contents)):
                heading = headings[elem].text+"\n"
                content=contents[elem].text+"\n"
                content.replace("<p>","")
                content.replace("</p>","")
                image=images[elem].get_attribute("src")+"\n"
                datestime=datestimes[elem].text+"\n"
                file.writelines([datestime,heading,content,image])
                sql = "INSERT INTO blogdata VALUES (%s, %s,%s,%s)"
 #               val = (datestime,heading,content,image)
#                mycursor.execute(sql, val)

        except:
            print("dead")
            pass
    except TimeoutException:
        print("Timed out while waiting for page to load")
    print("page",number,"checked.")
    
#mydb.commit()
file.close()
driver.close()
