import argparse
import pandas as pd
import time

parser = argparse.ArgumentParser()
parser.add_argument("seconds", type=int)
parser.add_argument("output_dir", type=str)
args = parser.parse_args()

print("Starting countdown")
for i in range(args.seconds, 0, -1):
    print(i)
    time.sleep(1)
print("Countdown finished")

pd.DataFrame({"seconds": [args.seconds]}).to_csv(
    args.output_dir + "/seconds.csv", index=False
)
