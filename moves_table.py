from board import Board

bounds_dict = {
		'file' : (ord('a'),ord('h')),
		'rank' : (1,8)
	}

bi_dict = Board().get_bijective_algebraic_board()

def get_diagnose_dict():
	return  {
			'_rank' : _rank, '_file' : _file, 
			'n_rank' : n_rank, 'n_file' : n_file,
			'n_file_square': n_file_square, 
			'n_rank_square' : n_rank_square, 
			'op': op, 'key': key
			}
			#'r_bool' : rank_in_bounds, 'f_bool': file_in_bounds, 

def diagnose(dct):
	print dct
	while True:
		a = raw_input('<<< ') 
		if a == 'a':
			print dct[a]
		elif a =='q':
			break
		else:
			print dct

def check_moves(dct):
	ret = []
	keys = dct.keys()
	for key in keys:
		ret.extend(map(bi_dict.get, dct[key]))
	return ret

class MovesClass(object):
	def __init__(self):
		self.cycle = [
			('pos', 'forward'),
			('neg', 'reverse')
			]
		self.square_indices = Board().get_bitboard()
		self.square_notation = Board().get_bijective_algebraic_board()

	def within_limits(self,lower_limit, value, upper_limit):
		return lower_limit <= value <= upper_limit

	def get_board(self):
		return Board().get_bitboard()

	def get_bounds(self):
		return bounds_dict

	def get_rank_file(self, square):
		"""
		a1 -> rank : 1, file : a
		"""
		_rank = int(square[1])
		_file = square[0]
		return _rank, _file

	def get_square(self, _rank, _file):
		return "%s%s" %(_file, _rank)

	def next_rank_file(self, op, _rank, _file, offset):
		"""
		self.next_rank & self.next_file should always output unnested list.
		"""
		n_ranks = list(self.next_rank(op, _rank, offset))
		n_files = list(self.next_file(op, _file, offset))
		return n_ranks, n_files

	def set_moves(self, square, offset):
		"""
		Has been generalized.
		The logic needs to be re-written for methods: 
							next_file, 
							next_rank, 
							change_square
		for each of the pieces.
		"""
		sqr_algebraic = self.square_notation[square]

		_rank, _file = self.get_rank_file(sqr_algebraic)

		ret = {}
		
		for op,key in self.cycle:
			n_ranks, n_files = self.next_rank_file(op, _rank, _file, offset)

			## NEEDS REFACTORING
			ret[key] =[]
			for n_rank in n_ranks:
				if n_rank:
					n_rank_square = self.get_square(n_rank, _file) 
					ret[key].append(self.square_notation[n_rank_square])

			for n_file in n_files:
				if n_file:
					n_file_square = self.get_square(_rank, n_file) 
					ret[key].append(self.square_notation[n_file_square])

		self.move_dict = ret	
			# diagnose( {'_rank' : _rank, '_file' : _file, 'n_rank' : n_rank, 'n_file' : n_file,
			# 'n_file_square': n_file_square, 'n_rank_square' : n_rank_square, 'op': op, 'key': key}) #'r_bool' : rank_in_bounds, 'f_bool': file_in_bounds, 

	def get_flat_list(self):
		dct = self.move_dict
		ret = []
		keys = dct.keys()
		for key in keys:
			ret.extend(map(bi_dict.get, dct[key]))
		return ret

	def check_rof(self, rank_or_file, r_o_f):
			return ord(rank_or_file) if r_o_f == 'file' else rank_or_file


class RookMoves(MovesClass):
	def change_square(self, op, r_o_f, rank_or_file, offset):
		"""
		Changes value of rank_or_file in positive or negative direction by offset.
		"""
		## Weird quirk, below line won't work. While in interpreter it works.
		#return check_rof() +offset if op=='pos' else -offset

		board_val = self.check_rof(rank_or_file, r_o_f) 
		mod_val =  +offset if op=='pos' else -offset
		
		return board_val + mod_val
		 
	def next_rank(self, op, _rank, offset):
		n_rank =  self.change_square(op,'rank', _rank, offset)
		r_lims = bounds_dict['rank']
		n_rank = n_rank if self.within_limits(r_lims[0],n_rank,r_lims[1]) else False
		return [n_rank]

	def next_file(self, op, _file, offset):
		f_lims = bounds_dict['file']
		n_file = self.change_square(op, 'file', _file, offset)		
		n_file =  chr(n_file) if self.within_limits(f_lims[0],n_file,f_lims[1]) else False
		return [n_file]

class BishopMoves(MovesClass):
	def change_square(self, op, _rank, _file, offset):
		"""
		Changes value of rank_or_file in positive or negative direction by offset.
		op --> decides Forward or Backward.
		"""
		#board_val = self.check_rof(rank_or_file, r_o_f) 
		#mod_val =  +offset if op=='pos' else -offset
				
		r_offset = offset
		if op =='rank': # Reverse
			r_offset *= -1

		n_rank = _rank + offset
		n_files = [  ]

		return board_val + mod_val
		 
	def next_rank(self, op, _rank, _file, offset):
		"""
		For a Bishop, Rank == Reverse & File == Forward
		"""
		n_rank =  self.change_square(op,'rank', _rank, offset)
		r_lims = bounds_dict['rank']
		n_rank = n_rank if self.within_limits(r_lims[0],n_rank,r_lims[1]) else False
		return n_rank

	def next_file(self, op, _rank, _file, offset):
		"""
		For a Bishop, Rank == Reverse & File == Forward
		"""
		f_lims = bounds_dict['file']
		n_file = self.change_square('file', _file, offset)		
		n_file =  chr(n_file) if self.within_limits(f_lims[0],n_file,f_lims[1]) else False
		return [n_file]

	def next_rank_file(self, op, _rank, _file, offset):
		"""
		self.next_rank & self.next_file should always output unnested list.
		"""
		n_ranks = list(self.next_rank(op, _rank, _file, offset))
		n_files = list(self.next_file(op, _rank, _file, offset))
		return n_ranks, n_files



#########################################################################

class MapAllPieceMoves(object):
	def __init__(self, piece):
		self.Piece = piece
		self.set_board_moves()

	def set_board_moves(self):
		extent = range(1,8)
		squares = xrange(0,64)
		self.dict = {}

		for square in squares:
			self.dict[square] = []
			for offset in extent:
				self.Piece.set_moves(square, offset)
				self.dict[square].extend(self.Piece.get_flat_list())

	def get_dict(self):
		return self.dict 



r = MapAllPieceMoves(RookMoves())
sq = 1
x = r.get_dict()[sq]
x.sort()
print "%s -> %s" %(sq,x)


# sq = 35
# by = 3
# print "%s[+-%s] -> %s" %(bi_dict[sq], by, check_moves(r.get_move(sq, by)))


# lat_border = "-----------------------------"*2 
# lon_border = '|'
# s = " ... | "*8

# row = "\n||%s|" %(s)[:-1]
# print lat_border, row*8, la
