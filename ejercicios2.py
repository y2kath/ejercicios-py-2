import tkinter as tk
from tkinter import messagebox
import pandas as pd

def validaciooon(usuario, contrasena):
    try:
        with open("usuarios.txt", "r") as file:
            for linea in file:
                usuario_guardado, contrasena_guardada = map(str.strip, linea.strip().split(","))
                if usuario == usuario_guardado and contrasena == contrasena_guardada:
                    return True
        return False
    except FileNotFoundError:
        messagebox.showerror("Error", "No hay archivo")
        return False

def consultaaas(consulta):
    try:
        df = pd.read_csv("base_datos.csv")
        if consulta == "Muestra aleatoria de 3 alumnos":
            resultado = df.sample(3)
        elif consulta == "Alumnos mayores de 17 años":
            resultado = df[df['edad'] > 17]
        elif consulta == "Alumnos ordenados por edad ascendente":
            resultado = df.sort_values(by='edad', ascending=True)
        elif consulta == "Cantidad de alumnos por carrera":
            resultado = df.groupby('carrera').agg({'nombre': 'count'}).reset_index()
        elif consulta == "Mediana de las edades de los alumnos":
            resultado = df['edad'].median()
        elif consulta == "Alumnos cuyos nombres terminan en 'a'":
            resultado = df[df['nombre'].str.endswith('a')]
        elif consulta == "Edad máxima encontrada":
            resultado = df['edad'].max()
        elif consulta == "Edad mínima encontrada":
            resultado = df['edad'].min()
        elif consulta == "Alumnos cuyo nombre empieza con 'G'":
            resultado = df[df['nombre'].str.startswith('G')]
        elif consulta == "Alumnos de la carrera de Programacion":
            resultado = df[df['carrera'] == 'Programacion']
        else:
            resultado = "Consulta no disponible."
        return resultado
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de base de datos.")
        return None

def verlaconsulta(consulta):
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    tk.Label(result_frame, text=f"{consulta}", font=("Arial", 14, "bold"), pady=10, fg="white", bg="#a0b7db").pack(fill="x")
    resultado = consultaaas(consulta)
    
    if isinstance(resultado, pd.DataFrame):
        text = tk.Text(result_frame, wrap="none", height=10, width=80, bg="#ECF0F1", fg="#4e6385", font=("Arial", 12))
        text.insert("1.0", resultado.to_string(index=False))
        text.pack(padx=10, pady=10)
    else:
        label = tk.Label(result_frame, text=str(resultado), relief="solid", bg="#ECF0F1", fg="#4e6385", font=("Arial", 12))
        label.pack(padx=10, pady=10)

def iniciodesesioon():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if usuario == "" or contrasena == "":
        messagebox.showerror("Error", "Ingresa usuario y contraseña")
        return

    if validaciooon(usuario, contrasena):
        messagebox.showinfo("Éxito", "Inicio de sesión correcto")
        vermenuu()
    else:
        messagebox.showerror("Error", "Usuario o contraseña inválidos")

def vermenuu():
    frame_iniciodesesioon.pack_forget()
    global result_frame
    result_frame = tk.Frame(ventana, bg="#a0b7db")
    result_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    frame_consultas = tk.Frame(ventana, bg="#a0b7db")
    frame_consultas.pack(padx=10, pady=10, fill="x")

    tk.Label(frame_consultas, text="Seleccionar consulta:", fg="white", bg="#a0b7db", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    consultas = [
        "Muestra aleatoria de 3 alumnos",
        "Alumnos mayores de 17 años",
        "Alumnos ordenados por edad ascendente",
        "Cantidad de alumnos por carrera",
        "Mediana de las edades de los alumnos",
        "Alumnos cuyos nombres terminan en 'a'",
        "Edad máxima encontrada",
        "Edad mínima encontrada",
        "Alumnos cuyo nombre empieza con 'G'",
        "Alumnos de la carrera de Programacion"
    ]
    
    for idx, consulta in enumerate(consultas):
        boton = tk.Button(frame_consultas, text=consulta, command=lambda c=consulta: verlaconsulta(c), bg="#374a69", fg="white", font=("Arial", 12, "bold"), relief="raised")
        boton.grid(row=(idx // 2) + 1, column=idx % 2, pady=3, padx=10, sticky="ew")

ventana = tk.Tk()
ventana.title("CONSULTAS PANDAS FUNDAMENTOS DE IA")
ventana.geometry("800x600")
ventana.configure(bg="#a0b7db")

frame_iniciodesesioon = tk.Frame(ventana, bg="#a0b7db")
frame_iniciodesesioon.pack(padx=10, pady=10)

tk.Label(frame_iniciodesesioon, text="Usuario:", fg="white", bg="#a0b7db", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(frame_iniciodesesioon, font=("Arial", 12))
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_iniciodesesioon, text="Contraseña:", fg="white", bg="#a0b7db", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_contrasena = tk.Entry(frame_iniciodesesioon, show="*", font=("Arial", 12))
entry_contrasena.grid(row=1, column=1, padx=5, pady=5)

boton_iniciodesesioon = tk.Button(frame_iniciodesesioon, text="Iniciar sesion", command=iniciodesesioon, bg="#374a69", fg="white", font=("Arial", 12, "bold"), relief="raised")
boton_iniciodesesioon.grid(row=2, columnspan=2, pady=10, sticky="ew")

ventana.mainloop()
