from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 웹 사이트 확인
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀이 'To-Do'를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main()