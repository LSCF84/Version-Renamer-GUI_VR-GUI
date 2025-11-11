import os
import glob
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

class VersionRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Renombrador de Versiones")
        self.root.geometry("900x700")
        
        # Variables
        self.directorio = tk.StringVar(value=os.getcwd())
        self.nombre_base = tk.StringVar(value="comprobador")
        self.archivos_lista = []
        self.nombres_asignados = set()
        self.archivos_seleccionados = set()  # Para trackear archivos seleccionados
        
        self.setup_ui()
        self.cargar_archivos()
        
    def setup_ui(self):
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Renombrado
        tab_rename = ttk.Frame(notebook, padding="10")
        notebook.add(tab_rename, text="Renombrado")
        
        # Pestaña 2: Acerca de
        tab_about = ttk.Frame(notebook, padding="10")
        notebook.add(tab_about, text="Acerca de")
        
        self.setup_rename_tab(tab_rename)
        self.setup_about_tab(tab_about)
        
    def setup_rename_tab(self, parent):
        # Configurar grid weights
        parent.columnconfigure(1, weight=1)
        
        # Directorio selección
        ttk.Label(parent, text="Directorio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.directorio, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(parent, text="Examinar", command=self.seleccionar_directorio).grid(row=0, column=2, padx=5, pady=5)
        
        # Nombre base
        ttk.Label(parent, text="Nombre base:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.nombre_base, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Botón actualizar
        ttk.Button(parent, text="Actualizar Lista", command=self.cargar_archivos).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Lista de archivos con checkbox
        ttk.Label(parent, text="Archivos encontrados (ordenados por fecha de modificación):").grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Frame para treeview con checkboxes
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Treeview para mostrar archivos con checkbox
        columns = ('seleccionado', 'nombre', 'fecha', 'nuevo_nombre')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree.heading('seleccionado', text='✓')
        self.tree.heading('nombre', text='Archivo Original')
        self.tree.heading('fecha', text='Fecha Modificación')
        self.tree.heading('nuevo_nombre', text='Nuevo Nombre')
        
        self.tree.column('seleccionado', width=30, anchor='center')
        self.tree.column('nombre', width=250)
        self.tree.column('fecha', width=150)
        self.tree.column('nuevo_nombre', width=250)
        
        # Scrollbar para treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind events para selección
        self.tree.bind('<Button-1>', self.on_tree_click)
        
        # Botones de selección
        select_frame = ttk.Frame(parent)
        select_frame.grid(row=5, column=0, columnspan=3, pady=5)
        
        ttk.Button(select_frame, text="Seleccionar Todos", command=self.seleccionar_todos).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_frame, text="Deseleccionar Todos", command=self.deseleccionar_todos).pack(side=tk.LEFT, padx=5)
        
        # Botones de acción
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Previsualizar Cambios", command=self.previsualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ejecutar Renombrado", command=self.ejecutar_renombrado).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_previsualizacion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Configurar expansión
        parent.rowconfigure(4, weight=1)
        parent.columnconfigure(1, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
    def setup_about_tab(self, parent):
        # Frame principal para Acerca de
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Renombrador de Versiones", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Descripción
        desc_text = """
Esta herramienta permite renombrar archivos Python con un sistema de 
versionado automático basado en la fecha de modificación.

Características principales:
• Renombrado automático por orden de antigüedad
• Selección individual de archivos
• Exclusión automática del archivo en ejecución
• Detección de nombres duplicados
• Interfaz gráfica intuitiva
• Previsualización de cambios
"""
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT)
        desc_label.pack(pady=10, padx=20)
        
        # Modificaciones y mejoras
        mods_frame = ttk.LabelFrame(main_frame, text="Últimas Modificaciones", padding="10")
        mods_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        mods_text = """
Versión 1.3 - 2025
• Añadida selección individual de archivos
• Exclusión automática del archivo en ejecución
• Checkboxes para selección múltiple

Versión 1.2 - 2025
• Implementada pestaña "Acerca de"
• Mejorado el manejo de errores
• Optimizado el algoritmo de renombrado

Versión 1.1 - 2025
• Añadida previsualización de cambios
• Detección automática de conflictos de nombres
• Interfaz más intuitiva

Versión 1.0 - 2025
• Versión inicial del renombrador
• Sistema básico de versionado
• Interfaz gráfica funcional
"""
        mods_label = ttk.Label(mods_frame, text=mods_text, justify=tk.LEFT)
        mods_label.pack()
        
        # Información del desarrollador
        dev_frame = ttk.Frame(main_frame)
        dev_frame.pack(pady=10)
        
        dev_text = "Desarrollado por - 2025"
        dev_label = ttk.Label(dev_frame, text=dev_text, font=("Arial", 10))
        dev_label.pack()
    
    def on_tree_click(self, event):
        """Maneja el clic en el treeview para seleccionar/deseleccionar"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            if column == "#1":  # Columna de checkbox
                current_value = self.tree.set(item, 'seleccionado')
                nuevo_valor = '✓' if current_value != '✓' else ''
                self.tree.set(item, 'seleccionado', nuevo_valor)
                
                # Actualizar conjunto de seleccionados
                archivo = self.tree.set(item, 'nombre')
                if nuevo_valor == '✓':
                    self.archivos_seleccionados.add(archivo)
                else:
                    self.archivos_seleccionados.discard(archivo)
    
    def seleccionar_todos(self):
        """Selecciona todos los archivos"""
        for item in self.tree.get_children():
            self.tree.set(item, 'seleccionado', '✓')
            archivo = self.tree.set(item, 'nombre')
            self.archivos_seleccionados.add(archivo)
    
    def deseleccionar_todos(self):
        """Deselecciona todos los archivos"""
        for item in self.tree.get_children():
            self.tree.set(item, 'seleccionado', '')
        self.archivos_seleccionados.clear()
    
    def obtener_archivo_actual(self):
        """Obtiene el nombre del archivo actual en ejecución"""
        try:
            # Diferentes métodos para obtener el nombre del archivo actual
            return os.path.basename(__file__)
        except:
            return None
        
    def seleccionar_directorio(self):
        directorio = filedialog.askdirectory(initialdir=self.directorio.get())
        if directorio:
            self.directorio.set(directorio)
            self.cargar_archivos()
            
    def limpiar_previsualizacion(self):
        self.nombres_asignados.clear()
        self.archivos_seleccionados.clear()
        self.cargar_archivos()
            
    def cargar_archivos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.nombres_asignados.clear()
        self.archivos_seleccionados.clear()
            
        try:
            os.chdir(self.directorio.get())
            archivos_py = glob.glob("*.py")
            
            # Excluir archivo actual en ejecución
            archivo_actual = self.obtener_archivo_actual()
            if archivo_actual and archivo_actual in archivos_py:
                archivos_py.remove(archivo_actual)
                print(f"Excluido archivo en ejecución: {archivo_actual}")
                
            if not archivos_py:
                messagebox.showinfo("Info", "No se encontraron archivos .py en la carpeta (excluyendo el archivo en ejecución).")
                return
                
            self.archivos_lista = []
            for archivo in archivos_py:
                tiempo_modificacion = os.path.getmtime(archivo)
                fecha_modificacion = datetime.fromtimestamp(tiempo_modificacion)
                self.archivos_lista.append({
                    'nombre_original': archivo,
                    'fecha_modificacion': fecha_modificacion,
                    'timestamp': tiempo_modificacion
                })
                
            self.archivos_lista.sort(key=lambda x: x['timestamp'])
            
            for archivo in self.archivos_lista:
                self.tree.insert('', tk.END, values=(
                    '✓',  # Seleccionado por defecto
                    archivo['nombre_original'],
                    archivo['fecha_modificacion'].strftime("%Y-%m-%d %H:%M:%S"),
                    ""
                ))
                self.archivos_seleccionados.add(archivo['nombre_original'])
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo acceder al directorio: {e}")
            
    def encontrar_proxima_version_disponible(self, nombre_base):
        i = 0
        while True:
            nombre_propuesto = f"{nombre_base}_v.1.{i}.py"
            if not os.path.exists(nombre_propuesto) and nombre_propuesto not in self.nombres_asignados:
                self.nombres_asignados.add(nombre_propuesto)
                return nombre_propuesto
            i += 1
            
    def previsualizar(self):
        for item in self.tree.get_children():
            self.tree.set(item, 'nuevo_nombre', '')
            
        nombre_base = self.nombre_base.get().strip()
        if not nombre_base:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre base.")
            return
            
        self.nombres_asignados.clear()
        
        # Solo procesar archivos seleccionados
        archivos_a_procesar = []
        for item in self.tree.get_children():
            archivo = self.tree.set(item, 'nombre')
            if archivo in self.archivos_seleccionados:
                archivos_a_procesar.append((item, archivo))
            
        for item, archivo in archivos_a_procesar:
            nuevo_nombre = self.encontrar_proxima_version_disponible(nombre_base)
            self.tree.set(item, 'nuevo_nombre', nuevo_nombre)
            
    def ejecutar_renombrado(self):
        if not self.archivos_seleccionados:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados para renombrar.")
            return
            
        nombre_base = self.nombre_base.get().strip()
        if not nombre_base:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre base.")
            return
            
        try:
            os.chdir(self.directorio.get())
            
            renombrados_exitosos = 0
            errores = []
            
            self.nombres_asignados.clear()
            
            # Solo procesar archivos seleccionados
            for item in self.tree.get_children():
                archivo_original = self.tree.set(item, 'nombre')
                if archivo_original in self.archivos_seleccionados:
                    try:
                        nuevo_nombre = self.encontrar_proxima_version_disponible(nombre_base)
                        
                        # Renombrar el archivo
                        os.rename(archivo_original, nuevo_nombre)
                        renombrados_exitosos += 1
                        
                        print(f"Renombrado: {archivo_original} -> {nuevo_nombre}")
                        
                    except Exception as e:
                        errores.append(f"{archivo_original}: {e}")
            
            if errores:
                mensaje = f"Se renombraron {renombrados_exitosos} archivos.\n\nErrores:\n" + "\n".join(errores)
                messagebox.showwarning("Renombrado parcial", mensaje)
            else:
                messagebox.showinfo("Éxito", f"Se renombraron {renombrados_exitosos} archivos correctamente.")
            
            self.cargar_archivos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el renombrado: {e}")

def main():
    root = tk.Tk()
    app = VersionRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()