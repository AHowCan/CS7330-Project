from dearpygui.core import *
from dearpygui.simple import *
from math import cos

TITLE = 'Our buses do not smell! Okay, maybe a little. But only in the summer. Oh alright, they smell damn awful in the summer. [SIGHING SOUND] [END OF AUTOMATED VOICE TRANSCRIPT]'


def plot_callback(sender, data):
    # keeping track of frames
    frame_count = get_data("frame_count")
    frame_count += 1
    add_data("frame_count", frame_count)

    # updating plot data
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")
    if len(plot_datax) > 2000:
        frame_count = 0
        plot_datax.clear()
        plot_datay.clear()
    plot_datax.append(3.14 * frame_count / 180)
    plot_datay.append(cos(3 * 3.14 * frame_count / 180))
    add_data("plot_datax", plot_datax)
    add_data("plot_datay", plot_datay)

    # plotting new data
    clear_plot("Plot")
    add_line_series("Plot", "Cos", plot_datax, plot_datay, weight=2)


with window("Tutorial"):
    add_plot("Plot", height=-1)
    add_data("plot_datax", [])
    add_data("plot_datay", [])
    add_data("frame_count", 0)
    set_render_callback(plot_callback)


set_main_window_title(TITLE)
start_dearpygui()
