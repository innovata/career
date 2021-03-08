
from jupyter.hydrogen import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from career import linkedin
from datetime import datetime


#============================================================
"""Initialize."""
#============================================================

driver = webdriver.Chrome()
lid = linkedin.LinkedInDriver(driver)
lid.login('loginpage')
lid.logined = True

#============================================================
"""Reload."""
#============================================================

importlib.reload(linkedin.driver)
importlib.reload(linkedin)
lid.profile = linkedin.profile.ProfileDriver(driver)
lid.setup_services()

#============================================================
"""ProfileDriver | Skills."""
#============================================================

pfd = lid.profile

pfd.driver.get(pfd.url)
pfd.scrolldown_upto_bottom()
pfd.click_editskill()
skills = pfd.collect_skills()
sorted(skills)
pd.DataFrame({'skill':skills}).to_csv(f"{PJT_PATH}/jupyter/data/myskills.csv", index=False)
