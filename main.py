from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from tkinter import ttk
import sys

def read_data(file_to_read,pos,grab):
    with open(file_to_read,"rb") as opened_file:
        opened_file.seek(pos,0)
        grabed_data=opened_file.read(grab)
    return grabed_data

def make_backup(filebkp):
    with open(filebkp,"rb") as rf_exe:
        chunk_size=4096
        with open(Path(filebkp).stem+".bak","wb") as wf_exe:
            rf_exe_chunk = rf_exe.read(chunk_size)
            while len(rf_exe_chunk) >0:
                wf_exe.write(rf_exe_chunk)
                rf_exe_chunk = rf_exe.read(chunk_size)

def save_changes(gamever):
    if gamever==0:
        if len(PC_server.get())>30:
            messagebox.showerror(title=app_name,message="El servidor supera la cantidad de caracteres")
        elif len(PC_stun.get())>26:
            messagebox.showerror(title=app_name,message="El servidor stun supera la cantidad de caracteres")
        else:
            if PC_backup_check:
                make_backup(PC_exe)
            try:
                with open(PC_exe,"r+b") as opened_file:
                    #primero ponemos en cero el espacio para escribir
                    #es por si ponen una ip o dns que sea con menos letras que el original, cosa muy probable
                    opened_file.seek(0x7B48C4,0)
                    i=0
                    while i<30:
                        opened_file.write(b'\x00')
                        i=i+1
                    opened_file.seek(0x7B5A1C,0)
                    i=0
                    while i<26:
                        opened_file.write(b'\x00')
                        i=i+1
                    #ahora si escribimos lo que nos dice el usuario
                    opened_file.seek(0x7B48C4,0)
                    opened_file.write(PC_server.get().encode('utf-8'))
                    opened_file.seek(0x7B5A1C,0)
                    opened_file.write(PC_stun.get().encode('utf-8'))
                update_entrybox(gamever)
                messagebox.showinfo(title=app_name,message="Cambios guardados con exito!")
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                messagebox.showerror(title=app_name, message="Error al escribir en PES6.exe\nejecute como administrador o revise los permisos")
    if gamever==1:
        if len(PS2_server.get())>30:
            messagebox.showerror(title=app_name,message="El servidor supera la cantidad de caracteres")
        elif len(PS2_stun.get())>26:
            messagebox.showerror(title=app_name,message="El servidor stun supera la cantidad de caracteres")
        else:
            if PS2_backup_check:
                make_backup(PS2_ovl1)
                make_backup(PS2_ovl20)
            try:
                with open(PS2_ovl20,"r+b") as opened_file:
                    #primero ponemos en cero el espacio para escribir
                    #es por si ponen una ip o dns que sea con menos letras que el original, cosa muy probable
                    opened_file.seek(0x85CE0,0)
                    i=0
                    while i<30:
                        opened_file.write(b'\x00')
                        i=i+1
                    opened_file.seek(0x85CE0,0)
                    opened_file.write(PS2_server.get().encode('utf-8'))
                with open(PS2_ovl1,"r+b") as opened_file:
                    opened_file.seek(0x1EBA0,0)
                    i=0
                    while i<26:
                        opened_file.write(b'\x00')
                        i=i+1
                    #ahora si escribimos lo que nos dice el usuario
                    opened_file.seek(0x1EBA0,0)
                    opened_file.write(PS2_stun.get().encode('utf-8'))
                update_entrybox(gamever)
                messagebox.showinfo(title=app_name,message="Cambios guardados con exito!")
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                messagebox.showerror(title=app_name, message="Error al escribir en los archivos ovl\nejecute como administrador o revise los permisos")
    if gamever==2:
        if len(WE10LE_server.get())>27:
            messagebox.showerror(title=app_name,message="El servidor supera la cantidad de caracteres")
        elif len(WE10LE_stun.get())>26:
            messagebox.showerror(title=app_name,message="El servidor stun supera la cantidad de caracteres")
        else:
            if WE10LE_backup_check:
                make_backup(WE10LE_ovl1)
                make_backup(WE10LE_ovl20)
            try:
                with open(WE10LE_ovl20,"r+b") as opened_file:
                    #primero ponemos en cero el espacio para escribir
                    #es por si ponen una ip o dns que sea con menos letras que el original, cosa muy probable
                    opened_file.seek(0x869E0,0)
                    i=0
                    while i<27:
                        opened_file.write(b'\x00')
                        i=i+1
                    opened_file.seek(0x869E0,0)
                    opened_file.write(WE10LE_server.get().encode('utf-8'))
                with open(WE10LE_ovl1,"r+b") as opened_file:
                    opened_file.seek(0x1F110,0)
                    i=0
                    while i<26:
                        opened_file.write(b'\x00')
                        i=i+1
                    #ahora si escribimos lo que nos dice el usuario
                    opened_file.seek(0x1F110,0)
                    opened_file.write(WE10LE_stun.get().encode('utf-8'))
                update_entrybox(gamever)
                messagebox.showinfo(title=app_name,message="Cambios guardados con exito!")
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                messagebox.showerror(title=app_name, message="Error al escribir en los archivos ovl\nejecute como administrador o revise los permisos")

def update_entrybox(gamever):
    if gamever==0:
        PC_stun.delete(0, 'end')
        PC_server.delete(0, 'end')
        server=read_data(PC_exe,0x7B48C4,0x1E)
        stun=read_data(PC_exe,0x7B5A1C,0x1A)
        PC_server.insert(0,server.decode('utf-8'))
        PC_stun.insert(0,stun.decode('utf-8'))
    if gamever==1:
        PS2_stun.delete(0, 'end')
        PS2_server.delete(0, 'end')
        server=read_data(PS2_ovl20,0x85CE0,0x1E)
        stun=read_data(PS2_ovl1,0x1EBA0,0x1A)
        PS2_server.insert(0,server.decode('utf-8'))
        PS2_stun.insert(0,stun.decode('utf-8'))
    if gamever==2:
        WE10LE_stun.delete(0, 'end')
        WE10LE_server.delete(0, 'end')
        server=read_data(WE10LE_ovl20,0x869E0,0x1B)
        stun=read_data(WE10LE_ovl1,0x1F110,0x1A)
        WE10LE_server.insert(0,server.decode('utf-8'))
        WE10LE_stun.insert(0,stun.decode('utf-8'))

def search_file(gamever):
    if gamever==0:
        global PC_label
        global PC_exe
        PC_label.destroy()
        PC_exe=filedialog.askopenfilename(initialdir=".",title="Select a file", filetypes=[("PES6 Executable", "*.exe")])
        if PC_exe!='':
            #print(Path(PC_exe).stat().st_size)
            PC_label=Label(PES6_PC,text=PC_exe)
            PC_label.place(x=1,y=250)
            update_entrybox(gamever)
        else: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=app_name, message="Seleccione un PES6.exe")
    if gamever==1:
        global PS2_label_1
        global PS2_label_20
        global PS2_ovl1
        global PS2_ovl20
        messagebox.showinfo(title=app_name, message="Seleccione primero el unknow_00001.ovl\ny luego el unknow_00020.ovl")
        PS2_label_1.destroy()
        PS2_label_20.destroy()
        PS2_ovl1=filedialog.askopenfilename(initialdir=".",title="Seleccione el unknow_00001", filetypes=[("unknow_00001", "*.ovl"),("unknow_00001", "*.bin"),("Todos los archivos", "*.*")])
        PS2_ovl20=filedialog.askopenfilename(initialdir=".",title="Seleccione el unknow_00020", filetypes=[("unknow_00020", "*.ovl"),("unknow_00020", "*.bin"),("Todos los archivos", "*.*")])
        if PS2_ovl1!='' or PS2_ovl20!='':
            #print(Path(PC_exe).stat().st_size)
            PS2_label_1=Label(PES6_PS2,text=PS2_ovl1)
            PS2_label_20=Label(PES6_PS2,text=PS2_ovl20)
            PS2_label_1.place(x=1,y=230)
            PS2_label_20.place(x=1,y=250)
            update_entrybox(gamever)
        else: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=app_name, message="Seleccione los archivos indicados!")
    if gamever==2:
        global WE10LE_label_1
        global WE10LE_label_20
        global WE10LE_ovl1
        global WE10LE_ovl20
        messagebox.showinfo(title=app_name, message="Seleccione primero el unknow_00001.ovl\ny luego el unknow_00020.ovl")
        WE10LE_label_1.destroy()
        WE10LE_label_20.destroy()
        WE10LE_ovl1=filedialog.askopenfilename(initialdir=".",title="Seleccione el unknow_00001", filetypes=[("unknow_00001", "*.ovl"),("unknow_00001", "*.bin"),("Todos los archivos", "*.*")])
        WE10LE_ovl20=filedialog.askopenfilename(initialdir=".",title="Seleccione el unknow_00020", filetypes=[("unknow_00020", "*.ovl"),("unknow_00020", "*.bin"),("Todos los archivos", "*.*")])
        if WE10LE_ovl1!='' or WE10LE_ovl20!='':
            #print(Path(PC_exe).stat().st_size)
            WE10LE_label_1=Label(WE10LE,text=WE10LE_ovl1)
            WE10LE_label_20=Label(WE10LE,text=WE10LE_ovl20)
            WE10LE_label_1.place(x=1,y=230)
            WE10LE_label_20.place(x=1,y=250)
            update_entrybox(gamever)
        else: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=app_name, message="Seleccione los archivos indicados!")
        
def close():
    root.destroy()
    sys.exit()

app_name="PES6/WE10LE Server Changer"
root = Tk()
root.title(app_name)
#root.geometry("400x200")
w = 400 # width for the Tk root
h = 300 # height for the Tk root
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

my_notebook=ttk.Notebook(root)
PES6_PC=Frame(my_notebook,width=w,height=h)
PES6_PS2=Frame(my_notebook,width=w,height=h)
WE10LE=Frame(my_notebook,width=w,height=h)

#PES 6 pc frame definicion de variables

PC_exe=r''
my_btn=Button(PES6_PC, text="Selecciona el ejecutable\nPES6.exe", command=lambda: search_file(0))
PC_backup_check=IntVar()
checkbox_backup=Checkbutton(PES6_PC, text="Hacer backup\nde PES6.exe",variable=PC_backup_check)
PC_label=Label(PES6_PC)
PC_server_lbl=Label(PES6_PC,text="Game server")
PC_server=Entry(PES6_PC,width=32)
PC_stun_lbl=Label(PES6_PC,text="Stun server")
PC_stun=Entry(PES6_PC,width=32)
PC_save=Button(PES6_PC, text="Guardar", command=lambda: save_changes(0))
PC_exit=Button(PES6_PC, text="Salir", command=close)

#PS2_ ps2 frame definicion de variables

PS2_ovl1=r''
PS2_ovl20=r''
PS2_select=Button(PES6_PS2, text="Seleccionar los\narchivos ovl", command=lambda: search_file(1))
PS2_backup_check=IntVar()
PS2_checkbox_backup=Checkbutton(PES6_PS2, text="Hacer backup de\nlos archivos ovl",variable=PS2_backup_check)
PS2_label_1=Label(PES6_PS2)
PS2_label_20=Label(PES6_PS2)
PS2_server_lbl=Label(PES6_PS2,text="Game server")
PS2_server=Entry(PES6_PS2,width=32)
PS2_stun_lbl=Label(PES6_PS2,text="Stun server")
PS2_stun=Entry(PES6_PS2,width=32)
PS2_save=Button(PES6_PS2, text="Guardar", command=lambda: save_changes(1))
PS2_exit=Button(PES6_PS2, text="Salir", command=close)
PS2_info=Label(PES6_PS2,text="*Importante, debe extraer los archivos 1 y 20 del over.afs")


#WE10LE ps2 frame definicion de variables

WE10LE_ovl1=r''
WE10LE_ovl20=r''
WE10LE_select=Button(WE10LE, text="Seleccionar los\narchivos ovl", command=lambda: search_file(2))
WE10LE_backup_check=IntVar()
WE10LE_checkbox_backup=Checkbutton(WE10LE, text="Hacer backup de\nlos archivos ovl",variable=WE10LE_backup_check)
WE10LE_label_1=Label(WE10LE)
WE10LE_label_20=Label(WE10LE)
WE10LE_server_lbl=Label(WE10LE,text="Game server")
WE10LE_server=Entry(WE10LE,width=32)
WE10LE_stun_lbl=Label(WE10LE,text="Stun server")
WE10LE_stun=Entry(WE10LE,width=32)
WE10LE_save=Button(WE10LE, text="Guardar", command=lambda: save_changes(2))
WE10LE_exit=Button(WE10LE, text="Salir", command=close)
WE10LE_info=Label(WE10LE,text="*Importante, debe extraer los archivos 1 y 20 del over.afs")



#notebook placing
my_notebook.pack()
PES6_PC.pack(fill="both", expand=1)
PES6_PS2.pack(fill="both", expand=1)
WE10LE.pack(fill="both", expand=1)
my_notebook.add(PES6_PC,text="PES6 PC")
my_notebook.add(PES6_PS2,text="PES6 PS2")
my_notebook.add(WE10LE,text="WE10LE")

#PES6 PC placing 
my_btn.place(x=120,y=150)
checkbox_backup.place(x=280,y=150)
PC_server_lbl.place(x=10,y=20)
PC_server.place(x=90,y=20)
PC_stun_lbl.place(x=10,y=40)
PC_stun.place(x=90,y=40)
PC_save.place(x=120,y=200)
PC_exit.place(x=200,y=200)

#PES6 PS2 placing 
PS2_select.place(x=130,y=150)
PS2_checkbox_backup.place(x=250,y=150)
PS2_server_lbl.place(x=10,y=20)
PS2_server.place(x=90,y=20)
PS2_stun_lbl.place(x=10,y=40)
PS2_stun.place(x=90,y=40)
PS2_save.place(x=120,y=200)
PS2_exit.place(x=200,y=200)
PS2_info.place(x=10,y=70)

#WE10LE PS2 placing 
WE10LE_select.place(x=130,y=150)
WE10LE_checkbox_backup.place(x=250,y=150)
WE10LE_server_lbl.place(x=10,y=20)
WE10LE_server.place(x=90,y=20)
WE10LE_stun_lbl.place(x=10,y=40)
WE10LE_stun.place(x=90,y=40)
WE10LE_save.place(x=120,y=200)
WE10LE_exit.place(x=200,y=200)
WE10LE_info.place(x=10,y=70)

root.resizable(False, False)
root.mainloop()