
from jupyter.hydrogen import *
from career.linkedin import jobs
import idebug as dbg
import inspect
from bs4 import BeautifulSoup
import re
from career import models

#============================================================
"""Handler."""
#============================================================

filter = {}
update = {'$rename':{'employees':'n_employees'}}
# self.tbl.update_many(filter, update, False)


#============================================================
"""검사."""
#============================================================

ids = self.tbl.distinct('_id', {'html':{'$ne':None}})
len(ids)
ids = self.tbl.distinct('_id', {'html':None})
len(ids)
n_employees = self.tbl.distinct('n_employees')
len(n_employees)
n_employees

#============================================================
"""Initialize | Reload."""
#============================================================

importlib.reload(models)
importlib.reload(jobs)

#============================================================
"""1차."""
#============================================================

self = jobs.HTMLParser()
# self.load_targets()
filter = {'html':{'$ne':None}, 'collect_dt':{'$ne':None}}
# filter = {'html':{'$ne':None}, 'collect_dt':{'$ne':None}, 'companyname':'letgo'}
# filter = {'html':{'$ne':None}, 'collect_dt':{'$ne':None}, 'n_employees':{'$ne':None}}
self.inputs
self.output
self.collect_upsert_keys
projection = {e:1 for e in self.collect_upsert_keys + self.output}
self.cursor = self.tbl.find(filter,projection).limit(10)
self.docs = list(self.cursor)
len(self.docs)
self.get_df()


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




new_docs = []
for i, d in enumerate(self.docs):
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
    new_docs.append(self.schematize().doc.copy())
    # break
# pp.pprint(self.schematize().doc)

# sorted(self.__dict__)

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

importlib.reload(jobs)
self = jobs.DocDataParser()

"""컬럼별 데이터-타입 조사"""

self.tbl.find()

# dir(self)
self.load_targets()
df = self.get_df()
df.dropna(axis=0, how='all', subset=['views'])[:1].T

# df = self.clean_dtcols(self.get_df())
numdf = self.clean_numcols(self.get_df())
numdf0 = numdf.copy()
sorted(self.num_cols)
numdf.info()
numdf

"""숫자+문자열 조합에서 숫자를 추출."""


numdf = numdf0.copy()
numdf =

numdf.sort_values('n_applicants')







text = '6–10 applicants'
text = '1–5 applicants'
p_applicant_location_cnt = re.compile('(\d+\W\d+)\s*(applicant[s]*)')
m = p_applicant_location_cnt.search(string=text)
print(m)
m.groups()
