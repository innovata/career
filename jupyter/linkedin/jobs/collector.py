
from jupyter.hydrogen import *
from selenium import webdriver
from career import linkedin
from datetime import datetime
%env USERID=innovata@naver.com
%env PW=abc54321


#============================================================
"""Initialize."""
#============================================================

driver = webdriver.Chrome()

lid = linkedin.LinkedInDriver(driver)
# lid.logined = True
lid.login('loginpage')
lid.setup_services()

#============================================================
"""Reload."""
#============================================================

importlib.reload(linkedin.driver)
importlib.reload(linkedin.jobs)
importlib.reload(linkedin)
lid.jobs = linkedin.jobs.JobsDriver(driver)

#============================================================
"""JobsDriver."""
#============================================================

# sorted(dir(lid.jobs))
lid.jobs.collect_dt = datetime.now().astimezone()
lid.jobs.move_to_job_search_page()
lid.jobs.put_searching_keyword(keyword='Data Analysis',location='United Kingdom')
lid.jobs.choose_date_posted(duration=0)
lid.jobs.choose_sort_by()
lid.jobs.extract_keyword_location()
lid.jobs.is_readyto_collect()
lid.jobs.iter_pagination()

lid.jobs.collect_on_keyword(keyword='Data Analysis', location='United Kingdom', duration=0)
# lid.jobs.collect_on_keyword(keyword='natural language processing', location='Spain', duration=0)
lid.jobs.collect_on_keyword(keyword='data engineer', location='Spain', duration=0)

search_keywords = [
    # 'Data Analytics',
    # 'Data Analysis',
    # 'Data Scientist',
    'Data Science',
    'Data Engineer',
    'Machine Learning',
    'Artificial Intelligence (AI)',
    'Natural Language Processing',
    'Business Intelligence (bi)',
    'Python',
    'Node.js',
]
lid.jobs.collect_on_keywords(location='Spain', duration=0, search_keywords=search_keywords)
lid.jobs.collect_on_keywords(location='United Kingdom', duration=0, search_keywords=search_keywords)


#============================================================
"""Jobdetails."""
#============================================================

lid.jobs.click_job_description_see_more()
lid.jobs.moveto_applicant_insights_send_feedback()
lid.jobs.moveto_company_insights_more_company()
lid.jobs.click_about_us_see_more()

#============================================================
"""Jobcard."""
#============================================================

lid.jobs.detect_jobcards()

#============================================================
"""Pagination."""
#============================================================

lid.jobs.detect_pagination()
lid.jobs.find_selected_page()
lid.jobs.click_next_page()
lid.jobs.report_pageloop()
