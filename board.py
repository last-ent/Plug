import string

import itertools
import array

class Board(object):
	def __get_algebraic_board_map(self):
		board_rank = array.array('B', map(chr,range(ord('a'),ord('h')+1)))
		board_file = array.array('B', [ i for i in range(1,9)])

		algebraic_board_map =  [ i for i in enumerate( [
									"%s%s" %(r,f) for r,f in 
									itertools.product(
										board_rank,
										board_file
										)]
									,start=0)]
		return algebraic_board_map

	def get_bijective_algebraic_board(self):
		ret = {}
		tup_list = self.__get_algebraic_board_map()
		#ret = map((ret[i],ret[j] = lambda i,j : j,i), tup_list)
		for i,j in tup_list:
			ret[i], ret[j] = j, i
		return ret

	def __get_bitboard(self):
		return array.array('B', [0 for i in xrange(1,65)])

	def __get_pieces(self):
		pieces = ['K','Q','N','R','B','P']
		piece_names = pieces + map(string.lower,pieces)
		return piece_names
	
	def get_pieces_bitboard_dict(self):
		pieces = self.__get_pieces()
		pieces_board_dict = dict([(piece,self.__get_bitboard()) for piece in pieces])
		return pieces_board_dict

#print Board().get_pieces_bitboard_dict()