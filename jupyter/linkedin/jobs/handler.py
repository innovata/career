
#============================================================ IDE.
from jupyter.hydrogen import *
#============================================================ Project.
from career.linkedin import jobs
#============================================================ Python.
import re
#============================================================ Data-Science.
from pymongo import ASCENDING, DESCENDING



#============================================================
"""Initialize | Reload."""
#============================================================

importlib.reload(jobs)
dup = jobs.Deduplicator(phase=2)

# sorted(dup.__dict__)
# dir(dup)

#============================================================
"""1차-Handler."""
#============================================================
# dup.filter
# dup.cols_order
# dup.cursor = dup.tbl.find(dup.filter).limit(5).sort('collect_dt', ASCENDING)
# dup.load()
# dup.get_df()
dup.load_targets()
# print(f"\n Sample df :\n{df[:1].reindex(columns=self.cols_order)}")

df1, df2 = dup.inspect_dup_df()
dup.delete_dup_data()

#============================================================
"""1차 중복제거 후 검사."""
#============================================================

ids = self.tbl.distinct('_id', {'html':{'$ne':None}})
len(ids)
ids = self.tbl.distinct('_id', {'html':None})
len(ids)
ids = self.tbl.distinct('_id', {'html':{'$ne':None}, 'collect_dt':{'$ne':None}})
len(ids)
ids = self.tbl.distinct('_id', {'html':{'$ne':None}, 'collect_dt':None})
len(ids)
ids = self.tbl.distinct('_id', {'html':{'$ne':None}, 'collect_dt':{'$ne':None}, 'posted_dt':{'$ne':None}})
len(ids)
ids = self.tbl.distinct('_id', {'html':{'$ne':None}, 'collect_dt':{'$ne':None}, 'posted_dt':None})
len(ids)


#============================================================
"""2차-Handler."""
#============================================================


dup.load_targets()


df1, df2 = dup.inspect_dup_df()
df1.info()
df2
len(dup.deleting_ids)
dup.delete_dup_data()

dup.report_status_after_1st_dedup()


#============================================================
"""n_employees Handler."""
#============================================================

jp = models.LinkedInJobPosting()
jp.schema = ['_id','rng_employees','n_employees']
dvc = jobs.DataValueCleaner()


# filter = {'rng_employees':'10001'}
# set = {'$set':{'rng_employees':'10,001'}}
# UpdateResult = jp.tbl.update_many(filter, set, upsert=False)
# dbg.UpdateResult(UpdateResult, caller="")

filter = {'rng_employees':{'$type':'int'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find(filter, projection)
jp.load(True)
df = jp.get_df()
df.info()
df = df.fillna('_None')
df.groupby('n_employees').count()
def inspect_failed_to_n_employees():
    jp.cursor = jp.tbl.find({'n_employees':''})
    jp.load(True)
    jp.get_df()


# p_num_str_mix = re.compile('(\d+[./-,]*\d*)\s*([a-zA-Z]+)')
p_rng_employees1 = re.compile('([\d,-]+)\s*(employee[s]*)')
p_rng_employees2 = re.compile('([\d,-]+)\s*(.*)')

for i,d in enumerate(jp.docs):
    jp.attributize(d)
    m = p_rng_employees2.search(jp.rng_employees)
    if m is None:
        # print(f" i : {i}")
        # print(f" rng_employees : {jp.rng_employees}")
        pass
    else:
        print(f" i : {i}")
        jp.rng_employees = m.groups()[0]
        if len(jp.rng_employees.split('-')) is 1:
            jp.n_employees = dvc.n_employees(jp.rng_employees)
        else:
            min = jp.rng_employees.split('-')[0]
            max = jp.rng_employees.split('-')[1]
            min = dvc.n_employees(min)
            max = dvc.n_employees(max)
            jp.n_employees = round((min + max)/2, 0)
        print(f" p_rng_employees : {m.groups()}\n n_employees : {jp.n_employees}\n rng_employees : {jp.rng_employees}")
        jp.update_doc(filter={'_id':jp._id}, upsert=False)


#============================================================
"""n_applicants Handler."""
#============================================================

jp = models.LinkedInJobPosting()
jp.schema = ['_id','n_applicants']
dvc = jobs.DataValueCleaner()

filter = {'n_applicants':{'$type':'string'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find(filter, projection)
jp.load(True)
df = jp.get_df()
df.info()

p_n_applicants = re.compile('\d+ applicant[s]*')
for i,d in enumerate(jp.docs):
    jp.attributize(d)
    m = p_rng_employees2.search(jp.n_applicants)
    if m is None:
        pass
    else:
        jp.n_applicants = dvc._purify_number(m.groups()[0])
        # print(f" i : {i}\n m.groups() : {m.groups()}\n n_applicants : {jp.n_applicants}")
        jp.update_doc(filter={'_id':jp._id}, upsert=False)


#============================================================
"""growthrate Handler."""
#============================================================

jp = models.LinkedInJobPosting()
jp.schema = ['_id','sector_growthrate']
dvc = jobs.DataValueCleaner()

filter = {'sector_growthrate':{'$type':'string'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find(filter, projection)
jp.load(True)
df = jp.get_df()
df.info()
df.groupby('sector_growthrate').count()


p_sector_growthrate = re.compile('(\d+%)\s*([a-zA-Z]*)')

for i,d in enumerate(jp.docs):
    jp.attributize(d)
    m = p_sector_growthrate.search(jp.sector_growthrate)
    if m is None:
        """No change"""
        jp.sector_growthrate = 0
    else:
        # print(f" i : {i}\n m.groups() : {m.groups()}")
        pct = m.groups()[0]
        pct = int(pct.replace('%','')) / 100
        updown = m.groups()[1]
        if updown == 'decrease':
            updown = -1
        else:
            updown = +1
        pct = pct * updown
        # print(f" pct : {pct}")
        jp.sector_growthrate = pct
    jp.update_doc(filter={'_id':jp._id}, upsert=False)

#============================================================
"""n_views Handler."""
#============================================================


jp = models.LinkedInJobPosting()
jp.schema = ['_id','n_views']
dvc = jobs.DataValueCleaner()

filter = {'n_views':{'$type':'string'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find({}, projection)
jp.load(True)
df = jp.get_df()
df.info()
df.groupby('n_views').count()

p_views = re.compile('([\d+,]+)\s*(view[s]*)')

for i,d in enumerate(jp.docs):
    jp.attributize(d)
    m = p_views.search(jp.n_views)
    if m is None:
        # print(jp.n_views)
        pass
    else:
        # print(f" i : {i}\n m.groups() : {m.groups()}")
        jp.n_views = dvc._purify_number(m.groups()[0])
        # print(f" n_views : {jp.n_views}")
        jp.update_doc(filter={'_id':jp._id}, upsert=False)


#============================================================
"""skills_match_ratio Handler."""
#============================================================


jp = models.LinkedInJobPosting()
jp.schema = ['_id','skills_match_ratio','skills_match_pct']
dvc = jobs.DataValueCleaner()

filter = {'skills_match_ratio':{'$type':'string'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find({}, projection)
jp.load(True)
df = jp.get_df()
df.info()
df.groupby('skills_match_ratio').count()

p_skills_match_ratio = re.compile('(\d+/\d+)\s*(.*)')

for i,d in enumerate(jp.docs):
    jp.attributize(d)
    m = p_skills_match_ratio.search(jp.skills_match_ratio)
    if m is None:
        # print(jp.skills_match_ratio)
        pass
    else:
        # print(f" i : {i}\n m.groups() : {m.groups()}")
        jp.skills_match_ratio = m.groups()[0]
        nums = jp.skills_match_ratio.split('/')
        jp.skills_match_pct = round(int(nums[0]) / int(nums[1]), 2)
        # print(f" skills_match_pct : {jp.skills_match_pct}")
        jp.update_doc(filter={'_id':jp._id}, upsert=False)



#============================================================
"""tenure Handler."""
#============================================================

jp = models.LinkedInJobPosting()
jp.schema = ['_id','tenure']
dvc = jobs.DataValueCleaner()

filter = {'tenure':{'$type':'string'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find(filter, projection)
jp.load(True)
df = jp.get_df()
df.info()
df.groupby('tenure').count()

p_tenure = re.compile('([\d+\.]+)\s*(.*)')

for i,d in enumerate(jp.docs):
    jp.attributize(d)
    m = p_tenure.search(jp.tenure)
    if m is None:
        print(f" i : {i}")
        print(jp.tenure)
    else:
        # print(f" m.groups() : {m.groups()}")
        jp.tenure = float(m.groups()[0])
        # print(f" tenure : {jp.tenure}")
        jp.update_doc(filter={'_id':jp._id}, upsert=False)



#============================================================
"""total_employees Handler."""
#============================================================

jp = models.LinkedInJobPosting()
jp.schema = ['_id','total_employees']
dvc = jobs.DataValueCleaner()

filter = {'total_employees':{'$type':'string'}}
projection = {e:1 for e in jp.schema}
jp.cursor = jp.tbl.find(filter, projection)
jp.load(True)
df = jp.get_df()
df.info()
df.groupby('total_employees').count()

for i,d in enumerate(jp.docs):
    jp.attributize(d)
    # print(f" i : {i}")
    jp.total_employees = int(jp.total_employees.replace(',',''))
    # print(jp.total_employees)
    jp.update_doc(filter={'_id':jp._id}, upsert=False)
