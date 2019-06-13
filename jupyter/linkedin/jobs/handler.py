
from jupyter.hydrogen import *
from career.linkedin import jobs
from pymongo import ASCENDING, DESCENDING

#============================================================
"""Initialize | Reload."""
#============================================================

importlib.reload(jobs)
dup = jobs.Deduplicator()

# sorted(dup.__dict__)
# dir(dup)

#============================================================
"""."""
#============================================================
# dup.filter
# dup.cols_order
# dup.cursor = dup.tbl.find(dup.filter).limit(5).sort('collect_dt', ASCENDING)
# dup.load()
# dup.get_df()
dup.load_targets()
# print(f"\n Sample df :\n{df[:1].reindex(columns=self.cols_order)}")

dup.review_dup_df()
dup.delete_dup_data()
