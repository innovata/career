* What machine learning libreries have you used if any? Pandas; Scikit; Weka; Neo4j; Akka; TensorFlow; GBM; Keras; Pytorch; ANOVA; Theano; Caret; MCMC
#============================================================ IDE.
from jupyter.hydrogen import *
#============================================================ Main.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#============================================================ Project.
from career import linkedin
#============================================================ Python.
from datetime import datetime



#============================================================
"""Initialize."""
#============================================================

driver = webdriver.Chrome()
lid = linkedin.LinkedInDriver(driver)
# lid.logined = True
lid.login('loginpage').setup_services()

# lid.jobs.login = lid.login
# lid.jobs.login()

#============================================================
"""Reload."""
#============================================================
from career import selenium as sln

importlib.reload(sln)
importlib.reload(linkedin.driver)
importlib.reload(linkedin.jobs)
importlib.reload(linkedin)
lid.jobs = linkedin.jobs.JobsDriver(driver)


#============================================================
"""JobsDriver."""
#============================================================

lid.jobs.login = lid.login
lid.jobs.login()
# sorted(dir(lid.jobs))
lid.jobs.collect_dt = datetime.now().astimezone()
lid.jobs.move_to_job_search_page()
lid.jobs.is_readyto_collect()


"""_collect_jobposting"""

lid.jobs.put_search_keyword('Natural Language Processing')
lid.jobs.put_search_location('Spain').click_search_button()
lid.jobs.choose_sort_by()
lid.jobs._collect_jobposting()


lid.jobs.collect_on_1condition(keyword='Business Intelligence (bi)', location='Spain', duration=0)
lid.jobs.collect_on_1condition(keyword='Node.js', location='United Kingdom', duration=0)
# lid.jobs.collect_on_1condition(keyword='natural language processing', location='Spain', duration=0)

search_keywords = [
    'Artificial Intelligence (AI)',
    'Natural Language Processing',
    'Business Intelligence (bi)',
    'Node.js',
    'Data Analytics',
    'Data Analysis',
    'Data Scientist',
    'Data Science',
    'Data Engineer',
    'Machine Learning',
    'Python',
]
lid.jobs.collect_on_keywords(location='Spain', duration=0, search_keywords=search_keywords)
lid.jobs.collect_on_keywords(location='United Kingdom', duration=0, search_keywords=search_keywords)
lid.jobs.collect_on_keywords(location='Germany', duration=0, search_keywords=search_keywords)
lid.jobs.collect_on_keywords(location='France', duration=0, search_keywords=search_keywords)
Netherlands


#============================================================
"""SearchCondition."""
#============================================================

lid.driver.current_url
lid.jobs._detect_nav_search_bar()
lid.jobs.put_search_keyword('Python')
lid.jobs.put_search_location('Spain')
lid.jobs.click_search_button()
lid.jobs.choose_date_posted(0)
lid.jobs.choose_sort_by()

#============================================================
"""Jobdetails."""
#============================================================

lid.jobs.detect_job_details()
lid.jobs.click_job_description_see_more()
lid.jobs.scrollto_applicant_insights_send_feedback()
lid.jobs.scrollto_company_insights_more_company()
lid.jobs.scrollto_commute()
lid.jobs.click_about_us_see_more()

aboutus = lid.driver.find_element_by_xpath('//div[contains(@class, "jobs-company") and contains(@class, "jobs-company--is-truncated")]')
seemore = aboutus.find_element_by_class_name('jobs-company__toggle-to-link')

# button = seemore.find_element_by_tag_name('button')
# ActionChains(lid.driver).move_to_element(button).perform()
# sln.clicker(webelem=button)

wait = WebDriverWait(seemore, 10)
button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
button
button.click()

lid.driver.implicitly_wait(1)
lid.jobs.wait_humanlike_reading_secs()
lid.jobs.act_in_job_details(5)

#============================================================
"""Jobcard."""
#============================================================

lid.jobs._inspect_jobcards()
# lid.jobs.next_jobcard()
# lid.jobs.next_jobcard(2)
lid.jobs.parse_active_jobcard()
# lid.jobs.iter_jobcards()



#============================================================
"""Pagination."""
#============================================================

lid.jobs.pagenum = 1
lid.jobs.pagination_start_dt = datetime.now().astimezone()
# lid.jobs._inspect_pagination()
lid.jobs.click_next_page()

lid.jobs.report_pageloop()

#============================================================
"""LinkedInDefender."""
#============================================================

lid.jobs.if_LinkedIn_is_pranking()
