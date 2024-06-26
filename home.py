from functions import *
import tkinter as tk
from tkinter import ttk
import bdagent

#VARIABLE GLOBAL POSICION Y DINAMICA
y_index = 0

def populateData():    
    cpu_data = getCpuWmicInfo()    
    mainboard_data = getMainBoardWmicInfo()
    memory_data = getMemoryWmicInfo()
    #Añadiendo las variables de CPU
    cpu_mader = filterManufacturers(cpu_data["Manufacturer"])
    cpu_name = cpu_data["Name"]    
    cpu_info = {}
    if(verifyTableExists("cpu" + cpu_mader.strip().lower() + "specs")):
        if(verifyCpuDataInDb(depurateCpuName(cpu_name), cpu_mader) == False):            
            cpu_info = getCpuIntelData(depurateCpuName(cpu_name))
            createTableCpuSpecsByMader(cpu_mader, cpu_info)
            insertCpuSpecsData(cpu_mader, cpu_info, depurateCpuName(cpu_name)) 
            cpu_bus = "  " + cpu_info["Velocidad del bus"]
            cpu_maxmemory = "  " + cpu_info["Tamao de memoria mximo (depende del tipo de memoria)"]
            cpu_memtype = "  " + cpu_info['Tipos de memoria']
            cpu_graphics = "  " + cpu_info['Nombre de GPU']            
        else:
            cpu_info = getCpuDbData(depurateCpuName(cpu_name), cpu_mader)
            cpu_bus = "  " + cpu_info["Velocidad_del_bus"]
            cpu_maxmemory = "  " + cpu_info["Tamao_de_memoria_mximo__depende_del_tipo_de_memoria_"]
            cpu_memtype = "  " + cpu_info['Tipos_de_memoria']
            cpu_graphics = "  " + cpu_info['Nombre_de_GPU'] 
    else:
        cpu_info = getCpuIntelData(depurateCpuName(cpu_name))
        createTableCpuSpecsByMader(cpu_mader, cpu_info)
        insertCpuSpecsData(cpu_mader, cpu_info, depurateCpuName(cpu_name))
        cpu_bus = "  " + cpu_info["Velocidad del bus"]
        cpu_maxmemory = "  " + cpu_info["Tamao de memoria mximo (depende del tipo de memoria)"]
        cpu_memtype = "  " + cpu_info['Tipos de memoria']
        cpu_graphics = "  " + cpu_info['Nombre de GPU']
    
    cpu_caption = cpu_data["Caption"]
    cpu_clock = "  " + cpu_data["MaxClockSpeed"] + " Mhz"
    cpu_cores = cpu_data["NumberOfCores"]
    cpu_threads = cpu_data["NumberOfLogicalProcessors"]
    cpu_width = "  " + cpu_data["DataWidth"] + " Bits"
    cpu_cache = "  " + cpu_info["Cach"]    
    cpu_cache_2 = " " + cpu_data["L2CacheSize"] + " Kb"
    cpu_cache_3 = " " + cpu_data["L3CacheSize"] + " Kb"
    cpu_image_label["text"] = "   " + cpu_name  
    cpu_mader_input.insert(tk.END, cpu_mader)
    cpu_mader_input.config(justify="center")
    cpu_mader_input.config(state="readonly")  
    cpu_type_input.insert(tk.END, cpu_caption)
    cpu_type_input.config(justify="center")
    cpu_type_input.config(state="readonly")
    cpu_clock_input.insert(tk.END, cpu_clock)    
    cpu_clock_input.config(state="readonly")
    cpu_cores_input.insert(tk.END, cpu_cores)
    cpu_cores_input.config(justify="center")
    cpu_cores_input.config(state="readonly")
    cpu_threads_input.insert(tk.END, cpu_threads)
    cpu_threads_input.config(justify="center")
    cpu_threads_input.config(state="readonly")
    cpu_width_input.insert(tk.END, cpu_width)
    cpu_width_input.config(justify="center")
    cpu_width_input.config(state="readonly") 
    cpu_cache_input.insert(tk.END, cpu_cache)
    cpu_cache_input.config(justify="center")
    cpu_cache_input.config(state="readonly")
    cpu_busspeed_input.insert(tk.END, cpu_bus)
    cpu_busspeed_input.config(justify="center")
    cpu_busspeed_input.config(state="readonly")    
    cpu_maxmem_input.insert(tk.END, cpu_maxmemory)
    cpu_maxmem_input.config(justify="center")
    cpu_maxmem_input.config(state="readonly")  
    cpu_memtype_input.insert(tk.END, cpu_memtype)
    cpu_memtype_input.config(justify="center")
    cpu_memtype_input.config(state="readonly")    
    cpu_graphics_input.insert(tk.END, cpu_graphics)
    cpu_graphics_input.config(justify="center")
    cpu_graphics_input.config(state="readonly")       
    cpu_cache_2_input.insert(tk.END, cpu_cache_2)
    cpu_cache_2_input.config(justify="center")
    cpu_cache_2_input.config(state="readonly")    
    cpu_cache_3_input.insert(tk.END, cpu_cache_3)
    cpu_cache_3_input.config(justify="center")
    cpu_cache_3_input.config(state="readonly") 
    #COMPLETANDO LOS DATOS DE LA PLACA BASE  
    mainboard_manufacturer = depurateMainBoardManufacturer(mainboard_data["Manufacturer"])
    mainboard_product = mainboard_data["Product"]
    if(verifyTableExists("Mainboard" + mainboard_manufacturer + "Specs")):
        if(verifyMainboardDataInDb(mainboard_product.strip(), mainboard_manufacturer) == True):
            mainboard_info = getMainboardDataDb(mainboard_manufacturer, mainboard_product.strip()) 
        else:
            mainboard_info = getMainBoardInfo(mainboard_product)  
            insertMainboardSpecsData(mainboard_manufacturer,mainboard_info, mainboard_product)         
    else:
        mainboard_info = getMainBoardInfo(mainboard_product.strip())
        createMainboardSpecsTable(mainboard_manufacturer, mainboard_info)
        insertMainboardSpecsData(mainboard_manufacturer, mainboard_info, mainboard_product)

    mainboard_image_label["text"] = "  " + mainboard_data["Manufacturer"]
    mainboard_mader_input.insert(tk.END, mainboard_data["Manufacturer"])
    mainboard_mader_input.config(justify="center")
    mainboard_mader_input.config(state="readonly")
    mainboard_model_input.insert(tk.END, mainboard_product)
    mainboard_model_input.config(justify="center")
    mainboard_model_input.config(state="readonly")
    slot_lines = len(mainboard_info["Expansion_Slots__includes_used_"].split("\n"))
    mainboard_slots_input = {}
    y_index = 160
    for i in range(0, slot_lines):        
        mainboard_slots_input[i] = tk.Entry(mainboard_frame)
        mainboard_slots_input[i].config(font=("Verdana", "9"))
        mainboard_slots_input[i].place(x=80, y=y_index, width=300)        
        mainboard_slots_input[i].insert(tk.END, mainboard_info["Expansion_Slots__includes_used_"].split("\n")[i])    
        mainboard_slots_input[i].config(state="readonly")
        y_index = y_index + 30
    ports_lines = len(mainboard_info["I_O_Ports"].split("\n"))
    mainboard_ports_input = {}
    mainboard_ports_label.place(x=10, y=y_index)
    for i in range(0, ports_lines):
        mainboard_ports_input[i] = tk.Entry(mainboard_frame)
        mainboard_ports_input[i].config(font=("Verdana", "9"))
        mainboard_ports_input[i].place(x=80, y=y_index, width=300) 
        mainboard_ports_input[i].insert(tk.END, mainboard_info["I_O_Ports"].split("\n")[i])    
        mainboard_ports_input[i].config(state="readonly")
        y_index = y_index + 30


#INICIO DE LA GUI DE LA APP TPINFO


root = tk.Tk()
root.config(width=1200, height=500)
root.title("Technic Help")
#inicializamos la ventana principal

notebook = ttk.Notebook(root)
notebook.place(x=0, y=0, width=1200, height=500)
#Añadimos el contenedor de pestañas

info_frame = tk.Frame(notebook)
notebook.add(info_frame, text="Info del Sistema")
#Creamos la primera pestaña

cpu_frame = tk.Frame(info_frame)
cpu_frame.config(width=395,height=500)
cpu_frame["relief"] = "solid"
cpu_frame["borderwidth"] = "1"
cpu_frame.pack(side="left")
#Creamos el primer bloque con la info de la CPU
cpu_title = tk.Label(cpu_frame, text="Información de la CPU")
cpu_title.config(anchor="center",font=("Verdana", 16))
cpu_title.place(x=0,y=0, width=390)
cpu_image = tk.PhotoImage(file="images/i3.png")
cpu_image_sub = cpu_image.subsample(3)
cpu_image_label = tk.Label(cpu_frame, image=cpu_image_sub, text="")
cpu_image_label.config(compound="left", font=("Verdana", "9"))
cpu_image_label.place(x=10,y=30)
cpu_mader_label = tk.Label(cpu_frame, text="Fabricante: ")
cpu_mader_label.place(x=10, y=100)
cpu_mader_input = tk.Entry(cpu_frame)
cpu_mader_input.config(font=("Verdana", "9"))
cpu_mader_input.place(x=80, y=100, width=300)
cpu_type_label = tk.Label(cpu_frame, text="Modelo: ")
cpu_type_label.place(x=10, y=130)
cpu_type_input = tk.Entry(cpu_frame)
cpu_type_input.config(font=("Verdana", "9"))
cpu_type_input.place(x=80, y=130, width=300)
cpu_clock_label = tk.Label(cpu_frame, text="Vel. Reloj: ")
cpu_clock_label.place(x=10, y=160)
cpu_clock_input = tk.Entry(cpu_frame)
cpu_clock_input.config(font=("Verdana", "9"),justify="center")
cpu_clock_input.place(x=80, y=160, width=80)
cpu_width_label = tk.Label(cpu_frame, text="Tamaño Datos: ")
cpu_width_label.place(x=180, y=160)
cpu_width_input = tk.Entry(cpu_frame)
cpu_width_input.config(font=("Verdana", "9"))
cpu_width_input.place(x=280, y=160, width=80)
cpu_cores_label = tk.Label(cpu_frame, text="Núcleos: ")
cpu_cores_label.place(x=10, y=190)
cpu_cores_input = tk.Entry(cpu_frame)
cpu_cores_input.config(font=("Verdana", "9"))
cpu_cores_input.place(x=80, y=190, width=80)
cpu_threads_label = tk.Label(cpu_frame, text="Hilos de Proceso: ")
cpu_threads_label.place(x=180, y=190)
cpu_threads_input = tk.Entry(cpu_frame)
cpu_threads_input.config(font=("Verdana", "9"))
cpu_threads_input.place(x=280, y=190, width=80)
cpu_cache_label = tk.Label(cpu_frame, text="Caché: ")
cpu_cache_label.place(x=10, y=220)
cpu_cache_input = tk.Entry(cpu_frame)
cpu_cache_input.config(font=("Verdana", "9"))
cpu_cache_input.place(x=80, y=220, width=300)
cpu_cache_2_label = tk.Label(cpu_frame, text="Cache L2: ")
cpu_cache_2_label.place(x=10, y=250)
cpu_cache_2_input = tk.Entry(cpu_frame)
cpu_cache_2_input.config(font=("Verdana", "9"))
cpu_cache_2_input.place(x=80, y=250, width=80)
cpu_cache_3_label = tk.Label(cpu_frame, text="Cache L3: ")
cpu_cache_3_label.place(x=180, y=250)
cpu_cache_3_input = tk.Entry(cpu_frame)
cpu_cache_3_input.config(font=("Verdana", "9"))
cpu_cache_3_input.place(x=280, y=250, width=80)
cpu_busspeed_label = tk.Label(cpu_frame, text="Vel. Bus: ")
cpu_busspeed_label.place(x=10, y=280)
cpu_busspeed_input = tk.Entry(cpu_frame)
cpu_busspeed_input.config(font=("Verdana", "9"))
cpu_busspeed_input.place(x=80, y=280, width=80)
cpu_maxmem_label = tk.Label(cpu_frame, text="Max. Mem: ")
cpu_maxmem_label.place(x=180, y=280)
cpu_maxmem_input = tk.Entry(cpu_frame)
cpu_maxmem_input.config(font=("Verdana", "9"))
cpu_maxmem_input.place(x=280, y=280, width=80)
cpu_memtype_label = tk.Label(cpu_frame, text="Tipos Mem: ")
cpu_memtype_label.place(x=10, y=310)
cpu_memtype_input = tk.Entry(cpu_frame)
cpu_memtype_input.config(font=("Verdana", "9"))
cpu_memtype_input.place(x=80, y=310, width=300)
cpu_graphics_label = tk.Label(cpu_frame, text="Graficos: ")
cpu_graphics_label.place(x=10, y=340)
cpu_graphics_input = tk.Entry(cpu_frame)
cpu_graphics_input.config(font=("Verdana", "9"))
cpu_graphics_input.place(x=80, y=340, width=300)
#Añadimos los elementos de la CPU


mainboard_frame = tk.Frame(info_frame)
mainboard_frame.config(width=395,height=500)
mainboard_frame["relief"] = "solid"
mainboard_frame["borderwidth"] = "1"
mainboard_frame.pack(side="left", padx=5)
mainboard_title = tk.Label(mainboard_frame, text="Información de la Placa Base")
mainboard_title.config(anchor="center",font=("Verdana", 16))
mainboard_title.place(x=0,y=0, width=390)
mainboard_image = tk.PhotoImage(file="images/asustek.png")
mainboard_image_sub = mainboard_image.subsample(3)
mainboard_image_label = tk.Label(mainboard_frame, image=mainboard_image_sub, text="")
mainboard_image_label.config(compound="left", font=("Verdana", "9"))
mainboard_image_label.place(x=10,y=40)
mainboard_mader_label = tk.Label(mainboard_frame, text="Fabricante: ")
mainboard_mader_label.place(x=10, y=100)
mainboard_mader_input = tk.Entry(mainboard_frame)
mainboard_mader_input.config(font=("Verdana", "9"))
mainboard_mader_input.place(x=80, y=100, width=300)
mainboard_model_label = tk.Label(mainboard_frame, text="Modelo: ")
mainboard_model_label.place(x=10, y=130)
mainboard_model_input = tk.Entry(mainboard_frame)
mainboard_model_input.config(font=("Verdana", "9"))
mainboard_model_input.place(x=80, y=130, width=300)
mainboard_slots_label = tk.Label(mainboard_frame, text="Expansión: ")
mainboard_slots_label.place(x=10, y=160)
mainboard_ports_label = ttk.Label(mainboard_frame, text="Puertos: ")



#Creamos el segundo bloque con la info de la Placa Base

memory_frame = tk.Frame(info_frame)
memory_frame.config(width=395,height=500)
memory_frame["relief"] = "solid"
memory_frame["borderwidth"] = "1"
memory_frame.pack(side="left")
memory_title = tk.Label(memory_frame, text="Información de la Memoria")
memory_title.config(anchor="center",font=("Verdana", 16))
memory_title.place(x=0,y=0, width=390)
#Creamos el tercer bloque con la info de la Memoria Ram





populateData()
root.mainloop()



