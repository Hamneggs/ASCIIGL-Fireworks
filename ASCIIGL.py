"""
	This module is a basic ASCII graphics library. Here is a small screenshot:
	
	a-------------------b
	|                   |
	| *                 |
	|                   |
	|                   |
	|                   |
	|    G              |
	|                   |
	|                   |
	|                   |
	c-------------------d
	
	"a" represents location (0, 0).
	"b" represents location (20, 0).
	"c" represents location (0, 10).
	"d" represents location (20, 10).
	The asterik is at location(2, 2).
	The "G" is at location (5, 6).
	
	---COORDINATE SYSTEM---
	That's right. All locations are in caret-space. This does not mean
	You can't have floating point location values, however. But at draw
	time, these sub-caret locations are floored (or ceiled, if the 
	flattening mode is set so).
	Nonetheless, remember that your new pixels are enormous.
	The size of the rendering surface is defined at initialization.
	
	---FRAMEBUFFER AND RENDERING---
	The framebuffer is a list of characters. When you issue a drawing command,
	this list is modified. It is reset to whatever character you've set the
	clear character and color to be whenever you call clear(). 
	*By default, it is a space whatever color your console is.*
	The actual drawing of the graphics is essentially double-buffered.
	When required to draw the screen to the console, the framebuffer list
	is copied down into a string juxtaposed with newlines at each "scanline".
	This string is then traditionally printed to the screen.
	
	---TIPS AND TRICKS---
	Console clear commands seem to be really slow. So during continuous
	drawing, you'll probably experience a nice little flicker. Therefore
	I recommend only redrawing the scene when there has been a change,
	e.g. a tetris block moved down or something.
	Using a COLOR-MODE other than PRESERVE_COLOR will drastically slow down
	rendering speed. Tearing will happen and frame-times will increase, slowing
	any animation linearly with each change to the color. So only use it if
	you're a prick.
	COLOR-MODES do not affect textures.
	Also, it is recommended that you capture keyboard exits in your program
	so that you can issue one final clear screen call, so you don't have any
	remnants of the final rendered ASCIIGL frame in your console.
	
	---TL;DR HOW TO USE---
	Initialize an instance of the ASCIIGL class. Set it up how you want
	by calling the various setters and getters USING THE APPROPRIATE TERMS
	FROM ASCIIGLConstants. 
	Then for every frame you want to render, first you perform your draw-calls,
	then call the blitting method.
	
	---TODO---
	More drawing functions.
    BETTER COLOR!
	WHY THE HELL IS THIS SO SLOW?
	
"""

#We import ASCIIGLConstants so we can see the various options
#available for customizing the ASCIIGL experience.
import ASCIIGLConstants

#We import ASCIIGLTexture so that we can draw textured stuff.
import ASCIIGLTexture

#Hey, we need to flatten things somehow. Might as well do it well.
import math

#This is done almost solely so that we can clear the screen.
import os

import string

class ASCIIGL(object):
	
	
	"""
		Initializes the ASCIIGL renderer.
		Parameters:
		sizeX:	The X size of the rendering surface. If this is bigger than your console window,
				you're fucked. 
		sizeY:	The Y size of the rendering surface.
	"""
	def __init__(self, sizeX, sizeY):
	
		"""
			We store the size of the surface for reference.
		"""
		self.sizeX = sizeX
		self.sizeY = sizeY
		
		"""
			The list of characters that make up the framebuffer.
		"""
		self.frameBuffer = []
		
		#Create a swapbuffer string.
		self.swapString = ""
		
		for i in range(sizeX * sizeY):
			self.frameBuffer.append(ASCIIGLConstants.clearCharacter)
						
	"""
		Changes the clear character, by changing the
		appropriate value in ASCIIGLConstants. 

	"""
	def setClearChar(self, clearChar):
		ASCIIGLConstants.clearCharacter = clearChar[0]
		
	"""
		Changes the flattening mode, by changing the
		appropriate value in ASCIIGLConstants. Again,
		it is highly recommended that you use a member
		defined in ASCIIGLConstants.
		
		VALUES from ASCIIGLConstants:
		FLAT_FLOOR:	Floors location values.
		FLAT_CEIL:	Ceils location values.
	"""
	def setFlatMode(self, mode):
		ASCIIGLConstants.flatMode = mode
	
	"""
		When drawing a rectangle or other shape with corners,
		There is a decision one has to make: Should the corners
		be of the horizontal border, or the vertical border?
		This is how you make that decision. 
		AGAIN, USE ASCIIGLConstants.
		
		VALUES from ASCIIGLConstants:
		FAVOR_VERT:		Favors the vertical border.
		FAVOR_HORIZ:	Favors the horizontal border.
	"""
	def setCornerMode(self, mode):
		ASCIIGLConstants.borderCornerMode = mode
	
	"""
		Resets text appearance.
	"""
	def resetAppearance(self):
		ASCIIGLConstants.bgColor   = ASCIIGLConstants.Back.RESET
		ASCIIGLConstants.textColor = ASCIIGLConstants.Fore.RESET
		ASCIIGLConstants.textStyle = ASCIIGLConstants.Style.RESET_ALL
		#Print the character into the console so that the ANSI codes are recognized and applied.
		print(ASCIIGLConstants.bgColor+ASCIIGLConstants.textColor+ASCIIGLConstants.textStyle+" ")
	
	"""
		An ASCIIGL Texture contains four components
		per texel, a background color, a foreground/character
		color, a character style, and the character itself.
		But you might not want to use all of these components
		all at once. Hence we have the texture mode.
		
		VALUES from ASCIIGLConstants:
		USE_TEX_ALL:		When sampling the texture, we grab each texel's style, 
							background color, forground color, and character.		
		USE_TEX_FORE_BACK:	Use the foreground/character color, character (obviously),
							and the background color.
		USE_TEX_BACK:		Use only the background color.	
		USE_TEX_STYLE:		Use only the character modified by the texel's style.
		USE_TEX_FORE_STYLE:	Use the foreground character modified by color and style.
		USE_TEX_NONE:		Turn off texture usage.
	"""
	def setTextureMode(self, mode):
		ASCIIGLConstants.textureMode = mode
	
	"""
		When using a texture, you might not want to replace existing pixels
		with texels from the texture. Rather, you might think to yourself,
		"I want to apply the appearance modifiers of the texel to the
		pixels already there!"
		That's where the texture blending mode comes into play.
		Note, this is intended to be used in conjunction with the more general
		texture mode.
		
		VALUES from ASCIIGLConstants:
		TEX_MULTIPLY: 	Only uses the appearance modifiers from the texture.
						Any texel that is queried will have a character of ''.
		TEX_ADDITIVE:	All elements of the texture are used.
	"""
	def setTextureBlendingMode(self, mode):
		ASCIIGLConstants.texBlendingMode = mode
	
	"""
		When drawing a shape, we must decide what fill mode
		to use.
		
		VALUES from ASCIIGLConstants:
		FILL_AND_BORDER: 	Draw both the fill and border.
		FILL_ONLY:			Draw only the fill.
		BORDER_ONLY:		Draw only the border.
		
		Of course, you could just change the parameters to whatever 
		you're drawing.
	"""
	def setFillMode(self, mode):
		ASCIIGLConstants.shapeFillMode = mode
	
	"""
		Sets the color mode of this ASCIIGL surface.
		
		VALUES from ASCIIGLConstants:
		EDIT_COLOR: 			Edit only the color of the text and 
								background.
		EDIT_COLOR_AND_STYLE:	Edit the color of the text and background,
								as well as the text's style.
		PRESERVE_COLOR:			Don't attempt to do anything with 
								the text's appearance.
	"""	
	def setColorMode(self, mode):
		ASCIIGLConstants.colorMode = mode
	
	"""
		Sets the text's color.
		Use ASCIIGLConstants.Fore, which is 
		inherited from Colorama.
	"""
	def setTextColor(self, coloramaForeColor):
		ASCIIGLConstants.textColor = coloramaForeColor
	
	"""
		Sets the text's style.
		Use ASCIIGLConstants.Style, which is 
		inherited from Colorama.
	"""
	def setTextStyle(self, coloramaTextStyle):
		ASCIIGLConstants.textStyle = coloramaTextStyle
	
	"""
		Sets the background color.
		Use ASCIIGLConstants.Back, which is 
		inherited from Colorama.
	"""
	def setBGColor(self, coloramaBackColor):
		ASCIIGLConstants.bgColor = coloramaBackColor
		
	"""
		Clears the screen so a new frame can be rendered and drawn.
		This, however, does not clear the framebuffer.
	"""
	def clearScreen(self):
		if os.name == 'nt': 
			os.system('cls')
		else: 
			os.system('clear')
	
	"""
		Resets the framebuffer to a fresh state, filled with the
		clearCharacter defined in ASCIIGLConstants.
	"""
	def clearFramebuffer(self):
		self.frameBuffer = []
		for i in range(self.sizeX * self.sizeY):
			self.frameBuffer.append(ASCIIGLConstants.clearCharacter)
	
	"""
		Pushes the given value out to an integer value based on the
		method defined in ASCIIGLConstants.
	"""
	def pushToInt(self, value):
		if ASCIIGLConstants.flatMode == ASCIIGLConstants.FLAT_FLOOR:
			value = math.floor(value)
		else:
			value = math.ceil(value)
		return int(value)
		
	"""
		Draws a rectangle, first drawing it's inside, then 
		the border.
		This is a much more tenuous task than the 
		textured rectangle.
		In fact, only use this rectangle when drawing GUIs.
		It's really intense, but also feature rich.
		
		HOW IT WORKS:
		Just read the damn code.
		
		PARAMETERS:
		x:					The X location of the rectangle.
		y:  				The Y location of the rectangle.
		sx:					The X size of the rectangle.
		sy: 				The Y size of the rectangle.
		fillChar:			The character that serves to fill the rectangle.
		horizBorderChar:	The horizontal border character.		
	"""
	def rect(self, x, y, sx, sy, fillChar, horizBorderChar, vertBorderChar):
		
		#For every character in the rectangle:
		for i in range(x, x+sx, 1):
			for k in range(y, y+sy, 1):
				#Take care of the top and bottom rows, which are part of the border:
				#That is, if we are supposed to draw the border.
				if ASCIIGLConstants.shapeFillMode == ASCIIGLConstants.FILL_AND_BORDER or ASCIIGLConstants.shapeFillMode == ASCIIGLConstants.BORDER_ONLY:
					if k == y or k == y+sy-1:
						self.character(i, k, horizBorderChar)
						#If we are favoring the vertical border at the corner, overwrite the
						#corners with the vertical border character.
						if ASCIIGLConstants.borderCornerMode == ASCIIGLConstants.FAVOR_VERT:
							if i == x or i == x+sx-1:
								self.character(i, k, vertBorderChar)
				#For the rows in the middle:
					else:
						#If the current location is on the border, we draw the border character.
						#Here we must also test the shape-fill-mode.
						if ASCIIGLConstants.shapeFillMode == ASCIIGLConstants.FILL_AND_BORDER or ASCIIGLConstants.shapeFillMode == ASCIIGLConstants.BORDER_ONLY:
							if i == x or i == x+sx-1:
								self.character(i, k, vertBorderChar)
						#Otherwise, we draw the fill character.
							else:
								if ASCIIGLConstants.shapeFillMode == ASCIIGLConstants.FILL_AND_BORDER or ASCIIGLConstants.shapeFillMode == ASCIIGLConstants.FILL_ONLY:
									self.character(i, k, fillChar)
									
	def simpleRect(self, x, y, sx, sy, borderChar, fillChar):
		
		for i in range(x, x+sx, 1):
			for k in range(y, y+sy, 1):
				if k == y or k == y+sy-1 or i == x or i == x+sx-1:
					self.applyTexel(i, k, borderChar)
				else:
					self.applyTexel(i, k, fillChar)
					
				
	"""
		Draws a textured rectangle.
		
		HOW IT WORKS:
		Goes through and queries for texels per-fragment.
		
		PARAMETERS:
		x:	The X position of the top right corner of the rectangle.
		y:	The Y position of the top right corner of the rectangle.
		sx: The X size of the rectangle.
		sy: The Y size of the rectangle.
		tx: The starting texel X coordinate.
		ty: The starting texel Y coordinate.
	"""
	def texRect(self, x, y, sx, sy, tx, ty, texture):
		
		#For every pixel in the area of the rectangle...
		for i in range(x, x+sx, 1):
			for k in range(y, y+sy, 1):
				#This is where things are changed up. We get a texel, and then apply it.
				self.applyTexel(i, k, texture.getTexel(tx+i, ty+k))
	
	"""
		Draws a textured line.
		
		HOW IT WORKS:
		Just like a standard line, except for each character in the line,
		we use the character stored in the locaiton of the the line.
		
		PARAMETERS:
		startX:		The starting X position of the line.
		startY:		The starting Y position of the line.
		endX:		The finishing X position of the line.
		endY:		The finishing Y position of the line.
		texAnchorX:	The texel X location in the ASCIIGLTexture
					that corresponds with the starting 
					location of the line.
		texAnchorY:	The texel Y location in the ASCIIGLTexture
					that corresponds with the starting 
					location of the line.
		texture:	The ASCIIGLTexture to sample texels from.
	"""
	def texLine(self, startX, startY, endX, endY, texAnchorX, texAnchorY, texture):
	
		#Normalize all parameters to integer values.
		startX = self.pushToInt(startX)
		startY = self.pushToInt(startY)
		endX = self.pushToInt(endX)
		endY = self.pushToInt(endY)
	
		#Get the X distance of the line.
		xLength = endX - startX
		
		#Get the Y distance of the line.
		yLength = endY - startY
		
		#Get the X increment.
		try:
			xIncrement = xLength/yLength
		except:
			xIncrement = 0
		
		#This is where things are changed up. We get a texel, and then apply it.
		for i in range (startY, endY, 1):
			self.applyTexel(startX + ( (i-startY)*xIncrement), i, texture.getTexel(((i-startY)*xIncrement)-startX+texAnchorX, i-startY+texAnchorY))
		
		
	"""
		Draws a single instance of the specified character at the
		location (x, y).
		HOW IT WORKS:
		We simply map the 2-D location given to the method
		to a 1-D array. That gives us the index of the 
		framebuffer we need to edit.
		Culling duties are also performed here. You know what? That's awesome.
		Why? Because essentially we are doing per-fragment culling. 
		
		HOW IT WORKS:
		First, we normalize the location, 
		then map our 2-D location to our 1-D framebuffer.
		Next we perform culling duties, 
		and finally we edit the framebuffer.
		Note, though, that we don't edit the framebuffer if the
		character is empty, none, or a carriage-moving escape character.
		This allows for somewhat of transparency.
		
		PARAMETERS:
		x:			The X location of the character.
		y:			The Y location of the character.
		character:	The character itself.
		
		RETURNS:
		Whether or not the character was culled.
	"""
	def character(self, x, y, character):
	
		#Normalize the location.
		x = self.pushToInt(x)
		y = self.pushToInt(y)
		
		#Map down the location into 1-D.
		index = int( ((y*self.sizeX) + x) % (self.sizeY*self.sizeX) )
		
		#These if statements perform culling duties.
		if(ASCIIGLConstants.cullMode == ASCIIGLConstants.CULL):
			if (x < 0 or x > self.sizeX):
				return True
			elif (y < 0 or y > self.sizeY):
				return True
		elif(ASCIIGLConstants.cullMode == ASCIIGLConstants.WRAP):
			index = index % (self.sizeY*self.sizeX)
		else:
			index = index % (self.sizeY*self.sizeX)
		
		#If the character is a nothing character, or a special character, we simply don't do
		#anything. 
		#character = str(character)
		#if (not character == "") or (not character == None) or (not character == "\n") or (not character == "\t") or (not character == "\r"):
			
		#Based on the appearance modification attributes defined in ASCIIGLConstants, we append color info to the pixel string.
		if(ASCIIGLConstants.colorMode == ASCIIGLConstants.EDIT_COLOR):
			self.frameBuffer[int(index)] = ASCIIGLConstants.bgColor + ASCIIGLConstants.textColor + character
		elif(ASCIIGLConstants.colorMode == ASCIIGLConstants.EDIT_COLOR_AND_STYLE):
			self.frameBuffer[int(index)] = ASCIIGLConstants.bgColor + ASCIIGLConstants.textColor + ASCIIGLConstants.textStyle + character
		else:
			self.frameBuffer[int(index)] = character
		
		#Finally, since the pixel was not culled, we return false.
		return False
	
	"""
		Applies a texel to a pixel in the framebuffer.
		
		HOW IT WORKS:
		First we normalize the location, then we mix down
		our location to 1-D.
		Next, based on the culling settings, we cull the texel.
		If it was not culled, we insert it into the framebuffer
		based on the blending mode.
		Note that we didn't do all the special character checks.
		That's because textures are formatted, and won't contain
		those.
		
		PARAMETERS:
		x:		The X location of the pixel to apply the texel to.
		y:		The Y location of the pixel to apply the texel to.
		texel:	The texel string to apply to the pixel.
	"""
	def applyTexel(self, x, y, texel):
	
		#Normalize the location.
		x = self.pushToInt(x)
		y = self.pushToInt(y)
		
		#Map down our location.
		index = (y*self.sizeX)+x
		
		#These if statements perform culling duties.
		if(ASCIIGLConstants.cullMode == ASCIIGLConstants.CULL):
			if (x < 0 or x > self.sizeX):
				return True
			elif (y < 0 or y > self.sizeY):
				return True
		elif(ASCIIGLConstants.cullMode == ASCIIGLConstants.WRAP):
			index = index % (self.sizeY*self.sizeX)
		else:
			index = index % (self.sizeY*self.sizeX)
		
		#Since texels are formatted, we don't need to worry about special character culling.
		
		#Based on the blending mode, we either append the texel's String to the pixel in
		#the framebuffer, or replace the pixel with it.
		if ASCIIGLConstants.texBlendingMode == ASCIIGLConstants.TEX_MULTIPLY:
			self.frameBuffer[int(index% (self.sizeY*self.sizeX-1))] += texel
		else:
			self.frameBuffer[int(index% (self.sizeY*self.sizeX-1))] = texel
			
		#Finaly, since our texel was not culled, we return false.
		return False
		
	
	"""
		Draws a line from (startX, startY) to (endX, endY),
		consisting of the character specified.
		
		HOW IT WORKS:
		First we get the distances covered in either axis
		by the line.
		Next, we divide the X distance by the Y distance. This
		gives us the step we increment the X value by to draw the current
		character.
		
		PARAMETERS:
		startX: 	The starting X location of the line.
		startY: 	The starting Y location of the line.
		endX:		The finishing X location of the line.
		endY:		The finishing Y location of the line.
		character:	The character to make the line out of.
	"""
	def line(self, startX, startY, endX, endY, character):
	
		startX = self.pushToInt(startX)
		startY = self.pushToInt(startY)
		endX = self.pushToInt(endX)
		endY = self.pushToInt(endY)
	
		#Get the X distance of the line.
		xLength = endX - startX
		
		#Get the Y distance of the line.
		yLength = endY - startY
		
		#Get the X increment.
		try:
			xIncrement = xLength/yLength
		except:
			xIncrement = 0
			
		for i in range (startY, endY, 1):
			self.character(startX + ( (i-startY)*xIncrement), i, character)
	
	"""
		Draws the string of text at the location (x, y).
		Newlines, and tabs are removed and accounted for
		manually to avoid currupting the framebuffer.
		
		HOW IT WORKS:
		First we create location variables to know where the
		current character should be printed.
		Then we go through every character in the text to be printed,
		checking to see if it is a newline, tab, or empty "", and
		adjust the location accordingly.
		Finally, if the character isn't one of the above characters,
		we draw it at the current location, and then increment the 
		current x position by one.
		
		PARAMETERS:
		x:		The X location of the text.
		y:		The Y location of the text.
		text:	The text to draw.
	"""
	def text(self, x, y, text):
	
		#We need to keep track of where the current
		#character should go.
		curX = self.pushToInt(x)
		curY = self.pushToInt(y)
		
		#We repr the string so that we maintain the escape characters.
		#text = str(text)
		
		for character in text:
			if(character == '\n'):
				curY += 1
				curX =  self.pushToInt(x)
			elif(character == '\t'):
				curY += 4
			elif(character == ''):
				None
			else:
				curX += 1
				self.character(curX, curY, character)
	
	"""
		Draws the framebuffer to the screen, as described out front.
		
		HOW IT WORKS:
		We create a string that we will use to render the framebuffer
		to the screen.
		Then we copy the framebuffer into that string, adding a newline
		every sizeX characters.
		Finally, we print that string. Simple.
		
		PARAMETERS:
		reallyClear:	If this is true, we fill the framebuffer with 
						the clear character. If false, we don't
	"""
	def blitToScreen(self, reallyClear):
		print('\x1b[1;1H')
		#print('\x1b[2J')
		self.swapString = ""
		for i in range(len(self.frameBuffer)):
			self.swapString += self.frameBuffer[i]
			if i % self.sizeX == 0:
				self.swapString += "\n"
		
		print(self.swapString)
		#print(stringToDraw)
		
		
		#print(charList)
		
		if(reallyClear == True):
			self.clearFramebuffer()
		
		
		
		
		
	
	
