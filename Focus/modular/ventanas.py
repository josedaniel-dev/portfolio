from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App
from datetime import datetime

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
                print("Fecha inválida")
        App.get_running_app().guardar_tareas()
        self.dismiss()

class ToDoItem(BoxLayout):
    text = StringProperty('')
    fecha_texto = StringProperty('Sin fecha de vencimiento')
