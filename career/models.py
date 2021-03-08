
from career import mongo_v2 as mongo
import pandas as pd
import inspect
from pandas.io.json import json_normalize


#============================================================
"""LinkedIn"""
#============================================================

def submodeling(obj, *args):
    submodel = "_".join(args)
    obj.submodel = f"{obj.modelname}__{submodel}"
    obj.tblname = obj.submodel
    return obj

class LinkedInJobPosting(mongo.Model):

    def __init__(self):
        super().__init__(__class__)
        self.inputs = ['search_keyword','search_location','collect_dt']
        self.output = ['html']
        ############################################################
        self.jobcard_cols = ['title','companyname','location']
        top_card = ['posted_time_ago','n_views','company_logo_url']
        self.topcard_cols = self.jobcard_cols + top_card
        job_summary = ['skills_match_ratio','skills_match_pct','n_applicants','job_level','rng_employees','n_employees','company_cate','connections']
        job_description = ['desc']
        job_description_details = ['seniority_level','industries','employment_type','job_functions']
        how_you_match = ['match_skills']
        applicant_insights = ['applicant_topskills','applicant_seniority_levels','applicant_educations','applicant_locations']
        self.company_insights = ['total_employees','company_growthrate','sector_growthrate','tenure']
        commute_aboutus = ['commute_addr','about_us']
        self.data_cols = top_card + job_summary + job_description + job_description_details + how_you_match + applicant_insights + self.company_insights + commute_aboutus
        ############################################################
        self.dt_cols = ['collect_dt','posted_time_ago','posted_dt']
        self.num_cols = ['n_views','skills_match_ratio','skills_match_pct','n_applicants','n_employees','total_employees','company_growthrate','sector_growthrate','tenure']
        self.cate_cols = ['search_keyword','search_location'] + self.jobcard_cols + ['company_logo_url','job_level','rng_employees','company_cate','seniority_level','employment_type']
        self.str_cols = job_description + commute_aboutus
        self.listtype_cols = ['industries','job_functions','match_skills','applicant_topskills']
        self.dicstype_cols = ['connections','applicant_seniority_levels','applicant_educations','applicant_locations']
        ############################################################
        self.collect_cols = self.inputs + self.output + self.jobcard_cols
        self.dedup1_cols = self.inputs + self.jobcard_cols + ['posted_time_ago']
        self.parse_cols = ['_id'] + self.data_cols
        self.dedup2_cols = ['search_keyword','search_location'] + self.jobcard_cols + ['posted_dt']
        self.analyze_cols = self.dt_cols + self.num_cols + self.cate_cols + self.str_cols + self.listtype_cols + self.dicstype_cols
        self.analyze_cols.remove('posted_time_ago')
