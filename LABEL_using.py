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
label = mne.read_label("../Label_examples/my_label-lh.label")
my_stc.subject = "avg_platon_27sub"

new = my_stc.in_label(label)

fig = new.plot()
fig.add_label(label)



