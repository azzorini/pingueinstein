#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot # Libreria de la API del bot.
from telebot import types # Tipos para la API del bot.
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time # Librería para hacer que el programa que controla el bot no se acabe.
import random
import logging
import sympy
import tresenraya as TER

TOKEN = '' # Nuestro token del bot (el que @BotFather nos dió).

partidas = {}

commands = {  # command description used in the "help" command

              'start': 'Arranca a este inteligente pingüino',
              'help': 'Ayuda de este genio',
			  'chiste': 'Chiste 100tifiko',
			  'einstein': 'Meme de einstein con el texto que se le pase',
			  'integra': '/integra a b f(x): Integra f(x) entre a y b',
			  'meme': 'Manda un meme 100tifiko aleatorio'
			  #'tres': 'Unirse/crear una partida de tres en raya',
			  #'juego': 'Hacer un movimiento en la partida (/juego b2)'
}

nMemes = 2

chistes = ["Van dos y se cae PRADO",
		   "Making bad chemistry jokes because all the good ones argon",
		   "¿Qué dice un grupo CH3 en lo alto de un tejado?\n¿Metilo o no metilo?",
		   "1 de cada 10 personas saben binario",
		   "Mi mujer tiene un gran físico - Albert Einstein",
		   "¿Cuál es la fórmula del agua bendita?\nH DIOS O",
		   "¿Qué es un langostino?\nUna langosta con un triple enlace",
		   "No soporto a los químicos, lo sodio",
		   "-¿Cuántos físicos hacen falta para cambiar una bombilla?\n-Dos, uno para sujetar la bombilla y otro para rotar el universo.",
		   "¿Cuál es la ley física más zen?\nLa ley de Ohm",
		   "Fotón a protón:\n-Hey, vente a la fiesta, vamos a ir unos cuantos.",
		   "¿Por qué se disuelve antes en agua un emo que un oso polar?\nPorque el emo es bipolar",
		   "Un vector le dice a un escalar a punto de suicidarse:\n-¡Para, que todo en esta vida tiene solución!\nA lo que el escalar responde:\n-Mi vida nunca tuvo sentido",
		   "Esto es una discusión entre i y pi:\ni:Sé racional\npi:Sé real",
		   "Schrödinger va en su coche a toda velocidad cuando la policía lo para y nota algo raro en su caja\n\nPolicía: ¡Abra su caja!\n\n*Schrödinger la abre sin ningún problema*\n\nEl policía queda atónito al ver al gato y dice:\nPolicía: Está muerto\nSchrödinger: Ahora lo está",
		   "Va Heisenberg en su coche por la autovía y lo para un policía. Éste le dice:\n-¿Sabe usted que va a 140 km/h?\n-¡Mierda, ya no sé donde estoy!"]

def definition_to_function(s):
    lhs, rhs = s.split("=", 1)
    rhs = rhs.rstrip('; ')
    args = sympy.sympify(lhs).args
    f = sympy.sympify(rhs)
    def f_func(*passed_args):
        argdict = dict(zip(args, passed_args))
        result = f.subs(argdict)
        return float(result)
    return f_func

def IntegralSimpsonCompuesto(f, x0, xf, n = 1000):
	if (n <= 0):
		return 0
	elif (n % 2 != 0):
		n += 1 # Necesitamos un n par por lo que si no lo es recurrimos al siguiente n

	h, suma_par, suma_impar = float(xf - x0) / n, .0, .0
	for i in range(2, n, 2):
		suma_impar += f(x0 + (i - 1) * h)
		suma_par += f(x0 + i * h)

	suma_impar = 4 * (suma_impar + f(x0 + (n - 1) * h))
	suma_par *= 2

	return (h / 3) * (f(x0) + f(xf) + suma_par + suma_impar)

class Partida:
	def __init__(self, cid, player1):
		self.juego = TER.Partida3EnRaya()
		self.cid = cid
		self.jugador = player1
		self.jugador1 = player1
		self.completo = False
		self.victoria = ' '

	def add_player2(self, player2):
		if (self.juagdor2 != 0):
			self.juagdor2 = player2
			return True
		return False

	def jugada(self, jugador, letra, numero):
		if (jugador == self.jugador):
			if (self.juego.jugada(letra, numero)):
				if (self.juego.victoria != ' '):
					self.victoria = self.juego.victoria
				return True
		return False

bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
#############################################
#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
	for m in messages: # Por cada dato 'm' en el dato 'messages'
		if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
			cid = m.chat.id # Almacenaremos el ID de la conversación.
			print("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
#############################################
#Funciones
@bot.message_handler(commands=['start'])
def command_start(m):

	cid = m.chat.id
	bot.send_message(cid, "Arrancando Pingüeinstein...\n¡Buenas! ¿En qué puedo servirle?")
	command_help(m)

@bot.message_handler(commands=['help'])
def command_help(m):

    cid = m.chat.id

    help_text = "Los siguientes comando están disponibles:\n\n"

    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['chiste']) # Indicamos que lo siguiente va a controlar el comando '/chiste'
def command_comentario(m): # Definimos una función que resuleva lo que necesitemos.
	cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
	bot.send_message( cid, random.choice(chistes)) # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.

@bot.message_handler(commands=['einstein'])
def einstein(m):
	cid = m.chat.id
	texto = m.text[len("/einstein "):]

	i = 40
	sigue = True
	while (i < len(texto) and sigue):
		while (texto[i] != ' ' and sigue):
			i -= 1
			if (i <= 0 or texto[i] == "\n"):
				sigue = False
		if (sigue):
			texto = texto[:i] + "\n" + texto[i:]
			i += 41


	img = Image.open("Einstein.jpg")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("impact.ttf", 32)
	draw.text((550, 250), texto + "\n\n                                             Albert Einstein",(255,255,255),font=font)
	img.save('Meme.jpg')
	bot.send_photo(cid, open('Meme.jpg', 'rb'))

@bot.message_handler(commands=['integra'])
def integral(m):
    cid = m.chat.id
    text = m.text[len("/integra "):]
    tam = len(text)

    i = 0
    while (i < tam and text[i] != ' '):
    	i += 1
    if (i == tam):
    	bot.send_message(cid, "Es necesario pasar tres argumentos a, b y f(x)")
    	return
    a = int(text[:i])
    j = i + 1
    while (j < tam and text[j] != ' '):
    	j += 1
    if (j == tam):
    	bot.send_message(cid, "Es necesario pasar tres argumentos a, b y f(x)")
    	return
    b = int(text[i+1:j])
    Sfuncion = text[j+1:]

    f = definition_to_function("f(x) = " + Sfuncion)
    valor = IntegralSimpsonCompuesto(f, a, b)
    bot.send_message(cid, "La integral de {} entre {} y {} da aproximadamente {}".format(Sfuncion, a, b, valor))

@bot.message_handler(commands=['msg'])
def send_mensaje(m):
    text = m.text[len("/msg "):]
    tam = len(text)

    i = 0
    while (i < tam and text[i] != ' '):
        i += 1
    if (i == tam):
        return
    cid = text[:i]
    mensaje = text[i+1:]

    bot.send_message(cid, mensaje)

@bot.message_handler(commands=['meme'])
def meme(m):
    cid = m.chat.id
    bot.send_photo(cid, open("Meme" + str(random.randint(1, nMemes)) + ".jpg", "rb"))

@bot.message_handler(func=lambda message: message.content_type == "text" and message.text.lower() == "salu2")
def saludo(m):
	cid = m.chat.id
	bot.reply_to(m, "Salu2 100tifkos")

@bot.message_handler(func=lambda message: message.content_type == "text" and message.text.lower() == "buenas noches")
def buenas_noches(m):
	cid = m.chat.id
	bot.reply_to(m, "Buenas noches, que descanses y que sueñes con los tensorcitos")

@bot.message_handler(func=lambda message: message.content_type == "text" and "prado" in message.text.lower())
def saludo(m):
	bot.reply_to(m, "¿Otra vez se ha caído el PRADO?")

@bot.message_handler(func=lambda message: message.content_type == "text" and "david blanco" in message.text.lower())
def DavidBlanco(m):
	bot.reply_to(m, "¿David Blanco? Buah, un grande ese señor")

@bot.message_handler(func=lambda message: message.content_type == "text" and "peralta" in message.text.lower())
def Peralta(m):
	bot.reply_to(m, "Esta demostración es de gratis. ¿He hecho algo? No, nada. Trivial")

@bot.message_handler(func=lambda message: message.content_type == "text" and "roque" in message.text.lower())
def Roque(m):
	bot.reply_to(m, "¿Les he escrito ya a ustedes la primera ley de la Termodinámica?\n\ndU = dQ - dW")

@bot.message_handler(func=lambda message: message.content_type == "text" and " 28 " in message.text)
def paco_polo(m):
	cid = m.chat.id
	bot.reply_to(m, "¿Has dicho 28?")
	bot.send_photo(cid, open("paco_polo.png", "rb"))


#############################################

#Peticiones
logger = logging.getLogger(__name__)

while True:

    try:

            bot.polling(none_stop=True)

    except Exception as err:

            logger.error(err)

            time.sleep(10)

            print('Error en la conexión')
