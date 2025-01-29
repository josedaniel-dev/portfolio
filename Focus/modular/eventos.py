from datetime import datetime
from ventanas import NotificacionPopup

def verificar_vencimientos(screen_manager):
    main_screen = screen_manager.get_screen('main')
    ahora = datetime.now()
    tareas_vencidas = []

    for tarea_widget in main_screen.ids.lista_tareas.children:
        if tarea_widget.fecha_texto != 'Sin fecha de vencimiento':
            fecha_vencimiento = datetime.strptime(tarea_widget.fecha_texto.replace('Vence: ', ''), '%d/%m/%Y')

            if (fecha_vencimiento - ahora).days < 0:
                tareas_vencidas.append(tarea_widget.text)

    if tareas_vencidas:
        mensaje_vencidas = "Las siguientes tareas ya han vencido:\n" + "\n".join(tareas_vencidas)
        popup_vencidas = NotificacionPopup(mensaje=mensaje_vencidas)
        popup_vencidas.open()

def recordatorio_periodico(screen_manager):
    mensaje = "Recordatorio: ¡Revisa tus tareas diarias!"
    popup = NotificacionPopup(mensaje=mensaje)
    popup.open()
