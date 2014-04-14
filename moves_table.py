from board import Board


bi_dict = Board().get_bijective_algebraic_board()

bounds_dict = {
		'file' : (ord('a'),ord('h')),
		'rank' : (1,8)
	}

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

class MovesBase(object):
	def __init__(self):
		"""
		Each Piece Class needs to initialize its method: piece_function
		"""
		self.cycle = ['forward', 'reverse']

	def within_limits(self, limit_dict, value):
		lower_limit = limit_dict[0]
		upper_limit = limit_dict[1]
		return lower_limit <= value <= upper_limit

	def get_bounds_dict(self):
		return bounds_dict

	def get_rank_file(self, square):
		"""
		square : a1 ==> rank : 1, file : a
		"""
		
		_rank = int(square[1])
		_file = square[0]
		return _rank, _file

	def get_square(self, _rank, _file):
		r_lims = bounds_dict['rank']
		f_lims = bounds_dict['file']
		r_bool = self.within_limits(r_lims, _rank)
		f_bool = self.within_limits(f_lims, ord(_file))
		if r_bool and f_bool:
			return "%s%s" %(_file, _rank)
		else:
			return False

	def next_moves(self, args_dict):
		if args_dict['direction'] == 'reverse':
				offset = -args_dict['offset']
		else:
			offset = +args_dict['offset']

		# [...]
		return self.piece_function(args_dict, offset)


	def set_moves(self, square, offset):
		"""
		# Forward: Rank:: 1->2, 2->3; File:: a->b, g->h
		# Reverse: Rank:: 2->1, 6->5; File:: b->a, f->e
		# self.next_moves should always return unnested list.
		
		"""
		_rank, _file = self.get_rank_file(square)

		ret = set()
		args_dict = {   
			'rank': _rank,
			'file': _file, 
			'offset': offset, 
			}
		for  direction in self.cycle:
			args_dict['direction'] = direction
			# [...]
			val = self.next_moves(args_dict)
			for i in val:
				ret.add(i)
		
		self.moves_list = ret

	def get_moves_list(self):
		return set(self.moves_list)


class RookMoves(MovesBase):
	def rook_moves(self, args_dict, offset):
		ret = []
		_rank, _file = args_dict['rank'], args_dict['file']
		
		n_rank =  _rank + offset
		r_sq = self.get_square(n_rank, _file)

		if r_sq:
			ret.append(r_sq)
		
		n_file = chr( ord(_file)+offset )
		f_sq = self.get_square(_rank, n_file)
		
		if f_sq:
			ret.append(f_sq)

		return ret

	piece_function = rook_moves
	
class BishopMoves(MovesBase):
	def bishop_moves(self, args_dict, offset):
		_rank, _file = args_dict['rank'], args_dict['file']

		n_rank = _rank + offset

		_file1 = chr(ord(_file) + offset)
		_file2 = chr(ord(_file) - offset )

		squares = [self.get_square(n_rank, _file1), self.get_square(n_rank, _file2)]

		return [ square for square in squares if square ]

	piece_function = bishop_moves
		
class QueenMoves(RookMoves, BishopMoves):
	def queen_moves(self, args_dict, offset):
		rook_moves = self.rook_moves(args_dict, offset)
		bishop_moves = self.bishop_moves(args_dict, offset)
		rook_moves.extend(bishop_moves)
		return rook_moves
		
	piece_function = queen_moves

class KingMoves(QueenMoves):
	def king_moves(self, args_dict, offset):
		offset = 1 if offset > 0 else -1
		king_moves = self.queen_moves(args_dict, offset)
		return king_moves

	piece_function = king_moves

class KnightMoves(RookMoves):
	def set_moves(self, square, offset):
		"""
		KnightMoves: The application of this method is overridden for Knight Class
		"""
		ret = set()

		offset = 2

		_rank, _file = self.get_rank_file(square)

		t_ranks  = [_rank +2, _rank -2]
		for r in t_ranks:
			sq = self.get_square(r, chr(ord(_file) + 1))
			if sq:
				ret.add(sq)
			sq = self.get_square(r, chr(ord(_file) -1 ))
			if sq:
				ret.add(sq)

		_f = ord(_file)
		
		t_files = [ chr(_f + 2), chr(_f - 2)]
		for f in t_files:
			sq = self.get_square(_rank +1, f )
			if sq:
				ret.add(sq)
			sq = self.get_square(_rank -1, f)
			if sq:
				ret.add(sq)
		self.moves_list = ret


class PawnMoves(MovesBase):
	def set_moves(self, square, offset=None):
		"""
		PawnMoves: The application of this method is overridden for Pawn Class
		"""
		_rank, _file = self.get_rank_file(square)
		ret = []
		

		if _rank == 2:
			# First Double Move.
			n_ranks = [3,4]
		else:
			n_ranks = [_rank + 1]

		for rank in n_ranks:
			sq = self.get_square(rank, _file)
			if sq:
				ret.append(sq)

		#En' Passant
		if _rank == 5:
			_f = ord(_file)
			_f = map(chr, [_f+1, _f-1])
			for f in _f:
				sq = self.get_square(6,f)
				if sq:
					ret.append(sq)
		self.moves_list = ret


	def set_attack_squares(self, square):
		"""
		PawnMoves:Needed because for movement squares != attack squares.
		"""
		self.set_moves(square)
		_rank, _file = self.get_rank_file(square)
		t_ranks = [ self.get_rank_file(sq) for sq in self.get_moves_list()]
		ranks = [ sq[0] for sq in t_ranks]
		
		t_file = ord(_file)
		n_files = map(chr, [t_file +1, t_file -1])

		ret = []
		for rank in ranks:
			for file_ in n_files:
				print rank, file_
				sq = self.get_square(rank, file_)

				if sq:
					ret.append(sq)
		return ret


#########################################################################

class MapAllPieceMoves(object):
	def __init__(self, piece):
		self.piece = piece
		self.set_board_moves()

	def set_board_moves(self):
		extent = range(1,8)
		squares = Board().get_algebraic_board_map()

		squares = [square[1] for square in squares]
		self.dict = {}

		for square in squares:
			self.dict[square] = []
			for offset in extent:
				self.piece.set_moves(square, offset)
				self.dict[square].extend(self.piece.get_moves_list())
			_moves = self.dict[square]
			self.dict[square] = list(set(_moves))

	def get_dict(self):
		return self.dict 

# r = MapAllPieceMoves(PawnMoves())
# sq = 1
# x = r.get_dict()

# y =  x['e5']
# # z = r.get_piece_ref().get_attack_squares('e2')
# y.sort()
# print y
# # print z
