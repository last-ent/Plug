from board import Board
#from operator

bounds_dict = {
		'file' : (ord('a'),ord('h')),
		'rank' : (1,8)
	}

# def check_bounds(indices,index):
# 		return if index in indices


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


class RookMoves(object):
	def __init__(self):
		self.square_indices = Board().get_bitboard()
		self.square_notation = Board().get_bijective_algebraic_board()
		self.cycle = [
			('pos', 'forward'),
			('neg', 'reverse')
			]

	def within_limits(self,lower_limit, value, upper_limit):
		return lower_limit <= value <= upper_limit

	def get_board(self):
		return Board().get_bitboard()

	def get_bounds(self):
		return bounds_dict

	def change_square(self, op, rank_or_file, offset):
		"""
		Changes value of rank_or_file in positive or negative direction by offset.
		"""
		return ord(rank_or_file) +offset if op == 'pos' else -offset
		
	def next_rank(self, op, rank_or_file, offset):
		n_rank =  self.change_square(op, rank_or_file, offset)
		return n_rank if self.within_limits(0,n_rank,8) else False

	def next_file(self, op, rank, offset):
		n_file = self.next_rank(op,rank,offset)
		return chr(n_file) if self.within_limits(0,n_file,256) else False

	def get_rank_file(self, square):
		"""
		a1 -> rank : 1, file : a
		"""
		_rank = square[1]
		_file = square[0]
		return _rank, _file

	def get_square(self, _rank, _file):
		return "%s%s" %(_file, _rank)

	def check_bounds(self, _rank, _file):
		r_lims = bounds_dict['rank']
		f_lims = bounds_dict['file']

		## Between Limits - Lower Limit <= Value <= Upper Limit
		r_bool = self.within_limits(r_lims[0], _rank, r_lims[1])
		f_bool = self.within_limits(f_lims[0], _file, f_lims[1])
		
		return r_bool, f_bool

	def get_move(self, square, offset):
		"""
		This rule is unique to each piece.
		"""
		sqr_algebraic = self.square_notation[square]

		_rank, _file = self.get_rank_file(sqr_algebraic)

		ret = {}
		
		for op,key in self.cycle:
			n_rank = self.next_rank(op, _rank, offset)
			
			n_file = self.next_file(op, _file, offset)
			
			rank_in_bounds, file_in_bounds = self.check_bounds(n_rank, n_file)

			## When moving along Rank - Algebraic
			n_rank_square = self.get_square(n_rank, _file) 
			#print n_rank_square, "n_rank"

			## When moving along File - Algebraic
			#print _rank, "_rank"
			#print chr(n_file), "n_file"
			n_file_square = self.get_square(_rank, n_file) 
			#print n_file_square, "file"

			## Given Algebraic Notation, get bitboard indices
			ret[key] =[]
			if rank_in_bounds:
				ret[key].append(self.square_notation[n_rank_square])

			if file_in_bounds:
				ret[key].append(self.square_notation[n_file_square])

			diagnose( {'r_bool' : rank_in_bounds, 'f_bool': file_in_bounds, '_rank' : _rank, '_file' : _file, 'n_rank' : n_rank, 'n_file' : n_file,
			'n_file_square': n_file_square, 'n_rank_square' : n_rank_square})

		return ret

r = RookMoves()
print r.get_move(0, 1)
