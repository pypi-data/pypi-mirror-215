"""
list of bash script wrappers, can be run using os.system(script)
"""
def peroid_run_script(script,wait_time):
    return f"while true; do {script}; sleep {wait_time}; done"


# parallel untar
# find . -type f -name '*.tar.gz' -print0 | xargs -0 -P 16 -n1 tar -xvf


