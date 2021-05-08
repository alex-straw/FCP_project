"""

GUI.py
Designed and written by James Irvin
May 2021

This script contains a class that defines the GUI and plots the outputs of simulation.py as an animated office.

Used by simulation.py.
"""

## Import modules
import matplotlib.backends.backend_tkagg
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import simulation
import time
from office import Office

class GUI:
    """This class is used to generate a Tkinter Graphical User Interface (GUI) which allows the user to change input parameters using widgets.

        The GUI is also used to present animated results from simulation.py as a matplotlib plot.

        The following parameters can be changed within the "parameters" dictionary [widget]

            "Number of people" - The number of people in the office [spin box]
            "Maximum Age" - Maximum possible age of people in the office [slider]
            "Minimum Age" - Minimum possible age of people in the office [slider]
            "Mask Adherence" - Percentage of people who wear a face mask [slider]
            "Social Distancing Adherence" - Percentage of people who adhere to social distancing measures [slider]
            "Office Plan" - Which floor of the office is simulated from the 4 choices [Listbox]
            "Simulation duration" - Number of movement interactions to model simulation over [slider]

        Once the user has specified their parameters they  can begin the simulation by pressing the "Begin Simulation" button.

        The simulated office space is then shown for each discrete time event.

        """

    def __init__(self, root):

        ##Initalisiing parameters
        parameters = {'Maximum Age': 65,
                      'Minimum Age': 20,
                      'Mask Adherence': 80,
                      'Social Distancing Adherence': 50,
                      'Office Plan': (0,),
                      'Number of People': 20,
                      'Number of infected': 5,
                      'Simulation Duration': 12}


        ## Main frame setup - GUI Controls
        root.title("COVID-19 MODELLING PARAMETERS")
        mainframe = ttk.Frame(root, padding="2 2 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ## Second frame setup - Figure window
        figframe = ttk.Frame(root, padding="2 2 12 12")
        figframe.grid(column=1, row=0, sticky=(N, W, E, S))


        ## Setup figure withing canvas to plot onto
        figure_plot = Figure(figsize=(5, 4), dpi=100, )
        y = np.random.random([10, 1])
        office_plot = figure_plot.add_subplot()
        office_plot.plot(y)
        canvas = FigureCanvasTkAgg(figure_plot, master=figframe)
        canvas.get_tk_widget().grid(column=1, row=0, sticky='we')
        canvas.draw()

        ## Toolbar to manipulate figure
        toolbar = NavigationToolbar2Tk(canvas, figframe, pack_toolbar=False) # pack_toolbar=False required for layout managment.
        toolbar.update() # Toolbar automatically updates (this is a built in function)
        toolbar.grid(column=1, row=1, sticky='we')
        canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}")) # popups that show when you hover over a toolbar button
        canvas.mpl_connect("key_press_event", key_press_handler)



        ## Label update functions
        def update_lbl_MaxAge(Max_Age):
            Min_Age = int(float((Min_Age_Slider.get())))
            Max_Age = int(float((Max_Age)))
            Max_Age_label['text'] = "Maximum age: " + str(Max_Age) + " years old"
            parameters.update({"Maximum Age": Max_Age})
            if Min_Age > Max_Age:
                switch_off_Begin_sim_button_state()
            else:
                switch_on_Begin_sim_button_state()

        def update_lbl_MinAge(Min_Age):
            Min_Age = int(float((Min_Age)))
            Max_Age = int(float((Max_Age_Slider.get())))
            Min_Age_label['text'] = "Minimum age: " + str(Min_Age) + " years old"
            parameters.update({"Minimum Age": Min_Age})
            if Min_Age > Max_Age:
                switch_off_Begin_sim_button_state()
            else:
                switch_on_Begin_sim_button_state()

        def update_lbl_MA(Mask_Adh):
            Mask_Adh = int(float((Mask_Adh)))
            MA_label['text'] = "Mask adherence: " + str(Mask_Adh) + "%"
            parameters.update({"Mask Adherence": Mask_Adh})

        def update_lbl_SD(Soc_Dist):
            Soc_Dist = int(float((Soc_Dist)))
            SD_label['text'] = "Social distancing adherence: " + str(Soc_Dist) + "%"
            parameters.update({"Social Distancing Adherence": Soc_Dist})

        def update_lbl_SimDur(Sim_Dur):
            Sim_Dur = int(float((Sim_Dur)))
            Sim_Dur_label['text'] = "Simulation duration: " + str(Sim_Dur) + " iterations"
            parameters.update({"Simulation Duration": Sim_Dur})

        def update_lb_office_plans(office_plans_var):
            office_plans_var = Office_Plans_Listbox.curselection()
            parameters.update({"Office Plan": office_plans_var})
            office = Office(parameters['Office Plan'][0])
            desk_no = len(office.desk_locations)
            test = 1

        def update_lb_num_people(People_Val):
            People_Val = int(Num_People.get())
            parameters.update({"Number of People": People_Val})
            change_Infected_People_max_val(People_Val)

        def update_lb_Inf_People(Infected_People_Val):
            Infected_People_Val = int(Inf_People.get())
            parameters.update({"Number of infected": Infected_People_Val})
            change_Num_People_min_val(Infected_People_Val)

        def switch_on_Begin_sim_button_state():
                Begin_sim_button.state(['!disabled'])

        def change_Infected_People_max_val(People_Val):
            Inf_People.config(to=People_Val)

        def change_Num_People_min_val(Infected_People_Val):
            Num_People.config(from_=Infected_People_Val)


        def switch_off_Begin_sim_button_state():
            if Begin_sim_button.instate(['!disabled']):
                Begin_sim_button.state(['disabled'])
            else:
                Begin_sim_button.state(['disabled'])

        def Begin_Sim():
            # print(parameters)
            # Begin_sim_button.state(['disabled'])
            # display_frames = simulation.main(parameters)
            # # test_plot = Figure(figsize=(5, 4), dpi=100, )
            # # new_plot = test_plot.add_subplot()
            # # new_plot.imshow(display_frames[1].tolist())
            # # newcanvas = FigureCanvasTkAgg(test_plot, master=figframe)
            # # newcanvas.get_tk_widget().grid(column=1, row=0, sticky='we')
            # # newcanvas.draw()
            #
            # for frame in display_frames:
            #     test_plot = Figure(figsize=(5, 4), dpi=100, )
            #     new_plot = test_plot.add_subplot()
            #     new_plot.imshow(frame)
            #     newcanvas = FigureCanvasTkAgg(test_plot, master=figframe)
            #     newcanvas.get_tk_widget().grid(column=1, row=0, sticky='we')
            #     newcanvas.draw_idle()
            #     time.sleep(1/30)
            #     figframe.update()
            #
            # Begin_sim_button.state(['!disabled'])

            Begin_sim_button.state(['disabled'])
            display_frames = simulation.main(parameters)
            # frame = 1

            for frame in display_frames:
                test_plot = Figure(figsize=(5, 4), dpi=100, )
                new_plot = test_plot.add_subplot()
                # frame += 1
                # new_plot.title(frame)
                new_plot.imshow(frame)
                newcanvas = FigureCanvasTkAgg(test_plot, master=figframe)
                newcanvas.get_tk_widget().grid(column=1, row=0, sticky='we')
                newcanvas.draw_idle()
                time.sleep(1/30)
                figframe.update()

            Begin_sim_button.state(['!disabled'])


        ### Labels and widgets

        ## Instructions label
        instructions_label = ttk.Label(mainframe, text='Please enter the following parameters:').grid(column=0, row=0, sticky='we')

        ## People label
        People_label = ttk.Label(mainframe, text='Number of people:').grid(column=0, row=1, sticky='we')

        ## Infected People label
        Infected_label= ttk.Label(mainframe, text='Number of infected people:').grid(column=0, row=3, sticky='we')

        ## Max age label
        Max_Age = IntVar()
        Max_Age_label = ttk.Label(mainframe)
        Max_Age_label.grid(column=0, row=5, sticky='we')

        ## Min age label
        Min_Age = IntVar()
        Min_Age_label = ttk.Label(mainframe)
        Min_Age_label.grid(column=0, row=7, sticky='we')

        ## Mask adherence label
        Mask_Adh = IntVar()
        MA_label = ttk.Label(mainframe)
        MA_label.grid(column=0, row=9, sticky='we')

        ## Social distancing label
        Soc_Dist = IntVar()
        SD_label = ttk.Label(mainframe)
        SD_label.grid(column=0, row=11, sticky='we')

        ## Office floor plans label
        Office_Plans_label = ttk.Label(mainframe, text='Office plan:').grid(column=0, row=13, sticky='we')

        ## Simulation Duration label
        Sim_Dur = IntVar()
        Sim_Dur_label = ttk.Label(mainframe)
        Sim_Dur_label.grid(column=0, row=15, sticky='we')

        ## Begin simulation button
        Begin_sim_button = ttk.Button(mainframe, text='Begin Simulation', command=Begin_Sim)
        Begin_sim_button.grid(column=0, row=17, sticky='we')

        ## Number of people spin box
        People_Val = IntVar()
        People_Val.set(parameters['Number of People'])  # set box to correct default value
        Num_People = ttk.Spinbox(mainframe,from_ =1.0, to=20, textvariable=People_Val)
        Num_People.grid(column=0, row=2, sticky=W)
        Num_People.state(['readonly'])
        Num_People.bind("<<Increment>>", lambda e: update_lb_num_people(People_Val))  # lambda used to create autonimous functions - If spin box valaue is changed the label will automatcailly be updated
        Num_People.bind("<<Decrement>>", lambda e: update_lb_num_people(People_Val))

        ## Number of people infected spin box
        Infected_People_Val = IntVar()
        Infected_People_Val.set(parameters['Number of infected'])  # set box to correct default value
        Inf_People = ttk.Spinbox(mainframe, from_=1.0, to=20, textvariable=Infected_People_Val)
        Inf_People.grid(column=0, row=4, sticky=W)
        Inf_People.state(['readonly'])
        Inf_People.bind("<<Increment>>", lambda e: update_lb_Inf_People(Infected_People_Val))
        Inf_People.bind("<<Decrement>>", lambda e: update_lb_Inf_People(Infected_People_Val))

        ## Max age slider
        Max_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Max_Age, command=update_lbl_MaxAge)
        Max_Age_Slider.grid(column=0, row=6, sticky='we')
        Max_Age_Slider.set(parameters['Maximum Age'])

        ## Min age slider
        Min_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Min_Age, command=update_lbl_MinAge)
        Min_Age_Slider.grid(column=0, row=8, sticky='we')
        Min_Age_Slider.set(parameters['Minimum Age'])

        ## Mask adherence slider
        Mask_Adh_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Mask_Adh, command=update_lbl_MA)
        Mask_Adh_Slider.grid(column=0, row=10, sticky='we')
        Mask_Adh_Slider.set(parameters['Mask Adherence'])

        ## Social distancing slider
        Soc_Dist_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Soc_Dist,command=update_lbl_SD)
        Soc_Dist_Slider.grid(column=0, row=12, sticky='we')
        Soc_Dist_Slider.set(parameters['Social Distancing Adherence'])

        ## Office plan listbox
        Office_Plans = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
        office_plans_var = StringVar(value=Office_Plans)
        Office_Plans_Listbox = Listbox(mainframe, listvariable=office_plans_var, height=4)
        Office_Plans_Listbox.grid(column=0, row=14, sticky='we')
        Office_Plans_Listbox.bind("<<ListboxSelect>>", lambda e: update_lb_office_plans(Office_Plans_Listbox.curselection()))

        ## Simulation Duration slider
        Sim_Dur_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=10.0, to=500.0, variable=Sim_Dur, command=update_lbl_SimDur)
        Sim_Dur_Slider.grid(column=0, row=16, sticky='we')
        Sim_Dur_Slider.set(parameters['Simulation Duration'])

        ## Quit application button
        Quit_app_button = ttk.Button(master=mainframe, text="Quit app", command=root.quit)
        Quit_app_button.grid(column=0, row=18, sticky='we')

        ##scalling to add space around widgets
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

def main():
    root = Tk()
    GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
