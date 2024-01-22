import argparse
import pandas as pd
import time
from code_package.util.cloud import s3_ls

parser = argparse.ArgumentParser()
parser.add_argument("seconds", type=int)
parser.add_argument("output_dir", type=str)
args = parser.parse_args()

print("Starting countdown")
for i in range(args.seconds, 0, -1):
    print(i)
    time.sleep(1)
print("Countdown finished")

print(s3_ls(args.output_dir))

pd.DataFrame({"seconds": [args.seconds]}).to_csv(args.output_dir + "/seconds.csv")
