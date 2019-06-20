
#============================================================ IDE.
from jupyter.hydrogen import *
#============================================================ Project.
from career import models, PJT_PATH
DATA_PATH = f"{PJT_PATH}/jupyter/data/linkedin/jobs"
import os
#============================================================ Python.
import re
import string
import inspect
from urllib.parse import urlparse, urlencode
import time
import json
from datetime import datetime, timedelta
#============================================================ Data-Science.
import pandas as pd
pd.__version__
from pandas.io.json import json_normalize
import numpy as np
"""NLP."""
# from nltk.tokenize import TweetTokenizer
# from nltk.corpus import stopwords
# from nltk import word_tokenize, pos_tag, DefaultTagger
# from collections import Counter
"""Visualization."""
# import matplotlib
# %matplotlib inline
# import matplotlib.pyplot as plt
#============================================================ My library.
import idebug as dbg



#============================================================
"""Initializer."""
#============================================================

jp = models.LinkedInJobPosting()

#============================================================
"""Data-type Analyzer."""
#============================================================

"""카테고리 컬럼에 대한 분석."""

def analyze_colfreq():
    analysis_cols = jp.schema.copy()
    nlp_cols = ['desc','aboutus']
    etc = ['company_addr','company_logo_url']
    freq_meaningless_cols = jp.listtype_cols + nlp_cols + jp.output
    for e in freq_meaningless_cols:
        if e in analysis_cols:
            analysis_cols.remove(e)

    colfreq_data = []
    for col in analysis_cols:
        values = jp.tbl.distinct(key=col)
        colfreq_data.append({
            'col':col,
            'cnt':len(values),
            'values':values,
        })

    colfreq_df = pd.DataFrame(colfreq_data)
    return colfreq_df.sort_values('cnt'), colfreq_data

df, colfreq_data = analyze_colfreq()
df.sort_values('col')
jndf = json_normalize(colfreq_data, 'values', ['col']).rename(columns={0:'value'})


"""스페인 comunidad 별로 잡포스팅 개수를 분석하는 것도 의미가 있을 듯."""

jndf.query('col == "title"').sort_values('value')

#============================================================
"""Skill-Terms-Analyzer."""
#============================================================

from career.linkedin import jobs
importlib.reload(jobs)
ska = jobs.SkillAnalyzer()


"""match_skills 에 대한 검색지역별 격차를 보여준다."""
es_skilldf = ska.listcol_valfreq_df(col='match_skills',search_location='spain')
uk_skilldf = ska.listcol_valfreq_df(col='match_skills',search_location='united')



#============================================================
"""Data-Preparation."""
#============================================================

freqdf = ska.make_skillfreq_df()
freqdf[:10]


#============================================================
"""Compare with my skills."""
#============================================================

myskilldf = pd.read_csv(f"{DATA_PATH}/myskills.csv")
myskilldf
myskills = myskilldf.skill.to_list()
TF = freqdf.index.isin(myskills)
freqdf[TF]


"""데이터 분리."""

applicant_0 = freqdf.query('applicantskill == 0')
len(applicant_0)
applicant_1 = freqdf.query('applicantskill > 0')
len(applicant_1)


applicant_0.sort_values('matchskill',ascending=False).head(50)
applicant_1.sort_values('matchskill',ascending=False).head(50)


freqdf.query('applicantskill == 0').query('matchskill >= 50').sort_values('matchskill',ascending=False)
freqdf
# freqdf.to_csv(f"{DATA_PATH}/freqdf.csv",index=True)

#============================================================
"""회사들이 원하는 skills 과 지원자들의 보유 skills 간의 분포 격차를 히스토그램으로 보여준다."""
#============================================================



#============================================================
"""Bar-Chart"""
#============================================================
bardf = ska.deindex(df=applicant_1)
title="Companies' wanted skills vs Applicants' skills"
ska.plot_bar(df=bardf[100:200], title=title, ylabel='Freq')
dpi = 300
title = title.replace("'",'').replace(' ','-')
ska.fig.savefig(f"{DATA_PATH}/{title}__{dpi}.png", dpi=dpi)
bardf[:100]


#============================================================
"""Scatter"""
#============================================================

scttdf = ska.deindex(applicant_1)
title = "Applicants' skills scatter based on Companies' requiring skills"
xlabel = "Skill id"
ylabel = "Freq"
ska.plot_scatter(scttdf,title,xlabel,ylabel)
dpi = 300
title = title.replace("'",'').replace(' ','-')
ska.fig.savefig(f"{DATA_PATH}/{title}__{dpi}.png", dpi=dpi)
scttdf[:10]
scttdf.query('applicantskill > 1500')

scttdf = ska.deindex(df=applicant_1.sort_values('applicantskill',ascending=False))
title = "Companies' requiring skills scatter based on Applicants' skills"
ylabel = "Freq"
ska.plot_scatter(scttdf, title, xlabel, ylabel)
dpi = 300
title = title.replace("'",'').replace(' ','-')
ska.fig.savefig(f"{DATA_PATH}/{title}__{dpi}.png", dpi=dpi)
scttdf[:10]

scttdf.query('matchskill > 250')
scttdf[99:105]
scttdf[220:]



#============================================================
"""어떤 산업군에 속한 회사가 얼마만큼의 job-posting을 했는지 보여준다."""
#============================================================

indusdf = ska.listcol_valfreq_df(col='industries')
indusdf
jobfuncdf = ska.listcol_valfreq_df(col='job_functions')
jobfuncdf
for i, col in enumerate(jp.listtype_cols):
    print(f"{'-'*60} i:{i} | col:{col}")
    tfdf = term_freq_df(df, col)
    # tfdf = tfdf.set_index('freq', drop=False)
    for k, e in enumerate(list(tfdf.columns)):
        if e == 'freq':
            pass
        else:
            reportdf = tfdf.reindex(columns=[e, 'freq']).groupby(e).count().sort_values(by='freq', ascending=False)
            print(f"{'- '*30} k:{k} | e:{e}\n{reportdf}")



filter = {'desc':{'$ne':None}, 'html':{'$ne':None}}
# filter = {'collect_dt':{'$gte':datetime(2019,5,21)}}
jp.find(filter, {'html':0, 'search_location':0})
len(jp.docs)

df = jp.get_df()
df = df.set_index('collect_dt', drop=False).sort_index()
df.tail(1).T

for col in jp.listtype_cols:
    df[col] = df[col].apply(lambda x: x if isinstance(x,list) else [])

for col in jp.listtype_cols:
    df[col] = df[col].apply(lambda x: [{col:e} for e in x if len(x) is not 0])

# data = df.reindex(columns=['match_skills','title']).to_dict('records')
# json_normalize(data, record_path='match_skills',meta=['title'],record_prefix='match_')
data = df.to_dict('records')
jndf = json_normalize(data)
jndf.tail(1).T



# filter = {'match_skills':{'$all':['Rhapsody']}}
# filter = {'search_keyword':{'$regex':'Machine','$options':'i'}}
# filter = {}
# df = jp.load(filter,{'_id':0}).get_df()
# len(df)
# df.info()





def pattern_handler(target_col='skills_match'):
    jp.load({'skills':{'$ne':None}}, {'_id':1, 'skills':1})
    len(jp.docs)
    p_job_match_skills_ratio = re.compile('\d+/\d+ skills match')
    p_job_applicants = re.compile('\d+ applicant[s]*')
    for d in jp.docs:
        jp.attributize(d)
        if p_job_match_skills_ratio.search(string=jp.skills_match) is not None:
            d['job_match_skills_ratio'] = jp.skills_match
            d['skills_match'] = None
            jp.update_one({'_id':jp._id}, {'$set':d}, False)
        if p_job_applicants.search(string=jp.skills_match) is not None:
            d['job_applicants'] = jp.skills_match
            d['skills_match'] = None
            jp.update_one({'_id':jp._id}, {'$set':d}, False)
    jp.update_many({}, {'$unset':{'skills_match':''}})

def column_mig_handler(src_col='skills', dst_col='match_skills'):
    jp.load({'skills':{'$ne':None}}, {'_id':1, 'skills':1})
    len(jp.docs)
    for d in jp.docs:
        jp.attributize(d)
        if len(jp.skills) is not 0:
            d['match_skills'] = jp.skills
            d['skills'] = None
            jp.update_one({'_id':jp._id}, {'$set':d}, False)
    jp.update_many({}, {'$unset':{'skills':''}})




"""전체 job-postings 에 대해 skills 를 분석."""



def treat_compound_nouns(text, terms):

    terms = list(set(terms))
    for term in terms:
        repl = term.replace(' ','-')
        text, numberof = re.subn(term, repl=repl, string=text, flags=re.I)
    return text

def report_termfreq_about_NL_of_1company(df, companyname_pat='modis', target='desc', terms=None):
    """특정회사의 job-description, about-us 등 장문에 대한 term-freq 분석."""
    df = df.reindex(columns=['companyname','desc','aboutus']).applymap(lambda x: None if x is np.nan else x)
    TF = df.companyname.str.contains(pat=companyname_pat, flags=re.I)
    jp.attributize(df[TF].to_dict('records')[0])
    print(f"{'*'*60}\n companynames :\n{df[TF].companyname}\n companyname : {jp.companyname}\n")
    if hasattr(jp, target) and getattr(jp, target) is not None:
        text = getattr(jp, target)
        if terms is not None:
            text = treat_compound_nouns(text, terms)
        print(text)
        tokens = TweetTokenizer().tokenize(text)
        if len(tokens) is not 0:
            tokens = [tok.lower() for tok in tokens]
            stwords = stopwords.words('english') + stopwords.words('spanish')
            tokens = [tok for tok in tokens if tok not in stwords]
            tokens = [tok.replace('-',' ') if '-' in tok else tok for tok in tokens ]
            tokens = [tok for tok in tokens if tok[:1].isalpha() is True]
            return report_freq(tokens)
    else:
        print(f"{'#'*60}\n hasattr(jp, {target}) is {hasattr(jp, target)},\n getattr(jp, {target}) is {getattr(jp, target)}.")

#
#
# report_termfreq_about_NL_of_1company(df, 'vistaprint', 'desc', skills)
#
#
# os.path.split('favicon.ico')
#
# root, ext = os.path.splitext('favicon.ico')
# ext[1:]
