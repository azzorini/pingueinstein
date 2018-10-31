jugador1 = 'X'
jugador2 = 'O'
TAM = 3

class Partida3EnRaya:
	def __init__(self):
		self.tablero = [[' ', ' ', ' '],
				   [' ', ' ', ' '],
				   [' ', ' ', ' ']]
		self.victoria = ' '
		self.jugador = jugador1
	
	def str(self):
		r = "   a b c\n1  " + self.tablero[0][0]
		for i in range(1, TAM):
			r += "|" + self.tablero[0][i]
		for i in range(1, TAM):
			r += "\n   ------\n{}  ".format(i+1) + self.tablero[i][0]
			for j in range(1, TAM):
				r += "|" + self.tablero[i][j]
		return r
		
	def lleno(self):
		for fil in self.tablero:
			for elemento in fil:
				if (elemento == ' '):
					return False
		return True
	
	def hay3(self):
		for i in range(0, TAM):
			j = 1
			if (self.tablero[i][0] == ' '):
				seguir = False
			else:
				seguir = True
				jugador = self.tablero[i][0]
			while (j < TAM and seguir):
				if (self.tablero[i][j] != jugador):
					seguir = False
				j += 1
			if (seguir):
				self.victoria = jugador
				return True
		
		for j in range(0, TAM):
			i = 1
			if (self.tablero[0][j] == ' '):
				seguir = False
			else:
				seguir = True
				jugador = self.tablero[0][j]
			while (i < TAM and seguir):
				if (self.tablero[i][j] != jugador):
					seguir = False
				i += 1
			if (seguir):
				self.victoria = jugador
				return True
		if (self.tablero[1][1] == ' '):
			return False
		else:
			jugador = self.tablero[1][1]
			if (self.tablero[0][0] == self.tablero[2][2]
				and self.tablero[0][0] == jugador):
				self.victoria = jugador
				return True
			elif (self.tablero[0][2] == self.tablero[2][0]
				   and self.tablero[0][2] == jugador):
				self.victoria = jugador
				return True
			else:
				return False
		
		
	
	def jugada(self, letra, numero):
		if (letra < 'a' or letra > 'c' or numero < 1 or numero > 3
			or self.victoria != ' '):
			return False
		nCol = ord(letra) - ord('a')
		nFil = numero - 1
		if (self.tablero[nFil][nCol] != ' '):
			return False
		self.tablero[nFil][nCol] = self.jugador
		if (self.jugador == jugador1):
			self.jugador = jugador2
		else:
			self.jugador = jugador1
		self.hay3()
		return True

if (__name__ == "__main__"):
	partida = Partida3EnRaya()
	while (partida.victoria == ' ' and not(partida.lleno())):
		print(partida.str())
		caracter = input("Introduce letra: ")
		num = input("Introduce numero: ")
		partida.jugada(caracter, num)
	if (not(partida.lleno())):
		print("Victoria de la {}".format(partida.victoria))
	else:
		print("Empate")
