
from .moves_table import *


##############################################################################
##############################################################################

import sqlite3 as sql
import sys

con = sql.connect('moveDB.db')

with con:
	cur = con.cursor()
	ex = cur.execute

	def create_table():
		cur.execute("""CREATE TABLE move_table(piece TEXT, move TEXT, attack TEXT,  square TEXT, to_01 TEXT ,  to_02 TEXT ,  
			to_03 TEXT ,  to_04 TEXT ,  to_05 TEXT ,  to_06 TEXT , 
			to_07 TEXT ,  to_08 TEXT ,  to_09 TEXT ,  to_10 TEXT ,  
			to_11 TEXT ,  to_12 TEXT ,  to_13 TEXT ,  to_14 TEXT ,  
			to_15 TEXT ,  to_16 TEXT ,  to_17 TEXT ,  to_18 TEXT ,  
			to_19 TEXT ,  to_20 TEXT ,  to_21 TEXT ,  to_22 TEXT ,  
			to_23 TEXT ,  to_24 TEXT ,  to_25 TEXT ,  to_26 TEXT ,  
			to_27 TEXT ,  to_28 TEXT ,  to_29 TEXT ,  to_30 TEXT)""")


	def insert_piece_moves():
		pieces = zip(['Knight', 'Rook', 'Bishop', 'Queen', 'King'], [KnightMoves, RookMoves, BishopMoves, QueenMoves, KingMoves])
		
		for pNm, pCl in pieces:
			pieceObj = MapAllPieceMoves(pCl())
			piece_dict =  pieceObj.get_dict()
			move_set = piece_dict.items()
			for moves in move_set:
				from_ = moves[0]
				move_lst = moves[1]

				lst = [pNm, 'yes','yes']
				lst.append(from_)
				lst.extend(move_lst)
				val = 34 - len(lst)
				lst.extend([None]*val)
							
				cur.execute('''INSERT INTO move_table VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
					?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', lst)

	def insert_pawn_moves():
		"""
		 moves_list.keys() -> ['attacks', 'moves', 'colour']
		 moves_list[key].values() -> list(moves)
		 moves_list['colour'] -> 'Black' or 'White'
		"""
		
		pawn = MapPawnMoves()
		lst = ['White', 'Black']
		for c in lst:
			pawn.set_colour(c)
			pawn.set_board_moves()
			pd = pawn.get_dict()
			move_set = pd.items()
			for moves in move_set:
				from_ = moves[0]
				ls_tup = ("%s Pawn"%c, 'yes','no', from_)
				mv_move_list = list(ls_tup)
				mv_move_list.extend(moves[1]['moves'])

				ls_tup = ("%s Pawn"%c, 'no', 'yes', from_)
				atk_move_list = list(ls_tup)
				atk_move_list.extend(moves[1]['attacks'])

				val = 34 - len(mv_move_list)
				mv_move_list.extend([None]*val)

				val = 34 - len(atk_move_list)
				atk_move_list.extend([None]*val)

				lsts = [mv_move_list, atk_move_list]
				for lst in lsts:
					cur.execute('''INSERT INTO move_table VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
						?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', lst)
	# #create_table()
	# insert_pawn_moves()
	# insert_piece_moves()

#	print ex('Select Count(*) from move_table ').fetchall()