from ventanas import ToDoItem
import json
import os
import csv

DATA_FILE = 'tareas.json'
CSV_FILE = 'tareas.csv'

def añadir_tarea(screen_manager, texto, fecha_vencimiento='Sin fecha de vencimiento', con_sonido=True):
    if texto.strip() == '':
        return
    item = ToDoItem(text=texto, fecha_texto=fecha_vencimiento)
    main_screen = screen_manager.get_screen('main')
    lista_tareas = main_screen.ids.get('lista_tareas')  # Acceder a lista_tareas correctamente
    if lista_tareas:
        lista_tareas.add_widget(item)
    main_screen.ids.tarea_input.text = ''  # Limpiar el campo de texto una vez añadida la tarea
    guardar_tareas(screen_manager)

def eliminar_tarea(screen_manager, item):
    main_screen = screen_manager.get_screen('main')
    lista_tareas = main_screen.ids.get('lista_tareas')
    if lista_tareas:
        lista_tareas.remove_widget(item)
    guardar_tareas(screen_manager)

def guardar_tareas(screen_manager):
    main_screen = screen_manager.get_screen('main')
    lista_tareas = main_screen.ids.get('lista_tareas')
    if lista_tareas:
        tareas = []
        for tarea_widget in lista_tareas.children:
            tarea = {
                'texto': tarea_widget.text,
                'fecha_vencimiento': tarea_widget.fecha_texto
            }
            tareas.append(tarea)

        with open(DATA_FILE, 'w') as f:
            json.dump(tareas, f)

def cargar_tareas(screen_manager, con_sonido=True):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            tareas = json.load(f)
            for tarea in tareas:
                añadir_tarea(screen_manager, tarea['texto'], tarea['fecha_vencimiento'], con_sonido=con_sonido)

def exportar_csv(screen_manager):
    main_screen = screen_manager.get_screen('main')
    lista_tareas = main_screen.ids.get('lista_tareas')
    if lista_tareas:
        tareas = []
        for tarea_widget in lista_tareas.children:
            tarea = [tarea_widget.text, tarea_widget.fecha_vencimiento]
            tareas.append(tarea)

        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Texto', 'Fecha de Vencimiento'])
            writer.writerows(tareas)

def importar_csv(screen_manager):
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                texto = row['Texto']
                fecha_vencimiento = row['Fecha de Vencimiento']
                añadir_tarea(screen_manager, texto, fecha_vencimiento, con_sonido=False)
