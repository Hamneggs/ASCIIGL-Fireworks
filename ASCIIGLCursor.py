"""
	This is a cursor that can be used within ASCIIGL rendering surfaces.
	It maintains it's location, and the character that represents it on 
	screen.
"""
class ASCIIGLCursor(object):
	
	"""
		Initializes the ASCIIGLCursor to have an x and y location, as well
		as a representative character.
		PARAMETERS:
		x:			The cursor's initial X location.
		y:			The cursor's initial Y location.
		character:	The character that will represent the cursor on screen.
	"""
	def __init__(self, x, y, character):
		self.x = x
		self.y = y
		self.char = character
	
	"""
		Moves the cursor by the vector <changeX, changeY>
		PARAMETERS:
		changeX: 	The amount by which to change the cursor's X location.
		changeY: 	The amount by which to change the cursor's Y location.
	"""
	def moveCursorBy(self, changeX, changeY):
		self.x += changeX
		self.y += changeY
	
	"""
		Sets the cursor's location to (newX, newY)
		PARAMETERS:
		newX:	The cursor's new X location.
		newY:	The cursor's new Y location.
	"""
	def setCursorLocation(self, newX, newY):
		self.x = newX
		self.y = newY
	
	"""
		Changes the cursor's representative character.
		PARAMETERS:
		newCharacter:	The new character to represent the character.
	"""
	def setCharacter(self, newCharacter):
		self.char = char
	
	"""
		Returns a tuple containing the x and y locations
		of the cursor.
		RETURNS:
		( x , y )
	"""
	def getCursorLocation(self):
		return (self.x, self.y)
	
	"""
		Draws the cursor onto the given ASCIIGL 
		rendering surface.
		PARAMETERS:
		ASCIIGLReference: 	The ASCIIGL rendering surface
							to draw the cursor on.
	"""
	def drawCursor(self, ASCIIGLReference):
		ASCIIGLReference.drawCharacter(x, y, char)
		