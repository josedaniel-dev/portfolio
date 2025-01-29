import json
import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime
import pygame
import threading
import os
from eventos import verificar_vencimientos, recordatorio_periodico

# Inicializar Pygame para manejar sonidos
pygame.mixer.init()

# Función para cargar sonido de forma segura
def cargar_sonido(ruta):
    try:
        return pygame.mixer.Sound(ruta)
    except pygame.error as e:
        print(f"Error al cargar el sonido {ruta}: {e}")
        return None

# Cargar los sonidos
sonido_agregar = cargar_sonido('assets/sonidos/agregar.wav')
sonido_eliminar = cargar_sonido('assets/sonidos/eliminar.wav')
sonido_bienvenida = cargar_sonido('assets/sonidos/bienvenida.wav')
sonido_cambiar_fecha = cargar_sonido('assets/sonidos/cambiar_fecha.wav')
sonido_other_buttons = cargar_sonido('assets/sonidos/other_buttons.wav')  # Sonido para otros botones

# Cargar el archivo KV manualmente
Builder.load_file('ui.kv')

DATA_FILE = 'tareas.json'
CSV_FILE = 'tareas.csv'

class SplashScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class NotificacionPopup(Popup):
    def __init__(self, mensaje, **kwargs):
        super(NotificacionPopup, self).__init__(**kwargs)
        self.title = "Notificación"
        self.size_hint = (0.7, 0.4)
        self.auto_dismiss = True
        self.ids.notificacion_texto.text = mensaje

class EditarTareaPopup(Popup):
    def __init__(self, to_do_item, **kwargs):
        super(EditarTareaPopup, self).__init__(**kwargs)
        self.to_do_item = to_do_item
        self.ids.texto_input.text = to_do_item.text
        self.ids.fecha_input.text = to_do_item.fecha_texto

    def validar_cambios(self):
        nuevo_texto = self.ids.texto_input.text
        nueva_fecha = self.ids.fecha_input.text

        if nuevo_texto.strip():
            self.to_do_item.text = nuevo_texto

        if nueva_fecha:
            try:
                fecha_obj = datetime.strptime(nueva_fecha, '%d/%m/%Y')
                self.to_do_item.fecha_texto = f'Vence: {fecha_obj.strftime("%d/%m/%Y")}'
            except ValueError:
                print("Fecha inválida, por favor usa el formato dd/mm/yyyy")

        app = App.get_running_app()
        app.guardar_tareas()
        self.dismiss()

class ToDoItem(BoxLayout):
    text = StringProperty('')
    fecha_texto = StringProperty('Sin fecha de vencimiento')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:  # Detecta el doble clic
                popup = EditarTareaPopup(self)
                popup.open()
        return super(ToDoItem, self).on_touch_down(touch)

class ToDoApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(MainScreen(name='main'))

        Clock.schedule_interval(self.verificar_vencimientos, 60 * 60)
        Clock.schedule_interval(self.recordatorio_periodico, 60 * 60 * 24)
        return self.sm

    def on_start(self):
        splash_screen = self.sm.get_screen('splash')
        splash_image = splash_screen.ids.splash_image
        self.animate_fade_in(splash_image)

        if sonido_bienvenida:
            sonido_bienvenida.play()

        self.cargar_tareas(con_sonido=False)

    def animate_fade_in(self, widget):
        anim = Animation(opacity=1, duration=2)
        anim.bind(on_complete=self.animate_fade_out)
        anim.start(widget)

    def animate_fade_out(self, animation, widget):
        anim = Animation(opacity=0, duration=2)
        anim.bind(on_complete=self.switch_to_main)
        anim.start(widget)

    def switch_to_main(self, *args):
        self.sm.current = 'main'

    def añadir_tarea(self, texto, fecha_vencimiento='Sin fecha de vencimiento', con_sonido=True):
        if texto.strip() == '':
            return
        item = ToDoItem(text=texto, fecha_texto=fecha_vencimiento)
        main_screen = self.sm.get_screen('main')
        main_screen.ids.lista_tareas.add_widget(item)
        main_screen.ids.tarea_input.text = ''

        if con_sonido and sonido_agregar:
            sonido_agregar.play()

        self.guardar_tareas()

    def eliminar_tarea(self, item):
        main_screen = self.sm.get_screen('main')
        main_screen.ids.lista_tareas.remove_widget(item)
        if sonido_eliminar:
            sonido_eliminar.play()
        self.guardar_tareas()

    def guardar_tareas(self):
        main_screen = self.sm.get_screen('main')
        tareas = []
        for tarea_widget in main_screen.ids.lista_tareas.children:
            tarea = {
                'texto': tarea_widget.text,
                'fecha_vencimiento': tarea_widget.fecha_texto
            }
            tareas.append(tarea)

        with open(DATA_FILE, 'w') as f:
            json.dump(tareas, f)

    def cargar_tareas(self, con_sonido=True):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                tareas = json.load(f)
                for tarea in tareas:
                    self.añadir_tarea(tarea['texto'], tarea['fecha_vencimiento'], con_sonido=con_sonido)

    def verificar_vencimientos(self, dt):
        verificar_vencimientos(self.sm)

    def recordatorio_periodico(self, dt):
        recordatorio_periodico(self.sm)

    def exportar_csv(self):
        try:
            main_screen = self.sm.get_screen('main')
            lista_tareas = main_screen.ids.lista_tareas
            tareas = []
            for tarea_widget in lista_tareas.children:
                tarea = [tarea_widget.text, tarea_widget.fecha_texto]
                tareas.append(tarea)

            with open(CSV_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Texto', 'Fecha de Vencimiento'])
                writer.writerows(tareas)
            print(f"Tareas exportadas a {CSV_FILE}")

        except Exception as e:
            print(f"Error al exportar CSV: {e}")

    def importar_csv(self):
        try:
            if os.path.exists(CSV_FILE):
                with open(CSV_FILE, newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        texto = row['Texto']
                        fecha_vencimiento = row['Fecha de Vencimiento']
                        self.añadir_tarea(texto, fecha_vencimiento, con_sonido=False)

        except Exception as e:
            print(f"Error al importar CSV: {e}")

if __name__ == '__main__':
    ToDoApp().run()
