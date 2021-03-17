import mne, os
import numpy as np
from mne import set_log_level


set_log_level("ERROR")
os.environ["SUBJECTS_DIR"] = "/home/niherus/Рабочий стол/Seminar_example/freesurfer"
file_num = lambda x: "%s. %s" % (x[0], x[1])


os.chdir("STC_examples")
examples = os.listdir()
print("=" * 100)
print(*map(file_num, enumerate(examples)), sep="\n")


my_stc = mne.read_source_estimate(examples[0])
print("=" * 100)
print(*vars(my_stc).keys(), sep="\n")

# data - 2D numpy array sourses x times
print("=" * 100)
print(my_stc.data)

# data is mutable, so you can use any numpy methods here
# Like this
my_stc.data[0, 0] = 2
print(my_stc.data.shape)

print('''
      first half of sourses is left hemisphere
      second half is right hemisphere
      
      0 - 10241 - left hemi
      10242 - 20484 - right hemi
      ''')

# We have to ways to get data from one hemi (left for example)
# First one
print(my_stc.data[:10242].shape)
# Second one
print(my_stc.lh_data.shape)
# Check if data is same
print(my_stc.data[:10242] == my_stc.lh_data)

# Same for right hemi
# First one
print(my_stc.data[10242:].shape)
# Second one
print(my_stc.rh_data.shape)
# Check if data is same
print(my_stc.data[10242:] == my_stc.rh_data)
print("=" * 100)
# time parames
print(my_stc.times)
# This parametre is immutable. You can't change it
try:
    my_stc.times = np.linspace(-3, 1, 4001)
except Exception as e:
    print(e)

# tmin - start time of the stc
print(my_stc.tmin)

# tmin is muttable. If you change tmin, then times will change too
my_stc.tmin = 2
print(my_stc.tmin)
print(my_stc.times)

# tstep - time step in times
print(my_stc.tstep)

# tstep is muttable. If you change tstep, then times will change too
my_stc.tstep = 2
print(my_stc.tstep)
print(my_stc.times)

# subject - name or id of the subject 
# AND FOLDER NAME with Brain Model
print(my_stc.subject)
# If it's None you can't plot stc with python. You change it
my_stc.subject = "avg_platon_27sub"

# vertices - indexes of of vetices that was taken from the original SourseSpace
print(my_stc.vertices)
# You can get mni coordinates if you would like more in STC_methods
