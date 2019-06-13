
#============================================================ Python
import re
import os
import inspect
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlencode, parse_qs
import time
import json
import copy
import inspect
import string
import pprint
pp = pprint.PrettyPrinter(indent=2)
from collections import Counter
#============================================================ Data-Science
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
#============================================================ Ecetera
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#============================================================ Project
from career import models
from career.iiterator import FunctionIterator
#============================================================ Libs
import sys
sys.path.append('/Users/sambong/libs/idebug')
sys.path.append('/Users/sambong/libs/ilib')
import idebug as dbg
from ilib import inumber

#============================================================
"""Collector
Version : 3
2019-05-29 기준,
LinkedIn 에서 25개 이상의 JobCards를 페이지 네비게이션 방식에서 Ajax기반의 스크롤 방식으로 변경했다.
따라서 version2에서 사용했던 Pagination 은 필요없고 version3에서는 Scroller를 새로 개발해야한다.
"""
#============================================================

def selenium_clicker(webelem):
    time.sleep(1)
    try:
        webelem.click()
    except Exception as e:
        print(f"{'#'*60}\n{os.path.abspath(__file__)} | {inspect.stack()[0][3]}\n Exception : {e}")
    else:
        return True

class SearchCondition:
    """검색조건 설정."""
    keywords_writing_secs = 3
    searchbutton_click_secs = 1

    def __init__(self):
        print(f"{'='*60}\n SearchCondition.__init__()")
        super().__init__()

    def put_searching_keyword(self, keyword='Data Analytics', location='Spain'):
        try:
            search_form = self.driver.find_element_by_id('nav-typeahead-wormhole')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n e : {e}")
            self.put_searching_keyword(keyword, location)
        else:
            keyword_box = search_form.find_element_by_xpath("//div[contains(@class, 'jobs-search-box__input--keyword')]")
            location_box = search_form.find_element_by_xpath("//div[contains(@class, 'jobs-search-box__input--location')]")
            search_button = search_form.find_element_by_xpath("//button[contains(@class, 'jobs-search-box__submit-button')]")

            keyword_box = keyword_box.find_element_by_tag_name('artdeco-typeahead-deprecated').find_elements_by_tag_name('input')[1]
            keyword_box.clear()
            print(f" 검색 키워드 입력시간 {self.keywords_writing_secs}초 설정.")
            time.sleep(self.keywords_writing_secs)
            keyword_box.send_keys(keyword)

            location_box = location_box.find_element_by_tag_name('artdeco-typeahead-deprecated').find_elements_by_tag_name('input')[1]
            location_box.clear()
            print(f" 지역명 입력시간 {self.keywords_writing_secs}초 설정.")
            time.sleep(self.keywords_writing_secs)
            location_box.send_keys(location)

            selenium_clicker(search_button)
            return self

    def choose_date_posted(self, duration=0):
        """
        past24hours = duration : [0]
        past_week = duration : [1]
        past_month = duration : [2]
        anytime = duration : [3]
        """
        time.sleep(2)
        try:
            filterbar_section = self.driver.find_element_by_xpath('//header[contains(@class, "search-filters-bar--jobs-search")]')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            self.choose_date_posted(duration)
        else:
            date_filter = filterbar_section.find_element_by_xpath("//button[contains(@aria-label, 'Date Posted filter')]")
            # 드롭-다운 선택지 불러오기.
            selenium_clicker(webelem=date_filter.find_element_by_tag_name('li-icon'))
            facets = filterbar_section.find_element_by_id("date-posted-facet-values")
            values = facets.find_elements_by_tag_name('li')
            # 기간 선택.
            selenium_clicker(webelem=values[duration].find_element_by_tag_name('label'))
            # 필터 적용.
            selenium_clicker(webelem=facets.find_element_by_xpath("//button[contains(@data-control-name, 'filter_pill_apply')]"))
            return self

    def choose_sort_by(self, sort='date'):
        try:
            sort_section = self.driver.find_element_by_id('sort-by-select')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            self.choose_sort_by(sort)
        else:
            sort_button = sort_section.find_element_by_id("sort-by-select-trigger")
            sort_option = sort_section.find_element_by_id('sort-by-select-options')
            cur_sort_value = sort_button.find_element_by_tag_name('p').text
            if sort not in cur_sort_value:
                # 옵션 선택 팝업 클릭.
                selenium_clicker(webelem=sort_button.find_element_by_tag_name('p'))
                # 최종 옵션 선택 및 적용.
                class_pat = f"jobs-search-dropdown__option-button--{sort}"
                xpath = f"//button[contains(@class, '{class_pat}')]"
                selenium_clicker(webelem=sort_option.find_element_by_xpath(xpath))
            return self

    def extract_keyword_location(self):
        uo = urlparse(self.driver.current_url)
        qs = parse_qs(uo.query)
        self.search_keyword = qs['keywords'][0]
        self.search_location = qs['location'][0]

class JobDetails(models.LinkedInJobPosting):

    scroll_to_see_more_secs = 3
    job_description_reading_secs = 10
    scroll_to_next_block_secs = 2
    job_details_human_reading_secs = 10
    job_details_ajax_waiting_secs = 3

    def __init__(self):
        print(f"{'='*60}\n JobDetails.__init__()")
        super().__init__()

    def detect_job_details(self):
        rightpanel_container = self.driver.find_elements_by_class_name('jobs-search-two-pane__details')
        if len(rightpanel_container) is 1:
            content_container = self.driver.find_elements_by_class_name('jobs-details__main-content')
            if len(content_container) is 1:
                print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Right-panel exists.\n")
                return True
            else:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(content_container) is not 1.\n")
                return False
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(rightpanel_container) is not 1.\n")
            return False

    def click_job_description_see_more(self):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n scroll_to_see_more_secs : {self.scroll_to_see_more_secs}")
        time.sleep(self.scroll_to_see_more_secs)
        try:
            job_description = self.driver.find_element_by_class_name('jobs-description')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            try:
                see_more_btn = job_description.find_element_by_class_name('artdeco-button')
            except Exception as e:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            else:
                ActionChains(self.driver).move_to_element(see_more_btn).perform()
                selenium_clicker(see_more_btn)
                # print(f"\n.\n.\n.\n {self.job_description_reading_secs}초 동안 job-description 읽는 척.\n.\n.\n.")
                # time.sleep(self.job_description_reading_secs)

    def moveto_applicant_insights_send_feedback(self):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n scroll_to_next_block_secs : {self.scroll_to_next_block_secs}")
        time.sleep(self.scroll_to_next_block_secs)
        try:
            applicant_insights = self.driver.find_element_by_class_name('jobs-premium-applicant-insights')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            try:
                send_feedback = applicant_insights.find_element_by_class_name('display-flex')
            except Exception as e:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            else:
                ActionChains(self.driver).move_to_element(send_feedback).perform()

    def moveto_applicant_insights_send_feedback_v1(self):
        time.sleep(self.scroll_to_next_block_secs)
        applicant_insights = self.driver.find_elements_by_class_name('jobs-premium-applicant-insights')
        if len(applicant_insights) is 1:
            send_feedback = applicant_insights[0].find_elements_by_class_name('display-flex')
            if len(send_feedback) is 1:
                ActionChains(self.driver).move_to_element(send_feedback[0]).perform()
            else:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(send_feedback) is not 1.")
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(applicant_insights) is not 1.")

    def moveto_company_insights_more_company(self):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n scroll_to_next_block_secs : {self.scroll_to_next_block_secs}")
        time.sleep(self.scroll_to_next_block_secs)
        try:
            company_insights = self.driver.find_element_by_class_name('jobs-premium-company-insights')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            try:
                more_company = company_insights.find_element_by_xpath("//a[contains(@data-control-name, 'see_more_company_link')]")
            except Exception as e:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            else:
                ActionChains(self.driver).move_to_element(more_company).perform()

    def moveto_commute(self):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n scroll_to_next_block_secs : {self.scroll_to_next_block_secs}")
        time.sleep(self.scroll_to_next_block_secs)
        try:
            commute_div = self.driver.find_element_by_id('commute-module')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            ActionChains(self.driver).move_to_element(commute_div).perform()

    def click_about_us_see_more(self):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n scroll_to_next_block_secs : {self.scroll_to_next_block_secs}")
        time.sleep(self.scroll_to_next_block_secs)
        try:
            article_tag = self.driver.find_element_by_class_name('jobs-company__toggle-to-link')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            try:
                button = article_tag.find_element_by_tag_name('button')
            except Exception as e:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            else:
                ActionChains(self.driver).move_to_element(button).perform()
                selenium_clicker(webelem=button)

    def debug_re_search(self):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n job_details_ajax_waiting_secs : {self.job_details_ajax_waiting_secs}")
        time.sleep(self.job_details_ajax_waiting_secs)
        print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}")
        html = self.driver.page_source

        m = re.search('jobs-premium-applicant-insights\s*',string=html)
        print(f"{'-'*60}\n jobs-premium-applicant-insights\s* re.search :\n {m}")

        m = re.search('jobs-premium-company-insights\s*',string=html)
        print(f"{'-'*60}\n jobs-premium-company-insights\s* re.search :\n {m}")

        m = re.search('jobs-company__card\s*',string=html)
        print(f"{'-'*60}\n jobs-company__card\s* re.search :\n {m}")

    def save_job_details(self):
        if hasattr(self,'search_keyword') and hasattr(self,'search_location') and hasattr(self,'companyname') and hasattr(self,'title'):
            self.html = self.driver.page_source
            filter = {
                'search_keyword':self.search_keyword,
                'search_location':self.search_location,
                'collect_dt':self.collect_dt,
                'companyname':self.companyname,
                'title':self.title,
            }
            print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n list(self.schematize().doc) : {list(self.schematize().doc)}.")
            self.insert_doc()
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 중요한 키값을 가지고 있지 않기 때문에 저장하지 않는다.\n")
        return self

    def collect_job_details(self):
        if self.detect_job_details():
            self.click_job_description_see_more()
            self.moveto_applicant_insights_send_feedback()
            self.moveto_company_insights_more_company()
            self.moveto_commute()
            self.click_about_us_see_more()
            self.debug_re_search()
            print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}")
            print(f"\n.\n.\n.\n {self.job_details_human_reading_secs}초 동안 job-details 읽는 척.\n.\n.\n.")
            time.sleep(self.job_details_human_reading_secs)
            self.save_job_details()
        else:
            pass

class JobCards(JobDetails):

    def __init__(self):
        print(f"{'='*60}\n JobCards.__init__()")
        super().__init__()

    def detect_jobcards(self):
        try:
            jobcard_ul = self.driver.find_element_by_class_name('jobs-search-results__list')
        except Exception as e:
            self.jobcards_iterable = False
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}\n self.jobcards_iterable : {self.jobcards_iterable}")
        else:
            self.jobcards = jobcard_ul.find_elements_by_class_name('artdeco-list__item')
            self.jobcards_iterable = True
            print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Job-cards exist.\n self.jobcards_iterable : {self.jobcards_iterable}")
        finally:
            return self

    def find_active_jobcard(self):
        if hasattr(self,'jobcards'):
            for i, jobcard in enumerate(self.jobcards):
                try: jobcard.find_element_by_class_name('job-card-search--is-active')
                except Exception as e: pass
                else:
                    self.active_jobcard_num = i
                    self.active_jobcard = self.jobcards[i]
                    break
            if hasattr(self,'active_jobcard_num') is False:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Active-Jobcard 가 존재하지 않는 말도 안되는 상황.")
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'jobcards') is False.")
        return self

    def click_next_jobcard(self):
        if hasattr(self,'active_jobcard_num'):
            if len(self.jobcards) is (self.active_jobcard_num+1):
                self.jobcards_iterable = False
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Current active jobcard({self.active_jobcard_num+1}) is the last one. Stop iteration.")
            else:
                self.jobcards_iterable = True
                next_jobcard = self.jobcards[self.active_jobcard_num+1]
                selenium_clicker(next_jobcard)
                print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n JobCard-Number {self.active_jobcard_num+1} 클릭.")
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'active_jobcard_num') is False.")

    def parse_active_jobcard(self):
        try:
            active_jobcard = self.driver.find_element_by_class_name('job-card-search--is-active')
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            try:
                jobcard = active_jobcard.find_element_by_class_name('job-card-search__content-wrapper')
            except Exception as e:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
            else:
                print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}")
                ############################################################
                try:
                    title = jobcard.find_element_by_class_name('job-card-search__title')
                except Exception as e:
                    print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
                else:
                    self.title = title.text.strip()
                    print(f" job-title : {self.title}")
                ############################################################
                try:
                    companyname = jobcard.find_element_by_class_name('job-card-search__company-name')
                except Exception as e:
                    print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
                else:
                    self.companyname = companyname.text.strip()
                    print(f" companyname : {self.companyname}")
                ############################################################
                try:
                    location = jobcard.find_element_by_class_name('job-card-search__location')
                except Exception as e:
                    print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
                else:
                    self.location = location.text.strip()
                    print(f" job-location : {self.location}")

    def iter_jobcards(self):
        if hasattr(self,'collect_dt') and hasattr(self,'search_keyword') and hasattr(self,'search_location'):
            self.jobcards_iterable = True
            while self.jobcards_iterable:
                """링크드인의 장난질에 대한 대응."""
                if self.if_LinkedIn_is_pranking():
                    self.find_active_jobcard().click_next_jobcard()
                else:
                    pass
                """링크드인의 장난질에 대한 대응 - 끝."""
                self.parse_active_jobcard()
                self.collect_job_details()
                # time.sleep(5)
                self.detect_jobcards().find_active_jobcard().click_next_jobcard()
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'search_keyword') and hasattr(self,'search_location') is False.")

class Pagination(JobCards):

    scroll_to_pagination = 1

    def __init__(self, dbgon=True, avg_runtime=1):
        print(f"{'='*60}\n Pagination.__init__()")
        self.dbgon = dbgon
        self.exp_runtime = avg_runtime
        self.page_num = 1
        self.pagelen = 1
        super().__init__()

    def detect_pagination(self):
        """class-value 'search-results-pagination-section'는 항상 존재하므로, 사용하지마라."""
        if hasattr(self,'start_dt') is False:
            self.start_dt = datetime.now().astimezone()
        indicators = self.driver.find_elements_by_class_name('artdeco-pagination__indicator--number')
        if len(indicators) is 0:
            self.pages_iterable = False
            if hasattr(self, 'pages'):
                delattr(self, 'pages')
            self.pagelen = 1
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(indicators) is 0.")
        else:
            self.pages_iterable = True
            self.pages = indicators
            self.pagelen = int(indicators[-1].text.strip())
        return self

    def find_selected_page(self):
        if hasattr(self,'pages'):
            for i, page in enumerate(self.pages, start=0):
                if 'selected' in page.get_attribute('class'):
                    self.selected_page_seq = i
                    self.selected_page = self.pages[i]
                    self.page_num = int(self.selected_page.text.strip())
                    print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Selected page is {self.page_num}.")
                    break
            if hasattr(self,'selected_page_seq') is False:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Active-page 가 존재하지 않는 말도 안되는 상황.")
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'pages') is False.")
        return self

    def click_next_page(self):
        if hasattr(self,'selected_page_seq'):
            if len(self.pages) is (self.selected_page_seq+1):
                self.pages_iterable = False
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Current selected page({self.page_num}) is the last. Stop iteration.")
            else:
                self.pages_iterable = True
                next_page = self.pages[self.selected_page_seq+1]
                next_page_num = next_page.text.strip()
                print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Page-Indicator {next_page_num} 클릭.\n scroll_to_pagination : {self.scroll_to_pagination}")
                button = next_page.find_element_by_tag_name('button')
                time.sleep(self.scroll_to_pagination)
                ActionChains(self.driver).move_to_element(button).perform()
                selenium_clicker(button)
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'selected_page_seq') is False.")

    def iter_pagination(self):
        if hasattr(self,'collect_dt') and hasattr(self,'search_keyword') and hasattr(self,'search_location'):
            self.pages_iterable = True
            while self.pages_iterable:
                """링크드인의 장난질에 대한 대응."""
                if self.if_LinkedIn_is_pranking():
                    self.find_selected_page().click_next_page()
                else:
                    pass
                """링크드인의 장난질에 대한 대응 - 끝."""
                self.detect_pagination()
                self.iter_jobcards()
                self.detect_pagination().find_selected_page().click_next_page()
                self.report_pageloop()
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'search_keyword') and hasattr(self,'search_location') is False.")

    def report_pageloop(self):
        cum_runtime = (datetime.now().astimezone() - self.start_dt).total_seconds()
        avg_runtime = cum_runtime / (self.page_num)
        leftover_runtime = avg_runtime * (self.pagelen - self.page_num)
        if self.dbgon is True:
            print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]} : {self.page_num}/{self.pagelen}")
            tpls = [
                ('누적실행시간', cum_runtime),
                ('잔여실행시간', leftover_runtime),
                ('평균실행시간', avg_runtime),
            ]
            for tpl in tpls:
                timeexp, unit = inumber.convert_timeunit(tpl[1])
                print(f" {tpl[0]} : {timeexp} ({unit})")
        if self.pagelen == self.page_num:
            if (self.exp_runtime is not None) and (avg_runtime > self.exp_runtime):
                print(f"{'*'*60}\n Save the final report into DB.")

class JobsDriver(SearchCondition, Pagination):

    base_url = 'https://www.linkedin.com/jobs/search/'
    search_keywords = [
        'Data Analytics',
        'Data Analysis',
        'Data Scientist',
        'Data Science',
        'Data Engineer',
        'Machine Learning',
        'Artificial Intelligence (AI)',
        'Natural Language Processing',
        'Business Intelligence (bi)',
        'Python',
        'Node.js',
    ]

    def __init__(self, driver):
        print(f"{'='*60}\n{self.__class__}.__init__()")
        self.driver = driver
        super().__init__()

    def move_to_job_search_page(self):
        if re.search(self.base_url, string=self.driver.current_url) is None:
            print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 현재페이지가 Job Search page가 아니므로, 검색페이지로 이동.")
            self.driver.get(self.base_url)
        else:
            pass

    def if_LinkedIn_is_pranking(self):
        if re.search(self.base_url, string=self.driver.current_url) is None:
            print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 링크드인이 장난질 치고 있으므로, 검색 페이지로 회귀.")
            self.driver.back()
            return True
        else:
            return False

    def is_readyto_collect(self):
        uo = urlparse(self.driver.current_url)
        if ('keywords' in uo.query) and ('location' in uo.query) and ('sortBy' in uo.query):
            return True
        else:
            return False

    def collect_on_keyword(self, keyword='machine learning', location='Spain', duration=0):
        fr = dbg.Function(inspect.currentframe()).report_init()
        ############################################################
        self.collect_dt = datetime.now().astimezone()
        self.move_to_job_search_page()
        self.put_searching_keyword(keyword, location).choose_date_posted(duration).choose_sort_by('date')
        self.extract_keyword_location()
        while self.is_readyto_collect() is False:
            print("\nself.is_readyto_collect() is False. Wait 2 seconds.\n")
            time.sleep(2)
        ############################################################
        self.iter_pagination()
        ############################################################
        fr.report_fin()

    def collect_on_keywords(self, search_keywords=None, location='Spain', duration=0):
        fr = dbg.Function(inspect.currentframe()).report_init()
        if search_keywords is None:
            search_keywords = self.search_keywords
        ############################################################
        fi = FunctionIterator(obj=search_keywords, func=self.collect_on_keyword, location=location, duration=duration)
        while fi.iterable:
            fi.nextop()
        ############################################################
        fr.report_fin()

#============================================================
"""1차 Parser."""
#============================================================

class HTMLParser(models.LinkedInJobPosting):
    """HTML element detection만을 위한 regex를 이곳에서 정의한다."""
    p_posted_time_ago = re.compile('(Posted)\s*(\d+)\s*(.+)ago', flags=re.I)
    p_views = re.compile('([\d+,]+)\s*(view[s]*)')

    p_skills_match_ratio = re.compile('\d+ skills match$')
    p_n_applicants = re.compile('\d+ applicant[s]*')
    p_seniority_level = re.compile('([\w-]+)\s*(level)$')
    p_rng_employees = re.compile('([\d,-]+)\s*(employee[s]*)')
    p_n_employees = re.compile('^([\d,]+)\s*(employee[s]*)')

    # p_seniority_level = re.compile('(\d+)\s*(\w+\s\w+)\s*(applicant[s]*)')
    p_applicant_education = re.compile('^jobs[a-z\s-]+__list')
    p_ratio = re.compile('^\d+\%')
    p_applicant_education_degree = re.compile('^have[\.\s]+')
    p_applicant_location_nm = re.compile('top-locations-title$')
    p_applicant_location_cnt = re.compile('top-locations-details$')

    p_total_employees = re.compile('Total employee[s]*', flags=re.I)
    p_company_growthrate = re.compile('Company-wide', flags=re.I)
    p_tenure = re.compile('[\.\d+]+\s*year[s]*')

    # filter = {'html':{'$ne':None}, 'desc':None}
    # filter = {'html':{'$ne':None}}
    filter = {'html':{'$ne':None}, 'collect_dt':{'$ne':None}}
    projection = {'collect_dt':1,'html':1}

    def __init__(self):
        super().__init__()
        self.change_schema()
        self.cleaner = DataValueCleaner()

    def change_schema(self):
        """파싱 후 업뎃저장할 컬럼만 임시 스키마로 설정."""
        for col in (self.inputs + self.output):
            if col in self.schema:
                self.schema.remove(col)
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}")
        print(f" Changed schema len : {len(sorted(self.schema))}")
        print(f" Changed schema : {sorted(self.schema)}")
        return self

    def load_targets(self, filter=None, projection=None):
        fr = dbg.Function(inspect.currentframe()).report_init()
        if filter is not None:
            self.filter = filter
        if projection is not None:
            self.projection = projection
        self.cursor = self.tbl.find(self.filter, self.projection)
        self.load()
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(self.docs) : {len(self.docs)}")
        fr.report_fin()
        return self
    ############################################################Job-Card
    def jobcard_title(self):
        pass

    def jobcard_companyname(self):
        pass

    def jobcard_location(self):
        pass
    ############################################################Top-Card
    """job-title, companyname, location, posted_time_ago, views"""
    def company_logo(self):
        s = self.soup.find('div', class_='jobs-details-top-card__company-logo-container')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'jobs-details-top-card__company-logo-container' is None.")
        else:
            img = s.find('img')
            if img is None:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'img-tag' is None.")
            else:
                if 'src' in list(img.attrs):
                    # print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n img.attrs :")
                    # pp.pprint(img.attrs)
                    self.company_logo_url = img.attrs['src']

    def job_title(self):
        s = self.soup.find('h1', class_='jobs-details-top-card__job-title')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'jobs-details-top-card__job-title' is None.")
        else:
            self.title = s.get_text().strip()

    def _companyname(self):
        s = self.soup.find('a', class_='jobs-details-top-card__company-url')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Top-Card__Company-Name' is None.")
        else:
            self.companyname = s.get_text().strip()

    def job_location(self):
        s = self.soup.find(class_='jobs-details-top-card__company-info')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n class_='jobs-details-top-card__company-info' is None.")
        else:
            companylocation = s.find(class_='jobs-details-top-card__bullet')
            if companylocation is None:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Top-Card__Company-Location' is None.")
            else:
                self.location = companylocation.get_text().strip()

    def postedtimeago_views(self):
        s = self.soup.find('p', class_='jobs-details-top-card__job-info')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'jobs-details-top-card__job-info' is None.")
        else:
            for string in s.stripped_strings:
                string = string.strip()
                if self.p_posted_time_ago.search(string=string) is not None:
                    self.posted_time_ago = string
                    ago_timedelta = self.cleaner.posted_time_ago(v=string, regex=self.p_posted_time_ago)
                    self.calc_posted_dt(ago_timedelta)
                if self.p_views.search(string=string) is not None:
                    self.n_views = self.cleaner.views(v=string, regex=self.p_views)

    def calc_posted_dt(self, ago_timedelta):
        if hasattr(self,'collect_dt'):
            self.posted_dt = self.collect_dt - ago_timedelta
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n hasattr(self,'collect_dt') is False.")
    ############################################################Job-Summary-3-boxes
    def job_box(self):
        job_box = self.soup.find('div',attrs={'data-test-job-summary-type':'job-list'})
        if job_box is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 3-boxes | job_box is None.")
        else:
            items = job_box.find_all('li')
            for item in items:
                text = item.get_text().strip()
                if self.p_skills_match_ratio.search(string=text) is not None:
                    self.skills_match_ratio = self.cleaner.skills_match_ratio(text)
                if self.p_n_applicants.search(string=text) is not None:
                    self.n_applicants = self.cleaner.n_applicants(text)
                m = self.p_seniority_level.search(string=text)
                if m is not None:
                    self.job_level = m.groups()[0]

    def company_box(self):
        s = self.soup.find('div',attrs={'data-test-job-summary-type':'company-list'})
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 3-boxes | company_box is None.")
        else:
            items = s.find_all('li')
            for item in items:
                text = item.get_text().strip()
                if self.p_n_employees.search(string=text) is not None:
                    self.n_employees = self.cleaner.n_employees(text)
                m = self.p_rng_employees.search(string=text)
                if m is not None:
                    self.rng_employees= m.groups()[0]
                if len(item) is 2:
                    self.company_cate = text

    def connections_box(self):
        s = self.soup.find('div',attrs={'data-test-job-summary-type':"connections-list"})
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 3-boxes | connections_box is None.")
        else:
            self.connections = []
            for atag in s.find_all('a',attrs={'data-control-name':"jobdetails_sharedconnections"}):
                cnt = atag.find('div',class_='job-flavors__label').get_text().strip()
                self.connections.append({
                    'cnt': self.cleaner.connection_cnt(cnt),
                    'source': atag.find('img').attrs['title'].strip(),
                })
    ############################################################Job-Description
    def job_description(self):
        s = self.soup.find(id='job-details')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n id='job-details' is None.")
        else:
            self.desc = s.find('span').get_text().strip()

    def _seniority_level_in_job_description(self):
        tags = self.soup.find_all('p', class_='js-formatted-exp-body', limit=1)
        if len(tags) is 0:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Seniority Level' is None.")
        else:
            self.seniority_level = tags[0].get_text().strip()

    def _industries(self):
        tags = self.soup.find_all('ul', class_='js-formatted-industries-list', limit=1)
        if len(tags) is 0:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Industry' is None.")
        else:
            self.industries = []
            for li in tags[0].find_all('li'):
                self.industries.append( li.get_text().strip() )

    def _employment_type(self):
        tags = self.soup.find_all('p', class_='js-formatted-employment-status-body', limit=1)
        if len(tags) is 0:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Employment Type' is None.")
        else:
            self.employment_type = tags[0].get_text().strip()

    def _job_functions(self):
        tags = self.soup.find_all('ul', class_='js-formatted-job-functions-list', limit=1)
        if len(tags) is 0:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Job Functions' is None.")
        else:
            self.job_functions = []
            for li in tags[0].find_all('li'):
                self.job_functions.append( li.get_text().strip() )

    def how_you_match(self):
        tags = self.soup.find_all('span', class_='jobs-ppc-criteria__value')
        if len(tags) is 0:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Skills' is None.")
        else:
            self.match_skills = []
            for tag in tags:
                self.match_skills.append( tag.get_text().strip() )
    ############################################################Competitive_intelligence_about_applicants
    def _applicant_for_this_job(self):
        pass

    def _applicant_topskills(self):
        s = self.soup.find('div', class_='top-skills')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Top skills' is None.")
        else:
            self.applicant_topskills = []
            for li in s.find_all('li'):
                """예외처리."""
                if li.find('span') is not None:
                    li.span.decompose()
                for string in li.stripped_strings:
                    self.applicant_topskills.append(string.strip())

    def _applicant_seniority_levels(self):
        s = self.soup.find('div',class_='applicant-experience')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Seniority level' is None.")
        else:
            self.applicant_seniority_levels = []
            for i, li in enumerate(s.find_all('li')):
                text = li.p.get_text().strip()
                m = self.p_seniority_level.search(string=text)
                if m is None:
                    print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Seniority level'{i}번째 is None.")
                else:
                    self.applicant_seniority_levels.append({
                        'count': self.cleaner.applicants_integer( m.groups()[0] ),
                        'lvname': m.groups()[1],
                        'max_cnt': self.cleaner.applicants_integer( li.progress.attrs['max'] ),
                        'now_cnt': self.cleaner.applicants_integer( li.progress.attrs['value'] ),
                    })

    def _applicant_educations(self):
        s = self.soup.find('div',class_='applicant-education')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Education' is None.")
        else:
            self.applicant_educations = []
            for li in s.find_all('li'):
                app_education = {}
                for span in li.find_all('span', class_=self.p_applicant_education):
                    text = span.get_text().strip()
                    if self.p_ratio.search(string=text) is not None:
                        app_education.update({'ratio':text})
                    if self.p_applicant_education_degree.search(string=text) is not None:
                        app_education.update({'degree':text})
                if len(list(app_education)) is not 0:
                    self.applicant_educations.append(app_education)

    def _applicant_locations(self):
        s = self.soup.find('div',class_=re.compile('jobs-premium-applicant-insights__top-locations\s'))
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Location' is None.")
        else:
            self.applicant_locations = []
            for li in s.find_all('li'):
                location = {}

                name = li.find('p', class_=self.p_applicant_location_nm)
                if name is not None:
                    location.update({'name':name.get_text().strip()})

                count = li.find('p', class_=self.p_applicant_location_cnt)
                if count is not None:
                    text = count.get_text().strip()
                    location.update({'count': self.cleaner.applicant_location_cnt(text)})

                if len(list(location)) is not 0:
                    self.applicant_locations.append(location)
    ############################################################Insight_look_at_company
    def hiring_trend(self):
        """Hiring trends over the last 2 years"""
        for li in self.soup.find_all('li',class_='jobs-premium-company-growth__stat-item'):
            mixed_txt = li.get_text().strip()
            if self.p_total_employees.search(string=mixed_txt) is not None:
                self.total_employees = self.cleaner.total_employees(mixed_txt)
            elif self.p_company_growthrate.search(string=mixed_txt) is not None:
                text = li.find('span', class_='visually-hidden').get_text().strip()
                self.company_growthrate = self.cleaner.growth(text)
            else:
                text = li.find('span', class_='visually-hidden').get_text().strip()
                self.sector_growthrate = self.cleaner.growth(text)

    def _tenure(self):
        """Average tenure"""
        s = self.soup.find('span',class_="jobs-premium-company-growth_average-tenure")
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'Average tenure ' is None.")
        else:
            text = s.find(string=self.p_tenure).strip()
            self.tenure = self.cleaner.tenure(text)
    ############################################################Ecetera
    def commute(self):
        s = self.soup.find('div', class_='jobs-commute-module__company-location')
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'See your commute' is None.")
        else:
            self.commute_addr = s.get_text().strip()

    def _about_us(self):
        s = self.soup.find(id="company-description-text")
        if s is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'About Us' is None.")
        else:
            self.about_us = s.get_text().strip()

    def parse(self):
        loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(self.docs))
        for d in self.docs:
            self.attributize(d)
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.company_logo()
            self.job_title()
            self._companyname()
            self.job_location()
            self.postedtimeago_views()
            self.job_box()
            self.company_box()
            self.connections_box()
            self.job_description()
            self._seniority_level_in_job_description()
            self._industries()
            self._employment_type()
            self._job_functions()
            self.how_you_match()
            self._applicant_topskills()
            self._applicant_seniority_levels()
            self._applicant_educations()
            self._applicant_locations()
            self.hiring_trend()
            self._tenure()
            self.commute()
            self._about_us()
            self.update_doc({'_id':d['_id']}, False)
            loop.report()

def parse(filter=None):
    p = HTMLParser()
    p.load_targets(filter).parse()

class DataValueCleaner:
    p_num_str_mix = re.compile('(\d+[./,]*\d*)\s*([a-zA-Z]+)')
    p_extract_just_num = re.compile('\d+[./,]*\d*')
    p_purify_num = re.compile('[\d,\.]+')
    p_ratio_str = re.compile('([\.\d+]+)\s*(\%)\s*(.*)')

    p_total_employees = re.compile('([0-9,]+)\s*(Total employee[s]*)', flags=re.I)
    p_applicant_location_cnt = re.compile('(\d+\W\d+|\d+)\s*(applicant[s]*)')
    ############################################################Top-Card
    def posted_time_ago(self, v, regex):
        if isinstance(v, str) and len(v) > 0:
            v = v.strip()
            m = regex.search(string=v)
            if m is None:
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m is None.\n posted_time_ago : {v}")
            else:
                num = int(m.groups()[1])
                if 'second' in v:
                    tdelta = timedelta(seconds=num)
                elif 'minute' in v:
                    tdelta = timedelta(minutes=num)
                elif 'hour' in v:
                    tdelta = timedelta(hours=num)
                elif 'day' in v:
                    tdelta = timedelta(days=num)
                elif 'week' in v:
                    tdelta = timedelta(weeks=num)
                elif 'month' in v:
                    tdelta = timedelta(days=num*30.5)
                elif 'year' in v:
                    tdelta = timedelta(days=num*365)
                else:
                    print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 이런 경우는 발생할 수 없다.\n posted_time_ago : {v}")
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n isinstance(v, str) and len(v) > 0 is False.\n posted_time_ago : {v}")
        return tdelta

    def views(self, v, regex):
        m = regex.search(string=v)
        if m is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m is None.")
        else:
            v = m.groups()
            # print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m.group() : {v}")
            v = self._purify_number(v[0])
        return v
    ############################################################Common-functions
    def _clean_num_str_mix(self, v):
        m = self.p_num_str_mix.search(string=v)
        if m is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m is None.")
        else:
            v = m.groups()
            # print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m.groups() : {v}")
        return v[0]

    def _purify_number(self, v):
        try:
            m = self.p_purify_num.search(string=v)
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
        else:
            if ',' in v:
                v = v.replace(',','')
            if '.' in v:
                v = float(v)
            else:
                v = int(v)
        finally:
            return v

    def skills_match_ratio(self, v):
        v = self._clean_num_str_mix(v)
        return v

    def n_applicants(self, v):
        v = self._clean_num_str_mix(v)
        v = self._purify_number(v)
        return int(v)

    def n_employees(self, v):
        v = self._purify_number(v)
        return v

    def connection_cnt(self, v):
        v = self._clean_num_str_mix(v)
        v = self._purify_number(v)
        return int(v)
    ############################################################Competitive_intelligence_about_applicants
    def applicants_integer(self, v):
        v = self._purify_number(v)
        return int(v)

    def applicant_location_cnt(self, v):
        m = self.p_applicant_location_cnt.search(string=v)
        if m is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m is None.\n v : {v}")
        else:
            v = m.groups()
            # print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m.groups() : {v}")
            v = v[0]
        return v
    ############################################################Premium-Services
    def total_employees(self, v):
        m = self.p_total_employees.search(string=v)
        if m is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m is None.\n v : {v}")
        else:
            v = m.groups()
            # print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m.groups() : {v}")
            v = self._purify_number(v[0])
            v = int(v)
        return v

    def growth(self, v):
        m = self.p_ratio_str.search(string=v)
        if m is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m is None.")
        else:
            g = m.groups()
            # print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n m.groups() : {g}")
            v = int(g[0]) / 100
            if 'decre' in g[2]:
                v *= -1
        return v

    def tenure(self, v):
        v = self._clean_num_str_mix(v)
        v = self._purify_number(v)
        return float(v)

#============================================================
"""2차 Parser."""
#============================================================

class DocDataParser(models.LinkedInJobPosting):

    num_str_mix_cols = ['skills_match_ratio','n_applicants','tenure','n_views']
    ratio_cols = ['company_growthrate','sector_growthrate']
    comma_number_cols = ['total_employees','n_views','']
    decimal_cols = ['tenure']
    integer_cols = ['n_applicants','n_views']

    def __init__(self):
        super().__init__()

    def load_targets(self, filter=None):
        projection = self.schema.copy()
        needless = self.inputs + self.output
        needless.remove('collect_dt')
        for e in needless:
            if e in projection:
                projection.remove(e)
        projection = {e:1 for e in projection}
        self.cursor = self.tbl.find(filter, projection)
        self.load()
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(self.docs) : {len(self.docs)}")
        return self

    def clean(self):
        df = self.get_df()
        df = self.clean_dtcols(df)
        df = self.extract_num_str_mix_cols(df)
        df = self.clean_numcols(df)
        return df

    def clean_dtcols(self, df):
        """날짜문자열을 날짜타입으로 변환"""
        def _clean_posted_time_ago(posted_time_ago):
            if isinstance(posted_time_ago, str) and len(posted_time_ago) > 0:
                m = re.search('\d+',string=posted_time_ago)
                if m is None:
                    print(f" m is None.\n posted_time_ago : {posted_time_ago}")
                else:
                    num = int(posted_time_ago[m.start():m.end()])
                    if 'second' in posted_time_ago:
                        return timedelta(seconds=num)
                    elif 'minute' in posted_time_ago:
                        return timedelta(minutes=num)
                    elif 'hour' in posted_time_ago:
                        return timedelta(hours=num)
                    elif 'day' in posted_time_ago:
                        return timedelta(days=num)
                    elif 'week' in posted_time_ago:
                        return timedelta(weeks=num)
                    elif 'month' in posted_time_ago:
                        return timedelta(days=num*30.5)
                    elif 'year' in posted_time_ago:
                        return timedelta(days=num*365)
                    else:
                        print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 이런 경우는 발생할 수 없다.\n posted_time_ago : {posted_time_ago}")

        # 수집일시, 포스팅시간정보 둘 중에 하나라도 없으면 계산불가.
        dtdf = df.reindex(columns=self.dt_cols+['_id']).dropna(axis=0, how='any')
        # len(dtdf)
        # dtdf.tail()
        dtdf.posted_time_ago = dtdf.posted_time_ago.apply(_clean_posted_time_ago)
        # dtdf.head()
        # dtdf.sort_values('posted_time_ago',ascending=False)
        # dtdf.info()
        dtdf['posted_dt'] = dtdf.collect_dt - dtdf.posted_time_ago
        self.dt_cols += ['posted_dt']
        # dtdf.sort_values('posted_dt',ascending=False)
        # return pd.merge(df, dtdf, on='_id')
        df.update(dtdf, join='left', overwrite=True, filter_func=None, errors='ignore')
        return df

    def extract_num_str_mix_cols(self, numdf):
        for col in self.num_str_mix_cols:
            addi_col = f"{col}_str"
            splitdf = numdf[col].str.extract(pat=r'(\d+[./,]*\d*)\s*([a-zA-Z]+)').rename(columns={0:col,1:addi_col})
            numdf.update(splitdf, join='left', overwrite=True, filter_func=None, errors='ignore')
            splitdf1 = splitdf.reindex(columns=[addi_col])
            numdf = numdf.join(splitdf1)
        return numdf

    def clean_numcols(self, df):
        print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(df) : {len(df)}")
        numdf = df.reindex(columns=self.num_cols+['_id']).dropna(axis=0, how='all', subset=self.num_cols)
        print(f" len(numdf) : {len(numdf)}")
        numdf = self._clean_ratio_cols(numdf)
        numdf = self._clean_comma_number_cols(numdf)
        numdf = self._clean_decimal_cols(numdf)
        numdf = self._clean_integer_cols(numdf)
        numdf = numdf.dropna(axis=0, how='all', subset=self.num_cols)
        # print(f" Fin len(numdf) : {len(numdf)}")
        # return pd.merge(df, numdf, on='_id')
        # df.update(numdf, join='left', overwrite=True, filter_func=None, errors='ignore')
        # return df
        return numdf

    def _clean_ratio_cols(self, numdf):

        def _clean_growth_col(x):
            if isinstance(x,str):
                if x.isnumeric():
                    return float(x)/100
                else:
                    return None
            elif isinstance(x,int):
                return float(x/100)
            elif isinstance(x,float):
                return x/100
            else:
                return None

        def _clean_growth_addi_col(x):
            if isinstance(x,str):
                if updown_p.search(string=x) is None:
                    return None
                else:
                    return x.strip()
            else:
                return None

        updown_p = re.compile('(in|de)crease', flags=re.I)
        for col in self.ratio_cols:
            addi_col = f"{col}_updown"
            growdf = numdf[col].str.extract(pat=r'(\d+)\%\s*(.*)').rename(columns={0:col,1:addi_col})
            numdf.update(growdf)
            growdf1 = growdf.reindex(columns=[addi_col])
            numdf = numdf.join(growdf1)
            numdf[col] = numdf[col].apply(_clean_growth_col)
            numdf[addi_col] = numdf[addi_col].apply(_clean_growth_addi_col)
        return numdf

    def _clean_comma_number_cols(self, numdf):
        for col in self.comma_number_cols:
            numdf[col] = numdf[col].apply(lambda x: x if x is np.nan else int(x.replace(',','')))
        return numdf

    def _clean_decimal_cols(self, numdf):
        for col in self.decimal_cols:
            numdf[col] = numdf[col].apply(lambda x: x if x is np.nan else int(x.replace('.','')))
        return numdf

    def _clean_integer_cols(self, numdf):
        for col in self.integer_cols:
            numdf[col] = numdf[col].apply(lambda x: x if x is np.nan else int(x))
        return numdf



#============================================================
"""Handler."""
#============================================================

"""테이블 중복제거."""
class Deduplicator(models.LinkedInJobPosting):

    input_consts = ['search_keyword','search_location']
    input_vars = ['collect_dt']
    output_consts = ['title','companyname','location']
    output_vars = ['posted_time_ago']
    subset = input_consts + input_vars + output_consts + output_vars
    cols_order = input_consts + output_consts + input_vars + output_vars + ['_id']
    """최근 수집-파싱을 분리한 데이터에 대해."""
    # filter = {'html':{'$ne':None}, 'desc':{'$ne':None}}
    """예전 html 없는 데이터에 대해."""
    filter = {'desc':{'$ne':None}}
    projection = {col:1 for col in subset}

    def load_targets(self):
        self.cursor = self.tbl.find(self.filter, self.projection)
        self.load()
        print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(docs) : {len(self.docs)}")
        return self

    def normalize_collect_dt(self, df):
        df = df.dropna(axis=0, how='any', thresh=None, subset=['collect_dt'])
        df.collect_dt = df.collect_dt.apply(lambda x: datetime(x.year, x.month, x.day, x.hour))
        return df

    def get_dup_df(self, keep):
        if hasattr(self,'docs'):
            df = self.get_df().sort_values(by=self.cols_order)
            df = self.normalize_collect_dt(df)
            TF = df.duplicated(subset=self.subset, keep=keep)
            print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(df[TF]) : {len(df[TF])}")
            return df[TF]
        else:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n if hasattr(self,'docs') is False.")

    def review_dup_df(self):
        df = self.get_dup_df(keep=False)
        if len(df) is not 0:
            return df.sort_values(by=self.cols_order).reindex(columns=self.cols_order)

    def delete_dup_data(self):
        df = self.get_dup_df(keep='first')
        if len(df) is not 0:
            self.DeleteResult = self.tbl.delete_many({'_id':{'$in':list(df._id)}})
            print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n DeleteResult : {self.DeleteResult}")
