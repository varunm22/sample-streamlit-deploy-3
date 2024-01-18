import os
import pandas as pd
import streamlit as st
import time
from code_package.streamlit.util.google_oauth import oauth
from code_package.util.batch import submit_batch_job, get_job_status
from code_package.util.cloud import s3_ls, read_yml_from_s3, write_yml_to_s3

RESULTS_DIR = "s3://varun-streamlit-apps/first_app/"
MAX_JOBS_TO_SHOW = 20

oauth()

st.title("First streamlit app")

action = st.selectbox("Select action", ["Launch Job", "Check Job Status"])
if action == "Launch Job":
    job_name = st.text_input("Enter job name", "countdown-test")
    seconds = st.slider("Select how many seconds", 1, 60, 5)
    if st.button("Launch job"):
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        job_dir = os.path.join(RESULTS_DIR, timestamp + "_" + job_name)
        job_id = submit_batch_job(
            f"python code_package/countdown/countdown.py {seconds}",
            job_name,
        )
        write_yml_to_s3(
            {"job_id": job_id, "job_name": job_name, "seconds": seconds},
            job_dir + "/job.yml",
        )
        st.write(f"Job launched")

elif action == "Check Job Status":
    jobs = s3_ls(RESULTS_DIR)
    for job in list(reversed(jobs))[:MAX_JOBS_TO_SHOW]:
        with st.expander(job.split("/")[-2]):
            job_info = read_yml_from_s3(job + "job.yml")
            st.write(f"Job name: {job_info['job_name']}")
            st.write(f"Status: {get_job_status(job_info['job_id'])}")
            try:
                results = pd.read_csv(job + "seconds.csv")
                st.write(f"Results: {results}")
            except:
                st.write("Results missing or unreadable")
