import string

import itertools
import array

class Board(object):
	def get_algebraic_board_map(self):
		board_file = list(map(chr,range(ord('a'),ord('h')+1)))
		board_rank = range(1,9)

		algebraic_board_map =  [ i for i in enumerate( [
									"%s%s" %(r,f) for r,f in 
									itertools.product(
										board_file,
										board_rank
										)]
									,start=0)]
		return algebraic_board_map

	def get_bijective_algebraic_board(self):
		"""
		Returns a dict with (key,value) pairs <- Square, Array Index; # Algebraic Notation
		                                      <- Array Index, Square; # Board Index
		Created in anticipation of reading a pgn file.
		"""
		ret = {}
		tup_list = self.get_algebraic_board_map()
		#ret = map((ret[i],ret[j] = lambda i,j : j,i), tup_list)
		for i,j in tup_list:
			ret[i], ret[j] = j, i
		return ret

	def get_bitboard(self):
		return array.array('B', [0 for i in xrange(1,65)])

	def __get_pieces(self):
		pieces = ['K','Q','N','R','B','P']
		piece_names = pieces + map(string.lower,pieces)
		return piece_names
	
	def get_pieces_bitboard_dict(self):
		"""
		Return a dictionary containing Bitboard for each of the Individual Piece.
		Used to denote current position of each piece.
		"""
		pieces = self.__get_pieces()
		pieces_board_dict = dict([(piece,self.get_bitboard()) for piece in pieces])
		return pieces_board_dict

#print Board().get_pieces_bitboard_dict()

