#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot # Libreria de la API del bot.
from telebot import types # Tipos para la API del bot.
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time # Librería para hacer que el programa que controla el bot no se acabe
import random
import logging
import os
import multiprocessing as mp
import sympy
from sympy.parsing.sympy_parser import parse_expr
import tresenraya as TER

token_file = open("TOKEN.txt", "r") # "TOKEN.txt" tiene el token que Bot Father nos dio en la primera línea
TOKEN = token_file.readline().replace("\n", "")
password = token_file.readline().replace("\n", "")
token_file.close()

partidas = {}

def read_jokes(filename): 
	r = []
	f = open(filename, "r")
	line = f.readline()
	while (line != ""):
		if (line == "[JOKE]\n"):
			chiste = f.readline().replace("\n", "")
			line = f.readline()
			while (line != "[JOKE]\n" and line != ""):
				chiste += "\n" + line.replace("\n", "")
				line = f.readline()
			r.append(chiste)
	return r

def muestra_lista(lista): 
	i = 0 
	r = "" 
	for elem in lista: 
		i += 1 
		r += str(i) + ": " + elem + "\n\n"
	return r

def guarda_chistes(filename, chistes):
	f = open(filename, "w")
	for chiste in chistes:
		f.write("[JOKE]\n" + chiste + "\n")

commands = {  # command description used in the "help" command

		'start': 'Arranca a este inteligente pingüino',
		'help': 'Ayuda de este genio',
		'chiste': 'Chiste 100tifiko',
		'einstein': 'Meme de einstein con el texto que se le pase',
		'integra': '/integra a b f(x): Integra f(x) entre a y b',
		'meme100tifiko': 'Manda un meme 100tifiko aleatorio',
		'primitiva': '/primitiva f(x): Calcula la primitiva de f(x)',
		'addchiste': '/addchiste chiste: Añade el chiste a la lista de chistes',
		'listachistes': '/listachistes: Muestra una lista con todos los chistes incluídos'
			  #'tres': 'Unirse/crear una partida de tres en raya',
			  #'juego': 'Hacer un movimiento en la partida (/juego b2)'
}

nMemes = 9

insultos = [" ligas menos que un gas noble", " eres el mejor protón de un átomo de hidrógeno",
	   ", hazle caso a Ignacio y mete los dedos en un enchufe", ", 28 hostias te mereces",
	   ", haznos un favor y deja de aumentar la entropía del Universo",
	   " haces menos falta que un paracaídas en un submarino", ", multiplícate por cero",
	   ", me recuerdas a PRADO. ¡Siempre estás por los suelos!"]

try:
	chistes = read_jokes("jokes.txt")
except:
	chistes = ["Van dos y se cae PRADO"]
	guarda_chistes("jokes.txt", chistes)

asignaturaschungas = ["Mecánica", "Termodinámica", "Electromagnetismo", "Cuántica",
                      "Física General", "Complejos", "Circuitos", "Álgebra"]

working_dir = os.getcwd()

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

    help_text = "Los siguientes comandos están disponibles:\n\n"

    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['chiste']) # Indicamos que lo siguiente va a controlar el comando '/chiste'
def command_comentario(m): # Definimos una función que resuleva lo que necesitemos.
	cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
	bot.send_message( cid, random.choice(chistes)) # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.

@bot.message_handler(commands=['addchiste'])
def command_addchiste(m):
	chistes.append(m.text[len("/addchiste "):])
	guarda_chistes("jokes.txt", chistes)

@bot.message_handler(commands=['listachistes'])
def command_listchiste(m):
	cid = m.chat.id
	bot.send_message(cid, muestra_lista(chistes))

@bot.message_handler(commands=['rmchiste'])
def command_addchiste(m):
	cid = m.chat.id
	try:
		contra, num = m.text[len("/rmchiste "):].split(" ")
		if (contra == password):
			del chistes[int(num)-1]
			guarda_chistes("jokes.txt", chistes)
		else:
			bot.send_message(cid, "Contraseña incorrecta")
	except:
		bot.send_message(cid, "Hubo un problema para borrar el chiste deseado")

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
    try:
        a = float(text[:i])
    except ValueError:
        bot.send_message(cid, "Los límites de integración tienen que ser números reales")
        return
    j = i + 1
    while (j < tam and text[j] != ' '):
    	j += 1
    if (j == tam):
    	bot.send_message(cid, "Es necesario pasar tres argumentos a, b y f(x)")
    	return
    try:
        b = float(text[i+1:j])
    except ValueError:
        bot.send_message(cid, "Los límites de integración tienen que ser números reales")
        return
        
    Sfuncion = text[j+1:]
    
    try:
        f = definition_to_function("f(x) = " + Sfuncion)
    except:
        bot.send_message(cid, "Error al reconocer la función a integrar")
        return
    try:
        valor = IntegralSimpsonCompuesto(f, a, b)
    except:
        bot.send_message(cid, "Error al reconocer la función a integrar")
        return
    bot.send_message(cid, "La integral de {} entre {} y {} da aproximadamente {}".format(Sfuncion, a, b, valor))

latex_doc = ["\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage[margin=5px]{geometry}\n\\thispagestyle{empty}\n\n\\begin{document}\n\t\\begin{math}",
			 "\\end{math}\n\\end{document}"]

def intento_integracion(f, q):
	q.put(sympy.integrate(f))

@bot.message_handler(commands=['primitiva'])
def primitiva(m):
	cid = m.chat.id
	funcion = m.text[len("/primitiva "):]
	try:
		f = parse_expr(funcion)
	except:
		bot.send_message(cid, "La función {} no es una función de x válida".format(funcion))
		return
	try:
		#queue = mp.Queue()
		#p = mp.Process(target=intento_integracion, args=(f, queue,))
		#p.start()
		#I = queue.get()
		#p.join(20)
		#if (p.is_alive()):
	        #	p.terminate()
	        #	p.join()
		I = sympy.integrate(f)
	except:
		bot.send_message(cid, "La función {} no puede integrarse, asegúrese de que solo tiene x de variable".format(funcion))
		return
	
	ecuacion  = sympy.Eq(sympy.Integral(f), I)
	try:
		if (ecuacion):
			bot.send_message(cid, "No se ha enccontrado solución analítica para la función: {}".format(funcion))
			return
	except:
		pass
	
	tex_content = latex_doc[0] + sympy.latex(ecuacion) + "+C" + latex_doc[1]

	f = open(working_dir + "/primitiva.tex", 'w')

	f.write(tex_content)

	f.close()

	os.system("pdflatex -output-directory=" + working_dir + " " + working_dir + "/primitiva.tex && pdfcrop " + working_dir + "/primitiva.pdf " + working_dir + "/primitiva-crop.pdf && pdftoppm " + working_dir + "/primitiva-crop.pdf | pnmtopng > " + working_dir + "/primitiva.png")
	bot.send_photo(cid, open(working_dir + "/primitiva.png", "rb"))
	
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

@bot.message_handler(commands=['meme100tifiko'])
def meme(m):
    cid = m.chat.id
    bot.send_photo(cid, open("Meme" + str(random.randint(1, nMemes)) + ".jpg", "rb"))

@bot.message_handler(commands=['animos_covid'])
def meme(m):
    cid = m.chat.id
    bot.send_message(cid, "Ánimo, si pudiste con {} podrás con este maldito virus".format(random.choice(asginaturaschungas)))

@bot.message_handler(func=lambda message: message.content_type == "text" and message.text.lower() == "salu2")
def saludo(m):
    	cid = m.chat.id
    	bot.reply_to(m, "Salu2 100tifkos")

@bot.message_handler(func=lambda message: message.content_type == "text" and message.text.lower() == "te quiero")
def loveyou(m):
    	bot.reply_to(m, "Yo también te quiero ♥ ¡LEJOS!")

@bot.message_handler(func=lambda message: message.content_type == "text" and message.text.lower() == "beta")
def loveyou(m):
    cid = m.chat.id
    user = m.from_user.username
    if (user != None):
        bot.send_message(cid, "@{} no seas impaciente que esto es todavía una beta".format(user))
    else:
        user = m.from_user.first_name + ' ' + m.from_user.last_name
        bot.send_message(cid, "¡{} ME CAGO EN TOH YA VA SIENDO HORA DE QUE TE HAGAS UN ALIAS TANTO FASTIDIAR A LA POBRE GENTE QUE PROGRAMAMOS BOTS!".format(user.upper()))

	
video = open("VideoNavidad.mp4", "rb")
@bot.message_handler(func=lambda message: message.content_type == "text" and "feliz navidad" in message.text.lower())
def FelizNavidad(m):
    cid = m.chat.id
    snowman = u'\U000026C4'
    
    bot.send_video(cid, video)
    bot.send_message (cid, "¡¡Feliz Navidad!!\n¡Que Bernier y Galindo os regalen muchos aprobados, los vais a nesecitar! " + snowman)

@bot.message_handler(func=lambda message: message.content_type == "text" and ("feliz año" in message.text.lower() or "feliz 2020" in message.text.lower()))
def newyear(m):
    bot.reply_to(m, "あけおめ！\n \n Feliz año nuevo! \n \n Feliz año 2020 \n \n Os deseo a todos un feliz año \n \n 🎉🎊🎉🎊🎉🎊🎉🎊🎉🎊")

@bot.message_handler(func=lambda message: message.content_type == "text" and ("buenos dias" in message.text.lower() or "buenos días" in message.text.lower()))
def buenos_dias(m):
	cid = m.chat.id
	bot.reply_to(m, "Buenos dias, que tengas un día tope cuántico")

@bot.message_handler(func=lambda message: message.content_type == "text" and "buenas noches" in message.text.lower())
def buenas_noches(m):
	cid = m.chat.id
	bot.reply_to(m, "Buenas noches, que descanses y que sueñes con los tensorcitos")

@bot.message_handler(func=lambda message: message.content_type == "text" and "prado" in message.text.lower())
def saludo(m):
	bot.reply_to(m, "¿Otra vez se ha caído el PRADO?")

# len("insulta a ") == 10
@bot.message_handler(func=lambda message: message.content_type == "text" and message.text.lower()[:10] == "insulta a ")
def insulto(m):
    cid = m.chat.id
    name = m.text[10:]
    insult = random.choice(insultos)
    bot.send_message(cid, "{}{}".format(name, insult))
    		
cabellofrases=["Okey Makey","Bueno estaba y se murió"]

@bot.message_handler(func=lambda message: message.content_type == "text" and "cabello" in message.text.lower())
def Cabello(m):
    cabellomsg = random.choice(cabellofrases)
    bot.reply_to(m, cabellomsg)

@bot.message_handler(func=lambda message: message.content_type == "text" and "david blanco" in message.text.lower())
def DavidBlanco(m):
	bot.reply_to(m, "¿David Blanco? Buah, un grande ese señor")

@bot.message_handler(func=lambda message: message.content_type == "text" and "peralta" in message.text.lower())
def Peralta(m):
	bot.reply_to(m, "Esta demostración es de gratis. ¿He hecho algo? No, nada. Trivial")

@bot.message_handler(func=lambda message: message.content_type == "text" and "roque" in message.text.lower())
def Roque(m):
	bot.reply_to(m, "¿Les he escrito ya a ustedes la primera ley de la Termodinámica?\n\ndU = dQ - dW")

#@bot.message_handler(func=lambda message: message.content_type == "text" and ("28" in message.text or " 28 " in message.text or " 28" in message.text or "veintiocho" in message.text.lower()))
#def paco_polo(m):
#	cid = m.chat.id
#	bot.reply_to(m, "¿Has dicho 28?")
#	bot.send_photo(cid, open("paco_polo.png", "rb"))

@bot.message_handler(func=lambda message: message.content_type == "text" and "bochan" in message.text.lower())
def bochan(m):
	cid = m.chat.id
	bot.reply_to(m, "Boo")
#	bot.send_photo(cid, open("bochan.png", "rb"))

@bot.message_handler(func=lambda message: message.content_type == "text" and "cabrerizo" in message.text.lower())
def cabrerizo(m):
	cid = m.chat.id
	bot.reply_to(m, "Tira de la cuerda")
	
bot.message_handler(func=lambda message: message.content_type == "text" and "luis javier" in message.text.lower())
def luis_javier(m): #programación 1ºC
    cid = m.chat.id
    bot.reply_to(m, "Rotundamente no!!!!")

bot.message_handler(func=lambda message: message.content_type == "text" and "Carmen" in message.text.lower())
def carmen(m): #quimica 1ºC
    cid = m.chat.id
    bot.reply_to(m, "k sub water / 0/a indeterminación")
    
@bot.message_handler(func=lambda message: message.content_type == "text" and ("ignacio" in message.text.lower() or "circuitos" in message.text.lower()))
def Ignacio(m):#circuitos 2º
    bot.reply_to(m, "Y si no me crees pues mete los dedos en un enchufe y mira a ver si el dolor es real")

@bot.message_handler(func=lambda message: message.content_type == "text" and "miguel angel" in message.text.lower())
def miguel_angel(m):
    bot.reply_to(m, "Tienes 125 correos nuevos de RODRÍGUEZ VALVERDE, MIGUEL ÁNGEL")

@bot.message_handler(func=lambda message: message.content_type == "text" and "bernier" in message.text.lower())
def bernier(m):
    bot.reply_to(m, "Buah, no veas con er DJ Petardo con él la fiesta está garantizada:\n\nwhile (true) {\n    fiesta++;\n}")
    
calixtofrases=["Uuuuhhh niceee", "I'm native from Ciudad Real... Royal City", "Pain in my brain"]

@bot.message_handler(func=lambda message: message.content_type == "text" and "calixto" in message.text.lower())
def Calixto(m):
    bot.reply_to(m, random.choice(calixtofrases))

@bot.message_handler(func=lambda message: message.content_type == "text" and "fail" in message.text.lower())
def trollFail(m):
    bot.reply_to(m, "Fail, la nota que vas a tener en " + random.choice(asignaturaschungas))
    

	
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
