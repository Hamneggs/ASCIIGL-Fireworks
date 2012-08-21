import ASCIIGL, ASCIIGLConstants, random, time, os, sys

width = 100


height = 60

riseSpeed = 2
particleSpeed = 3

frameCount = 0
maxFrameCount = 400


class PDir(object):
	U, D, L, R, UL, UR, DL, DR = range(8)

class FWState(object):
	rise, explode = range(2)

class Particle(object):
	
	x = 0
	y = 0
	dir = PDir.U
	characterSet = ["@", "#"]
	frames = 0
	offScreen = False
	
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.dir = direction
	
	def handle(self, renderer):
		offScreen = renderer.character(self.x, self.y, self.characterSet[self.frames%2])
		self.frames = self.frames+1
		if self.dir == PDir.U:	
			self.y-=1*particleSpeed
		elif self.dir == PDir.D:	
			self.y+=1*particleSpeed
		elif self.dir == PDir.L:	
			self.x-=1*particleSpeed
		elif self.dir == PDir.R:	
			self.x+=1*particleSpeed
		elif self.dir == PDir.UL:	
			self.y-=.25*particleSpeed
			self.x-=.25*particleSpeed
		elif self.dir == PDir.UR:	
			self.y-=.25*particleSpeed 
			self.x+=.25*particleSpeed
		elif self.dir == PDir.DL:	
			self.y+=.25*particleSpeed 
			self.x-=.25*particleSpeed
		elif self.dir == PDir.DR:	
			self.y+=.25*particleSpeed 
			self.x+=.25*particleSpeed

class Firework(object):
	
	def __init__(self, x, color, explodeHeight):
		self.ox = x
		self.cx = x
		self.oy = height
		self.cy = height
		self.color = color
		self.explodeHeight = explodeHeight
		self.state = FWState.rise
		self.particleList = []
		self.done = False
	
	def handle(self, renderer):
	
		if self.state == FWState.explode:
			self.done = True
			renderer.setTextColor(self.color)
			for i in range(len(self.particleList)):
				if not self.particleList[i].offScreen:
					self.done = False
					self.particleList[i].handle(renderer)
		else:
			renderer.setTextColor(ASCIIGLConstants.Fore.WHITE)
			renderer.line(self.cx, self.cy, self.ox, self.oy, ":")
			self.cy -= riseSpeed
			self.oy -= riseSpeed/2
			if(self.cy <= self.explodeHeight and self.state == FWState.rise):
				self.state = FWState.explode
				for i in range(8):
					#Sneaky sneaky...
					self.particleList.append(Particle(self.cx, self.cy, i))

class Sign(object):
	
	def handle(self, renderer):
		#renderer.rect(5, 5, 20, 10, " ", "=", "|")
		#As you can see, newlines will work as expected. They 
		#will not corrupt the framebuffer.
		renderer.text(5, 7, "Fireworks are the\nbest, aren't they,\nwhen ASCII?")
		#Of course, you can manually change the Y location of the 
		#text.
		#renderer.text(5, 12, "-GERARD")

class Fireworks(object):
	
	fireworkList = []
	sign = Sign()
	
	renderer = ASCIIGL.ASCIIGL(width, height)
	renderer.setColorMode(ASCIIGLConstants.EDIT_COLOR)
	renderer.setBGColor(ASCIIGLConstants.Back.BLACK)
	renderer.setTextStyle(ASCIIGLConstants.Style.BRIGHT)
	
	colorList = [ASCIIGLConstants.Fore.RED    ,
	             ASCIIGLConstants.Fore.GREEN  ,
	             ASCIIGLConstants.Fore.YELLOW ,
	             ASCIIGLConstants.Fore.BLUE   ,
	             ASCIIGLConstants.Fore.MAGENTA,
	             ASCIIGLConstants.Fore.CYAN,
				 ASCIIGLConstants.Fore.WHITE]
	
	
	def handle(self):
		for i in range(len(self.fireworkList)):
			if not self.fireworkList[i].done:
				self.fireworkList[i].handle(self.renderer)
			else:
				self.fireworkList[i] = None
		
		
		self.sign.handle(self.renderer)
		self.renderer.blitToScreen(True)
	
	def addFirework(self, x, explodeHeight):
		self.fireworkList.append(Firework(x, self.colorList[random.randrange(len(self.colorList))], explodeHeight))

def main():
	show = Fireworks()
	show.renderer.clearScreen()
	frameCount = 0
	maxFrameCount = 400
	while(frameCount < maxFrameCount):
		try:
			frameCount+=1
			show.renderer.text(0, height, "Frames: "+str(frameCount)+ " / "+str(maxFrameCount) )
			if(frameCount % 5 == 0):
				show.addFirework( random.randrange(int(width*.25), int(width*.75)), random.randrange(int(height*.05), int(height*.25)))
			show.handle()
			time.sleep(.01)
		except KeyboardInterrupt:
			maxFrameCount+=100
	show.renderer.resetAppearance()
	show.renderer.clearScreen()
	
main()
	


	