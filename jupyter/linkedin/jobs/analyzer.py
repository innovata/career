
from jupyter.hydrogen import *
from career import models
import re
import pandas as pd
# import os
import string
import inspect
from pandas.io.json import json_normalize
from urllib.parse import urlparse, urlencode
import time
import json
from datetime import datetime, timedelta
import idebug as dbg
import numpy as np
from career import PJT_PATH
DATA_PATH = f"{PJT_PATH}/jupyter/data"

"""Analyzer-Start"""
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag, DefaultTagger
from collections import Counter
"""Analyzer-End"""


"""Visualizer-Start"""
import matplotlib.pyplot as plt

"""Visualizer-End"""


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

def listcol_valfreq_df(col, search_location=None):
    if col in jp.listtype_cols:
        filter = {col:{'$ne':None}}
        if search_location is not None:
            filter.update({'search_location':{'$regex':search_location,'$options':'i'}})
        jp.cursor = jp.tbl.find(filter, projection={'_id':1, col:1})
        jp.load()

        jndf = json_normalize(jp.docs, col).rename(columns={0:col})
        jndf['freq'] = 1
        return jndf.groupby(col).count().sort_values(by='freq', ascending=False)
    else:
        print(f"입력한 컬럼({col})은 'listtype_cols'에 정의되어 있지 않다.")


"""match_skills 에 대한 검색지역별 격차를 보여준다."""

es_skilldf = listcol_valfreq_df(col='match_skills',search_location='spain')
uk_skilldf = listcol_valfreq_df(col='match_skills',search_location='united')

es_skilldf
uk_skilldf

jp.listtype_cols

#============================================================
"""회사들이 원하는 skills 과 지원자들의 보유 skills 간의 분포 격차를 히스토그램으로 보여준다."""
#============================================================

"""prepare_visualizing_data"""

matchskill_freqdf = listcol_valfreq_df(col='match_skills')
applicantskill_frqdf = listcol_valfreq_df(col='applicant_topskills')

len(matchskill_freqdf)
len(applicantskill_frqdf)
matchskill_freqdf[:1]
applicantskill_frqdf[:1]

matchskill_freqdf.index.name = 'skill'
matchskill_freqdf.index.name
applicantskill_frqdf.index.name = 'skill'
applicantskill_frqdf.index.name

matchskill_freqdf = matchskill_freqdf.rename(columns={'freq':'matchskill'})
applicantskill_frqdf = applicantskill_frqdf.rename(columns={'freq':'applicantskill'})

# pd.concat(objs=[matchskill_freqdf, applicantskill_frqdf], axis=0, join='inner', sort=True).sort_index()
freqdf = matchskill_freqdf.join(applicantskill_frqdf)
freqdf = freqdf.fillna(0)
freqdf = freqdf.applymap(lambda x: int(x))
freqdf.info()
freqdf = freqdf.sort_index()
freqdf.sort_index().T
freqdf[:10]

freqdf.query('applicantskill == 0').query('matchskill >= 50').sort_values('matchskill',ascending=False)
freqdf.query('matchskill == 0')#.query('matchskill > 100').sort_index()


"""Histogram"""


freqdf.to_records(index=False)
array = freqdf.to_numpy()
len(array)
array.shape
list(freqdf.index)[:10]

fig, ax = plt.subplots()
ax.hist(x=freqdf.to_numpy(), bins=len(freqdf), density=False, histtype='bar', label=list(freqdf.index))

# x = np.linspace(-5, 5, 1000)
# ax.plot(x, 1 / np.sqrt(2*np.pi) * np.exp(-(x**2)/2), linewidth=4)
ax.set_xticks([])
ax.set_yticks([])
fig.savefig(f"{DATA_PATH}/histogram_frontpage.png", dpi=500)


"""Bar-chart"""

ind = np.arange(len(freqdf))  # the x locations for the groups
width = 0.1  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(x=ind - width/2, height=list(freqdf.matchskill), width=0.8)
rects2 = ax.bar(x=ind + width/2, height=list(freqdf.applicantskill), width=0.8)

ax.set_ylabel('Freq')
ax.set_title("Companies' desired skills vs Applicants' skills")
ax.set_xticks(ind)
ax.set_xticklabels(list(freqdf.index))
ax.legend()
def autolabel(rects, xpos='center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')

autolabel(rects1, "left")
autolabel(rects2, "right")

fig.tight_layout()
# plt.show()
dpi = 2000
fig.savefig(f"{DATA_PATH}/Grouped-bar-chart-with-labels__{dpi}.png", dpi=dpi)


#============================================================
"""어떤 산업군에 속한 회사가 얼마만큼의 job-posting을 했는지 보여준다."""
#============================================================

listcol_valfreq_df(col='industries')

listcol_valfreq_df(col='job_functions')

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
