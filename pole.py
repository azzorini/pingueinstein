from datetime import datetime
import telebot
from telebot import types
import ast

class Pole:
    def __init__(self):
        self.pole, self.plata, self.fail, self.canaria, self.andaluza = 0, 0, 0, 0, 0

    def __init__(self, filename):
        f = open(filename, "r")
        try:
            self.pole = int(f.readline())
        except:
            self.pole = 0
        try:
            self.plata = int(f.readline())
        except:
            self.plata = 0
        try:
            self.fail = int(f.readline())
        except:
            self.fail = 0
        try:
            self.canaria = int(f.readline())
        except:
            self.canaria = 0
        try:
            self.andaluza = int(f.readline())
        except:
            self.andaluza = 0
        f.close()

    def guarda(self, f):
        f.write("{}\n{}\n{}\n{}\n{}".format(self.pole, self.plata, self.fail, self.canaria, self.andaluza))

    

    

    

    

    def isAndaluza(self):
        day = datetime.now().day
        hour = datetime.now().hour
        if (self.andaluza != day and hour >= 12):
            self.andaluza = day
            self.guarda()
            return True
        else:
            return False

class ScorePole:
	def __init__(self, puntuacion=0, dia=0):
		self.score = puntuacion
		self.day = dia
	def string(self):
		return str(self.score) + '\n' + str(self.day) + '\n'
	def read(self, f):
		self.score = int(f.readline())
		self.day = int(f.readline())

class PlayerPole:
	def __init__(self, usuario, pole = ScorePole(0, 0)
		canaria = ScorePole(0, 0), andaluza = ScorePole(0, 0)):
		if (type(usuario).__name__ == 'User'):
			self.user = usuario
			self.pole = pole
			self.canaria = canaria
			self.andaluza = andaluza
		elif (type(usuario).__name__ == 'TextIOWrapper'):
			self.read(usuario)
		elif (type(usuario).__name__ == 'dict'):
			userdict = ast.literal_eval(usuario['user'])
			self.user = types.User(userdict['id'], userdict['is_bot'],
				userdict['first_name'], userdict['username'],
				userdict['last_name'], userdict['language_code'])
			self.pole = usuario['pole']
			self.canaria = usuario['canaria']
			self.andaluza = usuario['andaluza']
		else:
			raise TypeError("Argumento 'usuario' es de un tipo no válido")

	def string(self):
		return (str(self.user) + '\n' + self.pole.string() + 
				 self.canaria.string() + self.andaluza.string())
	
	def dictionary(self):
		return dict({'user': str(self.user),
					  'pole': "ScorePole({}, {})".format(self.pole.score, self.pole.day),
					  'canaria': "ScorePole({}, {})".format(self.canaria.score, self.canaria.day),
					  'andaluza': "ScorePole({}, {})".format(self.andaluza.score, self.andaluza.day)})		
	
	def read(self, f):
		userdict = ast.literal_eval(f.readline())
		self.user = types.User(userdict['id'], userdict['is_bot'],
			userdict['first_name'], userdict['username'],
			userdict['last_name'], userdict['language_code'])
		self.score = int(f.readline())
		self.day = int(f.readline())

def sortPole(val):
	return val.pole.score

def sortCanaria(val):
	return val.canaria.score

def sortAndaluza(val):
	return val.andaluza.score

class GroupPole:
    def __init__(self, f, cid=0):
		if (type(f).__name__ == "TextIOWrapper"):
			self.read(f)
		else:
			if (cid == 0):
				raise TypeError("Argumento id no enviado")
			self.id = cid
			self.players = [f]
			self.pole_dict = {}

	def read(self, f):
		self.id = int(f.readline())
		line = f.readline()
		self.players = []
		while (line[:6] == "{'id':"):
			f.seek(f.tell() - len(line))
			self.players.append(PlayerPole(f))
			line = f.readline()
		self.pole_dict = eval(line)
		for key in self.pole_dict:
			self.pole_dict[key] = PlayerPole(eval(self.pole_dict[key]))
	
	def sort_players(self, criterio = sortPole):
		self.players.sort(key = criterio, reverse = True)
		
	def add_player(self, player):
		self.players.append(player)
	
	def save(self, f):
		f.write(str(self.id) + '\n')
		for p in self.players:
			f.write(p.string())
		s = "{"
		for key in self.pole_dict:
			s = (s + "'" + key + "': " +
				 str(self.pole_dict[key].dictionary()) + ", ")
		s = s[:len(s)-2] + "}\n"
		f.write(s)
		
	def id_repetida(self, pid):
		day = datetime.now().day
		try:
			if (self.pole_dict['pole'].user.id == pid
				and self.pole_dict['pole'].pole.day == day):
				return True
		except KeyError:
			return False
			
		try:
			if (self.pole_dict['plata'].user.id == pid
				and self.pole_dict['plata'].pole.day == day):
				return True
		except KeyError:
			return False
		try:
			if (self.pole_dict['fail'].user.id == pid
				and self.pole_dict['fail'].pole.day == day):
				return True
		except KeyError:
			return False
			
		return False
		
		def player_index(self, cid):
			for i in range(0, len(self.players)):
				if (self.players[i].user.id == cid):
					return i
			return -1
		
		def Pole(self, user):
			day = datetime.now().day
			if (day != self.pole_dict['pole'].pole.day):
				if (self.player_index(user.id) == -1):
					self.add_player(PlayerPole(user))
				index = self.player_index(user.id)
				self.players[index].pole.day = day
				self.players[index].pole.score += 3
				self.pole_dict['pole'] = self.players[index]
				return True
			else:
				return False
		def Plata(self, user):
			day = datetime.now().day
			if (self.id_repetida(user.id)):
				return False
			if (day == self.pole_dict['pole'].pole.day and 
				day != self.pole_dict['plata'].pole.day):
				if (self.player_index(user.id) == -1):
					self.add_player(PlayerPole(user))
				index = self.player_index(user.id)
				self.players[index].pole.day = day
				self.players[index].pole.score += 1
				self.pole_dict['plata'] = self.players[index]
				return True
			else:
				return False
		def Fail(self):
			if (self.id_repetida(user.id)):
				return False
			day = datetime.now().day
			if (day == self.pole_dict['pole'].pole.day and 
				day == self.pole_dict['plata'].pole.day and
				day != self.pole_dict['fail'].pole.day):
				if (self.player_index(user.id) == -1):
					self.add_player(PlayerPole(user))
				index = self.player_index(user.id)
				self.players[index].pole.day = day
				self.players[index].pole.score += 0.5
				self.pole_dict['fail'] = self.players[index]
				return True
			else:
				return False
		
		def Canaria(self, user):
			day = datetime.now().day
			hour = datetime.now().hour
			if (self.pole_dict['canaria'].canaria.day != day and hour >= 1):
				if (self.player_index(user.id) == -1):
					self.add_player(PlayerPole(user))
				index = self.player_index(user.id)
				self.players[index].canaria.day = day
				self.players[index].canaria.score += 1
				self.pole_dict['canaria'] = self.players[index]
				return True
			else:
				return False
				
		def Andaluza(self, user):
			day = datetime.now().day
			hour = datetime.now().hour
			if (self.pole_dict['andaluza'].andaluza.day != day and hour >= 12):
				if (self.player_index(user.id) == -1):
					self.add_player(PlayerPole(user))
				index = self.player_index(user.id)
				self.players[index].andaluza.day = day
				self.players[index].andaluza.score += 1
				self.pole_dict['andaluza'] = self.players[index]
				return True
			else:
				return False
		def polerank(self):
			self.sort_players()
			for j in self.players:
				nombre = j.user.username
				if (nombre == None):
					nombre = j.user.first_name + ' ' + j.user.last_name
				else:
					nombre = '@' + nombre
				
				

def AdminPole:
	def __init__(self, filename):
		try:
			f = open(filename, "r")
		except FileNotFoundError:
			self.groups = {}
			return
		line = f.readline()
		self.groups = {}
		while (line != ""):
			f.seek(f.tell() - len(line))
			grupo = GroupPole(f)
			self.groups[grupo.id] = grupo
			line = f.readline()
	
	def exists(self, cid):
		return cid in self.groups
	
	def add_group(self, cid, user):
		self.groups[cid] = GroupPole(user, cid)
