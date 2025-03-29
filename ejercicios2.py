import tkinter as tk
from tkinter import messagebox
import pandas as pd

def validar_login(usuario, contrasena):
    try:
        with open("usuarios.txt", "r") as file:
            for linea in file:
                usuario_guardado, contrasena_guardada = map(str.strip, linea.strip().split(","))
                if usuario == usuario_guardado and contrasena == contrasena_guardada:
                    return True
        return False
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de usuarios.")
        return False

def ejecutar_consulta(consulta):
    try:
        df = pd.read_csv("base_datos.csv")
        if consulta == "Consulta1":
            resultado = df.sample(3)  
        elif consulta == "Consulta2":
            resultado = df[df['edad'] > 17]  
        elif consulta == "Consulta3":
            resultado = df.sort_values(by='edad', ascending=True)  
        elif consulta == "Consulta4":
            resultado = df.groupby('carrera').count()[['nombre']]  
        elif consulta == "Consulta5":
            resultado = df['edad'].median()  
        elif consulta == "Consulta6":
            resultado = df[df['carrera'] == 'Programacion']  
        elif consulta == "Consulta7":
            resultado = df['edad'].max()  
        elif consulta == "Consulta8":
            resultado = df['edad'].min()  
        elif consulta == "Consulta9":
            resultado = df[df['nombre'].str.startswith('G')]  
        elif consulta == "Consulta10":
            resultado = df.groupby('carrera').mean(numeric_only=True)  
        else:
            resultado = "Consulta no disponible."
        return resultado
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de base de datos.")
        return None

def mostrar_consulta(consulta):
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    tk.Label(result_frame, text=f"{descripcion_consulta(consulta)}", font=("Arial", 12, "bold"), pady=5).pack()
    resultado = ejecutar_consulta(consulta)
    
    if isinstance(resultado, pd.DataFrame):
        text = tk.Text(result_frame, wrap="none", height=10, width=80)
        text.insert("1.0", resultado.to_string(index=False))
        text.pack()
    else:
        label = tk.Label(result_frame, text=str(resultado), relief="solid")
        label.pack()

def descripcion_consulta(consulta):
    descripciones = {
        "Consulta1": "Muestra aleatoria de 3 registros.",
        "Consulta2": "Personas con edad mayor a 17 años.",
        "Consulta3": "Lista de estudiantes ordenados por edad.",
        "Consulta4": "Cantidad de estudiantes por carrera.",
        "Consulta5": "Mediana de las edades.",
        "Consulta6": "Lista de estudiantes de Programación.",
        "Consulta7": "Edad máxima registrada en la base de datos.",
        "Consulta8": "Edad mínima registrada en la base de datos.",
        "Consulta9": "Estudiantes cuyo nombre empieza con 'G'.",
        "Consulta10": "Promedio de edad por carrera."
    }
    return descripciones.get(consulta, "Consulta desconocida")

def login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if usuario == "" or contrasena == "":
        messagebox.showerror("Error", "Por favor, ingresa usuario y contraseña.")
        return

    if validar_login(usuario, contrasena):
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        mostrar_menu_consultas()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def mostrar_menu_consultas():
    frame_login.pack_forget()
    global result_frame
    result_frame = tk.Frame(ventana)
    result_frame.pack(padx=10, pady=10)
    
    frame_consultas = tk.Frame(ventana)
    frame_consultas.pack(padx=10, pady=10)

    tk.Label(frame_consultas, text="Seleccionar consulta:").grid(row=0, column=0)
    consultas = [f"Consulta{i}" for i in range(1, 11)]
    
    for idx, consulta in enumerate(consultas):
        boton = tk.Button(frame_consultas, text=consulta, command=lambda c=consulta: mostrar_consulta(c), bg="blue", fg="black")
        boton.grid(row=idx+1, column=0)

ventana = tk.Tk()
ventana.title("Sistema de Consultas")
ventana.geometry("800x600")

frame_login = tk.Frame(ventana)
frame_login.pack(padx=10, pady=10)

tk.Label(frame_login, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(frame_login)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_login, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
entry_contrasena = tk.Entry(frame_login, show="*")
entry_contrasena.grid(row=1, column=1, padx=5, pady=5)

boton_login = tk.Button(frame_login, text="Iniciar sesión", command=login, bg="blue", fg="black")
boton_login.grid(row=2, columnspan=2, pady=10)

ventana.mainloop()
