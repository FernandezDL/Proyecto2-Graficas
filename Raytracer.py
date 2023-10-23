import pygame
from pygame.locals import * 

from rt import Raytracer
from figuras import *
from lights import *
from material import *

width = 512
height =512

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rt = Raytracer(screen)
rt.rtClearColor(0.7,0.5,0.7)
rt.envMap = pygame.image.load("images/fondo.jpg")
flowersTexture=pygame.image.load("images/flores.jpg")

grass = Material(diffuse=(0.4, 1, 0.4), spec = 32,  Ks = 0.1)
rock = Material(diffuse=(0,0,0), spec=32, Ks=0.2)
brick = Material(diffuse=(1,0.4,0.4), spec = 8,  Ks = 0.01)
drywall = Material(diffuse=(0.9, 0.9, 0.9), spec=16, Ks=0.1)
concrete_dark = Material(diffuse=(0.6, 0.6, 0.6), spec=16, Ks=0.2)
flowers= Material(texture=flowersTexture)

snow = Material(diffuse=(1,1,1), spec= 100, Ks= 0.1)
skin1= Material(diffuse=(0.8588, 0.5765, 0.3373), spec=32, Ks=0.1)
skin2= Material(diffuse=(0.9569, 0.6431, 0.3765), spec=32, Ks=0.1)
shirt = Material(diffuse=(0.1843, 0.3098, 0.3098), spec=200, Ks=0.2)
hair= Material(diffuse=(0.2353,0.1216,0.0667), spec=50, Ks=0.3)
eye = Material(diffuse=(0.4, 0.2, 0.1), spec=50, Ks=0.3)
blush= Material(diffuse=(0.9255, 0.5804, 0.4392), spec=1, Ks=0.5)
lips= Material(diffuse=(0.50196, 0, 0), spec=1, Ks=0.50)

redMirror = Material(diffuse=(0.8, 0.1, 0.1), spec=128, Ks=0.5, matType=REFLECTIVE)
grayMirror = Material(diffuse=(0.5, 0.5, 0.5), spec=128, Ks=0.9, matType=REFLECTIVE)
waterWithReflection = Material(diffuse=(0.4, 0.4, 1), spec=128, Ks=0.2, matType=REFLECTIVE)

glass = Material(diffuse=(0.9,0.9,0.9), spec = 64, Ks = 0.15, ior = 1.5, matType = TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9), spec = 64, Ks = 0.2, ior = 2.417, matType = TRANSPARENT)
dirtyGlass = Material(diffuse=(0.7, 0.7, 0.7), spec=32, Ks=0.05, ior=1.5, matType=TRANSPARENT)

#Figuras
#Circulo
rt.scene.append(Sphere(position=(0,0,-15), radius=6, material=flowers))

#Oreja izquierda
rt.scene.append(Sphere(position=(-1.4,0.5,-6), radius=0.6, material=skin2)) #Atras
rt.scene.append(Ellipsoid(position=(-1.25,0.5,-5.8), radii = (0.5, 0.4, 0.5), material=skin1)) #Adelante

#Arete izquiero
rt.scene.append(Sphere(position=(-1.4,-0.1,-5.6), radius=0.25, material=concrete_dark)) #Abajo
rt.scene.append(Sphere(position=(-1.3,-0.1,-5.3), radius=0.15, material=diamond)) #Arriba
rt.scene.append(Rectangle(position=(-1.4, 0.5, -5.5), normal=(0,0,1), width=0.1, height=0.5, material=glass)) #Palito
rt.scene.append(Ellipsoid(position=(-1.5, -1, -5.5), radii=(0.1, 0.3, 1), material=waterWithReflection)) #Piedra abajo

#Oreja derecha
rt.scene.append(Sphere(position=(1.4,0.5,-6), radius=0.6, material=skin2)) #Atras
rt.scene.append(Ellipsoid(position=(1.25,0.5,-5.8), radii = (0.5, 0.4, 0.5), material=skin1)) #Adelante

#Arete dercho
rt.scene.append(Sphere(position=(1.4,-0.1,-5.6), radius=0.25, material=concrete_dark)) #Abajo
rt.scene.append(Sphere(position=(1.3,-0.1,-5.3), radius=0.12, material=diamond)) #Arriba
rt.scene.append(Rectangle(position=(1.4, 0.5, -5.5), normal=(0,0,1), width=0.1, height=0.5, material=glass)) #Palito
rt.scene.append(Ellipsoid(position=(1.5, -1, -5.5), radii=(0.1, 0.3, 1), material=waterWithReflection)) #Piedra abajo

#Cara
rt.scene.append(Ellipsoid(position=(0,0.5,-5), radii = (1.2,1.5,1), material=skin1)) #Atras
rt.scene.append(Ellipsoid(position=(0, 0.5, -4.5), radii=(0.9, 1.2,1), material=skin2)) #Adelante

#Cuello
rt.scene.append(Cylinder(position=(0,-2,-6), height=3, radius=0.15, material=skin2)) 

#camisa
rt.scene.append(Ellipsoid(position=(0, -5, -7), radii=(2.8,3,1), material=shirt))
 
#Escote
rt.scene.append(Ellipsoid(position=(0,-4.5,-6.5), radii=(1.2,3,1), material=skin2))

#Collar
rt.scene.append(Ellipsoid(position=(0,-2.5,-6.2), radii=(0.7,0.9,1), material=redMirror)) #Primera linea
rt.scene.append(Ellipsoid(position=(0,-2.3,-6), radii=(0.55,0.8,1), material=skin2))
rt.scene.append(Ellipsoid(position=(0,-2.1,-5.9), radii=(0.5,0.7,1), material=redMirror)) #Segunda linea
rt.scene.append(Ellipsoid(position=(0,-1.9,-5.7), radii=(0.3,0.6,1), material=skin2))
rt.scene.append(Ellipsoid(position=(0,-1.5,-5.6), radii=(0.5,0.6,1), material=skin2))
rt.scene.append(Ellipsoid(position=(0,-2.15,-5.4), radii=(0.2,0.4,1), material=drywall)) #Piedra abajo
rt.scene.append(Ellipsoid(position=(0,-2,-5), radii=(0.1,0.07,1), material=dirtyGlass)) #Piedra arriba

#Pelo
rt.scene.append(Sphere(position=(-1,0.7,-4.3), radius=0.2, material=hair)) 
rt.scene.append(Sphere(position=(-1,1,-4.3), radius=0.25, material=hair)) 
rt.scene.append(Sphere(position=(-0.7,1.3,-4.3), radius=0.4, material=hair)) 
rt.scene.append(Sphere(position=(-0.3,1.8,-4.3), radius=0.4, material=hair)) 
rt.scene.append(Sphere(position=(0.35,1.8,-4.3), radius=0.4, material=hair))
rt.scene.append(Sphere(position=(0.5,1.5,-4.3), radius=0.4, material=hair))
rt.scene.append(Sphere(position=(0.9,1.25,-4.3), radius=0.4, material=hair)) 
rt.scene.append(Sphere(position=(1,1,-4.3), radius=0.25, material=hair)) 
rt.scene.append(Sphere(position=(1,0.7,-4.3), radius=0.2, material=hair)) 

#Facciones
rt.scene.append(Sphere(position=(-0.3,0.65,-3.5), radius=0.09, material=eye)) #Ojo izquierdo
rt.scene.append(Sphere(position=(0.3,0.65,-3.5), radius=0.09, material=eye)) #Ojo derecho
rt.scene.append(Sphere(position=(-0.48, 0.2,-3.5), radius=0.2, material=blush)) #Chapita izquierdo
rt.scene.append(Sphere(position=(0.48,0.2,-3.5), radius=0.2, material=blush)) #Chapita derecho
rt.scene.append(Ellipsoid(position=(0,-0.15,-3.5), radii=(0.3,0.08,1), material=lips)) #Boca
rt.scene.append(Rectangle(position=(0,0.05,-2), normal=(0,0,1), height=0.1, width=0.5, material=skin2))

#Cejas
rt.scene.append(Rectangle(position=(-0.2,-0.5,-2), normal=(0,0,1), height=0.05, width=0.25, material=hair)) #Derecha
rt.scene.append(Rectangle(position=(0.2,-0.5,-2), normal=(0,0,1), height=0.05, width=0.25, material=hair)) #Izquierda
rt.scene.append(Rectangle(position=(0,-0.5,-2), normal=(0,0,1), height=0.05, width=0.03, material=hair)) #Centro
rt.scene.append(Rectangle(position=(-0.04,-0.5,-2), normal=(0,0,1), height=0.05, width=0.03, material=hair)) #Centro Derecha
rt.scene.append(Rectangle(position=(0.04,-0.5,-2), normal=(0,0,1), height=0.05, width=0.03, material=hair)) #Centro Derecha

#Luces
rt.lights.append(AmbientLight(intensity=0.8))

rt.lights.append(DirectionalLight(direction=(1,1,0), intensity=0.7))
rt.lights.append(DirectionalLight(direction=(0,1,0), intensity=0.8))

rt.lights.append(PointLight(point=(0,-1, -3), intensity=0.9, color=(0.9569, 0.3922, 0.6471)))
rt.lights.append(PointLight(point=(-2,-4, -3), intensity=0.8, color=(1, 0.8431, 0)))

rt.rtClear()
rt.rtRender()

print("\nTiempo de renderizado:", pygame.time.get_ticks() / 1000, "segundos")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

rect = pygame.Rect(0,0, width, height)
sub= screen.subsurface(rect)
pygame.image.save(sub, "images/screenshot.jpg")

pygame.quit()


