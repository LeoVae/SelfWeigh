#!/usr/bin/python3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import datetime
try:
	from vars import vlist, v1, v2, vag_neto, vag_rega
except:
	vlist = "x"
	v1 = 0
	v2 = 0
	vag_neto = 0
	vag_rega = "nema"
import os, sys, csv
import pandas as pd
kliknuo = None
iztipkovnice = None
pathweighslips = os.path.abspath("~/SelfWeigh/weighslips")

def main():
	df = pd.read_csv("~/SelfWeigh/weighlist.csv", delim_whitespace=False).tail(100)
	df = df.reindex(index=df.index[::-1])
	df_list = [df.columns.tolist()] + df.reset_index().values.tolist()

	def func(eventObject):
		global vlist
		global vag_rega
		global dt_string
		global v1
		global v2
		global vag_neto
		global link_img
		global dt_string3
		prelist = izbornik.get()
		vlist = prelist.split(' ')[0]
		vag_rega = prelist.split(' ')[1]
		dt_string = prelist.split(' ')[2] + ' ' + prelist.split(' ')[3]
		dt_string = dt_string.replace("{","").replace("}","")
		dt_string3 = str(dt_string)
		v1 = prelist.split(' ')[4]
		v2 = prelist.split(' ')[5]
		vag_neto = prelist.split(' ')[6]
		prijevoznik = prelist.split(' ')[7]
		link_img_v1 = prelist.split(' ')[8]
		link_img = prelist.split(' ')[9]
		intVagRega = tk.StringVar(value=str(vag_rega))
		intWeigh1 = tk.StringVar(value=(str(v1), 'kg'))
		intWeigh2 = tk.StringVar(value=(str(v2), 'kg'))
		intVagNet = tk.StringVar(value=(str(vag_neto), 'kg'))
		l1.configure(textvariable=intVagRega)
		l2.configure(textvariable=intWeigh1)
		l3.configure(textvariable=intWeigh2)
		l4.configure(textvariable=intVagNet)
	
	def tipkovnica2():
		Keyboard_App = tk.Toplevel(root)
		Keyboard_App.lift()
		Keyboard_App.geometry("800x450")
		Keyboard_App.title(kliknuo)
		Keyboard_App.resizable(0,0)
		#Keyboard_App.overrideredirect(True) # goli prozor
		def donothing():
			pass
		Keyboard_App.protocol('WM_DELETE_WINDOW', donothing)
		def select(value):
			if value == "⌫":
				input = entry.get("1.0", 'end-2c')
				entry.delete("1.0", END)
				entry.insert("1.0", input, END)

			elif value == " Razmak ":
				entry.insert(tk.END, ' ')
				
			elif value == "Odustani":
				Keyboard_App.destroy()

			elif value == "Potvrdi":
				global iztipkovnice
				iztipkovnice = entry.get("1.0","end-1c")
				replace_fields()
				Keyboard_App.destroy()

			else:
				entry.insert(tk.END, value)

		buttons = [
			'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '=', "'", '"',
			'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Š', 'Đ', '⌫',
			'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Č', 'Ć', 'Ž', ';',
			'Y', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', ':', '-', '+', '/',
			'Odustani', ' Razmak ', 'Potvrdi',
		]
		entry = Text(Keyboard_App, width=30, height=2, font='Ubuntu 28 bold')
		entry.grid(row=1, columnspan=15)

		varRow = 2
		varColumn = 0

		for button in buttons:
			command = lambda x=button: select(x)
			if button != " Razmak " and button != "Odustani" and button != "Potvrdi":
				tk.Button(Keyboard_App, text=button, width=1, height=1, font='Ubuntu 28 bold', bg="black", fg="white",
							   activebackground="#ffffff", activeforeground="#000000", relief="groove", padx=14,
							   pady=8, bd=4, command=command).grid(row=varRow, column=varColumn)

			if button == " Razmak ":
				tk.Button(Keyboard_App, text=button, font="Ubuntu\ Condensed 16 bold", width=40, height=2, bg="#000000", fg="#ffffff",
							   activebackground="#ffffff", activeforeground="#000000", relief="raised", padx=4,
							   pady=1, bd=4, command=command).grid(row=6, columnspan=16)
							   
			if button == "Odustani":
				tk.Button(Keyboard_App, text=button, font="Ubuntu\ Condensed 16 bold", width=10, height=2, bg="#4D0000", fg="#ffffff",
							   activebackground="#ffffff", activeforeground="#000000", relief="raised", padx=4,
							   pady=1, bd=4, command=command).grid(row=6, column=0, columnspan=2)
							   
			if button == "Potvrdi":
				tk.Button(Keyboard_App, text=button, font="Ubuntu\ Condensed 16 bold", width=10, height=2, bg="#004200", fg="#ffffff",
							   activebackground="#ffffff", activeforeground="#000000", relief="raised", padx=4,
							   pady=1, bd=4, command=command).grid(row=6, column=11, columnspan=4)

			varColumn += 1
			if varColumn > 12:
				varColumn = 0
				varRow += 1
		Keyboard_App.transient(root)
		Keyboard_App.grab_set()
		root.wait_window(Keyboard_App)
		Keyboard_App.mainloop()
		

	root = tk.Tk()
	root.geometry("800x480")
	root.attributes('-fullscreen', True)
	now = datetime.now()
	dt_string = now.strftime("%d.%m.%Y.\n%H:%M:%S")
	dt_string2 = now.strftime("%d.%m.%Y.             %H:%M:%S")
	file_name = vlist
	os.chdir("~/SelfWeigh/weighslips")
	
	topframe = tk.Frame(root)
	topframe.place(x=295, y=10)
	bottomframe = tk.Frame(root)
	bottomframe.pack(side=tk.BOTTOM)
	bottomframe2 = tk.Frame(root)
	bottomframe2.pack(side=tk.BOTTOM)
	
	intVlist = tk.StringVar(value=str(vlist))
	intDate = tk.StringVar(value=str(dt_string))
	intVagRega = tk.StringVar(value=str(vag_rega))
	intWeigh1 = tk.StringVar(value=(str(v1), 'kg'))
	intWeigh2 = tk.StringVar(value=(str(v2), 'kg'))
	intVagNet = tk.StringVar(value=(str(vag_neto), 'kg'))
	

	def zovi1(event):
		global kliknuo
		kliknuo = 'Vrsta_Robe'
		tipkovnica2()
	def zovi2(event):
		global kliknuo
		kliknuo = 'Shipper'
		tipkovnica2()		
	def zovi3(event):
		global kliknuo
		kliknuo = 'Vozac'
		tipkovnica2()		
	def zovi4(event):
		global kliknuo
		kliknuo = 'Prodavac'
		tipkovnica2()		
	def zovi5(event):
		global kliknuo
		kliknuo = 'Kupac_ili_Preuzimatelj'
		tipkovnica2()


	tk.Label(topframe, font='Ubuntu\ Condensed 22', text="Vagarski list br.").grid(row=0)
	tk.Label(topframe, font='Ubuntu\ Condensed 22 bold', textvariable=intVlist).grid(row=0, column=1)
	tk.Label(topframe, font='Ubuntu\ Condensed 20', textvariable=intDate).grid(row=1)
	topframe.update()


	tk.Label(bottomframe, font='Ubuntu\ Condensed 17', text="LicensePlate:").grid(row=1, column=1, padx=10, pady=9)
	tk.Label(bottomframe, font='Ubuntu\ Condensed 17', text="Vaganje 1:").grid(row=1, column=3, padx=10, pady=9)
	tk.Label(bottomframe, font='Ubuntu\ Condensed 17', text="Vaganje 2:").grid(row=1, column=5, padx=10, pady=9)
	tk.Label(bottomframe, font='Ubuntu\ Condensed 17', text="Net:").grid(row=1, column=7, padx=10, pady=9)
	#tk.Label(leftframe2, font='Ubuntu\ Condensed 18', text="  ").grid(row=5, padx=20)

	l1=tk.Label(bottomframe, bg='#FCFCFC', font='Ubuntu\ Condensed 17 bold', textvariable=intVagRega)
	l1.grid(row=1, column=2, pady=5)
	l2=tk.Label(bottomframe, bg='#FCFCFC', font='Ubuntu\ Condensed 17 bold', textvariable=intWeigh1)
	l2.grid(row=1, column=4, pady=5)
	l3=tk.Label(bottomframe, bg='#FCFCFC', font='Ubuntu\ Condensed 17 bold', textvariable=intWeigh2)
	l3.grid(row=1, column=6, pady=5)
	l4=tk.Label(bottomframe, bg='#FCFCFC', font='Ubuntu\ Condensed 17 bold', textvariable=intVagNet)
	l4.grid(row=1, column=8, pady=5)
	bottomframe.update()


	tk.Label(bottomframe2, font='Ubuntu\ Condensed 18', text="Vagarinka:").grid(row=0, padx=20, pady=5)
	tk.Label(bottomframe2, font='Ubuntu\ Condensed 18', text="Vrsta robe:").grid(row=1, padx=20, pady=5)
	tk.Label(bottomframe2, font='Ubuntu\ Condensed 18', text="Shipper:").grid(row=2, padx=20, pady=5)
	tk.Label(bottomframe2, font='Ubuntu\ Condensed 18', text="Vozač:").grid(row=3, padx=20, pady=5)
	tk.Label(bottomframe2, font='Ubuntu\ Condensed 18', text="Prodavač:").grid(row=4, padx=20, pady=5)
	tk.Label(bottomframe2, font='Ubuntu\ Condensed 18', text="Kupac ili\nPreuzimatelj:").grid(row=7, padx=20, pady=0)
	
	def replace_fields():
		if kliknuo is 'Vrsta_Robe':
			I.delete (0,100)
			I.insert(0, iztipkovnice)
		elif kliknuo is 'Shipper':
			II.delete (0,100)
			II.insert(0, iztipkovnice)
		elif kliknuo is 'Vozac':
			III.delete (0,100)
			III.insert(0, iztipkovnice)
		elif kliknuo is 'Prodavac':
			IV.delete (0,100)
			IV.insert(0, iztipkovnice)
		elif kliknuo is 'Kupac_ili_Preuzimatelj':
			V.delete (0,100)
			V.insert(0, iztipkovnice)

	
	izbornik = ttk.Combobox(bottomframe2, values=df_list, state='readonly', font='Ubuntu\ Condensed 16 bold', width=50)
	izbornik.grid(sticky=W, row=0, column=1, pady=2, columnspan=4)
	izbornik.bind("<<ComboboxSelected>>", func)
	
	#ok = tk.Button(bottomframe2, text="Učitaj", command=func)
	#ok.grid(row=0, column=7, pady=2)
	
	I 		= tk.Entry(bottomframe2, bg='#FCFCFC', font='Ubuntu\ Condensed 16 bold', width=50)
	I.bind("<1>", zovi1)
	I.grid(sticky=W, row=1, column=1, pady=2, columnspan=4)

	II = tk.Entry(bottomframe2, bg='#FCFCFC', font='Ubuntu\ Condensed 16 bold', width=50)
	II.bind("<1>", zovi2)
	II.grid(sticky=W,row=2, column=1, pady=2, columnspan=4)
	
	III 		= tk.Entry(bottomframe2, bg='#FCFCFC', font='Ubuntu\ Condensed 16 bold', width=50)
	III.bind("<1>", zovi3)
	III.grid(sticky=W,row=3, column=1, pady=2, columnspan=4)
	
	IV 	= tk.Entry(bottomframe2, bg='#FCFCFC', font='Ubuntu\ Condensed 16 bold', width=50)
	IV.bind("<1>", zovi4)
	IV.grid(sticky=W, row=4, column=1, pady=2, columnspan=4)
		
	V 		= tk.Entry(bottomframe2, bg='#FCFCFC', font='Ubuntu\ Condensed 16 bold', width=50)
	V.bind("<1>", zovi5)
	V.delete (0,100)
	V.insert(0, "Vrček, Some  description")
	V.grid(sticky=W, row=7, column=1, padx=2, pady=2, columnspan=4)
	
	def empty_off():
		emptyvars()
		root.destroy()
	def ispisi_off():
		ispis()
		root.destroy()

	
	def emptyvars():
		os.chdir('~/SelfWeigh')
		with open('vars.py', 'w') as f:
			print('vlist = "x"', file=f)
			print('v1 = 0', file=f)
			print('v2 = 0', file=f)
			print('vag_neto = 0', file=f)
			print('vag_rega = "nema"', file=f)
			try:
				with open('~/SelfWeigh/vars.py', 'w') as rem_f:
					print ('file_name =', file_name, file = rem_f)
			except:
				print ('Ispis "file_name" u vars.py nije moguce.')
	
	def ispis():
		roba = I.get()
		prijevoznik = II.get()
		vozac = III.get()
		prodavac = IV.get()
		kupac = V.get()
		#with open('weighslips.txt', 'a') as f:
		
		str_v1 = str(v1)
		str_v2 = str(v2)
		str_vag_neto = str(vag_neto)
		str_vlist = str(vlist)
		
		file_name = (str(vlist) + "_na_zahtjev")
		with open(os.path.abspath(file_name), 'w') as f:
			print('YOUR-COMPANY, Some \ndescription\nAddress 123,\nCity\nwww.example.com\n', file=f)
			print(dt_string2, file=f)
			print('--------------------------------\nVagarski list br.',vlist, file=f)
			print('Vaganje 1:',v1, file=f)
			print('Vaganje 2:',v2, file=f)
			print('Net:    ',vag_neto, '\n--------------------------------', file=f)
			print('Vrsta Robe:',roba, file=f)
			print('LicensePlate:',vag_rega, file=f)
			print('Shipper:',prijevoznik, file=f)
			print('Vozac:',vozac, file=f)
			print('Prodavac:',prodavac, file=f)
			print('Kupac/Preuzimatelj:',kupac, '\n\n\n\n', file=f)
			
		with open('~/SelfWeigh/vars_print.py', 'w') as f:
			print('v1 =', '"' + str_v1 + '"', file=f)
			print('v2 =', '"' + str_v2 + '"', file=f)
			print('vag_neto =', '"' + str_vag_neto + '"', file=f)
			print('roba =', '"' + roba + '"', file=f)
			print('vag_rega =', '"' + vag_rega + '"' , file=f)
			print('prijevoznik =', '"' + prijevoznik + '"', file=f)
			print('vozac =', '"' + vozac + '"', file=f)
			print('prodavac =', '"' + prodavac + '"', file=f)
			print('kupac =', '"' + kupac + '"', file=f)
			print('vlist =', '"' + file_name + '"', file=f)
			print('link_img =', '"' + link_img + '"', file=f)
			print('dt_string =', '"' + dt_string3 + '"', file=f)
		emptyvars()
		with open('~/SelfWeigh/vars.py', 'w') as f:
			print ('file_name =', '"' + str(file_name) + '"', file=f)
		#os.system('python3 ~/SelfWeigh/print.py')
		os.popen("~/SelfWeigh/print_cups.py")
		#os.system("python3 ~/SelfWeigh/print_cups.py")
	
	
	tk.Button(root, text='     \nOdustani\n     ', bg='#FFE7E6', font='Ubuntu\ Condensed 18 bold', command=empty_off).place(x=20, y=10)
	tk.Button(root, text='\n   Ispiši   \n', bg='#E6FFE6', font='Ubuntu\ Condensed 18 bold', command=ispisi_off).place(x=665, y=10)
	
	root.update()
	#bottomframe2.update()
	root.mainloop()

if __name__ == "__main__":
	main()
