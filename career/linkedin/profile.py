
from career.ide import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from career import linkedin

#============================================================

#============================================================

class ProfileDriver:

    url = 'https://www.linkedin.com/in/jonghyuk-lee/'

    def __init__(self, driver):
        print(f"{'='*60}\n{self.__class__}.__init__()")
        self.driver = driver
        super().__init__()

    def scrolldown_upto_bottom(self):
        before_len = 1
        after_len = 2
        while after_len > before_len:
            print(f"{'-'*60}\n before_len : {before_len}\n after_len : {after_len}")
            cards = self.driver.find_elements_by_class_name('pv-profile-section')
            before_len = len(cards)
            for card in cards:
                ActionChains(self.driver).move_to_element(card).perform()
                try: h2 = card.find_element_by_class_name('pv-profile-section__card-heading')
                except Exception as e: pass
                else: print(f"h2 : {h2.text}")
            cards = self.driver.find_elements_by_class_name('pv-profile-section')
            after_len = len(cards)
        print(f"{'*'*60}\n before_len : {before_len}\n after_len : {after_len}")

    def click_editskill(self):
        x_edit_status = "//a[contains(@class, 'pv-profile-section__edit-action') and contains(@href, '/detail/skills/') and contains(@class, 'active')]"
        x_edit_btn = "//a[contains(@class, 'pv-profile-section__edit-action') and contains(@href, '/detail/skills/')]"
        edit_status = self.driver.find_elements_by_xpath(x_edit_status)
        if len(edit_status) is 0:
            try:
                edit_btn = self.driver.find_element_by_xpath(x_edit_btn)
            except Exception as e:
                print(f"{'#'*60}\n Exception : {e}")
                return False
            else:
                edit_btn.click()
                return True
        elif len(edit_status) is 1:
            print(f"Skills editting pop-up is active.")
        else:
            print(f"WTF")

    def collect_skills(self):
        items = self.driver.find_elements_by_class_name('pv-skills__category-list-item')
        return [item.text for item in items]
