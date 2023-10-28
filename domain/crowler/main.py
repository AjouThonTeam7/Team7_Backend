# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def make_rest_time(time_table):
    time_mapping = {
        "A": "09:00~10:30",
        "B": "10:30~12:00",
        "C": "12:00~13:30",
        "D": "13:30~15:00",
        "E": "15:00~16:30",
        "F": "16:30~18:00",
        "G": "18:00~19:30",
    }
    rest_time = []
    for x in time_mapping.items():
        if is_overlap(x[1], time_table):
            pass
        else:
            rest_time.append(x[0])
    return rest_time


def is_overlap(time_slot1, time_table):
    for time_slot2 in time_table:
        start_time1, end_time1 = map(
            lambda x: int(x[:2]) * 60 + int(x[3:]), time_slot1.split("~")
        )
        start_time2, end_time2 = map(
            lambda x: int(x[:2]) * 60 + int(x[3:]), time_slot2.split("~")
        )
        if start_time1 < end_time2 and start_time2 < end_time1:
            return True
    return False


def login(driver, ID, PASSWORD):
    driver.maximize_window()
    input_id = driver.find_element("name", "userId")
    input_pw = driver.find_element("name", "password")
    btn_login = driver.find_element("id", "loginSubmit")
    input_id.send_keys(f"{ID}")
    input_pw.send_keys(f"{PASSWORD}")
    btn_login.click()
    sleep(2)


def find_item(driver):
    week = ["월", "화", "수", "목", "금"]
    time_table = {}
    subject_table = []
    for w in week:
        day = driver.find_element(By.XPATH, f"//em[contains(text(), '{w}')]")
        day.click()
        sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        items = soup.find_all(class_="nb-t-05-item")
        # 결과를 저장할 리스트를 초기화합니다.
        time_schedule = []
        # 각 요소에서 시간대 정보를 추출합니다.
        for item in items:
            time_element = item.find(class_="ng-binding")
            subject_element = item.find(class_="theme-sub ng-binding")
            if time_element:
                time = time_element.get_text()
                time_schedule.append(time)
            if subject_element:
                subject = subject_element.get_text()
                subject_table.append(subject)
        time_table[w] = time_schedule
        major = soup.select_one(
            ".nb-p-01-myInfo dd.ng-binding").get_text().strip()
        name_element = soup.find("dt", class_="ng-binding")
        name = name_element.get_text(strip=True)
    return time_table, subject_table, major, name, soup
    # BeautifulSoup을 사용하여 HTML을 파싱합니다.

    # BeautifulSoup을 사용하여 HTML을 파싱합니다.


def run_crowler(ID, PASSWORD):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://mportal.ajou.ac.kr/main.do")
    print("chrome driver를 연결중입니다 ..")
    btn_menu_1 = driver.find_element(
        By.XPATH, "//a[contains(text(), '로그인하세요')]")
    sleep(2)
    btn_menu_1.click()
    # monday = driver.find_element(By.XPATH, f"//em[contains(text(), 월)]")
    # monday.click()
    # 암묵적으로 웹 자원 로드를 위해 5초까지 기다려 준다.
    wait = WebDriverWait(driver, 1)
    sleep(2)

    # login
    login(driver, ID, PASSWORD)
    print("login 중입니다...")
    sleep(7)
    # item 가져오기
    time_table, subject_table, major, name, soup = find_item(driver)
    print("정보를 가져오는 중입니다...")
    # json 전처리
    subject = list(set(subject_table))
    subject = [x.split()[0] for x in subject]
    rest_dict = {k: make_rest_time(v) for k, v in time_table.items()}
    major = major.split()[1]
    name = name.split("님")[0]
    # json 저장
    json_data = {}
    json_data["name"] = name
    json_data["major"] = major
    json_data["subject"] = subject
    json_data["day"] = rest_dict

    return json_data

    # file_path = "./sample.json"
    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(json_data, f, ensure_ascii=False, indent=4)
