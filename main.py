from tkinter import Tk, Label, Button
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# 웹페이지 로드 및 식단 크롤링 함수
def get_menu_for_day(date):
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 활성화
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # WebDriver 설정 및 페이지 로드
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://school.jbedu.kr/haeri/M01030301/list")


    # 페이지 소스를 BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 현재 날짜가 포함된 행 번호 계산
    first_day_of_month = date.replace(day=1)
    first_weekday_of_month = first_day_of_month.weekday()  # 월: 0, 화: 1, 수: 2, 목: 3, 금: 4, 토: 5, 일: 6
    day_of_week = date.weekday()  # 현재 날짜의 요일
    days_from_start_of_month = (date - first_day_of_month).days
    print(days_from_start_of_month)
    row_offset = (days_from_start_of_month // 7) + 2  # 첫 번째 주가 2부터 시작
    
    # 요일에 따른 셀렉터 설정
    days_selector = ['mon', 'tue', 'wed', 'thu', 'fri','sat','sun']
    selector = f"#usm-content-body-id > table > tbody > tr:nth-child({row_offset}) > td.{days_selector[day_of_week]}.tch-has"
    day_menu = soup.select_one(selector)
    print(row_offset,day_of_week)
    # '중식'에 해당하는 메뉴 추출
    if day_menu:
        menu_items = day_menu.find_all('li')
        menu = [item.text.strip() for item in menu_items]
        menu_text = "\n".join(menu)
    else:
        menu_text = "해당 날짜의 메뉴가 없습니다."

    driver.quit()
    return menu_text

# Tkinter GUI 설정
class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("학교 식단")
        
        # 날짜 관련 설정
        self.current_day = datetime.now()
        
        # 날짜와 식단을 보여줄 레이블
        self.label_date = Label(root, text=f"{self.current_day.strftime('%Y-%m-%d')}의 식단:", font=("Arial", 16))
        self.label_date.pack(pady=10)
        
        self.label_menu = Label(root, text="Loading...", font=("Arial", 14), wraplength=400, justify="left")
        self.label_menu.pack(pady=10)
        
        # 다음날 식단을 보여주는 버튼
        self.button_next = Button(root, text="다음 날", command=self.update_menu, font=("Arial", 12))
        self.button_next.pack(pady=10)

        # 처음 실행 시 현재 날짜의 메뉴 로드
        self.update_menu()

    # 메뉴 업데이트 함수
    def update_menu(self):
        # 날짜 레이블 업데이트
        self.label_date.config(text=f"{self.current_day.strftime('%Y-%m-%d')}의 식단:")
        
        # Selenium으로 식단 크롤링
        menu = get_menu_for_day(self.current_day)
        self.label_menu.config(text=menu)
        
        # 다음 날짜로 업데이트
        self.current_day += timedelta(days=1)


# Tkinter 실행
root = Tk()
app = MenuApp(root)
root.mainloop()
