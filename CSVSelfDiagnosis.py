import csv 
import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException

with open("./info.csv", "r", encoding="utf-8") as f:
    InfoCSV = csv.reader(f)
    UserInfo = []
    for row in InfoCSV:
        UserInfo.append(row)
    del UserInfo[0]

Password = UserInfo[0][5]
DiagnosisNum = 0
LoopNum = 0
input = False

subprocess.Popen('C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp" --window-size=500,1080 https://hcs.eduro.go.kr/#/relogin')
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome('./chromedriver.exe', options=option)
sleep(0.5)

try:
    driver.find_element_by_id('password').click()
except:
    driver.find_element_by_id('btnConfirm2').click()
    input = True

for info in UserInfo:
    CityProvince = info[1]
    SchoolLevel = info[2]
    SchoolName = info[3]
    UserName = info[0]
    BirthDate = info[4]

    if info[6] != "":
        print(UserName + "님의 자가진단을 건너뜁니다(사유: 유저 설정)")
        input = False
        continue
    DiagnosisNum = DiagnosisNum + 1
    LoopNum = LoopNum + 1
    sleep(1)
    
    try:
        driver.find_element_by_xpath(f"//*[contains(text(), '{UserName}')]")
    except:
        if LoopNum!= 1:
            input = True

    if input == True:
        Password = info[5]
        if LoopNum != 1:
            driver.get('https://hcs.eduro.go.kr/#/loginWithUserInfo')
        sleep(1)
        driver.find_element_by_id('schul_name_input').click()
        sleep(0.5)
        Select(driver.find_element_by_id('sidolabel')).select_by_visible_text(CityProvince)
        sleep(0.5)
        Select(driver.find_element_by_id('crseScCode')).select_by_visible_text(SchoolLevel)
        sleep(0.5)
        driver.find_element_by_id('orgname').send_keys(SchoolName)
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/table/tbody/tr[3]/td[2]/button').click()
        sleep(0.5)
        driver.find_element_by_css_selector("#softBoardListLayer > div.layerContentsWrap > div.layerSchoolSelectWrap > ul").click()
        sleep(0.5)
        driver.find_element_by_class_name('layerFullBtn').click()
        sleep(0.5)
        driver.find_element_by_id('user_name_input').send_keys(UserName)
        sleep(0.5)
        driver.find_element_by_id('birthday_input').send_keys(BirthDate)
        sleep(0.5)
        driver.find_element_by_id('btnConfirm').click()
        sleep(1.5)
        driver.find_element_by_id('password').click()

    try:
        alert = driver.switch_to.alert
        alert.accept()
        driver.find_element_by_id('password').click()
    except NoAlertPresentException:
        pass

    if LoopNum == 1 or input == True:
        for i in list(Password):
            sleep(0.2)
            driver.find_element_by_css_selector(f'[aria-label="{i}"]').click()
        input = False
        sleep(0.5)
        driver.find_element_by_id('btnConfirm').click()


    sleep(2)
    driver.find_element_by_xpath(f"//*[contains(text(), '{UserName}')]").click()
    sleep(1)

    try:
        alert = driver.switch_to.alert
        alert.accept()
        print(UserName + "님의 자가진단을 건너뜁니다(사유: 이미 완료됨)")
        DiagnosisNum = DiagnosisNum - 1
        continue
    except NoAlertPresentException:
        pass

    for i in range(1, 4):
        sleep(0.2)
        driver.find_element_by_css_selector(f"#container > div.subpage > div > div:nth-child(2) > div.survey_question > dl:nth-child({i}) > dd > ul > li:nth-child(1) > label").click()
    driver.find_element_by_id('btnConfirm').click()

    print(f"{UserName}님의 자가진단을 완료했습니다({str(DiagnosisNum)}번째)")
    sleep(0.5)
    driver.get('https://hcs.eduro.go.kr/#/main')
    
print(f'모든 자가진단이 완료되었습니다(총 {str(DiagnosisNum)}개)')
driver.close()