from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Chrome WebDriver 경로 설정


# Selenium을 이용하여 웹 페이지 로드
def get_menu_for_thursday():
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
    driver.get("https://school.jbedu.kr/haeri/M01030301/list")
    
    # 페이지 소스를 BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 목요일에 해당하는 메뉴 선택
    selector = "#usm-content-body-id > table > tbody > tr:nth-child(4) > td.thu.tch-has"
    thursday_menu = soup.select_one(selector)

    # '중식'에 해당하는 메뉴 추출
    if thursday_menu:
        menu_items = thursday_menu.find_all('li')
        menu = [item.text.strip() for item in menu_items]
        print("\n".join(menu))
    else:
        print("목요일에 해당하는 데이터가 없습니다.")
    
    driver.quit()

# 목요일 메뉴 가져오기
get_menu_for_thursday()
