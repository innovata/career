
import unittest
from career.linkedin.jobs import *
import pprint
pp = pprint.PrettyPrinter(indent=2)


@unittest.skip("showing class skipping")
class JobsDriverTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        jd = JobsDriver(driver='driver')
        attrs = [
            'base_url','search_keywords',
            'keywords_writing_secs','searchbutton_click_secs',
            'scroll_to_see_more_secs','scroll_to_premium_block_secs','job_details_human_reading_secs','job_details_ajax_waiting_secs',
        ]
        dirs = sorted(dir(jd))
        for attr in attrs:
            self.assertTrue(attr in dirs)


# @unittest.skip("showing class skipping")
class HTMLParserTestCase(unittest.TestCase):

    def setUp(self):
        self.p = HTMLParser()
        self.p.cursor = self.p.tbl.find(self.p.filter, self.p.projection).limit(100)
        self.p.load(True)

    #@unittest.skip("demonstrating skipping")
    def test__topcard(self):
        self.p.schema = self.p.parse_cols
        docslen = len(self.p.docs)
        for i, d in enumerate(self.p.docs, start=1):
            print(f"{'- '*60} {i}/{docslen}")
            self.p.attributize(d)
            self.p.soup = BeautifulSoup(self.p.html, 'html.parser')
            ############################################################Top-Card
            self.p.job_title()
            self.p._companyname()
            self.p.job_location()
            self.p.company_logo()
            self.p._posted_time_ago()
            self.p._n_views()
            ############################################################Job-Summary-3-boxes
            self.p.job_box()
            self.p.companyinfo_box()
            self.p._connections()
            ############################################################Job-Description
            self.p.job_description()
            self.p._seniority_level_in_job_description()
            self.p._industries()
            self.p._employment_type()
            self.p._job_functions()
            self.p.how_you_match()
            ############################################################Competitive_intelligence_about_applicants
            self.p._applicant_for_this_job()
            self.p._applicant_topskills()
            self.p._applicant_seniority_levels()
            self.p._applicant_educations()
            self.p._applicant_locations()
            ############################################################Insight_look_at_company
            self.p.hiring_trend()
            self.p._tenure()
            ############################################################Ecetera
            self.p.commute()
            self.p._about_us()
            ############################################################PPrint
            self.p.schematize().doc.update({'desc':'Description'})
            pp.pprint( self.p.doc )



if __name__ == '__main__':
    unittest.main()
