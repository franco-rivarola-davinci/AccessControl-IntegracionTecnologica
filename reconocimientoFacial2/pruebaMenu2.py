import cv2
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from opencv.fr.search.schemas import VerificationRequest
from openCvConfig import *
import cv2
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from pathlib import Path
from opencv.fr.persons.schemas import PersonBase

class MenuPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        # Agregar botones
        solicitar_acceso_button = Button(text="Solicitar acceso")
        solicitar_acceso_button.bind(on_press=self.solicitar_acceso)

        ingresar_usuarios_button = Button(text="Crear usuario")
        ingresar_usuarios_button.bind(on_press=self.crear_usuario)

        # Agregar botones al layout
        self.add_widget(solicitar_acceso_button)
        self.add_widget(ingresar_usuarios_button)

    def solicitar_acceso(self, instance):
        # Cambiar al layout de solicitar acceso
        self.clear_widgets()
        self.add_widget(SolicitarAccesoLayout())
    
    def crear_usuario(self, instance):
        # Aquí se puede incluir la lógica para pedir la contraseña
        self.clear_widgets()
        self.add_widget(CrearUsuario())


class SolicitarAccesoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Agregar botón para volver al menú principal
        volver_button = Button(text="Volver al menú")
        volver_button.size_hint = (1, 0.1)
        volver_button.pos_hint = {'x':0, 'y':0}
        volver_button.bind(on_press=self.volver_menu_principal)
        layout.add_widget(volver_button)

        # Cree un widget de imagen para mostrar la vista previa de la cámara
        self.image = Image()
        layout.add_widget(self.image)

        # Crear un label para mostrar el estado del acceso
        self.status_label = Label(text='Estado de acceso', size_hint=(1, 0.1), height=30, size_hint_min_y=30, size_hint_max_y=30)   
        layout.add_widget(self.status_label)


        # Crear un botón para tomar una foto
        button = Button(text="Tomar foto")
        button.size_hint = (1, 0.1)
        button.pos_hint = {'x':0, 'y':0}
        button.bind(on_press=self.take_photo)
        layout.add_widget(button)

        # Abrir la camara
        self.capture = cv2.VideoCapture(0)

        def update_camera_preview(dt):
            ret, frame = self.capture.read()

            # Convierta el frame en una textura y muéstrelo en el widget de imagen de Kivy
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

        
        Clock.schedule_interval(update_camera_preview, 1.0/30.0)

        self.add_widget(layout)
    
    def take_photo(self, instance):
        ret, frame = self.capture.read()
        cv2.imwrite('foto.jpg', frame)
        print("Foto tomada!")


        personas = sdk.persons.list()
        cantidadPersonas = personas.count 
        find = False 

        for i in range(cantidadPersonas):
            
            person_id = personas.persons[i].id
            verification_request = VerificationRequest(person_id, ["foto.jpg"])
            pReq = sdk.search.verify(verification_request)

         
            if pReq.score != 0 :
                find = True
                personaEncontrada = pReq.person.name
                self.status_label.text = "Acceso permitido, bienvenido " + personaEncontrada
                break

        if not find : 
            self.status_label.text = "No se encontraron coincidencias"
            

    def volver_menu_principal(self, instance):
        # Cambiar al layout del menú principal
        self.clear_widgets()
        self.add_widget(MenuPrincipal())

    def consultar_registro(self, instance):
        ret, frame = self.capture.read()
        cv2.imwrite('foto.jpg', frame)
        print("Foto tomada!")

        personas = sdk.persons.list()
        cantidadPersonas = personas.count 
        find = False 

        for i in range(cantidadPersonas):
            person_id = personas.persons[i].id
            verification_request = VerificationRequest(person_id, ["foto.jpg"])
            pReq = sdk.search.verify(verification_request)
         
            if pReq.score != 0 :
                find = True
                personaEncontrada = pReq.person.name
                self.status_label.text = "Acceso permitido, bienvenido " + personaEncontrada
                break

            if not find : 
                self.status_label.text = "No se encontraron coincidencias"

class CrearUsuario(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
    
        volver_button = Button(text="Volver al menu")
        volver_button.size_hint = (1, 0.1)
        volver_button.pos_hint = {'x':0, 'y':0}
        volver_button.bind(on_press=self.volver_menu_principal)
        layout.add_widget(volver_button)

        textinput = TextInput(password='Ingrese la contraseña', multiline=False)
        textinput.bind(on_text_validate=self.verificar_password)
        textinput.size_hint = (1, 0.1)
        textinput.pos_hint = {'x':0, 'y':0}
        layout.add_widget(textinput)

        self.add_widget(layout)

    def volver_menu_principal(self, instance):
        # Cambiar al layout del menú principal
        self.clear_widgets()
        self.add_widget(MenuPrincipal())


    def verificar_password(self, instance):
        #######################################
        password = instance.text
        if password == "password":

            self.clear_widgets()
            layout = BoxLayout(orientation='vertical')

            volver_button = Button(text="Volver al menu")
            volver_button.size_hint = (1, 0.1)
            volver_button.pos_hint = {'x':0, 'y':0}
            volver_button.bind(on_press=self.volver_menu_principal)
            layout.add_widget(volver_button)
                
            # Cree un widget de imagen para mostrar la vista previa de la cámara
            self.image = Image()
            layout.add_widget(self.image)

            # Crear un label para mostrar el estado del acceso
            self.status_label = Label(text='Estado de acceso', size_hint=(1, 0.1), height=30, size_hint_min_y=30, size_hint_max_y=30)   
            layout.add_widget(self.status_label)

            textinput = TextInput(multiline=False)
            textinput.size_hint = (1, 0.1)
            textinput.pos_hint = {'x':0, 'y':0}
            layout.add_widget(textinput)


            # Crear un botón para tomar una foto
            button = Button(text="Tomar foto")
            button.size_hint = (1, 0.1)
            button.pos_hint = {'x':0, 'y':0}
            button.bind(on_press=self.take_photo)
            layout.add_widget(button)

            # Abrir la camara
            self.capture = cv2.VideoCapture(0)

            def update_camera_preview(dt):
                ret, frame = self.capture.read()

                # Convierta el frame en una textura y muéstrelo en el widget de imagen de Kivy
                if ret:
                    buf1 = cv2.flip(frame, 0)
                    buf = buf1.tostring()
                    texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.image.texture = texture

            
            Clock.schedule_interval(update_camera_preview, 1.0/30.0)

            self.add_widget(layout)

                
        ########################################
        else:
            self.clear_widgets()
            self.add_widget(MenuPrincipal())
            
    def take_photo(self, instance):
        nombre = instance.text
        ret, frame = self.capture.read()
        cv2.imwrite('nuevoUsuario.jpg', frame)
        print("Foto tomada!") 

        image_base_path = Path("./")
        image_path = image_base_path / "nuevoUsuario.jpg"

        # The only mandatory parameter for a person is images
        # If id is unspecified, it will be auto-generated
        # If name is unspecified, it will be set to the person's id
        person = PersonBase([image_path], name=nombre)
        person = sdk.persons.create(person)



        
class MainApp(App):
    def build(self):
        # Crear ScreenManager
        screen_manager = ScreenManager()

        # Crear las pantallas y agregarlas al ScreenManager
        menu_screen = Screen(name='menu')
        menu_screen.add_widget(MenuPrincipal())
        screen_manager.add_widget(menu_screen)

        # Establecer la pantalla inicial
        screen_manager.current = 'menu'

        return screen_manager


if __name__ == '__main__':
    MainApp().run()