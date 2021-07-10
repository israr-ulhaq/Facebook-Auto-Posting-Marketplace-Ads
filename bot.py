from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import tkinter as tk
import keyboard

chrome_options = webdriver.ChromeOptions() 
prefs = {"profile.default_content_setting_values.notifications" : 2} 
chrome_options.add_experimental_option("prefs",prefs) 

# i have added chromium webdriver to PATH enviornment variable
driver = webdriver.Chrome(chrome_options=chrome_options)

driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'C:\Users\israr\Desktop\chromedriver.exe')

driver.maximize_window()
def startPostingAds():

    adsList = getAdsData()

    for adData in adsList:
        try:
            createItemPage = 'https://www.facebook.com/marketplace/create/item'
            driver.get(createItemPage)
            time.sleep(3)

            # uploading images

            photo = driver.find_element_by_xpath("//*[@aria-label='Add Photos']")
            photo.click()
            time.sleep(3)
            keyboard.write(adData['image'])
            keyboard.press('enter')

            # enter title

            title = driver.find_element_by_xpath("//*[@aria-label='Title']")
            title.send_keys(adData['title'])

            # enter price

            price = driver.find_element_by_xpath("//*[@aria-label='Price']")
            price.send_keys(adData['price'])

            # Select category .i.e Mobile

            category = driver.find_element_by_xpath("//*[@aria-label='Category']")
            category.click()
            for i in range(16):
                keyboard.press('tab')
                time.sleep(1)
            keyboard.press('enter')

            # select condition of mobile
            condition = driver.find_element_by_xpath("//*[@aria-label='Condition']")
            condition.click()
            sleep(1)
            pressTabAndThenDownArrowUntil(int(adData['condition']))

        # select device model 
            if (int(adData['model']))==0:
                pass
            else:
                model = driver.find_element_by_xpath("//*[@aria-label='Device name']")
                model.click()
                sleep(1)
                pressTabAndThenDownArrowUntil(int(adData['model']))

            # enter description
            description = driver.find_element_by_xpath("//*[@aria-label='Description']")
            description.send_keys(adData['description'])
            sleep(3)

            # enter location
            location = driver.find_element_by_xpath("//*[@aria-label='Location']")
            location.send_keys(adData['location'])
            time.sleep(3)
            keyboard.press('down')
            keyboard.press('enter')

            # # go to next page
            nextPageButton = driver.find_element_by_xpath("//*[@aria-label='Next']")
            nextPageButton.click()
            time.sleep(5)

            ##groups
            grp = driver.find_element_by_css_selector(".obtkqiv7 .bi6gxh9e:nth-of-type(1) .a8nywdso.bp9cbjyn")
            grp.click()
            sleep(3)

            # publish ad
            # try:
            #     publishButton = driver.find_element_by_xpath("//*[@aria-label='Publish']")
            #     publishButton.click()
            #     time.sleep(3)
            #     print(adData['title'] + " was uploaded successfully!!")
            # except:
            try:
                publishButton=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.buofh1pr.rj1gh0hx > div[role="button"]')))
                publishButton.click()
                time.sleep(5)
                print(adData['title']+ "was uploaded successfully!!")
            except:
                publishButton=driver.find_element_by_xpath("//*[@aria-label='Publish']")
                publishButton.click()
                time.sleep(3)
                print("Except succefullly")
        except:
            print(" was NOT uploaded successfully due to followig exception")
            driver.quit()
    driver.quit()            	

def pressTabAndThenDownArrowUntil(counter):
    for i in range(1, counter + 1):
        if(i == 1):
            keyboard.press('tab')
        else:
            keyboard.press('down')
        time.sleep(1)
    keyboard.press('enter')

def getAdsData():
    'Reading csv file'
    import csv
    with open ('ads.csv') as f:
        data = csv.DictReader(f)
        return (list(data))

def submit():
    name=name_entry.get()
    password=passw_var.get()

    name_var.set("")
    passw_var.set("")
    # root.quit()
    root.destroy()
    driver.get('https://www.facebook.com')
    emailelement = driver.find_element_by_id('email')
    emailelement.send_keys(name)
    passelement = driver.find_element_by_id('pass')
    passelement.send_keys(password)
    loginelement = driver.find_element_by_xpath("//button[@name='login']")
    loginelement.click()
    sleep(10)
    startPostingAds()
if __name__ == '__main__':
    root=tk.Tk()

    # setting the windows size
    root.geometry("800x400")

    # declaring string variable
    # for storing name and password
    name_var=tk.StringVar()
    passw_var=tk.StringVar()
  
    # creating a label for
    # name using widget Label
    name_label = tk.Label(root, text = 'Username',
                    font=('calibre',
                            10, 'bold'))

    # creating a entry for input
    # name using widget Entry
    name_entry = tk.Entry(root,
                    textvariable = name_var,font=('calibre',10,'normal'))

    # creating a label for password
    passw_label = tk.Label(root,
                    text = 'Password',
                    font = ('calibre',10,'bold'))

    # creating a entry for password
    passw_entry=tk.Entry(root,
                    textvariable = passw_var,
                    font = ('calibre',10,'normal'),
                    show = '*')

    # creating a button using the widget
    # Button that will call the submit function
    sub_btn=tk.Button(root,text = 'Submit',
                command = submit)

    # placing the label and entry in
    # the required position using grid
    # method
    name_label.grid(row=0,column=0
    )
    name_entry.grid(row=0,column=1)
    passw_label.grid(row=1,column=0)
    passw_entry.grid(row=1,column=1)
    sub_btn.grid(row=2,column=1)

    # performing an infinite loop
    # for the window to display
    root.mainloop()