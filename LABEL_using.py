import mne, os
import numpy as np
from mne import set_log_level
import matplotlib.pyplot as plt
set_log_level("ERROR")
os.environ["SUBJECTS_DIR"] = "/home/niherus/Рабочий стол/Seminar_example/freesurfer"
file_num = lambda x: "%s. %s" % (x[0], x[1])


os.chdir("STC_examples")
examples = os.listdir()
print("=" * 100)
print(*map(file_num, enumerate(examples)), sep="\n")

my_stc = mne.read_source_estimate(examples[0])
my_stc.subject = "avg_platon_27sub" 

 # read label file
label = mne.read_label("../Label_examples/my_label-lh.label") 

ris = "get activity just in label"

if ris == 'get activity just in label':
       
    # get activity just in label
    my_stc = my_stc.in_label(label) 
    fig = my_stc.plot()
    
elif ris == "add label on brain model":
    
    fig = my_stc.plot()
    # add label on brain model"
    fig.add_label(label, borders=True) # border - show borders or not








