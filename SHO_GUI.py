from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkm
from SHO_APP import SHO_APP


class SHO_:
	def __init__(self,master):
		self.master=master
		self.sho=SHO_APP()
		self.master_width=450
		self.master_height=450
		self.master.geometry("{}x{}".format(self.master_width,self.master_height))
		self.master.title("Smart Home Office -- Application Manager")
		self.master.config(bg="white")
		Grid.rowconfigure(self.master,0,weight=1)
		Grid.columnconfigure(self.master,0,weight=1)
		self.create_menu()
		self.create_mainframe1()
		self.create_mainframe2()
		self.fill_mainframe1()
		self.fill_mainframe2()


	def refresh(self):
		self.fill_mainframe1()
		self.fill_mainframe2()

	def create_menu(self):
		self.mainmenu=Menu(self.master)
		self.master.config(menu=self.mainmenu)

		self.OptionMenu=Menu(self.mainmenu)
		self.mainmenu.add_cascade(label="Options",menu=self.OptionMenu)
		self.OptionMenu.add_command(label="Open settings",command=self.open_settings)

		self.OptionMenu.add_separator()

		self.modeVar=IntVar()
		self.modeVar.set(2)
		self.OptionMenu.add_radiobutton(label="Day mode",value=1,variable=self.modeVar,command=self.refresh)
		self.OptionMenu.add_radiobutton(label="Night mode",value=2,variable=self.modeVar,command=self.refresh)
		self.OptionMenu.add_separator()
		self.OptionMenu.add_command(label="Refresh",command=self.refresh)

		self.OptionMenu.add_separator()

		self.NewsletterMenu=Menu(self.OptionMenu)
		self.OptionMenu.add_cascade(label="Newsletter",menu=self.NewsletterMenu)

		self.nlEnableVar=IntVar()
		self.nlEnableVar.set(1)
		self.NewsletterMenu.add_checkbutton(label="Enable",onvalue=1,offvalue=0,variable=self.nlEnableVar,
			command=self.change_Newsletter_Properties)

		self.selectCountryMenu=Menu(self.NewsletterMenu)
		self.selectCategoryMenu=Menu(self.NewsletterMenu)
		self.NewsletterMenu.add_cascade(label="Country of Interest",menu=self.selectCountryMenu,
			command=self.change_Newsletter_Properties)
		self.NewsletterMenu.add_cascade(label="Category of Interest",menu=self.selectCategoryMenu,
			command=self.change_Newsletter_Properties)

		self.countryVar=IntVar()
		self.countryVar.set(1)
		self.selectCountryMenu.add_radiobutton(label="us",value=1,variable=self.countryVar,command=self.change_Newsletter_Properties)
		self.selectCountryMenu.add_radiobutton(label="tw",value=2,variable=self.countryVar,command=self.change_Newsletter_Properties)

		self.categoryVar=IntVar()
		self.categoryVar.set(2)
		self.selectCategoryMenu.add_radiobutton(label="business",value=1,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)
		self.selectCategoryMenu.add_radiobutton(label="technology",value=2,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)
		self.selectCategoryMenu.add_radiobutton(label="entertainment",value=3,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)
		self.selectCategoryMenu.add_radiobutton(label="science",value=4,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)
		self.selectCategoryMenu.add_radiobutton(label="health",value=5,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)
		self.selectCategoryMenu.add_radiobutton(label="sport",value=6,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)
		self.selectCategoryMenu.add_radiobutton(label="general",value=7,variable=self.categoryVar,
			command=self.change_Newsletter_Properties)

	def change_Newsletter_Properties(self):
		country_list=["us","tw"]
		category_list=["business","technology","entertainment","science","health","sport","general"]
		self.sho.gmr.Enabled=bool(self.nlEnableVar.get())
		self.sho.gmr.country_of_interest=country_list[int(self.countryVar.get())-1]
		self.sho.gmr.category_of_interest=category_list[int(self.categoryVar.get())-1]

	def open_settings(self):
		try:
			if self.settings_root:
				self.settings_root.deicocnify()
		except:
			self.settings_root=Toplevel(self.master)
			self.settings_run=SHO_Settings(self.settings_root,self.sho)
			self.settings_root.transient()
			self.settings_root.focus_force()

	def create_mainframe1(self):
		self.mainframe1_bg="white"
		self.mainframe1_fg="black"
		self.mainframe1_row_number=25
		self.mainframe1_col_number=50

		self.mainframe1=Frame(self.master,bg=self.mainframe1_bg,cursor="hand2")
		self.mainframe1.grid(row=0,column=0,
			rowspan=self.mainframe1_row_number,
			columnspan=self.mainframe1_col_number,
			sticky=N+S+E+W)

		for rows in range(self.mainframe1_row_number):
			Grid.rowconfigure(self.mainframe1,rows,weight=1,uniform="foo")
			for cols in range(self.mainframe1_col_number):
				Grid.columnconfigure(self.mainframe1,cols,weight=1,uniform="foo")

	def create_mainframe2(self):
		self.mainframe2_bg="white"
		self.mainframe2_fg="black"
		self.mainframe2_row_number=25
		self.mainframe2_col_number=50

		self.mainframe2=Frame(self.master,bg=self.mainframe2_bg,cursor="hand2")
		self.mainframe2.grid(row=25,column=0,
			rowspan=self.mainframe2_row_number,
			columnspan=self.mainframe2_col_number,
			sticky=N+S+E+W)

		for rows in range(self.mainframe2_row_number):
			Grid.rowconfigure(self.mainframe2,rows,weight=1,uniform="foo")
			for cols in range(self.mainframe2_col_number):
				Grid.columnconfigure(self.mainframe2,cols,weight=1,uniform="foo")

	def fill_mainframe1(self):
		self.maincanvas1=Canvas(self.mainframe1)#,bg=self.mainframe1_bg)
		if int(self.modeVar.get())==1:
			self.maincanvas1.config(bg="white")
		else:
			self.maincanvas1.config(bg="black")
		self.maincanvas1.grid(row=0,column=0,rowspan=self.mainframe1_row_number,
			columnspan=self.mainframe1_col_number,sticky=N+S+E+W)
		self.config(self.maincanvas1)

		self.modeText=self.maincanvas1.create_text(150,100,font=("Helvetica",20),
						text="Automation mode")
		if int(self.modeVar.get())==1:
			self.maincanvas1.itemconfig(self.modeText,fill="black")
		else:
			self.maincanvas1.itemconfig(self.modeText,fill="white")
		if self.sho.get_automation_button()==1:
			self.modeFigure=self.maincanvas1.create_oval(300,70,400,130,fill="green",outline="green")
			self.modeInfo=self.maincanvas1.create_text(350,100,font=("Times",15),text="ON",justify="center")
		else:
			self.modeFigure=self.maincanvas1.create_oval(300,70,400,130,fill="red",outline="red")
			self.modeInfo=self.maincanvas1.create_text(350,100,font=("Times",15),text="OFF",justify="center")
		self.maincanvas1.bind("<Button-1>",self.change_state1)

	def fill_mainframe2(self):
		self.maincanvas2=Canvas(self.mainframe2)#,bg=self.mainframe2_bg)
		if int(self.modeVar.get())==1:
			self.maincanvas2.config(bg="white")
		else:
			self.maincanvas2.config(bg="black")
		self.maincanvas2.grid(row=0,column=0,rowspan=self.mainframe2_row_number,
			columnspan=self.mainframe2_col_number,sticky=N+S+E+W)
		self.config(self.maincanvas2)

		self.controlText=self.maincanvas2.create_text(150,100,font=("Helvetica",20),
						text="Light switch")
		if int(self.modeVar.get())==1:
			self.maincanvas2.itemconfig(self.modeText,fill="black")
		else:
			self.maincanvas2.itemconfig(self.modeText,fill="white")
		if self.sho.get_control_button()==1:
			self.controlFigure=self.maincanvas2.create_oval(300,70,400,130,fill="green",outline="green")
			self.controlInfo=self.maincanvas2.create_text(350,100,font=("Times",15),text="ON",justify="center")
		else:
			self.controlFigure=self.maincanvas2.create_oval(300,70,400,130,fill="red",outline="red")
			self.controlInfo=self.maincanvas2.create_text(350,100,font=("Times",15),text="OFF",justify="center")
		self.maincanvas2.bind("<Button-1>",self.change_state2)


	def change_state1(self,event):
		if self.maincanvas1.itemcget(self.modeFigure,"fill")=="green":
			self.maincanvas1.itemconfig(self.modeFigure,fill="red",outline="red")
			self.maincanvas1.itemconfig(self.modeInfo,text="OFF")
			self.sho.set_automation_button(0)
		else:
			self.maincanvas1.itemconfig(self.modeFigure,fill="green",outline="green")
			self.maincanvas1.itemconfig(self.modeInfo,text="ON")
			self.sho.set_automation_button(1)

	def change_state2(self,event):
		if self.maincanvas2.itemcget(self.controlFigure,"fill")=="green":
			self.maincanvas2.itemconfig(self.controlFigure,fill="red",outline="red")
			self.maincanvas2.itemconfig(self.controlInfo,text="OFF")
			self.sho.set_control_button(0)
		else:
			self.maincanvas2.itemconfig(self.controlFigure,fill="green",outline="green")
			self.maincanvas2.itemconfig(self.controlInfo,text="ON")
			self.sho.set_control_button(1)

	
	def config(self,widget):
		Grid.rowconfigure(widget,0,weight=1)
		Grid.columnconfigure(widget,0,weight=1)



class SHO_Settings:
	def __init__(self,master,sho):
		self.master=master
		self.sho=sho
		self.master_width=500
		self.master_height=500
		self.master.geometry("{}x{}".format(self.master_width,self.master_height))
		self.master.minsize(self.master_width,self.master_height)
		self.master.maxsize(self.master_width,self.master_height)
		self.master.title("Smart Home Office -- Settings")
		self.master.config(bg="white")
		Grid.rowconfigure(self.master,0,weight=1)
		Grid.columnconfigure(self.master,0,weight=1)
		self.settings_init_data=self.load_data()
		#print(self.settings_init_data)
		self.create_mainframe()
		self.fill_mainframe()

	def load_data(self):
		lightVar=self.sho.get_light_delay()
		if self.sho.gmr:
			gmrVar=1
		else:
			gmrVar=0
		gmrDelayVar=int(self.sho.gmr.get_sleep_delay())
		gmrFromVar=str(self.sho.gmr.push_from_.time())[0:-3]
		gmrToVar=str(self.sho.gmr.push_to.time())[0:-3]


		return (lightVar,gmrVar,gmrDelayVar,gmrFromVar,gmrToVar)

	def create_mainframe(self):
		self.mainframe_bg="white"
		self.mainframe_fg="black"
		self.mainframe_row_number=25
		self.mainframe_col_number=25

		self.mainframe=Frame(self.master,bg=self.mainframe_bg)
		self.mainframe.grid(row=0,column=0,
			rowspan=self.mainframe_row_number,
			columnspan=self.mainframe_col_number,
			sticky=N+S+E+W)

		for rows in range(self.mainframe_row_number):
			Grid.rowconfigure(self.mainframe,rows,weight=1,uniform="foo")
			for cols in range(self.mainframe_col_number):
				Grid.columnconfigure(self.mainframe,cols,weight=1,uniform="foo")

	def fill_mainframe(self):
		self.lightLabel=Label(self.mainframe,text="Light on-delay",
						font=("Times",14),bg=self.mainframe_bg)
		self.lightLabel.grid(row=0,column=0,columnspan=6,sticky=N+S+E+W)
		self.config(self.lightLabel)

		self.lightVar=IntVar()
		self.lightVar.set(int(self.settings_init_data[0]))
		self.light_delay=ttk.Entry(self.mainframe,width=10,textvariable=self.lightVar)
		self.light_delay.grid(row=0,column=6,columnspan=2,
			sticky=N+S+E+W)
		self.config(self.light_delay)

		minuteLabel=Label(self.mainframe,text="minute(s)",bg=self.mainframe_bg,
							font=("Times",13))
		minuteLabel.grid(row=0,column=9,columnspan=5,sticky=N+S+E+W)
		self.config(minuteLabel)

		separator=Label(self.mainframe,text=80*"_",bg=self.mainframe_bg)
		separator.grid(row=2,column=0,columnspan=25,sticky=N+S+E+W)
		self.config(separator)

		self.gmrLabel=Label(self.mainframe,text="Good Morning Routine",font=("Times",14),
			bg=self.mainframe_bg)
		self.gmrLabel.grid(row=5,column=0,columnspan=6,sticky=N+S+E+W)
		self.config(self.gmrLabel)

		self.gmrVar=IntVar()
		self.gmrVar.set(int(self.settings_init_data[1]))
		self.gmrCheckBtn=Checkbutton(self.mainframe,bg=self.mainframe_bg,
			onvalue=1,offvalue=0,
			relief="flat",
			variable=self.gmrVar)
		self.gmrCheckBtn.grid(row=5,column=7,columnspan=2,sticky=N+S+E+W)
		self.config(self.gmrCheckBtn)

		self.gmrDelayLabel=Label(self.mainframe,text="GMR sleep delay",font=("Times",14),
			bg=self.mainframe_bg)
		self.gmrDelayLabel.grid(row=9,column=0,columnspan=6,sticky=N+S+E+W)
		self.config(self.gmrDelayLabel)

		self.gmrDelayVar=IntVar()
		self.gmrDelayVar.set(int(self.settings_init_data[2]))
		self.gmrDelayEntry=ttk.Entry(self.mainframe,textvariable=self.gmrDelayVar)
		self.gmrDelayEntry.grid(row=9,column=7,columnspan=5,sticky=N+S+E+W)
		self.config(self.gmrDelayEntry)

		secondsLabel=Label(self.mainframe,text="seconds",bg=self.mainframe_bg,font=("Times",13))
		secondsLabel.grid(row=9,column=13,columnspan=5,sticky=N+S+E+W)
		self.config(secondsLabel)

		self.gmrNotification=Label(self.mainframe,text="Set time period to receive notification",
			font=("Helvetica",14),bg=self.mainframe_bg)
		self.gmrNotification.grid(row=12,column=0,columnspan=15,sticky=N+S+E+W)
		self.config(self.gmrNotification)

		self.gmrNotifyFromLabel=Label(self.mainframe,text="From",font=("Helvetica",14),
			bg=self.mainframe_bg)
		self.gmrNotifyFromLabel.grid(row=15,column=0,columnspan=3,sticky=N+S+E+W)
		self.config(self.gmrNotifyFromLabel)

		self.gmrFromVar=StringVar()
		self.gmrFromVar.set(str(self.settings_init_data[3]))
		self.gmrNotifyFromEntry=ttk.Entry(self.mainframe,textvariable=self.gmrFromVar)
		self.gmrNotifyFromEntry.grid(row=15,column=4,columnspan=3,sticky=N+S+E+W)
		self.config(self.gmrNotifyFromEntry)

		self.gmrNotifyToLabel=Label(self.mainframe,text="To",font=("Helvetica",14),
			bg=self.mainframe_bg)
		self.gmrNotifyToLabel.grid(row=19,column=0,columnspan=3,sticky=N+S+E+W)
		self.config(self.gmrNotifyToLabel)

		self.gmrToVar=StringVar()
		self.gmrToVar.set(str(self.settings_init_data[4]))
		self.gmrNotifyToEntry=ttk.Entry(self.mainframe,textvariable=self.gmrToVar)
		self.gmrNotifyToEntry.grid(row=19,column=4,columnspan=3,sticky=N+S+E+W)
		self.config(self.gmrNotifyToEntry)

		self.Okbtn=ttk.Button(self.mainframe,text="save",command=self.save_changes)
		self.Okbtn.grid(row=23,rowspan=2,column=15,columnspan=2,sticky=N+S+E+W)
		self.config(self.Okbtn)

		self.CancelBtn=ttk.Button(self.mainframe,text="cancel",command=self.cancel_changes)
		self.CancelBtn.grid(row=23,rowspan=2,column=19,columnspan=2,sticky=N+S+E+W)
		self.config(self.CancelBtn)

	def save_changes(self):
		#try:
		light_delay=int(self.lightVar.get())
		self.sho.set_light_delay(light_delay)
		print("Light delay set to",light_delay,"minute(s)")
		gmr=int(self.gmrVar.get())
		if gmr:
			self.sho.gmr.set_mode(True)
			print("GMR set to true")
		else:
			self.sho.gmr.set_mode(False)
			print("GMR set to false")
		gmr_sleep_delay=int(self.gmrDelayVar.get())
		self.sho.set_gmr_sleep_delay(gmr_sleep_delay)
		print("GMR sleep delay changed to",gmr_sleep_delay)
		from_=str(self.gmrFromVar.get())
		to=str(self.gmrToVar.get())
		self.sho.set_gmr_time_for_push_notification(from_,to)
		print("Notification period set from "+from_+" to "+to)
		self.master.destroy()
		# except:
		# 	tkm.showwarning("Error detected","An error occured, make sure your values are correct")

	def cancel_changes(self):
		self.master.destroy()


	def config(self,widget):
		Grid.rowconfigure(widget,0,weight=1)
		Grid.columnconfigure(widget,0,weight=1)


def main():
	root=Tk()
	run=SHO_(root)
	root.mainloop()

if __name__=="__main__":
	main()