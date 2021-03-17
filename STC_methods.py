import mne, os
import numpy as np
from mne import set_log_level
from scipy import stats
from statsmodels.stats import multitest as mul

def signed_p_val(t, p_val):

   if t >= 0:
      return 1 - p_val
   else:
      return -(1 - p_val)


set_log_level("ERROR")
os.environ["SUBJECTS_DIR"] = "/home/niherus/Рабочий стол/Seminar_example/freesurfer"
file_num = lambda x: "%s. %s" % (x[0], x[1])


os.chdir("STC_examples")
examples = os.listdir()
print("=" * 100)
print(*map(file_num, enumerate(examples)), sep="\n")

my_stc = mne.read_source_estimate(examples[0])

print("=" * 100)

func_fil = lambda x: x not in vars(my_stc).keys() and "_" not in x
print("Main methods of stc")
print(*filter(func_fil, dir(my_stc)), sep="\n")

# copy 
# if you want edit dublicate of your stc and don't want spoil your origin stc
# you can't just assign your stc data to new variable
print("demonstration with simple assignment")
my_stc2 = my_stc
print("my_stc", my_stc.tmin)
print("my_stc2", my_stc.tmin)
my_stc.tmin = 3

print("my_stc", my_stc.tmin)
print("my_stc2", my_stc2.tmin)

# Same will be with any other parameters
my_stc = mne.read_source_estimate(examples[0])
# to avoid this situation use copy
print("demonstration with assignment with copy")

my_stc2 = my_stc.copy()
print("my_stc", my_stc.tmin)
print("my_stc2", my_stc.tmin)
my_stc.tmin = 3

print("my_stc", my_stc.tmin)
print("my_stc2", my_stc2.tmin)
print("=" * 100)

my_stc = mne.read_source_estimate(examples[0])
# crop - methods for cutting specific part of your data in time range

print(my_stc.shape)
print(my_stc.tmin)
my_stc = my_stc.crop(tmin=-0.5, tmax=1.5)
print(my_stc.shape)
print(my_stc.tmin)

print("=" * 100)
my_stc = mne.read_source_estimate(examples[0])
# resample - if you want change your sample rate (in Hz)
print(my_stc.shape)
my_stc = my_stc.resample(50)
print(my_stc.shape)

print("=" * 100)
# save - if you want to save new stc after editing
my_stc.save("new_stc")

# mean, sqrt, sum do the same as in numpy
print(my_stc.mean()) # mean all timerange
print(my_stc.sum()) # sum all timerange 
print(my_stc.sqrt()) # sqrt all timerange BE WARE OF NEGATIVE VALUE!!!
print("=" * 100)
my_stc = mne.read_source_estimate(examples[0])
# apply_baseline - if you want to substract baseline (only substract, there
# is no other mode of applying baseline)
print("before", my_stc.data[200, 50])
my_stc = my_stc.apply_baseline(baseline=(1.0, 1.5))
print("after", my_stc.data[200, 50])

# plot to show your stc file
# DON'T FORGET TO SET SUBJECT NAME and SUBJECTS_DIR system variable
my_stc.subject = "avg_platon_27sub"
#my_stc.plot()
fig = my_stc.plot(surface="inflated", show=False) 
# To find other surface check ../freesurfer/avg_platon_27sub/surf

# if you want to save one picture
fig.save_image("my_sreen.png") #‘pyvista’
#fig.save("my_sreen.png") #NO ‘pyvista’

'''
Parameters

    surface: str

        The type of surface (inflated, white etc.).
    hemi: str

        Hemisphere id (ie ‘lh’, ‘rh’, ‘both’, or ‘split’). In the case of ‘both’, both hemispheres are shown in the same window. In the case of ‘split’ hemispheres are displayed side-by-side in different viewing panes.
    colormap: str | np.ndarray of float, shape(n_colors, 3 | 4)

        Name of colormap to use or a custom look up table. If array, must be (n x 3) or (n x 4) array for with RGB or RGBA values between 0 and 255. The default (‘auto’) uses ‘hot’ for one-sided data and ‘mne’ for two-sided data.
    time_label: str | callable() | None

        Format of the time label (a format string, a function that maps floating point time values to strings, or None for no label). The default is 'auto', which will use time=%0.2f ms if there is more than one time point.
    smoothing_steps: int

        The amount of smoothing.
    transparent: bool | None

        If True: use a linear transparency between fmin and fmid and make values below fmin fully transparent (symmetrically for divergent colormaps). None will choose automatically based on colormap type.

    time_viewer: bool | str

        Display time viewer GUI. Can also be ‘auto’, which will mean True for the PyVista backend and False otherwise.

        Changed in version 0.20.0: “auto” mode added.


    figure instance of mayavi.core.api.Scene | instance of matplotlib.figure.Figure | list | int | None

        If None, a new figure will be created. If multiple views or a split view is requested, this must be a list of the appropriate length. If int is provided it will be used to identify the Mayavi figure by it’s id or create a new figure with the given id. If an instance of matplotlib figure, mpl backend is used for plotting.
    views str | list

        View to use. Can be any of:

        ['lateral', 'medial', 'rostral', 'caudal', 'dorsal', 'ventral',
         'frontal', 'parietal', 'axial', 'sagittal', 'coronal']

        Three letter abbreviations (e.g., 'lat') are also supported. Using multiple views (list) is not supported for mpl backend.

        When plotting a standard SourceEstimate (not volume, mixed, or vector) and using the PyVista backend, views='flat' is also supported to plot cortex as a flatmap.

        Changed in version 0.21.0: Support for flatmaps.
    colorbar bool

        If True, display colorbar on scene.
    clim str | dict

        Colorbar properties specification. If ‘auto’, set clim automatically based on data percentiles. If dict, should contain:

            kind‘value’ | ‘percent’

                Flag to specify type of limits.
            limslist | np.ndarray | tuple of float, 3 elements

                Lower, middle, and upper bounds for colormap.
            pos_limslist | np.ndarray | tuple of float, 3 elements

                Lower, middle, and upper bound for colormap. Positive values will be mirrored directly across zero during colormap construction to obtain negative control points.

        Note

        Only one of lims or pos_lims should be provided. Only sequential colormaps should be used with lims, and only divergent colormaps should be used with pos_lims.
    cortexstr or tuple

        Specifies how binarized curvature values are rendered. Either the name of a preset PySurfer cortex colorscheme (one of ‘classic’, ‘bone’, ‘low_contrast’, or ‘high_contrast’), or the name of mayavi colormap, or a tuple with values (colormap, min, max, reverse) to fully specify the curvature colors. Has no effect with mpl backend.
    sizefloat or tuple of float

        The size of the window, in pixels. can be one number to specify a square window, or the (width, height) of a rectangular window. Has no effect with mpl backend.
    backgroundmatplotlib color

        Color of the background of the display window.
    foregroundmatplotlib color | None

        Color of the foreground of the display window. Has no effect with mpl backend. None will choose white or black based on the background color.
    initial_timefloat | None

        The time to display on the plot initially. None to display the first time sample (default).
    time_unit‘s’ | ‘ms’

        Whether time is represented in seconds (“s”, default) or milliseconds (“ms”).
    backend ‘auto’ | ‘mayavi’ | ‘pyvista’ | ‘matplotlib’

        Which backend to use. If 'auto' (default), tries to plot with pyvista, but resorts to matplotlib if no 3d backend is available.
        New in version 0.15.0.
        
    title str | None

        Title for the figure. If None, the subject name will be used.

        New in version 0.17.0.
    show_traces bool | str | float

        If True, enable interactive picking of a point on the surface of the brain and plot its time course. This feature is only available with the PyVista 3d backend, and requires time_viewer=True. Defaults to ‘auto’, which will use True if and only if time_viewer=True, the backend is PyVista, and there is more than one time point. If float (between zero and one), it specifies what proportion of the total window should be devoted to traces (True is equivalent to 0.25, i.e., it will occupy the bottom 1/4 of the figure).

        New in version 0.20.0.
 
'''





