
def to_int(i):
	try:
		i = int(i)
	except:
		pass
	return i

def fen_to_array(s):
	ret = [
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
		]

	s = s.split("/")
	row_indx = 0
	import pprint
	while row_indx < 8:
		line_indx = 0
		row = s[row_indx]
		row =  list(row)

		while line_indx < 8:
			sq = row[line_indx]

			sq = to_int(sq)
			if isinstance(sq, int):
				line_indx += sq
			else:
				ret[row_indx][line_indx] = sq
				line_indx +=1
		row_indx+=1
	
	#pprint.pprint(ret)
	return ret

def console_board(s):	
	r = "_________________________________"
	#r = '-'*len(_r)
	print r
	board = fen_to_array(s)
	_sq = "| %s "
	f = ''
	for row in board:
		#print i
		_f = ''
		for sq in row:
			_f+= _sq %sq
			
		f+=_f+"|\n"+r+"\n"
	print f
if __name__ == '__main__':
	s = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
	console_board(s)