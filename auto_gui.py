#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Clase que facilita el uso de PyAutoGUI para multiples aplicaciones.

INVESTIGAR SI REALMENTE CONVIENE USAR ESTE MODULO U OTRO.

Fuente:
https://pyautogui.readthedocs.io/en/latest/
https://pyautogui.readthedocs.io/en/latest/quickstart.html
"""

import pyautogui
from time import sleep
from files_use import FileUse
from threading import Thread

class AutoGUI(object):
	"""Clase que facilita el uso de PyAutoGUI para multiples aplicaciones"""
	def __init__(self):
		super(AutoGUI, self).__init__()
		self.special_keys = ["alt", "altleft", "altright", "enter", "ctrl", "ctrlleft", "ctrlright", "capslock"
							"esc", "escape", "up", "down", "left", "right", "shift", "shiftleft", "shiftright"
							"space", "tab"] + ["f" + str(i) for i in range(1, 25)]
		self.init()

	def init(self):
		"""
		Inicializa el objeto de control de archivos.
		"""
		self.files_control = FileUse()
		
	def send_keys(self, keys_list=None):
		"""
		Presiona las teclas enviadas o escribe el contenido de la 'tecla'

		 - Si se le pasa una suma de teclas, mantiene las modificadoras
		   y presiona las comunes.
		 - Si se le pasan modificadoras solas las presiona.
		"""
		if keys_list:
			for key in keys_list:
				if "+" in key and len(key) > 1:
					keys = key.split("+") # Divide la cadena para obtener las teclas

					for key in keys: # Sirve para cualquier cantidad de modificadores
						if key in self.special_keys:
							pyautogui.keyDown(key)
							# Presiona los modificadores
						else:
							pyautogui.press(key)
							# Presiona las teclas comunes

					for key in keys:
						if key in self.special_keys:
							pyautogui.keyUp(key)
					# Suelta todas los modificadores
				elif key in self.special_keys:
					pyautogui.press(key)
				else:
					pyautogui.typewrite(key)

	def mouse_move(self, move=None, rel=False, drag=False, function=None, iters=0):
		"""
		Mueve el mouse segun move.

		 - Si recibe una funcion, ejecuta la funcion despues de cada ciclo.
		 - "rel" habilita el movimiento relativo.
		 - "drag" mueve el mouse con un boton presionado.
		 - Si no recibe coordenadas (move), devuelve la posicion actual del mouse
		"""
		if move == None:
			return pyautogui.position()

		if drag:
			pyautogui.mouseDown()
			if rel:
				pyautogui.moveRel(move[0], move[1])
			else:
				pyautogui.moveTo(move[0], move[1])
			pyautogui.mouseUp()

		if function:
			for i in range(iters):
				x, y = function()
				pyautogui.moveTo(x, y)
		else:
			if rel:
				pyautogui.moveRel(move[0], move[1])
			else:
				pyautogui.moveTo(move[0], move[1])

	def click(self, mode, clicks=1):
		"""
		Clickea en la posicion en la que se encuentra el mouse.
		Si mode:
		 - 0: Click izquierdo, una vez
		 - 1: Click derecho
		 - 2: Doble click
		 - 3: Triple click
		 - 4: Click medio
		"""
		if mode == 0:
			pyautogui.click()
		elif mode == 1:
			pyautogui.click(button='right')
		elif mode == 2:
			pyautogui.click(clicks=2)
		elif mode == 3:
			pyautogui.click(clicks=clicks)
		else:
			pyautogui.click(button='middle')

	def scroll(self, amount, percent=False):
		"""
		Baja o sube en la pantalla.

		 - Si percent == True, se mueve ese porcentaje del alto de la pantalla
		"""
		if percent:
			amount = int((amount / 100) * self.get_screen_properties()[0])

		pyautogui.scroll(amount)

	def get_screen_properties(self):
		"""
		Devuelve las propiedades fundamentales de la pantalla.
		"""
		return list(pyautogui.size())

	def save_screenshot(self, filename=""):
		"""
		Obtiene una captura de pantalla y la guarda en un archivo
		"""
		file = self.files_control.create_file(filename, extension = "png")

		return pyautogui.screenshot(file.name)

	def get_on_screen(self, image):
		"""
		Funciones que obtienen imagenes en pantalla y su locacion.

		 - Usar OpenCV para localizacion avanzada.
		"""
		try:
			coordenadas = locateCenterOnScreen(image, grayscale=True)
		except ImageNotFoundException as e:
			coordenadas = False

		return coordenadas

	def gui_functions(self, kind, options):
		"""
		Funcion que decide que interfaz usar y la genera.
		"""
		if kind == "alert":
			result = pyautogui.alert(title=options[0], text=options[1], button=options[2])
		elif kind == "confirm":
			result = pyautogui.confirm(title=options[0], text=options[1], buttons=options[2])
		elif kind == "prompt":
			result = pyautogui.prompt(title=options[0], text=options[1], default=options[2])
		elif kind == "password":
			result = pyautogui.password(title=options[0], text=options[1], default=options[2], mask='*')

		options[3](result)
		# Funcion que recibe la respuesta

	def gui(self, kind, options, asyncronous=False):
		"""
		Engloba todas las posibles interfaces que ofrece pyautogui en una funcion.

		 - type define el tipo de interfaz
		 - options es una lista con los parametros que toma solo los necesarios
		"""
		if len(options) != 4:
			return None
		# Siempre recibe cuatro parametros
		# El ultimo es la funcion a la que se le pasa la respuesta

		if asyncronous:
			self.hilo = Thread(target=self.gui_functions, args=(kind, options,))
			self.hilo.start()
		else:
			self.gui_functions(kind, options)

def main():
	autogui = AutoGUI()

	sleep(2)

	autogui.gui("password", ["hola", "que", "tal", lambda x: print(x)])

main()