#!/usr/bin/env python
import Pmw, Tkinter, string, random, pylab, sys, os, re,\
       tkMessageBox, tkFileDialog, tkColorChooser, utilities
from numpy import *
from pylab import *
from Tkinter import *
from sys import argv, exit
from Scientific.TkWidgets.TkPlotCanvas import \
     PolyLine, PolyMarker, PlotGraphics, PlotCanvas
from matplotlib.backends.backend_tkagg import \
     FigureCanvasTkAgg, NavigationToolbar2TkAgg

class FitParameters:
    """
    Parameters setting dialog box for Fitlab!
    """
    def __init__(self,
                 parent,         
                 status_line,
                 peak_no=1,
                 constrained=True,
                 func='g',    
                 balloon=None,   
                 scrolled=True): 
        """
        Create widgets.
        
        parent           parent widget
        status_line      Label with status of user actions
        balloon          balloon help widget
        scrolled         scrolled main frame or not
        """
        self.master = parent
        self.status_line = status_line
        self.balloon = balloon
        self.peakfit = None
        self.peak_no = peak_no
        self.constrained = constrained
        self.func = func
            
        if scrolled:
            self.topframe = Pmw.ScrolledFrame(self.master,
                 usehullsize=1, hull_height=290, hull_width=390)
            self.create(self.topframe.interior())
        else:
            self.topframe = Frame(self.master, borderwidth=2, relief='groove')
            self.topframe.pack(expand=True, fill='both')
            self.create(self.topframe)

    def pack(self, **kwargs):
        """
        Pack the topframe. The location of the InputFields GUI in
        the parent widget can be controlled by the calling code.
        """
        self.topframe.pack(kwargs, expand=True, fill='both')

    def quit(self):
        self.master.quit()
        
    def create(self,parent):
        """pack nicely the parameters' querries"""
        frame_par = Frame(parent); frame_par .pack(side='left',fill='y',expand='yes')
        frame_cmin= Frame(parent); frame_cmin.pack(side='left',fill='y',expand='yes')
        frame_cmax= Frame(parent); frame_cmax.pack(side='left',fill='y',expand='yes')
        param_widgets = []
        param_widgets_values = []
        constraint_widgets = []
        constraint_widgets_values = []
        if (self.func == 'g' or self.func == 'l'):
           for i in range(self.peak_no):
               text = 'xo_%i'%(i+1)
               param  = DoubleVar(); param.set(1.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'sigma_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'A_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
                  
               if self.constrained:
                 for i in range(3):
                  pair = []
                  text = 'min'
                  cmin  = DoubleVar(); cmin.set(0.0)
                  pair.append(Pmw.EntryField(frame_cmin,
                                   labelpos='w',
                                   label_text=text,
                                   entry_width='10',
                                   entry_textvariable=cmin,))
                  cmax  = DoubleVar(); cmax.set(3000.0)
                  text = 'max'
                  pair.append(Pmw.EntryField(frame_cmax,
                                   labelpos='w',
                                   label_text=text,
                                   entry_width='10',
                                   entry_textvariable=cmax,))
                  constraint_widgets.append(pair)
                  constraint_widgets_values.append([cmin.get(),cmax.get()])

        elif self.func == 'lg1':
           for i in range(self.peak_no):
               text = 'xo_%i'%(i+1)
               param  = DoubleVar(); param.set(1.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'sigma_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'A_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'm_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
                  
               if self.constrained:
                 for i in range(4):
                  pair = []
                  text = 'min'
                  cmin  = DoubleVar(); cmin.set(0.0)
                  pair.append(Pmw.EntryField(frame_cmin,
                                   labelpos='w',
                                   label_text=text,
                                   entry_width='10',
                                   entry_textvariable=cmin,))
                  cmax  = DoubleVar(); cmax.set(3000.0)
                  text = 'max'
                  pair.append(Pmw.EntryField(frame_cmax,
                                   labelpos='w',
                                   label_text=text,
                                   entry_width='10',
                                   entry_textvariable=cmax,))
                  constraint_widgets.append(pair)
                  constraint_widgets_values.append([cmin.get(),cmax.get()])

        elif self.func == 'lg2':
           for i in range(self.peak_no):
               text = 'xo_%i'%(i+1)
               param  = DoubleVar(); param.set(1.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'sigmaL_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'sigmaG_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'A_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
               #
               text = 'm_%i'%(i+1)
               param  = DoubleVar(); param.set(3.0)
               param_widgets.append(Pmw.EntryField(frame_par,
                                    labelpos='w',
                                    label_text=text,
                                    entry_width='10',
                                    entry_textvariable=param,))
               param_widgets_values.append(param.get())
                  
               if self.constrained:
                 for i in range(5):
                  pair = []
                  text = 'min'
                  cmin  = DoubleVar(); cmin.set(0.0)
                  pair.append(Pmw.EntryField(frame_cmin,
                                   labelpos='w',
                                   label_text=text,
                                   entry_width='10',
                                   entry_textvariable=cmin,))
                  cmax  = DoubleVar(); cmax.set(3000.0)
                  text = 'max'
                  pair.append(Pmw.EntryField(frame_cmax,
                                   labelpos='w',
                                   label_text=text,
                                   entry_width='10',
                                   entry_textvariable=cmax,))
                  constraint_widgets.append(pair)
                  constraint_widgets_values.append([cmin.get(),cmax.get()])
                                      
        for widget in param_widgets:
            widget.pack(side='top')

        for widget_min,widget_max in constraint_widgets:
            widget_min.pack(side='top')
            widget_max.pack(side='top')

        Pmw.alignlabels(param_widgets     )
        l1 = []
        l2 = []
        for i in range(len(constraint_widgets)):
            l1.append(constraint_widgets[i][0])
            l2.append(constraint_widgets[i][1])
        Pmw.alignlabels(l1);Pmw.alignlabels(l2)
        
        self.param_widgets        = param_widgets
        self.param_widgets_values = array(param_widgets_values,dtype=float64)
        self.constraint_widgets = constraint_widgets
        self.constraint_widgets_values = array(constraint_widgets_values,dtype=float64)

    def update(self):
        """updates all parameters and their constraints if any"""
        for i,par in enumerate(self.param_widgets):
            self.param_widgets_values[i] = par.get()
        for i,constr in enumerate(self.constraint_widgets):
            self.constraint_widgets_values[i,0] = constr[0].get()
            self.constraint_widgets_values[i,1] = constr[1].get()
            
    def get(self):
        """return parameters and their constraints if any"""
        return self.param_widgets_values, self.constraint_widgets_values

class InputLists:
    """
    Demonstrate various widgets that let the user choose
    items from some kind of list:
    standard listbox, combo boxes, radio buttons, collection of
    checkbuttons, option menu.
    """
    def __init__(self, parent, status_line, balloon=None):
        self.master = parent
        self.status_line = status_line
        self.balloon = balloon
        self.frame = Frame(self.master, borderwidth=3)
        # pack self.frame in a separate function
        self.create(self.frame)

    def pack(self, **kwargs):
        self.frame.pack(kwargs)
        
    def create(self, parent):

        header = Label(parent, text='Widgets for list data - FitLab Studio Future!:D', 
                       font='courier 14 bold', foreground='blue',
                       background='#%02x%02x%02x' % (196,196,196))
        header.pack(side='top', pady=10, ipady=10, fill='x')

        # frame for left-to-right packing of single-selection
        # list-like widgets:
        frame = Frame(parent); frame.pack(side='top')
        # the various widgets are aligned with a common top line,
        # obtained by anchor='n'

        # create list:
        listitems = ['list item ' + str(i+1) for i in range(40)]

        # standard listbox:
        self.list1 = Pmw.ScrolledListBox(frame,
               listbox_selectmode='single', # 'multiple'
               vscrollmode='static', hscrollmode='dynamic',
               listbox_width=12, listbox_height=6,
               label_text='plain listbox\nsingle selection',
               # labelpos is needed if label_text is present,
               # choices: n (north), nw (north-west), s (south) ...
               labelpos='n',  
               selectioncommand=self.status_list1)
        self.list1.pack(side='left', padx=10, anchor='n')
        # insert items:
        for item in listitems:
            self.list1.insert('end', item)  # insert after end of list
        # could also say
        # self.list.configure(items=listitems)
        # or give the items value as keyword 'items='
        # at construction time

        # example on updating an option in, e.g., the Tkinter
        # Listbox part of a Pmw.ScrolledListBox:
        # self.list.component('listbox').configure(background='blue')
        # i.e. the parts (listbox, label, etc) are ordinary Tkinter
        # widgets that can be extracted by the component method

        # simple combo box with list and entry for chosen item:
        self.combo1 = Pmw.ComboBox(frame,
               label_text='simple combo box',
               labelpos='nw',
               scrolledlist_items=listitems,
               selectioncommand=self.status_combobox,
               listbox_height=6,
               dropdown=False)
        self.combo1.pack(side='left', padx=10, anchor='n')

        # dropdown combo box with entry for chosen item and
        # button for showing the list:
        self.combo2 = Pmw.ComboBox(frame,
               label_text='dropdown combo box',
               labelpos='nw',
               scrolledlist_items=listitems,
               selectioncommand=self.status_combobox,
               listbox_height=6,
               dropdown=True)  # the only difference from combo1
        self.combo2.pack(side='left', padx=10, anchor='n')
        if self.balloon is not None:
            self.balloon.bind(self.combo2, 'Click on arrow to display list')

        frame_left = Frame(parent); frame_left.pack(side='left')
        
        # standard listbox:
        self.list2 = Pmw.ScrolledListBox(frame_left,
               listbox_selectmode='multiple',
               vscrollmode='static', hscrollmode='dynamic',
               listbox_width=12, listbox_height=6,
               label_text='plain listbox\nmultiple selection',
               labelpos='n',
               items=listitems,
               selectioncommand=self.status_list2)
        self.list2.pack(side='left', anchor='n')

        # frame_right holds other widgets packed top-bottom:
        frame_right = Frame(parent); frame_right.pack(side='left')

        # option menu:
        self.option_var = StringVar(); self.option_var.set('item2')
        self.option1 = Pmw.OptionMenu(frame_right,
               labelpos='w',  # n, nw, ne, e, and so on
               label_text='Option Menu:',
               items=['item1', 'item2', 'item3', 'item4'],
               menubutton_textvariable=self.option_var,
               menubutton_width=6,
               command=self.status_option)
        self.option1.pack(side='top', anchor='w')
        
        # plain Tk radio buttons, tied to a variable:
        self.radio_var = StringVar() # common variable for radio buttons
        self.radio1 = Frame(frame_right)
        self.radio1.pack(side='top', pady=5)
        Label(self.radio1,
              text='Tk radio buttons').pack(side='left')
        for radio in ('radio1', 'radio2', 'radio3', 'radio4'):
            r = Radiobutton(self.radio1, text=radio, variable=self.radio_var,
                            value='radiobutton no. ' + radio[5],
                            command=self.status_radio1)
            r.pack(side='left')

        # Pmw radio buttons
        self.radio2 = Pmw.RadioSelect(frame_right,
               selectmode='single',
               buttontype='radiobutton', # 'button': plain button layout
               labelpos='w',
               label_text='Pmw radio buttons\nsingle selection',
               orient='horizontal',
               frame_relief='ridge', # try some decoration...
               command=self.status_radio2)
        self.radio2.pack(side='top', padx=10, anchor='w')
        # add items; radio buttons are only feasible for a few items:
        for text in ('item1', 'item2', 'item3', 'item4'):
            self.radio2.add(text)
        self.radio2.invoke('item2')  # 'item2' is pressed by default


        # check button list:
        self.radio3 = Pmw.RadioSelect(frame_right,
               selectmode='multiple',
               buttontype='checkbutton',
               labelpos='w',
               label_text='Pmw check buttons\nmultiple selection',
               orient='horizontal',
               frame_relief='ridge', # try some decoration...
               command=self.status_radio3)
        self.radio3.pack(side='top', padx=10, anchor='w')
        # add items; radio buttons are only feasible for a few items:
        for text in ('item1', 'item2', 'item3', 'item4'):
            self.radio3.add(text)
        # press 'item2' and 'item4' by default:
        self.radio3.invoke('item2');  self.radio3.invoke('item4')

    def status_list1(self):
        """Extract single list selection."""
        selected_item   = self.list1.getcurselection()[0]
        selected_index = self.list1.curselection()[0]
        text = 'selected list item=' + str(selected_item) + \
               ', index=' + str(selected_index)
        self.status_line.configure(text=text)

    def status_list2(self):
        """Extract multiple list selections."""
        selected_items   = self.list2.getcurselection() # tuple
        selected_indices = self.list2.curselection()    # tuple
        text = 'list items=' + str(selected_items) + \
               ', indices=' + str(selected_indices)
        self.status_line.configure(text=text)

    def status_combobox(self, value):
        text = 'combo box value = ' + str(value)
        self.status_line.configure(text=text)

    def status_radio1(self):
        text = 'radiobutton variable = ' + self.radio_var.get()
        self.status_line.configure(text=text)
        
    def status_radio2(self, value):
        text = 'Pmw check buttons: ' + value
        self.status_line.configure(text=text)
        
    def status_radio3(self, button_name, pressed):
        if pressed: action = 'pressed'
        else:       action = 'released'
        text = 'Pmw radio button ' + button_name + ' was ' + \
               action + '; pressed buttons: ' + \
               str(self.radio3.getcurselection())
        self.status_line.configure(text=text)

    def status_option(self, value):
        self.status_line.configure(text='option menu = ' + value)
        # or, since self.option_var is tied to the option menu,
        # ...configure(text='option menu ' + self.option_var)
        
class FitWork:
    """
    Fitting dialog box for Fitlab!
    """
    def __init__(self,
                 parent,         
                 status_line,
                 data=None,
                 balloon=None,   
                 scrolled=True): 
        """
        Create widgets.
        
        parent           parent widget
        status_line      Label with status of user actions
        balloon          balloon help widget
        scrolled         scrolled main frame or not
        """
        self.master = parent
        self.status_line = status_line
        self.balloon = balloon
        ### defaults for fitting
        self.__peak_no = 1
        self.__func = 'g'
        self.__if_constrained = False
        if data is not None:
           self.__x = data[:,0]
           self.__y = data[:,1]
        self.__if_peakfit = False
            
        if scrolled:
            self.topframe = Pmw.ScrolledFrame(self.master,
                 usehullsize=1, hull_height=610, hull_width=840)
            self.create(self.topframe.interior())
        else:
            self.topframe = Frame(self.master, borderwidth=2, relief='groove')
            self.topframe.pack(expand=True, fill='both')
            self.create(self.topframe)
            
    def pack(self, **kwargs):
        """
        Pack the topframe. The location of the InputFields GUI in
        the parent widget can be controlled by the calling code.
        """
        self.topframe.pack(kwargs, expand=True, fill='both')
                    
    #def __init__(self,parent,smpl_f,bkgr_f,bgn=2100,end=2300):
    def create(self,parent):

        # frames
        frame_graph = Frame(parent); frame_graph.pack(side='left',fill='both',expand='yes')
        #frame_param = Frame(parent); frame_param.pack(side='left',fill='y',expand='yes')
        sub_frame_peaks = Frame(parent); sub_frame_peaks.pack(side='top',fill='both')
        #sub_frame_param = Frame(parent); sub_frame_param.pack(side='top',fill='both')
        self.frame =  frame_graph
        # canvas
        self.fig = pylab.figure(1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graph)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, frame_graph )
        self.toolbar.update()

        # option menu
        self.peak_no = IntVar(); self.peak_no.set(1)
        self.peak_no_widget = Pmw.OptionMenu(sub_frame_peaks,
               labelpos='n',  # n, nw, ne, e, and so on
               label_text='Peak number',
               items=[1,2,3,4],
               menubutton_textvariable=self.peak_no,
               menubutton_width=3,
               command=self._get_peak_no)
      
        # Pmw radio buttons
        self.check_func_widget = Pmw.RadioSelect(sub_frame_peaks,
               selectmode='single',
               buttontype='radiobutton', ### 'button': plain button layout
               labelpos='n',
               #label_text='Select type of function to fit:',
               orient='vertical',
               frame_relief='ridge', ### try some decoration...
               command=self._get_func)

        ### add items; radio buttons are only feasible for a few items:
        for text in ('Gaussian', 'Lorenzian', 'LG-1', 'LG-2', 'Voight'):
            self.check_func_widget.add(text)
        self.check_func_widget.invoke('Gaussian')  ### 'item2' is pressed by default
        
        # checkbutton:
        self.if_constrained = IntVar(); self.if_constrained.set(0)
        self.if_constrained_widget = Checkbutton(sub_frame_peaks,
                        text='Constrained',
                        variable=self.if_constrained,
                        command=self._get_if_constrained)

        # buttons
        self.param_button_widget = Button(sub_frame_peaks,
                                         text='Set Parameters',
                                         background='white',
                                         foreground='blue',
                                         command=self._parameter_dialog)
                                         
        self.fit_button_widget = Button(sub_frame_peaks,
                                         text='Fit',
                                         background='green',
                                         foreground='blue',
                                         command=self._fit)
        self.__pack()
        self.__plot()
    
    def _get_peak_no(self,value):
        self.__peak_no = value
        self._status_option(value)
        
    def _get_if_constrained(self):
        self.__if_constrained = bool(self.if_constrained.get())
        self._status_checkbutton()

    def _get_func(self,value):
        self.__func = value
        if   value == 'Gaussian' : self.__func = 'g'
        elif value == 'Lorenzian': self.__func = 'l'
        elif value == 'Voight'   : self.__func = 'v'
        elif value == 'LG-1'     : self.__func = 'lg1'
        elif value == 'LG-2'     : self.__func = 'lg2'
        self._status_radio_check_func(value)
        
    def __pack(self):
        """packs all intrinsic widgets"""
        # --- canvas
        self.canvas._tkcanvas.pack(side='top', fill='both', expand='yes')
        # --- peak number selector
        self.peak_no_widget.pack(side='top',anchor='center',ipady=4,ipadx=2,padx=10,pady=10)
        # --- radio buttons for fitting type selection
        self.check_func_widget.pack(side='top',padx=10,pady=10)
        # --- check button for constrained fitting selection
        self.if_constrained_widget.pack(side='top',padx=10,pady=10)
        # --- parameter set button
        self.param_button_widget.pack(side='top',padx=10,pady=10,
                                                 ipadx=15,ipady=15)
        # --- fit button
        self.fit_button_widget.pack(side='top',padx=10,pady=10,
                                                 ipadx=15,ipady=15)

    def __plot(self):
        """plots the selected peaks"""
        self.ax1  = self.fig.add_subplot(111)
        self.ax1.grid(False)
        self.ax1.set_title("Signal Fitting Workplate")
        self.ax1.set_xlabel("Frequency [cm$^{-1}$]")
        self.ax1.set_ylabel("Absorbance")
        
        self.ax1.axis([min(self.__x),max(self.__x),min(self.__y),max(self.__y)])        
        self.line1, = self.ax1.plot(self.__x,self.__y,linewidth='2',label='raw')
        self.fig.legend((self.line1,),('raw',),loc='upper right')

    def _fit(self,method='slsqp'):
        """perform fitting"""
        peak = utilities.Peak(self.__x,self.__y)
        constr = self.__constraints
        peak_no = self.__peak_no
        bounds = []
        if constr.any():
            for c in  constr: bounds.append((c[0],c[1]))
        if self.__parameters is None: pass
        peak.set_peak(peak_no,func_name=self.__func)
        
        opts = self.__get_opts()
        
        peak.fit(opts,method=method,bounds=bounds)
        param   = peak.get_parameters()
        fitdata = peak.get_fit()
        peaks   = peak.get_peaks()
        print 'R^2: %20.6f' % peak.get_r2()
        print 'PARAMETERS\n\n', param

        print " Reseted?: ",str(self.__if_peakfit)
        if not self.__if_peakfit:
           self.__if_peakfit = True
           self.line2, = self.ax1.plot(self.__x,fitdata,':',label='fit',linewidth='2')
           if peak_no > 1:
              self.line3, = self.ax1.plot(self.__x,peaks[0],label='peak 1')
              self.line4, = self.ax1.plot(self.__x,peaks[1],label='peak 2')
              if peak_no > 2:
                 self.line5, = self.ax1.plot(self.__x,peaks[2],label='peak 3')
                 if peak_no > 3:
                    self.line6, = self.ax1.plot(self.__x,peaks[3],label='peak 3')
        else:
           self.line2.set_ydata(fitdata)
           if peak_no > 1:
              self.line3.set_ydata(peaks[0])
              self.line4.set_ydata(peaks[1])
              if peak_no > 2:
                 self.line5.set_ydata(peaks[2])
                 if peak_no > 3:
                    self.line6.set_ydata(peaks[3])

        self.canvas.draw()

    def __get_opts(self):
        """create opts list for fit method of Peak class"""
        pars = self.__parameters
        peak_no = self.__peak_no
        if (self.__func == 'g' or self.__func == 'l'):
          if   peak_no ==1: 
               opts = [['xo_1',pars[0]], ['sigma_1',pars[1] ],['A_1',pars[2]]]
          elif peak_no ==2: 
               opts = [['xo_1',pars[0]], ['sigma_1',pars[1]], ['A_1',pars[2]],
                       ['xo_2',pars[3]], ['sigma_2',pars[4]], ['A_2',pars[5]]]
          elif peak_no ==3: 
               opts = [['xo_1',pars[0]], ['sigma_1',pars[1]], ['A_1',pars[2]],
                       ['xo_2',pars[3]], ['sigma_2',pars[4]], ['A_2',pars[5]],
                       ['xo_3',pars[6]], ['sigma_3',pars[7]], ['A_3',pars[8]]]
          elif peak_no ==4: 
               opts = [['xo_1',pars[0 ]], ['sigma_1',pars[1 ]], ['A_1',pars[2 ]],
                       ['xo_2',pars[3 ]], ['sigma_2',pars[4 ]], ['A_2',pars[5 ]],
                       ['xo_3',pars[6 ]], ['sigma_3',pars[4 ]], ['A_3',pars[5 ]],
                       ['xo_4',pars[9 ]], ['sigma_4',pars[10]], ['A_4',pars[11]]]
        elif self.__func == 'lg1':
          if   peak_no ==1: 
               opts = [['xo_1',pars[0]], ['sigma_1',pars[1] ],['A_1',pars[2]], ['m_1',pars[3]]]
          elif peak_no ==2: 
               opts = [['xo_1',pars[0]], ['sigma_1',pars[1]], ['A_1',pars[2]], ['m_1',pars[3]],
                       ['xo_2',pars[4]], ['sigma_2',pars[5]], ['A_2',pars[6]], ['m_2',pars[7]]]
          elif peak_no ==3: 
               opts = [['xo_1',pars[0]], ['sigma_1',pars[1]], ['A_1',pars[2]], ['m_1',pars[3]],
                       ['xo_2',pars[4]], ['sigma_2',pars[5]], ['A_2',pars[6]], ['m_2',pars[7]],
                       ['xo_3',pars[8]], ['sigma_3',pars[9]], ['A_3',pars[10]], ['m_3',pars[11]]]
          elif peak_no ==4: 
               opts = [['xo_1',pars[0 ]], ['sigma_1',pars[1 ]], ['A_1',pars[2 ]], ['m_1',pars[3 ]],
                       ['xo_2',pars[4 ]], ['sigma_2',pars[5 ]], ['A_2',pars[6 ]], ['m_2',pars[7 ]],
                       ['xo_3',pars[8 ]], ['sigma_3',pars[9 ]], ['A_3',pars[10]], ['m_3',pars[11]],
                       ['xo_4',pars[12]], ['sigma_4',pars[13]], ['A_4',pars[14]], ['m_4',pars[15]]]
        elif self.__func == 'lg2':
          if   peak_no ==1: 
               opts = [['xo_1',pars[0]], ['sigmaL_1',pars[1]], ['sigmaG_1',pars[2]],['A_1',pars[3]], ['m_1',pars[4]]]
          elif peak_no ==2: 
               opts = [['xo_1',pars[0]], ['sigmaL_1',pars[1]], ['sigmaG_1',pars[2]], ['A_1',pars[3]], ['m_1',pars[4]],
                       ['xo_2',pars[5]], ['sigmaL_2',pars[6]], ['sigmaG_2',pars[7]], ['A_2',pars[8]], ['m_2',pars[9]]]
          elif peak_no ==3: 
               opts = [['xo_1',pars[0]], ['sigmaL_1',pars[1]], ['sigmaG_1',pars[2]], ['A_1',pars[3]], ['m_1',pars[4]],
                       ['xo_2',pars[5]], ['sigmaL_2',pars[6]], ['sigmaG_2',pars[7]], ['A_2',pars[8]], ['m_2',pars[9]],
                       ['xo_3',pars[10]], ['sigmaL_3',pars[11]], ['sigmaG_3',pars[12]], ['A_3',pars[13]], ['m_3',pars[14]]]
          elif peak_no ==4: 
               opts = [['xo_1',pars[0 ]], ['sigmaL_1',pars[1 ]], ['sigmaG_1',pars[2]], ['A_1',pars[3 ]], ['m_1',pars[4 ]],
                       ['xo_2',pars[5 ]], ['sigmaL_2',pars[6 ]], ['sigmaG_2',pars[7]], ['A_2',pars[8 ]], ['m_2',pars[9 ]],
                       ['xo_3',pars[10]], ['sigmaL_3',pars[11]], ['sigmaG_3',pars[12]], ['A_3',pars[13]], ['m_3',pars[14]],
                       ['xo_4',pars[15]], ['sigmaL_4',pars[16]], ['sigmaG_4',pars[17]], ['A_4',pars[18]], ['m_4',pars[19]]]
        return opts
                        
    def update(self):
        """replot the data and add fitted peaks"""
        pass
    
    def reset(self):
        """reset fitting (start from the beginning)"""
        self.__if_peakfit = False
        print " I have reset myself! Start fitting again, young lad or laddness!"
            
    def _parameter_dialog(self):
        self.t2 = Tkinter.Tk()
        self.t2.frame = Frame(self.t2)
        self.frame = Frame(self.master)
        self.parameter_d = Pmw.Dialog(self.t2.frame,
                          title='Fitting workshop',
                          buttons=('Apply', 'Cancel'),
                          #defaultbutton='Apply',
                          command=self._parameter_dialog_action)

        self.parameter_d_gui = FitParameters(self.parameter_d.interior(),
                                         self.status_line,peak_no=self.__peak_no,
                                         func=self.__func,constrained=self.__if_constrained,
                                         balloon=self.balloon, scrolled=True)
        self.parameter_d_gui.pack()
        
    def _parameter_dialog_action(self, result):
        # result contains the name of the button that we clicked
        if result == 'Apply':
            self.parameter_d_gui.update()
            self.__parameters, self.__constraints = self.parameter_d_gui.get()
            print " PARAMETES"
            print self.__parameters
            print " CONSTRAINTS"
            print self.__constraints
        else:
            text = 'your input parameters were lost!'
            self.status_line.configure(text=text)
            #self.parameter_d.quit()
            self.reset()
            self.parameter_d.destroy()
            self.t2.destroy()
            #self.frame.destroy()
            
        # does not work: self.dialog.deactivate(result)
        #self.parameter_d.destroy()  # destroy dialog window
                
    def _status_checkbutton(self):
        self.status_line.configure(text='Constrained optimization: ' + \
                                   str(self.if_constrained.get()))

    def _status_option(self, value):
        #self.status_line.configure(text=self.func_fit)
        # or
        self.status_line.configure(text=value)

    def _status_radio_check_func(self, value):
        text = value
        self.status_line.configure(text=text)
                
class FitFields:
    """
    Fit your data with Fitlab!
    """
    def __init__(self,
                 parent,         
                 status_line, 
                 smpl=None,
                 bkgr=None,
                 x=None,
                 balloon=None,   
                 scrolled=True): 
        """
        Create widgets.
        
        parent           parent widget
        status_line      Label with status of user actions
        balloon          balloon help widget
        scrolled         scrolled main frame or not
        """
        self.master = parent
        self.status_line = status_line
        self.balloon = balloon
        self.set_data(smpl,bkgr,x)
        self.__value1 = 0.0
        self.__value2 = 0.0
                      
        if scrolled:
            # use an intelligent Pmw.ScrolledFrame widget to hold the
            # whole window; scrollbars are automatically added if necessary
            self.topframe = Pmw.ScrolledFrame(self.master,
                 usehullsize=1, hull_height=610, hull_width=740)
            # (just Pmw.ScrolledFrame(self.master) gives a fixed-size
            # domain with scrollbars; height/weight should here be adjusted
            # pack self.topframe in a separate function)

            # create all other widgets inside the top frame:
            self.create(self.topframe.interior())
            # or: self.create(self.topframe.component('frame'))
        else:
            # use a standard Tkinter Frame with adaptive size:
            self.topframe = Frame(self.master, borderwidth=2, relief='groove')
            self.topframe.pack(expand=True, fill='both')
            # create all other widgets inside the top frame:
            self.create(self.topframe)

    def pack(self, **kwargs):
        """
        Pack the topframe. The location of the InputFields GUI in
        the parent widget can be controlled by the calling code.
        """
        self.topframe.pack(kwargs, expand=True, fill='both')
                    
    #def __init__(self,parent,smpl_f,bkgr_f,bgn=2100,end=2300):
    def create(self,parent):

        # frames
        frame_graph = Frame(parent); frame_graph.pack(side='top',fill='both',expand='yes')
        frame_right = Frame(parent); frame_right.pack(side='left')
        frame_buttn = Frame(parent); frame_buttn.pack(side='right')
        frame_peaks = Frame(parent); frame_peaks.pack(side='right')
        frame_freqs = Frame(parent); frame_freqs.pack(side='right')
        
        # canvas
        self.fig = pylab.figure(1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, frame_graph )
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        #self.master.protocol("WM_DELETE_WINDOW", self.master.quit)
               
        # sliders
        self.m1 = DoubleVar();  self.m1.set(0.0)
        self.move_smpl_widget = Scale(frame_right,
                                       orient='horizontal',
                                       #label="Sample",
                                       from_=-0.1, to=0.1, 
                                       sliderlength=10,
                                       #,tickinterval=0.1
                                       length=450, 
                                       resolution=0.0001,
                                       variable = self.m1,
                                       command=self._move1)
                                       
        self.m2 = DoubleVar();  self.m2.set(0.0)
        self.move_bkgr_widget = Scale(frame_right,
                                       orient='horizontal',
                                       #label="Background",
                                       from_=-0.1, to=0.1,
                                       sliderlength=10,
                                       #,tickinterval=0.1
                                       length=450,
                                       resolution=0.0001,
                                       variable = self.m2,
                                       command=self._move2)

        self.s1 = DoubleVar();  self.s1.set(1.0)
        self.scle_smpl_widget = Scale(frame_right,
                                       orient='horizontal',
                                       #label="Sample",
                                       from_=0.5, to=2.0, 
                                       sliderlength=10,
                                       #,tickinterval=0.1
                                       length=450, 
                                       resolution=0.0001,
                                       variable = self.s1,
                                       command=self._scale1)
                                       
        self.s2 = DoubleVar();  self.s2.set(1.0)
        self.scle_bkgr_widget = Scale(frame_right,
                                       orient='horizontal',
                                       #label="Sample",
                                       from_=0.5, to=2.0, 
                                       sliderlength=10,
                                       #,tickinterval=0.1
                                       length=450, 
                                       resolution=0.0001,
                                       variable = self.s2,
                                       command=self._scale2)

        # buttons
        self.quit_button_widget = Button(frame_buttn,
                                         text='Quit',
                                         background='yellow',
                                         foreground='blue',
                                         command=self._quit)
        
        # checkbutton:
        self.if_gaussian = IntVar(); self.if_gaussian.set(1)
        self.if_gaussian_widget = Checkbutton(parent,
                        text='Gaussian',
                        variable=self.if_gaussian,
                        command=self._status_checkbutton)
      
        # Pmw radio buttons
        self.check_func_widget = Pmw.RadioSelect(frame_right,
               selectmode='single',
               buttontype='radiobutton', ### 'button': plain button layout
               labelpos='n',
               #label_text='Select type of function to fit:',
               orient='horizontal',
               frame_relief='ridge', ### try some decoration...
               command=self._status_radio_check_func)

        ### add items; radio buttons are only feasible for a few items:
        for text in ('Gaussian', 'Lorenzian', 'Voight'):
            self.check_func_widget.add(text)
        self.check_func_widget.invoke('Gaussian')  ### 'item2' is pressed by default

        # entry fields
        self.min_freq = DoubleVar(); self.min_freq.set(self.__min_freq_start)
        self.min_freq_widget = Pmw.EntryField(frame_freqs, 
                               labelpos='n', 
                               label_text='Min',
                               validate=None,
                               entry_textvariable=self.min_freq, 
                               entry_width=10,)
                               
        # entry fields
        self.max_freq = DoubleVar(); self.max_freq.set(self.__max_freq_start)
        self.max_freq_widget = Pmw.EntryField(frame_freqs, 
                               labelpos='n', 
                               label_text='Max',
                               validate=None,
                               entry_textvariable=self.max_freq, 
                               entry_width=10,)
        
        self.__pack()
        self.__plot()
    
    def __pack(self):
        """packs all intrinsic widgets"""
        # --- buttons
        widgets = (self.quit_button_widget,)
        for w in widgets: w.pack(side='right',anchor='center',ipady=4,ipadx=2,padx=10,pady=10)

        # --- sliders
        widgets = (self.move_smpl_widget,
                   self.move_bkgr_widget,
                   self.scle_smpl_widget,
                   self.scle_bkgr_widget,)
        for w in widgets:
            w.pack(side='top', anchor='w')
        Pmw.alignlabels(widgets)  

        # --- entry fields
        widgets = (self.min_freq_widget,
                   self.max_freq_widget,)
        for w in widgets:
            w.pack(side='top', padx=10, anchor='w')
                                           
    def _status_checkbutton(self):
        self.status_line.configure(text='Gaussian fitting checkbutton: ' + \
                                   str(self.if_gaussian.get()))

    def _status_option(self, value):
        #self.status_line.configure(text=self.func_fit)
        # or
        self.status_line.configure(text=value)
        
    def _status_radio_check_func(self, value):
        text = value
        self.status_line.configure(text=text)

    def _quit(self): 
        self.master.quit()
        
    def _dest(self): 
        self.master.destroy()
        exit()        

    def _fit(self): pass
    
    def __plot(self):
        """plot initial state"""
        self.ax1  = self.fig.add_subplot(211)
        self.ax2  = self.fig.add_subplot(212,sharex=self.ax1,sharey=self.ax1)
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax1.set_title("Your spectras")
        self.ax1.set_ylabel("Absorbance")
        self.ax2.set_title("Difference spectrum")
        self.ax2.set_xlabel("Frequency [cm$^{-1}$]")
        self.ax2.set_ylabel("Absorbance")

        self.line1, = self.ax1.plot(self.x,self.smpl)
        self.line2, = self.ax1.plot(self.x,self.bkgr)
        self.line3, = self.ax2.plot(self.x,self.diff)
        
        self.ax1.axis([min(self.x),max(self.x),min(self.smpl),max(self.smpl)])
        self.ax2.axis([min(self.x),max(self.x),min(self.smpl),max(self.smpl)])

    def get_frequency_ranges(self):
        self.__min_freq_start = float64(self.min_freq.get())
        self.__max_freq_start = float64(self.max_freq.get())
        ranges = (self.__min_freq_start,self.__max_freq_start)
        return ranges
    
    def get_difference_spectrum(self):
        return self.diff
    
    def set_data(self,smpl,bkgr,x):
        """sets initial data to memory"""
        self.smpl     = smpl.copy()
        self.smpl_ref = smpl.copy()
        self.bkgr     = bkgr.copy()
        self.bkgr_ref = bkgr.copy()
        self.x        = x.copy()
        self.diff     = self.smpl - self.bkgr
        self.__min_freq_start = min(x)
        self.__max_freq_start = max(x)

    def _scale1(self,value1):
        self.smpl = self.smpl_ref * float64(value1)
        self.diff = self.smpl - self.bkgr
        self.line1.set_ydata(self.smpl)
        self.line3.set_ydata(self.diff)
        self.canvas.draw()

    def _scale2(self,value1):
        self.bkgr = self.bkgr_ref * float64(value1)
        self.diff = self.smpl - self.bkgr
        self.line2.set_ydata(self.bkgr)
        self.line3.set_ydata(self.diff)
        self.canvas.draw()

    def _move1(self,value1):
        self.smpl += float64(value1) - self.__value1
        self.smpl_ref = self.smpl
        self.diff = self.smpl - self.bkgr
        self.line1.set_ydata(self.smpl)
        self.line3.set_ydata(self.diff)
        self.canvas.draw()
        self.__value1 = float64(value1)

    def _move2(self,value2):
        self.bkgr += float64(value2) - self.__value2
        self.bkgr_ref = self.bkgr
        self.diff = self.smpl - self.bkgr
        self.line2.set_ydata(self.bkgr)
        self.line3.set_ydata(self.diff)
        self.canvas.draw()
        self.__value2 = float64(value2)
    

class FitLab:
    def __init__(self, parent, smpl=None, bkgr=None):
        self.master = parent
        self.balloon = Pmw.Balloon(self.master)  # used for all balloon helps

        self.smpl = self.read_csv(smpl)[:,1]
        self.bkgr = self.read_csv(bkgr)[:,1]
        self.x    = self.read_csv(bkgr)[:,0]
        # write messages about window actions in a common status label:
        frame = Frame(self.master)
        # pack frame with status label at the bottom:
        frame.pack(side='bottom', anchor='w', fill='x', expand=True)
        #Label(frame, text='Widget action response: ', 
        #      font='helvetica 8', anchor='w').pack(side='left')
        self.status_line = Label(frame, relief='groove', #relief='sunken',
                                 font='helvetica 8', anchor='w')
        # configure text later
        self.status_line.pack(side='left', fill='x', expand=True)

        self.pulldown_menus(self.master)
        self.fields = FitFields(self.master, self.status_line,
                               smpl=self.smpl, bkgr=self.bkgr, x=self.x,
                               balloon=self.balloon, scrolled=False)
        self.fields.pack(side='top',padx=30,pady=20)

        Button(self.master, text='Display widgets for list data',
               command=self.list_dialog, width=29).pack(padx=20,pady=2,side='left',
                                                        fill='x',expand=1)
        
        Button(self.master, text='Display the source code',
               command=self.display_code, width=29).pack(padx=20,pady=2,side='left',
                                                         fill='x',expand=1)
        
        # type q to quit:
        self.master.bind('<q>', self.quit) # self.quit needs an event argument

    def update(self):
        """update data"""
        pass
    
    def read_csv(self,file,fmin=0,fmax=1e40):
        """read csv file"""              
        data = []                        
        f = open(file)                   
        line = f.readline()
        while line:                      
          a,b = line.split(',')         
          if float64(a)<=fmax: break
          line = f.readline()           
        while (a>=fmin and line):
          a,b = line.split(',') 
          a = float64(a)                
          b = float64(b)                
          data.append([a,b])            
          line = f.readline()           
        return array(data,dtype=float64) 
            
    def display_code(self):
        self.display_file(sys.argv[0], self.master)

    def pulldown_menus(self, parent):
        self.menu_bar = Pmw.MenuBar(parent,
                                    hull_relief='raised',
                                    hull_borderwidth=1,
                                    balloon=self.balloon,
                                    hotkeys=True,  # define accelerators
                                    )
        self.menu_bar.pack(fill='x')

        self.menu_bar.addmenu('File', None, tearoff=True)
        self.menu_bar.addmenuitem('File', 'command',
             statusHelp='Open a file',
             label='Open...',
             command=self.file_read)
        self.menu_bar.addmenuitem('File', 'command',
             statusHelp='Save a file',
             label='Save as...',
             command=self.file_save)
        self.menu_bar.addmenuitem('File', 'command',
             statusHelp='Exit this application',
             label='Quit',
             command=self.quit)

        self.menu_bar.addmenu('Dialogs',
             'Demonstrate various Tk/Pmw dialog boxes', # balloon help
             tearoff=True)

        self.menu_bar.addmenuitem('Dialogs', 'command',
             label='Tk confirmation dialog',
             command=self.confirmation_dialog)

        self.menu_bar.addmenuitem('Dialogs', 'command',
             label='Tk message dialog',
             command=self.Tk_message_dialog)

        self.menu_bar.addmenuitem('Dialogs', 'command',
             label='Pmw message dialog',
             command=self.Pmw_message_dialog)

        self.menu_bar.addmenuitem('Dialogs', 'command',
             label='Fitting work room',
             command=self.fitting_dialog)

        self.menu_bar.addcascademenu('Dialogs', 'Color dialogs',
             statusHelp='Exemplify different color dialogs')

        self.menu_bar.addmenuitem('Color dialogs', 'command',
             label='Tk Color Dialog',
             command=self.tk_color_dialog)

        self.menu_bar.addmenuitem('Color dialogs', 'command',
             label='Pynche color dialog',
             command=self.pynche_color_dialog)
        
        self.menu_bar.addmenu('Future...',
             'Demonstrate various widgets and effects',
             tearoff=True)

        self.menu_bar.addmenuitem('Future...', 'command',
             label='List data',
             command=self.list_dialog)

        self.menu_bar.addmenuitem('Future...', 'command',
             label='Relief/borderwidth',
             command=self.relief_dialog)

        self.menu_bar.addmenuitem('Future...', 'command',
             label='Bitmaps',
             command=self.bitmap_dialog)

        self.menu_bar.addmenu('Help', None, side='right')

        self.menu_bar.addmenuitem('Help', 'command',
             label='Tutorial',
             command=self.tutorial)

        self.balloon_on = IntVar(); self.balloon_on.set(1)
        self.menu_bar.addmenuitem('Help', 'checkbutton',
             label='Balloon help',
             variable=self.balloon_on,
             command=self.toggle_balloon)

    def confirmation_dialog(self):
        message = 'This is an example of a FitLab Studio conformation dialog box'
        ok = tkMessageBox.askokcancel('OK', message)
        if ok:
            self.status_line.configure(text="'Quit' was pressed")
        else:
            self.status_line.configure(text="'Cancel' was pressed")

    def Tk_message_dialog(self):
        message = 'This is an example of a FitLab Studio message dialog box'
        answer = tkMessageBox.Message(icon='info', type='ok',
                 message=message, title='About').show()
        self.status_line.configure(text="'%s' was pressed" % answer)

    def Pmw_message_dialog(self):
        # message is typeset as a label so we need explicit newlines:
        message = """\
This is an example of the Pmw.MessageDialog box,
which is useful for writing longer text messages
to the FitLab Studio user."""
        Pmw.MessageDialog(self.master, title='Description',
                          buttons=('Quit',), message_text=message,
                          message_justify='left',
                          message_font='helvetica 12',
                          icon_bitmap='info',
                          # must be present if icon_bitmap is:
                          iconpos='w')  

    def fitting_dialog(self):
        self.fitting_d = Pmw.Dialog(self.master,
                          title='Fitting workshop',
                          buttons=('Apply', 'Cancel'),
                          #defaultbutton='Apply',
                          command=self.fitting_dialog_action)
        
        a,b = self.fields.get_frequency_ranges()
        diff= self.fields.get_difference_spectrum()
        data = self.__cut(self.x,diff,a,b)
        self.fitting_d_gui = FitWork(self.fitting_d.interior(),
                                     self.status_line,
                                     balloon=self.balloon, 
                                     data=data,
                                     scrolled=True)
        self.fitting_d_gui.pack()

    def fitting_dialog_action(self, result):
        # result contains the name of the button that we clicked
        if result == 'Apply':
            # example on extracting dialog variables:
            print "Hi"
            # (changing variables in self.gui are reflected in
            # the self.status_line)
        else:
            text = 'you just canceled the dialog'
            self.status_line.configure(text=text)
        # does not work: self.dialog.deactivate(result)
        self.fitting_d.destroy()  # destroy dialog window

    def __cut(self,x,data,a,b):
        t = []
        for i in xrange(len(data)):
            ww = x[i]
            if a<=ww<=b: t.append([x[i],data[i]])
        return array(t,dtype=float64)
            
    def file_read(self):
        fname = tkFileDialog.Open(filetypes=[('anyfile','*')]).show()
        text = 'chosen file to open: ' + os.path.basename(fname)
        self.status_line.configure(text=text)
        # the dialog checks the validity of the filename, but
        # pressing Cancel results in an empty return string
        if fname:
            self.display_file(fname, self.master)
        
    def display_file(self, filename, parent):
        """Read file into a text widget in a _separate_ window."""
        filewindow = Toplevel(parent) # new window

        f = open(filename, 'r');  filestr = f.read();  f.close()
        # determine the number of lines and the max linewidth:
        lines = filestr.split('\n')
        nlines = len(lines)
        maxwidth = max(map(lambda line: len(line), lines))
        
        filetext = Pmw.ScrolledText(filewindow,
             borderframe=5, # a bit space around the text
             vscrollmode='dynamic', hscrollmode='dynamic',
             labelpos='n', label_text='Contents of file '+filename,
             text_width=min(80,maxwidth),
             text_height=min(50,nlines),
             text_wrap='none',  # do not break lines
             )
        filetext.pack(expand=True, fill='both')

        filetext.insert('end', filestr)

        # add a quit button:
        Button(filewindow, text='Quit',
               command=filewindow.destroy).pack(pady=10)

        # force the new window to be in focus:
        filewindow.focus_set()

    def file_save(self):
        fname = tkFileDialog.SaveAs(
                filetypes=[('temporary files','*.tmp')],
                initialfile='myfile.tmp',
                title='Save a file').show()
        text = 'chosen file to save: "' + os.path.basename(fname) + '"'
        self.status_line.configure(text=text)

    def quit(self, event=None):
        self.master.destroy()

    def tk_color_dialog(self):
        # see python src, subdirectory Lib/lib-tk
        # and the tkColorChooser.py file
        color = tkColorChooser.Chooser(
            initialcolor='gray',title='Choose background color').show()
        # or:
        # color = tkColorChooser.askcolor()

        # color[0] is now an (r,g,b) tuple and
        # color[1] is a hexadecimal number; send the latter to
        # tk_setPalette to change the background color:
        # (when Cancel is pressed, color is (None,None))
        if color[0] is not None:
            self.master.tk_setPalette(color[1])
            text = 'new background color is ' + str(color[0]) + \
                   ' (rgb) or ' + str(color[1])
            self.status_line.configure(text=text)

        
    def pynche_color_dialog(self):
        #from pynche import pyColorChooser
        #color = pyColorChooser.askcolor(parent=self.master)
        # or
        import pynche.pyColorChooser
        color = pynche.pyColorChooser.askcolor(self.master)
        try:
            self.master.tk_setPalette(color[1])
            text = 'new background color is ' + str(color[0]) + \
                   ' (rgb) or ' + color[1]
            self.status_line.configure(text=text)
        except: pass
        
    def list_dialog(self):
        self.list_d = Pmw.Dialog(self.master,
                          title='Example of widgets for list data for future development of FitLab Studio!!!',
                          buttons=('Quit',), defaultbutton='Quit')
        lists = InputLists(self.list_d.interior(), self.status_line,
                           balloon=self.balloon)
        lists.pack(side='left')

    def relief_dialog(self):
        self.relief_d = Pmw.Dialog(self.master,
                          title='List of relief and borderwidth',
                          buttons=('Quit',),   # (default)
                          defaultbutton='Quit')

        self.reliefs_borderwidth(self.relief_d.interior())

    def reliefs_borderwidth(self, parent):
        # use a frame to align examples on various relief values:
        frame = Frame(parent); frame.pack(side='top',pady=15)
        # will use the grid geometry manager to pack widgets in this frame

        reliefs = ('groove', 'raised', 'ridge', 'sunken', 'flat')
        row = 0
        for borderwidth in (0,2,4,6):
            label = Label(frame, text='reliefs with borderwidth=%d: ' \
                          % borderwidth)
            label.grid(row=row, column=0, sticky='w', pady=5)
            for i in range(len(reliefs)):
                l = Label(frame, text=reliefs[i], relief=reliefs[i],
                          borderwidth=borderwidth)
                l.grid(row=row, column=i+1, padx=5, pady=5)
            row += 1

    def bitmap_dialog(self):
        self.bitmap_d = Pmw.Dialog(self.master,
                          title='Demo of predefined bitmaps',
                          buttons=('Quit',),
                          defaultbutton='Quit',
                          command=self.bitmap_dialog_action)

        self.bitmap_demo(self.bitmap_d.interior())

    def bitmap_demo(self, parent):
        # predefined bitmaps:
        bitmaps = ('error', 'gray25', 'gray50', 'hourglass',
                   'info', 'questhead', 'question', 'warning')
        Label(parent, text="""\
Predefined bitmaps, which can be used to
label dialogs (questions, info, etc.) for 
future development of FitLab Studio""",
              foreground='red').pack()
        frame = Frame(parent); frame.pack(side='top', pady=5)
        for i in range(len(bitmaps)):  # write name of bitmaps
            Label(frame, text=bitmaps[i]).grid(row=0, column=i+1)
        for i in range(len(bitmaps)):  # insert bitmaps
            Label(frame, bitmap=bitmaps[i]).grid(row=1, column=i+1)

    def bitmap_dialog_action(self, result):
        # result contains the name of the button that we clicked
        if result == 'Quit':
            if tkMessageBox.askyesno('Yes', 'Are you sure you want to quit?'):
                self.bitmap_d.destroy()

    def tutorial(self):
        self.tutorial_d = Pmw.Dialog(self.master,
                          title='Short explanation of this application',
                          buttons=('Quit',),
                          defaultbutton='Quit')
        text = """\
=================================================================
              Welcome to FitLab Studio 2013 !!!
=================================================================
This application demonstrates many of the most common tools in
graphical user interfaces with spectroscopic data. It provides
very poverful set of utilities for post-processing, fitting and
analyzing your spectras!. The typical usage is to (i) launch

   %s

Happy happy!!!!
Happy happy!!!!
""" % sys.argv[0]

        # determine the number of lines and the max linewidth:
        lines = text.split('\n');  nlines = len(lines)
        maxwidth = max(map(lambda line: len(line), lines))

        help = Pmw.ScrolledText(self.tutorial_d.interior(),
             borderframe=5, # a bit space around the text
             vscrollmode='dynamic', hscrollmode='dynamic',
             labelpos='n',
             label_text='How to make use of this application',
             text_width=min(80,maxwidth), text_height=min(50,nlines),
             text_wrap='none')
        help.pack()
        help.insert('end', text)

    def toggle_balloon(self):
        if self.balloon_on.get():
            self.balloon.configure(state='both')  # on
        else:
            self.balloon.configure(state='none')  # off
            
    # this one is not active; provides just an example:
    def Tk_pulldown(self, parent):
        """
        Demonstrate how to create a menu bar with basic Tk
        components. This is a lower-level alternative to
        Pmw.MenuBar.
        """
        # pull-down menu:
        self.pulldown = Menubutton(parent, text='Pulldown Menu',
                                   relief='groove', underline=False)
        self.pulldown.pack(side='left',padx=10)
    
        # add entries in the 'Pulldown Menu' menu:
        self.pulldown_menu = Menu(self.pulldown, tearoff=True)

        # first menu entry:
        self.pulldown_menu.add_command(label='Tk Confirmation Dialog',
             command=self.confirmation_dialog, underline=0, accelerator='Alt+C')

        self.pulldown_menu.add_command(label='Tk Message Dialog',
             command=self.about_dialog, underline=0, accelerator='Alt+T')

        self.pulldown_menu.add_command(label='Pmw Message Dialog',
             command=self.message_dialog, underline=4, accelerator='Alt+M')

        self.pulldown_menu.add_command(label='Pmw User-Defined Dialog',
             command=self.userdef_dialog, underline=4, accelerator='Alt+U')

        # add cascading menu, here an entry "File Dialogs"
        # with two submenus, "Open" and "Save As":
        self.file_menu = Menu(self.pulldown_menu, tearoff=True)
        self.pulldown_menu.add_cascade(label='File Dialogs',
             menu=self.file_menu, underline=0)
        self.file_menu.add_command(label='Open',
                                   command=self.file_read)
        self.file_menu.add_command(label='Save As',
                                   command=self.file_save)

        # continue with main menu:
        self.pulldown_menu.add('separator')  # horizontal line
        self.pulldown_menu.add_command(label='Tk Color Dialog',
                                       command=self.tk_color_dialog)
        self.pulldown_menu.add_command(label='Pynche Color Dialog',
                                       command=self.pynche_color_dialog)

        # set up a pointer from the menubutton back to the menu:
        # (required for the pull-down menu to be displayed!)
        self.pulldown['menu'] = self.pulldown_menu


def create_fields():
    """Launch a GUI consisting of class FitFields only."""
    root = Tk()
    Pmw.initialise(root)
    status = Label(root) 
    widget = FitFields(root, status)
    widget.pack()
    status.pack()  # get the status line below the widgets
    root.mainloop()
import tkMessageBox
    
def run_fitlab(bkgr,smpl):
    root = Tk()
    Pmw.initialise(root)
    root.title('Fitlab Studio 2013')
    widget = FitLab(root,bkgr=bkgr,smpl=smpl)
    # this widget packs itself...
    #def ask_quit():
    #if tkMessageBox.askokcancel("Quit", "You want to quit now? *sniff*"):
    # root.destroy()
    #root.protocol("WM_DELETE_WINDOW", ask_quit)
    root.mainloop()
    
# run FitLab and enjoy!!!
if __name__ == '__main__':
    #create_fields()
    smpl = sys.argv[1]
    bkgr = sys.argv[2]
    run_fitlab(bkgr,smpl)