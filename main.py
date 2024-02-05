import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pyperclip as pp
import time
import random
import os
# MySQL 연결 정보
db_host = "my8002.gabiadb.com"
db_user = "amsdb"
db_password = "ghrn1004!!"
db_name = "amsdb"  # 여기에 실제 사용하는 데이터베이스 이름을 입력하세요


# Tkinter 애플리케이션 클래스 정의
class ProductManagementApp:
    driver = ''
    def dbConn(self):
        self.conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.conn.autocommit = True  # 자동 커밋 모드 활성화
        self.cursor = self.conn.cursor()

    def __init__(self, root):
        self.root = root
        self.root.title("제품 정보 관리")

        # MySQL 연결
        self.dbConn()

        # UI 생성
        self.create_ui()



    def create_ui(self):
        # 탭 생성
        self.tabControl = ttk.Notebook(self.root)

        # 조회 탭
        self.tab_view = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_view, text="조회")

        # 조회 탭의 내용
        self.tree = ttk.Treeview(self.tab_view, columns=("CP_ID", "PRDT_NM", "PRDT_URL", "VALID_YN"), show="headings")
        self.tree.heading("CP_ID", text="번호")
        self.tree.heading("PRDT_NM", text="제품명")
        self.tree.heading("PRDT_URL", text="제품 URL")
        self.tree.heading("VALID_YN", text="검증여부")
        self.tree.pack(fill=tk.BOTH, expand=1)

        # 조회 버튼
        btn_view = ttk.Button(self.tab_view, text="조회", command=self.load_data)
        btn_view.pack()

        # 수정 탭
        self.tab_edit = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_edit, text="수정")

        # 수정 탭의 내용
        lbl_prdt_nm = ttk.Label(self.tab_edit, text="제품명:")
        lbl_prdt_nm.grid(row=0, column=0, padx=5, pady=5)
        self.entry_prdt_nm = ttk.Entry(self.tab_edit)
        self.entry_prdt_nm.grid(row=0, column=1, padx=5, pady=5)

        lbl_prdt_url = ttk.Label(self.tab_edit, text="제품 URL:")
        lbl_prdt_url.grid(row=1, column=0, padx=5, pady=5)
        self.entry_prdt_url = ttk.Entry(self.tab_edit)
        self.entry_prdt_url.grid(row=1, column=1, padx=5, pady=5)

        # 수정 버튼
        btn_update = ttk.Button(self.tab_edit, text="수정", command=self.update_data)
        btn_update.grid(row=4, columnspan=2, pady=10)

        # 추가 탭
        self.tab_add = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_add, text="추가")

        # 추가 탭의 내용
        lbl_add_prdt_nm = ttk.Label(self.tab_add, text="제품명:")
        lbl_add_prdt_nm.grid(row=0, column=0, padx=5, pady=5)
        self.entry_add_prdt_nm = ttk.Entry(self.tab_add)
        self.entry_add_prdt_nm.grid(row=0, column=1, padx=5, pady=5)

        lbl_add_prdt_url = ttk.Label(self.tab_add, text="제품 URL:")
        lbl_add_prdt_url.grid(row=1, column=0, padx=5, pady=5)
        self.entry_add_prdt_url = ttk.Entry(self.tab_add)
        self.entry_add_prdt_url.grid(row=1, column=1, padx=5, pady=5)

        # 검증 탭
        self.tab_validation = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_validation, text="검증")

        # 검증 버튼
        # btn_validation = ttk.Button(self.tab_validation, text="검증", command=self.sample_validation_function)
        # btn_validation.pack()
        btn_validation = ttk.Button(self.tab_validation, text="검증", command=self.sample_validation_function_threaded)
        btn_validation.pack()
        # 추가 버튼
        btn_add = ttk.Button(self.tab_add, text="추가", command=self.add_data)
        btn_add.grid(row=2, columnspan=2, pady=10)

        self.tabControl.pack(expand=1, fill="both")


       # Create a progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, fill=tk.X)

    def sample_validation_function_threaded(self):
        # 샘플 검증 함수를 별도의 스레드에서 실행
        validation_thread = threading.Thread(target=self.sample_validation_function)
        validation_thread.start()

    def load_data(self):
        self.dbConn()
        try:
            # 데이터 조회 및 트리뷰 업데이트
            query = "SELECT CP_ID, PRDT_NM, PRDT_URL, VALID_YN FROM T_CP_CHK"
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            # 기존 아이템 제거
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 조회 결과를 트리뷰에 추가
            for row in data:
                list2 = list(row)
                if row[3]==0:
                    list2[3] = 'Y'
                elif row[3]==1:
                    list2[3] = 'N'

                item_id = self.tree.insert("", "end", values=list2)
                # Set the tag based on the 'VALID_YN' value
                if row[3] == 1:  # Assuming 'N' means invalid
                    self.tree.tag_configure('invalid', background='orange',foreground='white')
                    self.tree.item(item_id, tags=('invalid',))
        except mysql.connector.Error as e:
            messagebox.showerror("오류", f"MySQL 연결 중 에러 발생: {str(e)}")

    def update_data(self):
        self.dbConn()
        # 선택된 행 확인
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("오류", "수정할 행을 선택하세요.")
            return

        # 선택된 행의 데이터 가져오기
        prdt_nm = self.entry_prdt_nm.get()
        prdt_url = self.entry_prdt_url.get()

        # 데이터베이스 업데이트
        selected_id = self.tree.item(selected_item, "values")[0]
        query = "UPDATE T_CP_CHK SET PRDT_NM=%s, PRDT_URL=%s, UPT_DT =SYSDATE() WHERE CP_ID=%s"
        values = (prdt_nm, prdt_url, selected_id)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("성공", "데이터가 성공적으로 업데이트되었습니다.")
            self.load_data()
        except Exception as e:
            messagebox.showerror("오류", f"데이터 업데이트 중 오류 발생: {str(e)}")
            self.conn.rollback()

    def add_data(self):
        self.dbConn()
        # 입력된 데이터 가져오기
        prdt_nm = self.entry_add_prdt_nm.get()
        prdt_url = self.entry_add_prdt_url.get()

        # 데이터베이스에 새로운 행 추가
        query = "INSERT INTO T_CP_CHK (PRDT_NM, PRDT_URL) VALUES (%s, %s)"
        values = (prdt_nm, prdt_url)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("성공", "새로운 데이터가 성공적으로 추가되었습니다.")
            self.load_data()
        except Exception as e:
            messagebox.showerror("오류", f"데이터 추가 중 오류 발생: {str(e)}")
            self.conn.rollback()


    def sample_validation_function(self):
        self.dbConn()

        def driverSetting():
            chrome_options = webdriver.ChromeOptions()
            # Headless 모드 (브라우저 창이 표시되지 않음)
            chrome_options.add_argument('--headless')
            # 윈도우 크기 설정
            chrome_options.add_argument('window-size=1920x1080')
            # 사용자 에이전트 설정
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
            # GPU 사용 안 함
            chrome_options.add_argument('disable-gpu')
            # Sandbox 비활성화
            chrome_options.add_argument('--no-sandbox')
            # 불필요한 로깅 비활성화
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # 기타 추가 옵션들을 필요에 따라 설정할 수 있습니다.
            # WebDriver 인스턴스 생성시 옵션 적용
            driver = webdriver.Chrome(options=chrome_options)
            return driver


        def openBlog(url):
            driver.execute_script(f"window.open('{url}');")
            driver.switch_to.window(driver.window_handles[1])

        def closeBlog():
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        query = "SELECT CP_ID, PRDT_NM, PRDT_URL, VALID_YN FROM T_CP_CHK"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        total_items = len(data)
        for index,prdt in enumerate(data):
            print(prdt[1])
            print(prdt[2])
            #driver.get(prdt[2])
            driver = driverSetting()
            driver.get(prdt[2])
            checkurl = driver.find_elements(By.XPATH, "//*[@class='prod-not-find-unknown']")
            print(len(checkurl))
            driver.quit()
            if len(checkurl) == 0:
                self.update_database(prdt[0], 0)
            elif len(checkurl) > 0:
                self.update_database(prdt[0], 1)

            # Calculate progress percentage
            progress_percentage = (index + 1) / total_items * 100
            self.progress_var.set(progress_percentage)
            self.root.update_idletasks()

        # Reset progress bar after completion
        self.progress_var.set(0)
        messagebox.showinfo("검증", "검증 샘플 함수가 실행되었습니다.")

    def update_database(self, cp_id, valid_yn):
        query = "UPDATE T_CP_CHK SET VALID_YN=%s , UPT_DT =SYSDATE() WHERE CP_ID=%s"
        values = (valid_yn, cp_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            self.load_data()
        except Exception as e:
            print(f"Error updating database: {str(e)}")
            self.conn.rollback()

# 메인 실행부
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManagementApp(root)
    root.mainloop()
