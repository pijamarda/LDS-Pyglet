#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from data import *

MAXWIDTH = 640
MAXHEIGHT = 480
VELOCIDAD = 3
LIMITE = MAXHEIGHT/2.5
MAXSCALE=3.0
MINSCALE=2.0
INCREMENTOS=0.1

class Persona:
	def __init__(self,s,x,y):
		self.s=s
		self.s.scale=1
		self.x=x
		self.y=y
		self.dx=x
		self.dy=y
	def pintar(self):
		self.s.set_position(self.x-self.s.width/2,self.y-self.s.height/2)
		self.s.scale=self.ajustar()
		self.s.draw()
	def set_destino(self,x,y):
		self.dx=x
		if (y<LIMITE):
			self.dy=y
		else: 
			self.dy=LIMITE
	def actualizarPos(self):
		if not(self.x == self.dx and (self.x==self.dy)):
			if (self.dx>0 and self.dx<MAXWIDTH 
				and self.dy>0 and self.dy<MAXHEIGHT):
				if self.x < self.dx:
					self.x += VELOCIDAD
				if self.y < self.dy:
					self.y += VELOCIDAD
				if self.x > self.dx:
					self.x -= VELOCIDAD
				if self.y > self.dy:
					self.y -= VELOCIDAD

	#Esta funcion ajusta el tamaño de la persona (sprite), dependiendo de donde
	#este situada en la ventana. Los valores que chequean son:
	#LIMITE: Hasta donde puede llegar la persona "peter"
	#MINSCALE: Marca el tamaño minimo que tendra el personaje
	#MAXSCALE: El tamaño maximo que tendra el personaje
	#INCREMENTOS: Como va variando el personaje, todavia no tengo claro como
	#			  afecta. Creo que puede marcar la brusquedad del cambio.
	#			  probar mas adelantes

	def ajustar(self):
		scale=1
		#Primero vamos a averiguar en cuantos saltos en total puede variar
		#el personaje, esto nos lo da "divisor"
		divisor = (MAXSCALE-MINSCALE)/INCREMENTOS
		#cociente marca por cada cuantos pixels debemos aumentar la escala
		cociente=LIMITE/divisor
		#la escala final se calcula sumando al minimo de la escala el numero de
		#incrementos calculados dependiendo de la posicion actual del personaje
		scale=MINSCALE+((LIMITE-self.s.y)/cociente)*INCREMENTOS
		#print(LIMITE,divisor, cociente, scale)
		return scale

class Objeto:
	def __init__(self,num,nombre,x,y,texto):
		self.img=self.cargarImagenes(num,nombre)
		self.num=num
		self.x=x
		self.y=y		
		self.width=self.img[0].width
		self.height=self.img[0].height
		self.textX=x
		self.textY=y
		self.activo=True
		self.textoTemp=texto
	def pintar(self):
		if self.activo:
			self.img[int(counter)].set_position(self.x,self.y)		
			self.img[int(counter)].draw()
			self.mostrarTexto(self.textX,self.textY)
			self.accion(peter.x, peter.y)
		
	def mostrarTexto(self,x,y):
		if self.colision(x,y):			
			self.texto=pyglet.text.Label(self.textoTemp,
									font_name="Times New Roman",
									font_size=20,
									x=x, y=y)
			self.texto.draw()

	def colision(self,x,y):
		col = False
		if (x>self.x and x<self.x+self.width):
			if (y>self.y and y<self.y+self.height):
				col=True
		return col

	def cargarImagenes(self,num, name):
		arrS=[]
		for i in range(num):
			tmpI = pyglet.image.load("./img/"+name+str(i)+".png")
			tmpS = pyglet.sprite.Sprite(tmpI)
			arrS.append(tmpS)
		return arrS

	def actualizar(self,dt):
		global counter
		counter=(counter+dt)%self.num

	def accion(self,x,y):
		if (self.colision(x,y)):
			print("objeto alcanzado")
			self.activo=False


class Nivel:
	def __init__(self,nombre,fondo):
		self.fondo = pyglet.image.load("./img/"+fondo)
		self.nombre=nombre		
		self.objetos=[]		
	def printInfo(self):
		print(self.nombre, self.numObjetos)
	def pintar(self):
		self.fondo.blit(0,0)
		for i in range(len(self.objetos)):
			self.objetos[i].pintar()
	def numObjetos(self):
		return len(self.objetos)

window = pyglet.window.Window(width=MAXWIDTH, height=MAXHEIGHT)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

nivel=[]
nivelActual=0
nivel.append(Nivel(Ni.n0,Ni.n0b))
nivel[nivelActual].objetos.append(Objeto(Ob.an,Ob.a,Ob.ax,Ob.ay,Ob.at))
nivel[nivelActual].objetos.append(Objeto(Ob.bn,Ob.b,Ob.bx,Ob.by,Ob.bt))

imgBala = pyglet.image.load('./img/bala.png')
s_peter = pyglet.sprite.Sprite(imgBala)
peter = Persona(s_peter,0,0)
counter=.0

@window.event
def on_draw():	
	window.clear()	
	nivel[nivelActual].pintar()
	peter.pintar()

@window.event
def on_mouse_motion(x, y, button, modifiers):
	for i in range(nivel[nivelActual].numObjetos()):
		nivel[nivelActual].objetos[i].textX=x
		nivel[nivelActual].objetos[i].textY=y

def pintar_fondo(fondo):
	fondo.blit(0,0)

@window.event
def on_mouse_press(x, y, button, modifiers):	
	peter.set_destino(x,y)

def update(dt):
	peter.actualizarPos()
	for i in range(nivel[nivelActual].numObjetos()):
		nivel[nivelActual].objetos[i].actualizar(dt)

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()