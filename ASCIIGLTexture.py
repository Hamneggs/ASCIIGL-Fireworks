"""
	This class represents a texture object for ASCIIGL.
	Data organisation is very similar to the framebuffer
	of ASCIIGL.
	All data of texels are formatted in the way of 
	Colorama.
	
	---DATA ORGANISATION---
	Texel:		Each texel is stored as such:
				"[Background Color]"+
				"[Character Color]" +
				"[Texel Character]" +
				"[Character Style]" 
	
	Texture:	Every texture is a linear list of texels.
				We store the x and y sizes as members of the
				texture object so that we can navigate through
				the linear list in two dimensions.
	
	File:		The texture file is formatted as follows:
				"[X size]"$"[Y size]"
				[texel (0, 0)]$
				[texel (1, 0)]$
				[texel (2, 0)]$
				...
				[texel (0, 1)]$
				[texel (1, 1)]$
				[texel (2, 1)]$
				...
				...
				[texel (x, y)]
				where each texel is formatted like so:
				"[Background Color]"$"[Character Color]"$"[Texel Character]"$"[Character Style]"
	
	---NOTES---
	There isn't any on-the-fly texture resizing. At the pixel sizes
	we're dealing with, most features won't be bigger than
	one pixel wide. Combine that with a restricted pallete,
	and the idea of a skewed and scaled texture image
	tarnishes at an alarming rate.
	
"""
import ASCIIGL, ASCIIGLConstants

class Texture(object):
	
	"""
		Initializes the texture object by creating
		a texel table, loading all of the data from the file into it, 
		and creating members for the size of the texture.
		
		PARAMETERS:
		The name of the texture file, with extension.
		
		RAISES:
		RuntimeError, if the filename does not include the proper extension.
	"""
	def __init__(filename):
		try:
			if not str(filename).endsIn(".AGLT"):
				raise RuntimeError
		except:
			print ("File "+filename+" has an improper extension.")
			 
		fileInfo = loadFile(filename)
		self.texelTable = fileInfo[0]
		self.sizeX = fileInfo[1]
		self.sizeY = fileInfo[2]
	
	"""
		Loads the texture file.
		
		PARAMETERS:
		The name of the file to be found and loaded.
		
		RETURNS:
		A tuple containing the list of texels, the X size, 
		and Y size of the texture.
		
		HOW IT WORKS:
		Loads the file, then for each line,
		if it is the first line, read in the line's data as
		two ints--the X and Y size of the texture.
		Otherwise, load the line as a texel, with each
		of the line's four elements getting it's own index.
		
		RAISES:
		RuntimeError, if given a the name of an incorrect file.
	"""
	def loadFile(self, filename):
		
		#Create variables to store the considered
		#data loaded from the file.
		sizeX = 0
		sizeY = 0
		texels = []		
		
		#You know, so we know that we are at the first line.
		first = True
		
		#Open the file and load its lines into dataLines.
		try:
			dataLines = open(filename)
		except RuntimeError:
			print("The texture file " + filename + "could not be\nloaded due to an incorrect filename,\nor that the file does not exist.")
		
		#For every one of those loaded lines,
		for line in dataLines:
			#First split the line...
			lineContents = line.split("$")
			#Then if it is the first line...
			if First:
				#it stores the size of the texture, and 
				#hence must be considered as such.
				sizeX = int(lineContents[0])
				sizeY = int(lineContents[1])
			#Otherwise...
			else:
				#Append the line-list intact to the texel list.
				#This ensures that every appearance modifier the
				#texel had in file is given its own index in the
				#new texel list.
				texels.append(lineContents)
			#Also, we must set the First boolean to false, so we
			#don't corrupt our loading routine.
			First = False

		#Finally we return a size-3 tuple containing first the
		#texel array, then the X and Y sizes of the texture.
		return (texels, sizeX, sizeY)
	
			
	"""
		Returns a single String that is the character and 
		appearance modifiers of the texel at locaiton (x, y), 
		tailored to suit the current texture mode and texture
		blending mode.
		
		PARAMETERS:
		x:	The X-location of the texel being queried.
		y:	The Y-location of the texel being queried.
		
		HOW IT WORKS:
		We linearize the location given into 1-D space, 
		and grab the texel data at that location.
		We then modify our copy of that data according
		to the current texture and texture-blending 
		modes.
		
		RETURNS:
		A string containing all of the specified elements of
		the requested texel.
	"""
	def getTexel(x, y):
	
		#Create an empty string to hold the texel data.
		texel = ''
		
		#Get the entirety of the texel data, so we can take the bits that we need.
		wholeTexel = texelTable[int( ( ((y*self.sizeX)+x)*4)%(self.sizeX*self.sizeY*4)) : int( ( ((y*self.sizeX)+x)*4)%(self.sizeX*self.sizeY*4))+4]
		
		#The texel data will be appended to the underlying pixel in this mode, 
		#so we don't want to introduce another space-taking character.
		if(ASCIIGLConstants.textureBlendingMode == ASCIIGLConstants.TEX_MULTIPLY):
			wholeTexel[2] = ''
		#In additive mode, the texel replaces the pixel, so we neet to take the space.
		else:
			texel = ' '
			
		if ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_ALL:		
			texel = wholeTexel[0:-1] 
		elif ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_FORE_BACK: 	
			texel = wholeTexel[0:2] 
		elif ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_BACK: 	
			texel += wholeTexel[0]
		elif ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_STYLE:	
			texel += wholeTexel[3]
		elif ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_FORE:	
			texel = wholeTexel[1:2]		
		elif ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_FORE_STYLE:  
			texel = wholeTexel[2:3]		
		elif ASCIIGLConstants.textureMode == ASCIIGLConstants.USE_TEX_NONE:
			None
		
		return texel
	
	"""
		Draws all of the texels of the image into
		the supplied rendering surface beginning at
		location (x, y)
		
		PARAMETERS:
		x:		The X location on the rendering surface
				to start drawing the texture.
		y:		The Y location on the rendering surface
				to start drawing the texture.
		surface:The ASCIIGL rendering surface onto
				which the texture is to be drawn.
	"""
	def drawTexture(x, y, surface):
		for i in range(self.sizeX):
			for k in range(self.sizeY):
				surface.applyTexel(x+i, y+k, self.getTexel(i, k))
				
			
	