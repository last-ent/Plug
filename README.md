# Plug - *Python Chess Engine* #


## Introduction ##

This is an attempt to create a Chess Engine in Python. The main
intention is to understand various steps involved to create a chess
engine.

There are two main sources for information on  Chess Programming:

* [GameDev.net's Chess Programming](http://www.gamedev.net/page/resources/_/technical/artificial-intelligence/chess-programming-part-i-getting-started-r1014)

* [Chess Programming Wiki](chessprograming.wikispaces.com).

Chess Programming Wiki is quite elaborate and it is the ultimate
resource. However when starting (and on a tight schedule) it isn't
ideal. The article on Game Dev forums is much better. Hence we shall be
starting with Game Dev, once solid understanding has been reached - We
can go back to look for cracks in our understanding & program, and
improve upon them using CP Wiki.

## Milestones ##

**Plug** will be designed in progresive steps. Each step will depend on
the code from previous step. Below are the milestones -

### BitBoard ###

This section deals with creating a Bitboard and related data.
Update: It seems that currently we might not need BitBoard representation for Python.
### BitBoard Representation ###

##### 64 Square Board

We are done with this part. Details will follow later.

##### Main Chess Board Representation

Done.

##### Individual Piece Location Bitboard

Done with this part.

##### Possible Piece Move per Square Bitboard

The aim of this section is to have a set of pre-calculated moves for
each of the pieces at each of the square. This will help us to hasten
possible move list later in the program. A common interface can be
expected for each class:


```python
#!python


class MovesBase

class RookMoves (MovesBase)
class BishopMoves(MovesBase)
class QueenMoves(RookMoves, BishopMoves)
class KingMoves (RookMoves, BishopMoves)
class KnightMoves(MovesBase)

class PawnMoves(MovesBase)
  """
  While This class inherits from MovesBase, it has completely different method calls to retrieve the data.
  """
```

In order to generate the complete move list, MapClasses have been created:


```python
#!python

class MapAllPieceMoves
  """
  Applicable for Knight, Bishop, Rook, Queen, Knight
  """

class MapPawnMoves
  """
  Applicable for Pawn - Normal Move, Double Move, For Black & White, En' Passant
  """


```


The list of moves will be generated for each piece in (supposed)
increased complexity:

**Rook**

Rook has to move in straight lines along Rank & File as well as Back & Forth. 
Completed.

**Bishop**

Bishop moves along diagonals.
Completed.

**King**

King is a child of Queen within extent limited to single square.
Completed.

**Queen**

Queen is child of Rook & Bishop.
Completed.

**Knight**

Knight had to be written in a different fashion. Making it a modification of Rook :: Rook +- file/rank, wasn't effective.
Complete.

**Pawn**

Pawn was the most complex one to write. It has the maximum rules. Separate tables for Attack and Movement. Pawn Promotion still hasn't been written. Expectation is that it will be handled by the engine.
Complete.

##### Move Table

All of the classes created above have been mapped into an sqlite3 db called **moveDB.db**.

Data is stored as follows:
**Piece | Move | Attack | Square | to_01 | to_02 | ... | to_30**

* Piece - [King, Queen, Rook, Bishop, Knight]. For Pawn, "%s Pawn" %(White or Black)
* Move - Determines if moves are used for Movement. 
* Attack - Determines if moves are used for Attack. Required for Pawn.
* Square - Square from which the piece needs to move.
* to_01 ... to_30 - Destination Squares. Maximum number of squares covered are by a Queen of 27 squares. On safe side, 30 squares are allocated.

##### Hash Keys for Chess Boards?

An easy way to implement Hash Keys for Chess Boards is to use FEN diagrams, or atleast a subset. 

A FEN diagram follows following format:

rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

rnbqkbnr  
pppppppp  
8        <-- Numbers represent continuous spaces before a piece is encountered.  
8  
8  
8  
PPPPPPPP  
RNBQKBNR  


**Chessboard Representation** 
```
#!plain text

_________________________________
| r | n | b | q | k | b | n | r |
_________________________________
| p | p | p | p | p | p | p | p |
_________________________________
|   |   |   |   |   |   |   |   |
_________________________________
|   |   |   |   |   |   |   |   |
_________________________________
|   |   |   |   |   |   |   |   |
_________________________________
|   |   |   |   |   |   |   |   |
_________________________________
| P | P | P | P | P | P | P | P |
_________________________________
| R | N | B | Q | K | B | N | R |
_________________________________

Logic for above FEN Representation has been implemented in module **console_board_repr.py**

```

**console_board_repr.py** has two main functions:

* fen_to_array: Converts a given FEN position into an 8x8 array board.
* console_board: Which takes a FEN position and prints an 8x8 chessboard in console.

Done.

##### FEN -> Algebraic Board & Algebraic Board -> FEN.
*Next we need to create two functions that help us to easily transition between FEN and algebraic notation. *

FEN To Algebraic & Algerbaic to FEN has been implemented. The whole interface and logic feels inefficient and messy. It might have to be re-written later on.

##### Influence Graph

Influense Graph shows all the squares a piece can cover from current square.  
This will be used to calculate the next two sections. **Check, Castle** & **En'Passant, Pawn Promotion**.


##### Check, Castle


##### En'Passant, Pawn Promotion


##### History Tables

Will be cofigured much later.

##### Transposition Tables

Might be applied later if performance is too low.



### Data Structures

More Data Structures might be required later on.

### Move Generation

### Basic Search

### Advanced Search

### Evaluation Functions
