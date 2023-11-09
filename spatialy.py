import pygame, sys, random, math
import pygame.gfxdraw
import numpy as np

class Explosion:
	def __init__(self, x, y, width, height, spritelist, currentframe, frametime, lastupdatetime):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.spritelist = spritelist
		self.currentframe = currentframe
		self.frametime = frametime
		self.lastupdatetime = lastupdatetime

class Star:
	def __init__(self, x, y, intensity, speed):
		self.x = x
		self.y = y
		self.intensity = intensity
		self.speed = speed
	
	def moveleft(self, delta_t):
		self.x -= self.speed*delta_t
		if self.x < 0:
			self.x = STARFIELD_WIDTH-1
	
	def starisonscreen(self):
		return self.x < SCREEN_WIDTH


class Ship:
	def __init__(self, x, y, width, height, sprite, direction, moving, hp):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.sprite = sprite
		self.direction = direction
		self.moving = moving
		self.hp = hp
		self.boostdestination_x = 0
		self.boostdestination_y = 0
		self.boostanimation = 0
		self.boosting = False
	
	def moveup(self, delta):
		if self.y > delta:
			self.y -= delta
	
	def movedown(self, delta):
		if self.y < SCREEN_HEIGHT-self.height-1:
			self.y += delta
	
	def moveleft(self, delta):
		if self.x > delta:
			self.x -= delta
	
	def moveright(self, delta):
		if self.x < SCREEN_WIDTH-self.width-1:
			self.x += delta
	
	def takedamage(self, damage):
		self.hp -= damage
		if self.hp > 0:
			return True
		else:
			return False

	def boostupright(self):
		pass
	
	def boostdownright(self):
		pass
		
	def boostdownleft(self):
		pass
		
	def boostupleft(self):
		pass
	
	def boostup(self):
		pass
	
	def boostdown(self):
		pass
	
	def boostleft(self):
		pass
	
	def boostright(self):
		pass
		

class Enemy:
	def __init__(self, x, y, width, height, v_x, v_y, lastupdatetime, hp, lastfiretime, takingdamage, damageanimation, backwardsdamageanimation, damageanimationframe, lastanimationupdatetime, direction):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.v_x = v_x
		self.v_y = v_y
		self.lastupdatetime = lastupdatetime
		self.hp = hp
		self.lastfiretime = lastfiretime
		self.takingdamage = takingdamage
		self.damageanimation = damageanimation
		self.backwardsdamageanimation = backwardsdamageanimation
		self.damageanimationframe = damageanimationframe
		self.lastanimationupdatetime = lastanimationupdatetime
		self.direction = direction
	
	def moveup(self, delta_t):
		if self.y > math.fabs(self.v_y)*delta_t:
			if self.y < SCREEN_HEIGHT-1-self.height:
				self.y += self.v_y*delta_t
			else:
				self.v_y *= -1
				self.y = SCREEN_HEIGHT-1-self.height-5
		else:
			self.v_y *= -1
			self.y = math.fabs(self.v_y)*delta_t+5
		

	def moveleft(self, delta_t):
		if self.x > 0 and self.x <= SCREEN_WIDTH-self.width:
			self.x += self.v_x*delta_t
			return True
		else:
			if random.random() < 0.15:
				self.direction *= -1
				self.v_x *= -1
				if self.x <= 0:
					self.x = 3
				else:
					self.x = SCREEN_WIDTH-self.width-3
				return True
			else:
				return False
	
	def moveright(self, delta_t):
		if self.x < SCREEN_WIDTH-self.width-1:
			self.x += self.v_x*delta_t
			return True
		else:
			return False
	
	def takedamage(self, damage):
		self.hp -= damage
		if self.hp > 0:
			return True
		else:
			return False

	def draw(self):
		global currenttime
		if self.direction == -1:
			animation = self.damageanimation
		else:
			animation = self.backwardsdamageanimation
		if self.takingdamage:
			if currenttime - self.lastanimationupdatetime > 75:
				self.lastanimationupdatetime = currenttime
				self.damageanimationframe += 1
				if self.damageanimationframe == len(animation):
					self.damageanimationframe = 0
					self.takingdamage = False
			if self.takingdamage:
				screen.blit(animation[self.damageanimationframe], (self.x, self.y))
		else:
			screen.blit(animation[0], (self.x, self.y))
			

class Projectile:
	def __init__(self, x, y, width, height, v, sprite, lastupdatetime, friendly):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.v = v
		self.sprite = sprite
		self.lastupdatetime = lastupdatetime
		self.friendly = friendly

def finishgame():
	pygame.mixer.stop()
	gameoverfont = pygame.font.Font(None, 75)
	screen.fill(BLACK)
	gameovertext = gameoverfont.render("GAME OVER",1,WHITE)
	textpos = gameovertext.get_rect(centerx=SCREEN_WIDTH/2,centery=SCREEN_HEIGHT/2)
	screen.blit(gameovertext, textpos)	
	pygame.display.update()

	while 1:
		pygame.event.get()
		keystates = pygame.key.get_pressed()
		if keystates[pygame.K_RETURN] or keystates[pygame.K_ESCAPE]: break
	sys.exit()

BOOST_DISPLACEMENT = 450
COLLISION_DAMAGE = 25
HPBAR_WIDTH = 250
HPBAR_HEIGHT = 20
OHBAR_WIDTH = 300
OHBAR_HEIGHT = 20
EXPLOSION_WIDTH = 89
EXPLOSION_HEIGHT = 90
SECONDEXPLOSION_WIDTH = 64
SECONDEXPLOSION_HEIGHT = 64
PI = 3.14159265
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1030
STARFIELD_WIDTH = 5000
STARFIELD_HEIGHT = 1030
NUMBER_OF_FARAWAY_STARS = 1000
NUMBER_OF_NEAR_STARS = 500
PLASMA_WIDTH = 45
PLASMA_HEIGHT = 8
PLASMA_SPEED = 1.2
PLASMA_DAMAGE = 34
ENEMYFIRE_WIDTH = 31
ENEMYFIRE_HEIGHT = 10
ENEMYFIRE_SPEED = 0.9
ENEMYFIRE_DAMAGE = 25
ENEMY1_WIDTH = 42
ENEMY1_HEIGHT = 59
ENEMY_BASESPEED = 0.6
ENEMY_FIRE_PROBABILITY = 0.65
PLAYER_MOVESPEED = 8

pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
screen.fill(BLACK)
pygame.display.update()

boostduration = 50
score = 1000
diagonaladjust = 1/math.sqrt(2)
gameover = False
gameoverdelay = 3000
currenttime = pygame.time.get_ticks()
lasttime = currenttime
lasttime2 = currenttime
lastmovetime = currenttime
lastfiretime = currenttime
lastlasertime = currenttime
lastinverttime = currenttime
lastenemyspawntime = currenttime
lastshaketime = currenttime
lastdifficultyincreasetime = currenttime
lastboosttime = currenttime
lastohupdatetime = currenttime
delay = 15
delay2 = 3
movedelay = 13
firedelay = 250
invertdelay = 300
enemyspawndelay = 100
enemyfiredelay = 700
shakescreendelay = 10
boostdelay = 250
laserdelay = 1500
laserbeamduration = 750
laseron = False
difficultyincreasedelay = 10000
shipsprite = pygame.image.load("ship.png").convert_alpha()
backwardsshipsprite = pygame.image.load("ship_backwards.png").convert_alpha()
plasmasprite = pygame.image.load("plasma.png").convert_alpha()
enemyshot = pygame.image.load("enemyshot.png").convert_alpha()
megabombicon = pygame.image.load("megabomb.png").convert_alpha()
lasericon = pygame.image.load("lasericon.png").convert_alpha()
weaponselectframe = pygame.image.load("weaponselectframe.png").convert_alpha()
enemy_spawn_probability = 0.05
megabombs = 3
lasershots = 5
ohreductionrate = 0.035
oh = 0
secweapchoice = 0

#Generate a number of far-away stars with random positions and place in a list:
farstarlist = []
for i in range(NUMBER_OF_FARAWAY_STARS):
	farstarlist.append(Star(random.randint(0,STARFIELD_WIDTH), random.randint(0,STARFIELD_HEIGHT), 150, 0.15))

#Generate a number of near stars with random positions and place in a list:
nearstarlist = []
for i in range(NUMBER_OF_NEAR_STARS):
	nearstarlist.append(Star(random.randint(0,STARFIELD_WIDTH), random.randint(0,STARFIELD_HEIGHT), 255, 0.1))

#Initialize a list for projectile objects:
projectilelist = []

#Initialize a list for enemy objects:
enemylist = []

#Initialize a list of explosion objects:
explosionlist = []

#Load the animation surface lists:
explosionspritelist = []
for i in range(13):
	explosionfile = "explosion"+str(i)+".png"
	explosionspritelist.append(pygame.image.load(explosionfile).convert_alpha())
	
secondexplosionspritelist = []
for i in range(16):
	explosionfile = "secondexplosion"+str(i)+".png"
	secondexplosionspritelist.append(pygame.image.load(explosionfile).convert_alpha())

enemy1damagedspritelist = []
enemy1damagedspritelist.append(pygame.image.load("enemy1.png").convert_alpha())
for i in range(8):
	damagefile = "enemy1damaged"+str(i)+".png"
	enemy1damagedspritelist.append(pygame.image.load(damagefile).convert_alpha())

backwardsenemy1damagespritelist = []
backwardsenemy1damagespritelist.append(pygame.image.load("enemy1backwards.png").convert_alpha())
for i in range(8):
	damagefile = "enemy1backwardsdamaged"+str(i)+".png"
	backwardsenemy1damagespritelist.append(pygame.image.load(damagefile).convert_alpha())

firesound = pygame.mixer.Sound("alienshoot1.ogg")
explosionsound = pygame.mixer.Sound("explosion.ogg")
secondexplosionsound = pygame.mixer.Sound("secondexplosion.ogg")
thrustsound = pygame.mixer.Sound("thrust2.ogg")
thrustsound.set_volume(0.25)
hitsound = pygame.mixer.Sound("hitsound.ogg")
hitsound.set_volume(0.75)
megabombsound = pygame.mixer.Sound("megabomb.ogg")
laserbeamsound = pygame.mixer.Sound("laserbeam.ogg")

print("Okay, first let's configure the joystick!")
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
number_of_joysticks = pygame.joystick.get_count()
print("Number of joysticks: ", number_of_joysticks)
if number_of_joysticks > 0:
	joystick = pygame.joystick.Joystick(0)
	print("Number of joystick axes: ", joystick.get_numaxes())
	print("Joystick instance ID: ", joystick.get_instance_id())
	print("Joystick name: ", joystick.get_name())
	print("Number of buttons: ", joystick.get_numbuttons())
	
#	done = False
#	while not done:
#		for event in pygame.event.get():
#			if event.type == pygame.QUIT:
#				done = True
#			
#			if event.type == pygame.KEYDOWN:
#				done = True
#			
#			if event.type == pygame.JOYBUTTONDOWN:
#				print("Button pressed: ", event.button)
#				print()

clock = pygame.time.Clock()
shakescreen = False
shakeindex = 0

font = pygame.font.Font(None, 25)

playerobject = Ship(SCREEN_WIDTH/2-32, SCREEN_HEIGHT/2-24, shipsprite.get_width(), shipsprite.get_height(), shipsprite, 1, False, 100)


while True:
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			sys.exit()
	
	keypresses = pygame.key.get_pressed()
	currenttime = pygame.time.get_ticks()
	screen.fill(BLACK)
	
	#Handle key presses for making a boosted movement:
	#if keypresses[pygame.K_s] and not gameover:
	#	playerobject.
	
	#Handle key presses for switching secondary weapon:
	#if (keypresses[pygame.K_LALT]):

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				secweapchoice += 1
				if secweapchoice == 2:
					secweapchoice = 0			
		if event.type == pygame.QUIT:
			sys.exit()
	
	#Handle key presses for shaking the screen:
	if (keypresses[pygame.K_LALT] or joystick.get_button(0)) and not shakescreen and not gameover and megabombs > 0 and oh == 0 and secweapchoice == 0:
		oh = 100
		shakescreen = True
		megabombs -= 1
		megabombsound.play()
		joystick.rumble(100, 100, 1000)
		score += 1000*len(enemylist)
		for enemy in enemylist:
			pygame.draw.rect(screen, BLACK, ((enemy.x,enemy.y),(enemy.width,enemy.height)))
			explosionlist.append(Explosion(enemy.x, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, explosionspritelist, 0, 90, currenttime))
			explosionsound.play()
		enemylist.clear()
		d = PI*random.random()
		screencopy = screen.copy()
		screenbackup = screen
		screen = screencopy
		screen.fill(BLACK)
		print("Number of enemies left after shake: ", len(enemylist))
	
	#Handle key presses for movement:
	if keypresses[pygame.K_UP] or keypresses[pygame.K_DOWN] or keypresses[pygame.K_LEFT] or keypresses[pygame.K_RIGHT] or math.fabs(joystick.get_axis(0)) > 0.01 or math.fabs(joystick.get_axis(1)) > 0.01 and not gameover:
		if currenttime - lastmovetime > movedelay:
			lastmovetime = currenttime
			if keypresses[pygame.K_RIGHT] and keypresses[pygame.K_UP] or (joystick.get_axis(0) > 0.01 and joystick.get_axis(1) < -0.01):
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_x = playerobject.x+BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_x > SCREEN_WIDTH-playerobject.width:
						playerobject.boostdestination_x = SCREEN_WIDTH-playerobject.width
					playerobject.boostdestination_y = playerobject.y-BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_y < 0:
						playerobject.boostdestination_y = 0
					playerobject.boosting = True
				else:
					playerobject.moveup(PLAYER_MOVESPEED*diagonaladjust)
					playerobject.moveright(PLAYER_MOVESPEED*diagonaladjust)
			elif keypresses[pygame.K_RIGHT] and keypresses[pygame.K_DOWN] or (joystick.get_axis(0) > 0.01 and joystick.get_axis(1) > 0.01):
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_x = playerobject.x+BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_x > SCREEN_WIDTH-playerobject.width:
						playerobject.boostdestination_x = SCREEN_WIDTH-playerobject.width
					playerobject.boostdestination_y = playerobject.y+BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_y > SCREEN_HEIGHT-playerobject.height:
						playerobject.boostdestination_y = SCREEN_HEIGHT-playerobject.height
					playerobject.boosting = True
				else:
					playerobject.movedown(PLAYER_MOVESPEED*diagonaladjust)
					playerobject.moveright(PLAYER_MOVESPEED*diagonaladjust)
			elif keypresses[pygame.K_LEFT] and keypresses[pygame.K_UP] or (joystick.get_axis(0) < -0.01 and joystick.get_axis(1) < -0.01):
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_x = playerobject.x-BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_x < 0:
						playerobject.boostdestination_x = 0
					playerobject.boostdestination_y = playerobject.y-BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_y < 0:
						playerobject.boostdestination_y = 0
					playerobject.boosting = True
				else:
					playerobject.moveup(PLAYER_MOVESPEED*diagonaladjust)
					playerobject.moveleft(PLAYER_MOVESPEED*diagonaladjust)
			elif keypresses[pygame.K_LEFT] and keypresses[pygame.K_DOWN] or (joystick.get_axis(0) < -0.01 and joystick.get_axis(1) > 0.01):
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_x = playerobject.x-BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_x < 0:
						playerobject.boostdestination_x = 0
					playerobject.boostdestination_y = playerobject.y+BOOST_DISPLACEMENT*diagonaladjust
					if playerobject.boostdestination_y > SCREEN_HEIGHT-playerobject.height:
						playerobject.boostdestination_y = SCREEN_HEIGHT-playerobject.height
					playerobject.boosting = True
				else:
					playerobject.movedown(PLAYER_MOVESPEED*diagonaladjust)
					playerobject.moveleft(PLAYER_MOVESPEED*diagonaladjust)
			elif keypresses[pygame.K_UP] or joystick.get_axis(1) < -0.01:
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_y = playerobject.y-BOOST_DISPLACEMENT
					if playerobject.boostdestination_y < 0:
						playerobject.boostdestination_y = 0
					playerobject.boosting = True
				else:
					playerobject.moveup(PLAYER_MOVESPEED)
			elif keypresses[pygame.K_DOWN] or joystick.get_axis(1) > 0.01:
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_y = playerobject.y+BOOST_DISPLACEMENT
					if playerobject.boostdestination_y > SCREEN_HEIGHT-playerobject.height:
						playerobject.boostdestination_y = SCREEN_HEIGHT-playerobject.height
					playerobject.boosting = True
				else:
					playerobject.movedown(PLAYER_MOVESPEED)
			elif keypresses[pygame.K_LEFT] or joystick.get_axis(0) < -0.01:
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_x = playerobject.x-BOOST_DISPLACEMENT
					if playerobject.boostdestination_x < 0:
						playerobject.boostdestination_y = 0
					playerobject.boosting = True
				else:
					playerobject.moveleft(PLAYER_MOVESPEED)
			elif keypresses[pygame.K_RIGHT] or joystick.get_axis(0) > 0.01:
				if keypresses[pygame.K_s] and currenttime - lastboosttime > boostdelay:
					lastboosttime = currenttime
					playerobject.boostdestination_x = playerobject.x+BOOST_DISPLACEMENT
					if playerobject.boostdestination_x > SCREEN_WIDTH-playerobject.width:
						playerobject.boostdestination_x = SCREEN_WIDTH-playerobject.width
					playerobject.boosting = True
				else:
					playerobject.moveright(PLAYER_MOVESPEED)
			if not playerobject.moving:
				thrustsound.play(loops = -1)
				playerobject.moving = True
	else:
		if playerobject.moving:
			playerobject.moving = False
			thrustsound.stop()
	
	#Handle key presses for firing:
	if keypresses[pygame.K_LCTRL] or joystick.get_button(2) and not gameover:
		if oh == 0:
		#if currenttime - lastfiretime > firedelay:
			oh = 9
			#lastfiretime = currenttime
			f_y = playerobject.y+playerobject.height/2		
			if playerobject.direction == 1:
				f_x = playerobject.x+playerobject.width
			else:
				f_x = playerobject.x-PLASMA_WIDTH
			f_width = PLASMA_WIDTH
			f_height = PLASMA_HEIGHT
			f_v = PLASMA_SPEED*playerobject.direction
			f_sprite = plasmasprite
			f_updatetime = currenttime
			projectilelist.append(Projectile(f_x, f_y, f_width, f_height, f_v, f_sprite, f_updatetime, True))
			firesound.play()
	if (keypresses[pygame.K_LALT] or joystick.get_button(3)) and not gameover and (not laseron) and oh == 0 and secweapchoice == 1 and lasershots > 0:
		laserbeamsound.play()
		lasershots -= 1
		oh = 75
		lastlasertime = currenttime
		laseron = True
	
	#Handle key presses for changing direction:
	if (keypresses[pygame.K_LSHIFT] or joystick.get_button(4) or joystick.get_button(5)) and not gameover:
		if currenttime - lastinverttime > invertdelay:
			lastinverttime = currenttime
			pygame.draw.rect(screen, BLACK, ((playerobject.x,playerobject.y),(playerobject.width,playerobject.height)))
			playerobject.direction *= -1
			if playerobject.direction == 1:
				playerobject.sprite = shipsprite
			else:
				playerobject.sprite = backwardsshipsprite
			print(playerobject.direction,'\n')
	
	#Handle key presses for exiting:		
	if keypresses[pygame.K_ESCAPE]:
		sys.exit()
	
	#Update the far-away stars:
	delta_t = currenttime - lasttime
	if delta_t > delay:
		lasttime = currenttime	
		#Move far-away stars from list:
		for i in range(NUMBER_OF_FARAWAY_STARS):
			#if farstarlist[i].x < 1920:
				#pygame.gfxdraw.pixel(screen, int(farstarlist[i].x), int(farstarlist[i].y), BLACK)
			farstarlist[i].moveleft(delta_t)
	
	#Update the near stars:
	delta_t = currenttime - lasttime2
	if delta_t > delay2:
		lasttime2 = currenttime		
		#Move near stars from list:
		for i in range(NUMBER_OF_NEAR_STARS):
			#if nearstarlist[i].x < 1920:
				#pygame.gfxdraw.pixel(screen, int(nearstarlist[i].x), int(nearstarlist[i].y), BLACK)
			nearstarlist[i].moveleft(delta_t)

	#Spawn a new enemy:
	if currenttime - lastenemyspawntime > enemyspawndelay and not shakescreen:
		lastenemyspawntime = currenttime
		if random.random() <= enemy_spawn_probability:
			if random.random() <= 0.85:
				enemy_x = SCREEN_WIDTH - ENEMY1_WIDTH
				enemy_v_x = -ENEMY_BASESPEED*diagonaladjust+0.15*random.uniform(-1,1)
				enemy_direction = -1
			else:
				enemy_x = 5
				enemy_v_x = ENEMY_BASESPEED*diagonaladjust-0.15*random.uniform(-1,1)
				enemy_direction = 1
			enemy_y = random.randint(ENEMY1_HEIGHT+1,SCREEN_HEIGHT-ENEMY1_HEIGHT-1)
			enemy_v_y = random.randint(-1,1)*ENEMY_BASESPEED*diagonaladjust+0.15*random.randint(-1,1)
			enemy_hp = 100
			#self, x, y, width, height, sprite, v_x, v_y, lastupdatetime, hp, lastfiretime, takingdamage, damageanimation, damageanimationframe, lastanimationupdatetime, direction
			#self, x, y, width, height, v_x, v_y, lastupdatetime, hp, lastfiretime, takingdamage, damageanimation, backwardsdamageanimation, damageanimationframe, lastanimationupdatetime, direction
			enemylist.append(Enemy(enemy_x, enemy_y, ENEMY1_WIDTH, ENEMY1_HEIGHT, enemy_v_x, enemy_v_y, currenttime, enemy_hp, currenttime, False, enemy1damagedspritelist, backwardsenemy1damagespritelist, 0, currenttime, enemy_direction))

	#Update enemies:
	enemyremovelist = []
	for enemy in enemylist:
		#pygame.draw.rect(screen, BLACK, ((enemy.x,enemy.y),(enemy.width,enemy.height)))
		
		#Make enemy fly closer to player if they are far away:
		if enemy.y - playerobject.y > 3*playerobject.height and enemy.x > playerobject.x:
			enemy.v_y = -0.45*diagonaladjust*ENEMY_BASESPEED
		elif playerobject.y - enemy.y > 3*playerobject.height and enemy.x > playerobject.x:
			enemy.v_y = 0.45*diagonaladjust*ENEMY_BASESPEED
		
		#Check if enemy is colliding with player:
		elif (math.fabs(enemy.x+enemy.width/2-(playerobject.x+playerobject.width/2)) < enemy.width/2+playerobject.width/2-5) and (math.fabs(enemy.y+enemy.height/2-(playerobject.y+playerobject.height/2)) < enemy.height/2+playerobject.height/2-5) and not gameover:		
			if not playerobject.takedamage(COLLISION_DAMAGE):
				pygame.draw.rect(screen, BLACK, ((playerobject.x,playerobject.y),(playerobject.width,playerobject.height)))
				explosionlist.append(Explosion(playerobject.x, playerobject.y, SECONDEXPLOSION_WIDTH, SECONDEXPLOSION_HEIGHT, secondexplosionspritelist, 0, 75, currenttime))
				secondexplosionsound.play()
				gameover = True
				gameovertime = currenttime
			else:
				explosionlist.append(Explosion(enemy.x, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, explosionspritelist, 0, 90, currenttime))
				enemyremovelist.append(enemy)
				#enemylist.remove(enemy)
				explosionsound.play()
		
		#Make enemy fire if they are close to player:
		if currenttime - enemy.lastfiretime > enemyfiredelay:
			enemy.lastfiretime = currenttime
			if math.fabs((enemy.y+enemy.height/2) - (playerobject.y+playerobject.height/2)) < 2*playerobject.height and ((enemy.x > playerobject.x and enemy.direction == -1) or (enemy.x < playerobject.x and enemy.direction == 1)):
				if random.random() < ENEMY_FIRE_PROBABILITY:
					f_y = enemy.y+enemy.height/2
					if enemy.direction == -1:
						f_x = enemy.x-ENEMYFIRE_WIDTH
					else:
						f_x = enemy.x+enemy.width
					f_width = ENEMYFIRE_WIDTH
					f_height = ENEMYFIRE_HEIGHT
					f_v = ENEMYFIRE_SPEED*enemy.direction
					f_sprite = enemyshot
					f_updatetime = currenttime
					projectilelist.append(Projectile(f_x, f_y, f_width, f_height, f_v, f_sprite, f_updatetime, False))
		
		delta_t = currenttime-enemy.lastupdatetime
		enemy.lastupdatetime = currenttime
		enemy.moveup(delta_t)
		
		#Check if the enemy is colliding with another enemy:
		for otherenemy in enemylist:
			if not (otherenemy == enemy) and (math.fabs(enemy.x+enemy.width/2-(otherenemy.x+otherenemy.width/2)) < enemy.width/2+otherenemy.width/2-5) and (math.fabs(enemy.y+enemy.height/2-(otherenemy.y+otherenemy.height/2)) < enemy.height/2+otherenemy.height/2-5):
				explosionlist.append(Explosion(enemy.x, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, explosionspritelist, 0, 90, currenttime))
				explosionlist.append(Explosion(otherenemy.x, otherenemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, explosionspritelist, 0, 90, currenttime))
				explosionsound.play()
				explosionsound.play()
				enemyremovelist.append(enemy)
				enemyremovelist.append(otherenemy)
		if not enemy.moveleft(delta_t):
			enemylist.remove(enemy)
	for enemy in enemyremovelist:
		if enemy in enemylist:
			enemylist.remove(enemy)

	#Update projectiles:
	projectileremovelist = []
	for proj in projectilelist:
		proj.x += (currenttime-proj.lastupdatetime)*proj.v
		proj.lastupdatetime = currenttime
		projectileremoved = False
		for enemy in enemylist:
			if (math.fabs(proj.x+proj.width/2-(enemy.x+enemy.width/2)) < proj.width/2+enemy.width/2-5) and (math.fabs(proj.y+proj.height/2-(enemy.y+enemy.height/2)) < proj.height/2+enemy.height/2-5):
				if not enemy.takedamage(PLASMA_DAMAGE) or ((proj.v < 0 and enemy.direction < 0) or (proj.v > 0 and enemy.direction > 0)):
					explosionlist.append(Explosion(enemy.x, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, explosionspritelist, 0, 90, currenttime))
					explosionsound.play()
					enemylist.remove(enemy)
					score += 1000
				else:
					enemy.takingdamage = True
					enemy.lastanimationupdatetime = currenttime
					enemy.damageanimationframe = 1
					hitsound.play()
				projectileremovelist.append(proj)
				projectileremoved = True
		if (math.fabs(proj.x+proj.width/2-(playerobject.x+playerobject.width/2)) < proj.width/2+playerobject.width/2-5) and (math.fabs(proj.y+proj.height/2-(playerobject.y+playerobject.height/2)) < proj.height/2+playerobject.height/2-5) and not projectileremoved and not gameover:
			if not playerobject.takedamage(ENEMYFIRE_DAMAGE):
				explosionlist.append(Explosion(playerobject.x, playerobject.y, SECONDEXPLOSION_WIDTH, SECONDEXPLOSION_HEIGHT, secondexplosionspritelist, 0, 75, currenttime))
				secondexplosionsound.play()
				gameover = True
				gameovertime = currenttime
			projectileremovelist.append(proj)
			projectileremoved = True
		if not projectileremoved and (proj.x > SCREEN_WIDTH or proj.x <= 0):
			if proj.friendly:
				score -= 300
			projectilelist.remove(proj)
	for proj in projectileremovelist:
		if proj in projectilelist:
			projectilelist.remove(proj)

	#Update laser:
	if laseron:
		if currenttime - lastlasertime < laserbeamduration:
			for enemy in enemylist:
				if ((enemy.y+enemy.height >= playerobject.y+0.75*playerobject.height-2 and enemy.y <= playerobject.y+0.75*playerobject.height-2) or (enemy.y <= playerobject.y+0.75*playerobject.height+2 and enemy.y+enemy.height >= playerobject.y+0.75*playerobject.height+2)):
					if (playerobject.direction > 0 and enemy.x > playerobject.x+playerobject.width) or (playerobject.direction < 0 and enemy.x < playerobject.x):
						explosionlist.append(Explosion(enemy.x, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, explosionspritelist, 0, 90, currenttime))
						explosionsound.play()
						enemylist.remove(enemy)
			if playerobject.direction > 0:
				pygame.draw.line(screen, (50,50,255), (playerobject.x+0.9*playerobject.width, playerobject.y+0.75*playerobject.height), (SCREEN_WIDTH-1, playerobject.y+0.75*playerobject.height), width=5)
			else:
				pygame.draw.line(screen, (50,50,255), (0, playerobject.y+0.75*playerobject.height), (playerobject.x+0.1*playerobject.width, playerobject.y+0.75*playerobject.height), width=5)
		else:
			laseron = False

	#Update explosions:
	for explosion in explosionlist:
		if currenttime-explosion.lastupdatetime > explosion.frametime:
			explosion.lastupdatetime = currenttime
			#pygame.draw.rect(screen, BLACK, ((explosion.x,explosion.y),(explosion.width,explosion.height)))
			explosion.currentframe += 1
			if explosion.currentframe == len(explosion.spritelist):
				explosionlist.remove(explosion)
	
	#Update any boosting:
	if playerobject.boosting == True:
		if currenttime - lastboosttime > boostduration:
			playerobject.x = playerobject.boostdestination_x
			playerobject.y = playerobject.boostdestination_y
			playerobject.boosting = False
	
	#Update the stats bar:
	pygame.draw.rect(screen, (15,15,15), ((0,1030),(1920,50)))
	hptext = font.render("HP: ",1,WHITE)
	hptextpos = hptext.get_rect(centerx=35, centery=1058)
	screen.blit(hptext, hptextpos)
	hpbarlength = playerobject.hp/100*HPBAR_WIDTH
	pygame.draw.rect(screen, RED, ((72,1047),(hpbarlength,HPBAR_HEIGHT)))
	pygame.draw.rect(screen, WHITE, ((70,1045),(HPBAR_WIDTH+4,HPBAR_HEIGHT+4)), 1)
	leveltext = font.render("DIFFICULTY: ",1,WHITE)
	leveltextpos = leveltext.get_rect(centerx=430, centery=1058)
	screen.blit(leveltext, leveltextpos)
	difficultytext = font.render(f"{enemy_spawn_probability*100:.0f}%",1,WHITE)
	difficultytextpos = difficultytext.get_rect(centerx=500, centery=1058)
	screen.blit(difficultytext, difficultytextpos)
	scoreastext = font.render(f"{score}",1,WHITE)
	scoreastextpos = scoreastext.get_rect(centerx=660, centery=1058)
	screen.blit(scoreastext, scoreastextpos)
	scoretext = font.render("SCORE: ",1,WHITE)
	scoretextpos = scoretext.get_rect(centerx=600, centery=1058)
	screen.blit(scoretext, scoretextpos)
	ohtext = font.render("OVERHEATING: ",1,WHITE)
	ohtextpos = ohtext.get_rect(centerx=800, centery=1058)
	screen.blit(ohtext, ohtextpos)
	ohbarlength = oh/100*OHBAR_WIDTH
	pygame.draw.rect(screen, RED, ((880,1047),(ohbarlength,OHBAR_HEIGHT)))
	pygame.draw.rect(screen, WHITE, ((878,1045),(OHBAR_WIDTH+4,OHBAR_HEIGHT+4)), 1)
	
	#secondary weapon:
	secondaryweapontext = font.render("SECONDARY WEAPON: ",1,WHITE)
	secondaryweapontextpos = secondaryweapontext.get_rect(centerx=1330, centery=1058)
	screen.blit(secondaryweapontext, secondaryweapontextpos)
	megabombsastext = font.render(f"{megabombs}",1,WHITE)
	megabombsastextpos = megabombsastext.get_rect(centerx=1452, centery=1058)
	screen.blit(megabombsastext, megabombsastextpos)
	screen.blit(megabombicon, (1463, 1040))
	#screen.blit(weaponselectframe, (1435, 1035))
	lasershotsastext = font.render(f"{lasershots}",1,WHITE)
	lasershotsastextpos = lasershotsastext.get_rect(centerx=1520, centery=1058)
	screen.blit(lasershotsastext, lasershotsastextpos)
	screen.blit(lasericon, (1536, 1045))
	#screen.blit(weaponselectframe, (1505, 1035))
	screen.blit(weaponselectframe, (1438+secweapchoice*70, 1035))
	
	#Update the overheating (make ship lose heat):
	oh -= ohreductionrate*(currenttime-lastohupdatetime)
	if oh < 0:
		oh = 0
	lastohupdatetime = currenttime
	
	#Update the enemy spawn probability:
	if (currenttime - lastdifficultyincreasetime > difficultyincreasedelay) and enemy_spawn_probability < 1:
		lastdifficultyincreasetime = currenttime
		pygame.draw.rect(screen, BLACK, difficultytextpos)
		enemy_spawn_probability += 0.01
		if enemy_spawn_probability > 1:
			enemy_spawn_probability = 1
	
	#Check if it's time to go to the gameover screen:
	if gameover and (currenttime - gameovertime > gameoverdelay):
		finishgame()
	
	#Draw the explosions:
	for e in explosionlist:
		screen.blit(e.spritelist[e.currentframe], (e.x, e.y))
	
	#Draw all the far-away stars:
	for i in range(NUMBER_OF_FARAWAY_STARS):
		if farstarlist[i].x < 1920:
			b = farstarlist[i].intensity
			pygame.gfxdraw.pixel(screen, int(farstarlist[i].x), int(farstarlist[i].y), (b,b,b))
	
	#Draw all the near stars:
	for i in range(NUMBER_OF_NEAR_STARS):
		if nearstarlist[i].x < 1920:
			b = nearstarlist[i].intensity
			pygame.gfxdraw.pixel(screen, int(nearstarlist[i].x), int(nearstarlist[i].y), (b,b,b))
	
	#Draw all the projectiles:
	for i in range(len(projectilelist)):
		screen.blit(projectilelist[i].sprite, (projectilelist[i].x, projectilelist[i].y))
	
	#Draw the player:
	if not gameover:
		screen.blit(playerobject.sprite, (playerobject.x, playerobject.y))
	
	#Draw the enemies:
	for e in enemylist:
		e.draw()
		#screen.blit(e.sprite, (e.x, e.y))
	
	if shakescreen:
		screenbackup.fill(BLACK)
		if currenttime-lastshaketime > shakescreendelay:
			lastshaketime = currenttime
			screenbackup.fill(BLACK)
			screenbackup.blit(screen, (50*math.sin(0.65*shakeindex+d), 65*math.sin(0.75*shakeindex)))		
			shakeindex += 1
			if shakeindex > 100:
				screenbackup.blit(screen, (0, 0))
				shakeindex = 0
				screen = screenbackup
				shakescreen = False
	
	pygame.display.update()

