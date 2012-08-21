
#Thanks to Jonathan Hartley for Colorama.
#Website:	http://code.google.com/p/colorama/
from colorama import init, Fore, Back, Style

#Just in case we are on a Windows platform, we call
#init()
init()

"""
	This module is simply a bunch of constants for
	ASCIIGL.
"""

"""
	The method floating point values are flattened into integers for
	character placement in the framebuffer.
"""
FLAT_FLOOR = 1
FLAT_CEIL  = 2
flatMode = FLAT_FLOOR

"""
	The parameters associated with clearing the screen.
"""
clearCharacter = " "

"""
	The mode by which to choose the border character for
	corners of shapes.
"""
FAVOR_VERT = 1
FAVOR_HORIZ = 2
borderCornerMode = FAVOR_HORIZ
	
"""
	The fill mode of shapes.
"""
BORDER_ONLY = 1
FILL_ONLY = 2
FILL_AND_BORDER = 4
shapeFillMode = FILL_AND_BORDER

"""
	The culling mode. Does the item wrap around,
	or does it just go offscreen?
"""
CULL = 1
WRAP = 2
cullMode = CULL

"""
	The text wrap mode. Does text wrap around at the 
	text's X location, or at the start of the next line
	of the framebuffer.
"""
WRAP_AT_LOCATION = 1
WRAP_AT_LINE = 2
textWrapMode = WRAP_AT_LOCATION

EDIT_COLOR = 1
EDIT_COLOR_AND_STYLE = 2
PRESERVE_COLOR = 4
colorMode = EDIT_COLOR_AND_STYLE


"""
	The color of the text.
"""
textColor = Fore.RESET

"""
	The style of the text.
"""
textStyle = Style.NORMAL

"""
	The color of the background.
"""
bgColor = Back.RESET

"""
	The texture mode. 
	USE_TEX_ALL:		When sampling the texture, we grab each texel's style, 
						background color, forground color, and character.		
	USE_TEX_FORE_BACK:	Use the foreground/character color, character (obviously),
						and the background color.
	USE_TEX_BACK:		Use only the background color.	
	USE_TEX_STYLE:		Use only the character modified by the texel's style.
	USE_TEX_FORE_STYLE:	Use the foreground character modified by color and style.
	USE_TEX_NONE:		Turn off texture usage.
	
"""
USE_TEX_ALL 		= 1
USE_TEX_FORE_BACK 	= 2
USE_TEX_BACK 		= 4
USE_TEX_STYLE		= 8
USE_TEX_FORE		= 16
USE_TEX_FORE_STYLE  = 32
USE_TEX_NONE		= 64
textureMode = USE_TEX_ALL
	
"""
	Texture blending mode. Yep, that's right: Blending modes in ASCII.
	TEX_MULTIPLY: 	Only uses the appearance modifiers from the texture.
					Any texel that is queried will have a character of ''.
	TEX_ADDITIVE:	All elements of the texture are used.
"""
TEX_MULTIPLY	= 1
TEX_ADDITIVE	= 2
texBlendingMode = TEX_ADDITIVE

	

	