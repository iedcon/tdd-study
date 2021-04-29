from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: 공작깃털 사기', [row_text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 웹 사이트 확인
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #작업을 추가하자!
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        #"공작깃털 사기"라고 입력한다.
        inputbox.send_keys('공작깃털 사기')
        # 엔터키를 치면 페이지가 갱신되고 작업목록에 1: 공작깃털 사기"가 추가된다.
        inputbox.send_keys(Keys.ENTER)

        #추가 작업을 입력한다.
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "id_new_item"))
        )
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)
        
        #작업 목록에서 입력한 항목들을 확인할 수 있다.
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "id_list_table"))
        )
        self.check_for_row_in_list_table('1: 공작깃털 사기')
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')

        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main()