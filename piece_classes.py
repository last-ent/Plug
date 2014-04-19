import sqlite3 as sql
import string, itertools

con = sql.connect('moveDB.db')
cur = con.cursor()
ex = con.execute

from moves_generator.board import Board

#print dir(Board)

board_dict = Board().get_bijective_algebraic_board()
x = [i for i in board_dict.keys() if isinstance(i, str) and i[1]=='7']
x.sort()
print x 

piece_repr = {
	
	'White': {
		'King': 'K',
		'Queen': 'Q',
		'Knight' : 'N',
		'Bishop' : 'B',
		'Rook' : 'R',
		'Pawns' : 'P',

	},

	'Black': {
		'King': 'k',
		'Queen': 'q',
		'Knight' : 'n',
		'Bishop' : 'b',
		'Rook' : 'r',
		'Pawns' : 'p',
	},
}

class ChessBoard(object):
	squares = board_dict
	def __init__(self):
		pieces = {
			'White': {
				'King': ['e1'],
				'Queen': ['d1'],
				'Knight' : ['b1', 'g1'],
				'Bishop' : ['c1','f1'],
				'Rook' : ['a1', 'h1'],
				'Pawns' : ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],

			},
			'Black': {
				'King': ['e8'],
				'Queen': ['d8'],
				'Knight' : ['b8', 'g8'],
				'Bishop' : ['c8','f8'],
				'Rook' : ['a8', 'h8'],
				'Pawns' : ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
			},
		}



ChessBoard().read_fen()