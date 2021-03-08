
from jupyter.hydrogen import *
from career.linkedin import jobs
import idebug as dbg
import inspect
from bs4 import BeautifulSoup
import re
from career import models


#============================================================
"""Initialize | Reload."""
#============================================================

importlib.reload(models)
importlib.reload(jobs)
self = jobs.HTMLParser()


#============================================================
"""HTMLParser."""
#============================================================

"""load_targets."""

# self.load_targets()
self.filter
self.projection
self.cursor = self.tbl.find(self.filter, self.projection).limit(100)
self.load(True)


# ------------------------------------------------------------
# company_logo
# ------------------------------------------------------------

company_logo_urls = []
for i,d in enumerate(self.docs):
    self.attributize(d)
    self.soup = BeautifulSoup(self.html, 'html.parser')
    ############################################################
    s = self.soup.find('div', class_='jobs-details-top-card__company-logo-container')
    if s is None:
        print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'jobs-details-top-card__company-logo-container' is None.")
    else:
        img = s.find('img')
        if img is None:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n 'img-tag' is None.")
        else:
            if 'src' in list(img.attrs):
                print(f" i : {i}")
                self.company_logo_url = img.attrs['src']
                company_logo_urls.append(self.company_logo_url)
    ############################################################
company_logo_urls

# ------------------------------------------------------------
# n_views
# ------------------------------------------------------------

d = self.docs[0]
# d
self.soup = BeautifulSoup(d['html'], 'html.parser')
s = self.soup.find('div',attrs={'data-test-job-summary-type':'company-list'})
print(s.prettify())
# s = self.soup.find(class_='jobs-details-top-card__job-info')
# s = self.soup.find('a', class_='jobs-details-top-card__company-url')
# print(s.prettify())
self.company_box()
self.schematize().doc
string = '1,001-5,000 employees'
p_n_employees_rng = re.compile('^([\d,]+)\s*(employee[s]*)')
m = p_n_employees_rng.search(string)
m.groups()
m1 = m.groups()[0].split('-')
m1

# ------------------------------------------------------------
# companyinfo_box
# ------------------------------------------------------------

company_cates = []
rng_employees_li = []
n_employees_li = []
for i,d in enumerate(self.docs):
    self.attributize(d)
    self.soup = BeautifulSoup(self.html, 'html.parser')
    ############################################################
    try:
        s = self.soup.find('div',attrs={'data-test-job-summary-type':'company-list'})
    except Exception as e:
        print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Exception : {e}")
    else:
        items = s.find_all('li')
        for item in items:
            text = item.get_text().strip()
            m = self.p_rng_employees.search(string=text)
            if m is None:
                self.company_cate = text
                company_cates.append(self.company_cate)
            else:
                self.rng_employees= m.groups()[0]
                if len(self.rng_employees.split('-')) is 2:
                    min = self.cleaner.purify_number(self.rng_employees.split('-')[0])
                    max = self.cleaner.purify_number(self.rng_employees.split('-')[1])
                    self.n_employees = round((min + max)/2, 0)
                else:
                    self.n_employees = self.cleaner.n_employees(self.rng_employees)
                rng_employees_li.append(self.rng_employees)
                n_employees_li.append(self.n_employees)
    ############################################################
company_cates
rng_employees_li
n_employees_li

"""parse."""






for k, v in self.schematize().doc.items():
    print(f"{'-'*60}\n {k} : {type(v)}")
# self.update_doc({'_id':d['_id']}, False)
pp.pprint(new_docs[0])

self.docs = new_docs
df = self.get_df()
len(df)

def inspect_specific_row_dtype(df, row):
    sampledf = df[row:row+1].T
    print(f"len(sampledf)===n_cols : {len(sampledf)}")
    sampledf['dtype'] = sampledf.rename(columns={row:'one'}).one.apply(lambda x: type(x))
    return sampledf.reindex(columns=['dtype',0])

inspect_specific_row_dtype(df, 8)
# df.match_skills
df.info()
df

#============================================================
"""2차 Parser."""
#============================================================
