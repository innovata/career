
import subprocess


print(f"{'='*60}\n\n UnitTest Starts.\n\n{'='*60}\n")


# print(f"{'*'*60}\n stock.krx\n{'*'*60}")
# subprocess.run("python -m unittest -v stock/tests/krx.py", shell=True, check=True)

# print(f"{'*'*60}\n stock.trddate.day\n{'*'*60}")
# subprocess.run("python -m unittest stock/tests/trddata/day.py", shell=True, check=True)

print(f"{'*'*60}\n career.linkedin.jobs\n{'*'*60}")
subprocess.run("python -m unittest career/tests/jobs.py", shell=True, check=True)
