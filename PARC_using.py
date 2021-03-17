
import mne, os
import numpy as np
from mne import set_log_level
from surfer import Brain
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

#ris = "show all parc"
ris = "show a few labels from parc"

if ris == "show all parc":
    fig = my_stc.plot()
    fig.add_annotation("aparc.a2009s") # adding parcelation. 
    # To find other parcellation check ../freesurfer/avg_platon_27sub/label
   
elif ris == "show a few labels from parc":
    list_of_labels = mne.read_labels_from_annot("avg_platon_27sub", "aparc.a2009s", "lh") # reading parcellation. 
    # To find other parcellation check ../freesurfer/avg_platon_27sub/label
    fig = my_stc.plot()
    
    for lab in list_of_labels:
        if "temp" in lab.name: # condition to check relevant labels from parcellation
            fig.add_label(lab, borders=True)


