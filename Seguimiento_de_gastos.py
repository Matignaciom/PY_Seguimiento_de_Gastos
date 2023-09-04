import tkinter as tk
from tkinter import messagebox
import json
import csv
import matplotlib.pyplot as plt

class SeguimientoGastos:
    def __init__(self):
        self.gastos = []
        self.presupuestos = {}
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open('datos.json', 'r') as archivo:
                datos = json.load(archivo)
                self.gastos = datos.get('gastos', [])
                self.presupuestos = datos.get('presupuestos', {})
        except FileNotFoundError:
            pass

    def guardar_datos(self):
        datos = {
            'gastos': self.gastos,
            'presupuestos': self.presupuestos
        }
        with open('datos.json', 'w') as archivo:
            json.dump(datos, archivo)

    def registrar_gasto(self, fecha, categoria, monto):
        self.gastos.append({
            'fecha': fecha,
            'categoria': categoria,
            'monto': monto
        })
        self.verificar_alerta_presupuesto(categoria)
        self.guardar_datos()
        messagebox.showinfo("Registro Exitoso", "Gasto registrado exitosamente!")

    def establecer_presupuesto(self, categoria, presupuesto):
        self.presupuestos[categoria] = presupuesto
        self.guardar_datos()
        messagebox.showinfo("Presupuesto Establecido", f"Presupuesto para '{categoria}' establecido en {presupuesto}.")

    def mostrar_gastos(self):
        texto_gastos = "\n".join([f"Fecha: {gasto['fecha']} | Categoría: {gasto['categoria']} | Monto: {gasto['monto']}" for gasto in self.gastos])
        messagebox.showinfo("Historial de Gastos", "Historial de Gastos:\n" + texto_gastos)

    def mostrar_presupuestos(self):
        texto_presupuestos = "\n".join([f"Categoría: {categoria} | Presupuesto: {presupuesto}" for categoria, presupuesto in self.presupuestos.items()])
        messagebox.showinfo("Presupuestos", "Presupuestos:\n" + texto_presupuestos)

    def mostrar_distribucion_categorias(self):
        gastos_por_categoria = {}
        for gasto in self.gastos:
            categoria = gasto['categoria']
            monto = gasto['monto']
            gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + monto
        
        categorias = list(gastos_por_categoria.keys())
        montos = list(gastos_por_categoria.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categorias, montos)
        plt.xlabel('Categorías')
        plt.ylabel('Monto Gastado')
        plt.title('Distribución de Gastos por Categoría')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def verificar_alerta_presupuesto(self, categoria):
        if categoria in self.presupuestos:
            presupuesto_restante = self.presupuestos[categoria]
            if presupuesto_restante <= 0:
                messagebox.showwarning("Alerta de Presupuesto", f"¡Alerta! Has excedido el presupuesto en la categoría '{categoria}'")
            elif presupuesto_restante <= 0.2 * self.presupuestos[categoria]:
                messagebox.showwarning("Alerta de Presupuesto", f"¡Alerta! Estás cerca de alcanzar el presupuesto en la categoría '{categoria}'")

    def exportar_informe_mensual(self, mes, año):
        nombre_archivo = f"informe_{año}_{mes}.csv"
        with open(nombre_archivo, mode='w', newline='') as archivo:
            nombres_columnas = ['Fecha', 'Categoría', 'Monto']
            escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
            escritor.writeheader()

            for gasto in self.gastos:
                fecha_gasto = gasto['fecha']
                mes_gasto, año_gasto = map(int, fecha_gasto.split('/')[1:])
                if mes_gasto == mes and año_gasto == año:
                    escritor.writerow({
                        'Fecha': gasto['fecha'],
                        'Categoría': gasto['categoria'],
                        'Monto': gasto['monto']
                    })
        messagebox.showinfo("Informe Exportado", f"Informe mensual de {mes}/{año} exportado exitosamente como '{nombre_archivo}'.")

def principal():
    raiz = tk.Tk()
    raiz.title("Seguimiento de Gastos")

    seguimiento = SeguimientoGastos()

    # Función para registrar gasto
    def registrar_gasto():
        ventana_registro = tk.Toplevel(raiz)
        ventana_registro.title("Registrar Gasto")

        tk.Label(ventana_registro, text="Fecha (dd/mm/aaaa):").pack()
        entrada_fecha = tk.Entry(ventana_registro)
        entrada_fecha.pack()

        tk.Label(ventana_registro, text="Categoría:").pack()
        entrada_categoria = tk.Entry(ventana_registro)
        entrada_categoria.pack()

        tk.Label(ventana_registro, text="Monto:").pack()
        entrada_monto = tk.Entry(ventana_registro)
        entrada_monto.pack()

        def enviar_gasto():
            fecha = entrada_fecha.get()
            categoria = entrada_categoria.get()
            monto = float(entrada_monto.get())

            seguimiento.registrar_gasto(fecha, categoria, monto)
            ventana_registro.destroy()

        boton_enviar = tk.Button(ventana_registro, text="Registrar", command=enviar_gasto)
        boton_enviar.pack()

    # Función para establecer presupuesto
    def establecer_presupuesto():
        ventana_presupuesto = tk.Toplevel(raiz)
        ventana_presupuesto.title("Establecer Presupuesto")

        tk.Label(ventana_presupuesto, text="Categoría:").pack()
        entrada_categoria = tk.Entry(ventana_presupuesto)
        entrada_categoria.pack()

        tk.Label(ventana_presupuesto, text="Presupuesto:").pack()
        entrada_presupuesto = tk.Entry(ventana_presupuesto)
        entrada_presupuesto.pack()

        def enviar_presupuesto():
            categoria = entrada_categoria.get()
            presupuesto = float(entrada_presupuesto.get())

            seguimiento.establecer_presupuesto(categoria, presupuesto)
            ventana_presupuesto.destroy()

        boton_enviar = tk.Button(ventana_presupuesto, text="Establecer", command=enviar_presupuesto)
        boton_enviar.pack()

    # Función para mostrar historial de gastos
    def mostrar_historial_gastos():
        seguimiento.mostrar_gastos()

    # Función para mostrar presupuestos
    def mostrar_presupuestos():
        seguimiento.mostrar_presupuestos()

    # Función para mostrar distribución de gastos por categoría
    def mostrar_distribucion_categorias():
        seguimiento.mostrar_distribucion_categorias()

    # Función para exportar informe
    def exportar_informe():
        ventana_informe = tk.Toplevel(raiz)
        ventana_informe.title("Exportar Informe")

        tk.Label(ventana_informe, text="Mes (número):").pack()
        entrada_mes = tk.Entry(ventana_informe)
        entrada_mes.pack()

        tk.Label(ventana_informe, text="Año:").pack()
        entrada_año = tk.Entry(ventana_informe)
        entrada_año.pack()

        def enviar_informe():
            mes = int(entrada_mes.get())
            año = int(entrada_año.get())

            seguimiento.exportar_informe_mensual(mes, año)
            ventana_informe.destroy()

        boton_enviar = tk.Button(ventana_informe, text="Exportar", command=enviar_informe)
        boton_enviar.pack()

    # Crear botones y elementos de la GUI
    tk.Button(raiz, text="Registrar Gasto", command=registrar_gasto).pack()
    tk.Button(raiz, text="Establecer Presupuesto", command=establecer_presupuesto).pack()
    tk.Button(raiz, text="Historial de Gastos", command=mostrar_historial_gastos).pack()
    tk.Button(raiz, text="Presupuestos", command=mostrar_presupuestos).pack()
    tk.Button(raiz, text="Distribución de Gastos por Categoría", command=mostrar_distribucion_categorias).pack()
    tk.Button(raiz, text="Exportar Informe Mensual", command=exportar_informe).pack()
    tk.Button(raiz, text="Salir", command=raiz.destroy).pack()

    raiz.mainloop()

if __name__ == "__main__":
    principal()
