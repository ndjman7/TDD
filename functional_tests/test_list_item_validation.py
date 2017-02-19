import time
from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    # def test_cannot_add_empty_list_items(self):
    #     # 에디스는 메인 페이지에 접속해서 빈 아이템을 실수로 등록하려고 한다
    #     # 입력 상자가 비어 있는 상태에서 엔터키를 누른다
    #     self.browser.get(self.server_url)
    #     self.get_item_input_box().send_keys('\n')
    #
    #     # 페이지가 새로고침되고, 빈 아이템을 등록할 수 없다는
    #     # 에러 메시지가 표시된다.
    #     error = self.get_error_element()
    #     self.assertEqual(error.text, "\n              You can't have an empty list item\n            ")
    #
    #     # 다른 아이템을 입력하고 이번에는 정상 처리된다.
    #     self.get_item_input_box().send_keys('우유 사기\n')
    #     self.wait_for_row_in_list_table('1: 우유 사기')
    #
    #     # 그녀는 고의적으로 다시 빈 아이템을 등록한다
    #     self.get_item_input_box().send_keys('\n')
    #     # 리스트 페이지에 다시 에러 메시지가 표시된다
    #     self.wait_for_row_in_list_table('1: 우유 사기')
    #     error = self.get_error_element()
    #     self.assertEqual(error.text, "\n              You can't have an empty list item\n            ")
    #
    #     # 아이템을 입력하면 정상 동작한다.
    #     self.get_item_input_box().send_keys('tea 만들기\n')
    #     self.wait_for_row_in_list_table('1: 우유 사기')
    #     self.wait_for_row_in_list_table('2: tea 만들기')

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # She starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # And she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # 에디스는 메인 페이지로 돌아가서 신규 목록을 시작한다.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('콜라 사기')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 콜라 사기')

        # 실수로 중복 아이템을 입력한다.
        self.get_item_input_box().send_keys('콜라 사기')
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 도움이 되는 에러 메시지를 본다
        self.wait_for_row_in_list_table('1: 콜라 사기')
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '이미 리스트에 해당 아이템이 있습니다'
        ))

    # def test_error_messages_are_cleared_on_input(self):
    #     # 에디스는 검증 에러를 발생시키도록 신규 목록을 시작한다.
    #     self.browser.get(self.server_url)
    #     self.get_item_input_box().send_keys('Banter too thick')
    #     self.get_item_input_box().send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Banter too thick')
    #     self.get_item_input_box().send_keys('Banter too thick')
    #     self.get_item_input_box().send_keys(Keys.ENTER)
    #
    #     self.wait_for(lambda: self.assertTrue(
    #         self.get_error_element().is_displayed()
    #     ))
    #
    #     # 에러를 제거하기 위해 입력 상자에 타이핑하기 시작한다.
    #     self.get_item_input_box().send_keys('a')
    #     self.get_item_input_box().send_keys(Keys.ENTER)
    #
    #     # 에러 메시지가 사라진 것을 보고 기뻐한다.
    #     self.wait_for(lambda: self.assertFalse(
    #         self.get_error_element().is_displayed()
    #     ))
