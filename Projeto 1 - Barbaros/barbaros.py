# -*- coding: cp1252 -*-
# MC504 - Sistemas Operacionais
# Projeto 1 - Animacao de um problema envolvendo Threads
# Problema escolhido: "O jantar dos selvagens"
# Grupo: Arthur Alvarez (RA 116180) e Pedro Figueiredo (RA 123198)

from threading import Thread, Lock
import time
import os
import random

import sys, pygame
from pygame.locals import *

##Definicao da Thread com os grafícos para animacao
class Graphics(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self): #Funcao a ser executada pela Thread ao ser criada
        pygame.init()

        self.bgim = "background.png"
        self.ayla0 = "ayla0.png"
        self.kino0 = "kino0.png"
        self.cook0 = "cook0.png"
        self.filled_pot = "filled_pot.png"
        self.empty_pot = "empty_pot.png"

        self.size = width, height = 1024, 768
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
        self.waitTime = 5

        self.background = pygame.image.load(self.bgim).convert()

        self.cook0 = pygame.image.load(self.cook0).convert_alpha()
        self.cook0_rect = self.cook0.get_rect()
        self.cook0 = pygame.transform.scale(self.cook0, (80, 116))
        self.cook0_rect.x = 200
        self.cook0_rect.y = 50

        self.filled_pot = pygame.image.load(self.filled_pot).convert_alpha()
        self.filled_pot_rect = self.filled_pot.get_rect()
        self.filled_pot = pygame.transform.scale(self.filled_pot, (160, 124))
        self.filled_pot_rect.x = 600
        self.filled_pot_rect.y = 175

        self.empty_pot = pygame.image.load(self.empty_pot).convert_alpha()
        self.empty_pot_rect = self.empty_pot.get_rect()
        self.empty_pot = pygame.transform.scale(self.empty_pot, (160, 124))
        self.empty_pot_rect.x = 600
        self.empty_pot_rect.y = 175

        self.ayla0 = pygame.image.load(self.ayla0).convert_alpha()
        self.ayla0_rect = self.ayla0.get_rect()
        self.ayla0 = pygame.transform.scale(self.ayla0, (64, 128))

        self.kino0 = pygame.image.load(self.kino0).convert_alpha()
        self.kino0_rect = self.kino0.get_rect()
        self.kino0 = pygame.transform.scale(self.kino0, (64, 128))

        global N
        self.barbaro = []
        self.barbaro_rect = []
        for i in range(0,N):
            r = random.randrange(0,2)
            if r == 0:
                self.barbaro.append(self.ayla0)
            else:
                self.barbaro.append(self.kino0)
            self.barbaro_rect.append(self.barbaro[i].get_rect())
            self.barbaro_rect[i].x = 512
            self.barbaro_rect[i].y = 768 - 550+i*128

        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        self.potIsFilled = True
        self.font = pygame.font.Font("ArialBlack.ttf", 32)

        self.reconstructScenery(self.potIsFilled)
        pygame.display.flip()

        global graphicsAreInitialized
        graphicsAreInitialized = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    os._exit(1)
                    sys.exit()
            self.reconstructScenery(self.potIsFilled)
            pygame.display.flip()
            

    def reconstructScenery(self, isPotFilled):
        self.screen.blit(self.background, (0,0))
        if isPotFilled:
            self.screen.blit(self.filled_pot, self.filled_pot_rect)
        else:
            self.screen.blit(self.empty_pot, self.empty_pot_rect)
        for i in range (0, N):
            self.screen.blit(self.barbaro[i], self.barbaro_rect[i])
        self.screen.blit(self.cook0, self.cook0_rect)
        text = self.font.render("Porcoes: " + str(servings), True, (0, 0, 128))
        self.screen.blit(text, (800 - text.get_width() // 2, 80 - text.get_height() // 2))
        text = self.font.render("Numero de Barbaros: " + str(N), True, (0, 0, 128))
        self.screen.blit(text, (800 - text.get_width() // 2, 50 - text.get_height() // 2))

    def goToPotAnimation (self):
        for i in range(0,70):
            self.barbaro_rect[0].x += 2
            pygame.time.wait(self.waitTime)

    def leavePot (self):
        global N
        for i in range(0,(N*128)/2):
            self.barbaro_rect[0].y += 2
            pygame.time.wait(self.waitTime)
        for i in range(0,70):
            self.barbaro_rect[0].x -= 2
            pygame.time.wait(self.waitTime)
            
        aux = self.barbaro[0]
        aux_rect = self.barbaro_rect[0]
        for i in range(0,N-1):
            self.barbaro[i] = self.barbaro[i+1]
            self.barbaro_rect[i] = self.barbaro_rect[i+1]
        self.barbaro[N-1] = aux
        self.barbaro_rect[N-1] = aux_rect
        for i in range (0, 64):
            for i in range(0,N):
                self.barbaro_rect[i].y -= 2
            pygame.time.wait(self.waitTime)

    def refillPot (self):
        global servings
        for i in range(0,200):
            self.cook0_rect.x += 2
            pygame.time.wait(self.waitTime)
        pygame.time.wait(500)
        self.potIsFilled = True
        servings = M
        pygame.time.wait(300)
        for i in range(0,200):
            self.cook0_rect.x -= 2
            pygame.time.wait(self.waitTime)

    def changePotSpriteToEmpty(self):
        self.potIsFilled = False
        print "Pote esta vazio"
                    
    def changePotSpriteToFilled(self):
        self.potIsFilled = True
        print "Pote esta cheio"
                    

##Definicao da Thread Barbaro 
class Barbaro(Thread):
    def __init__(self, n, graphics):
        Thread.__init__(self)
        self.n = n
        self.graphics = graphics
        
    def run(self): #Funcao a ser executada pela Thread ao ser criada
        while True:
            mutex.acquire()
            self.goToPot()
            if servings == 0:
                emptyPot.release()
                fullPot.acquire()
            self.getServingFromPot()
            self.eat()
            mutex.release()

    def goToPot(self):
        #Barbaro vai ate o pote
        global servings
        print "Barbaro", self.n, "se dirige ao pote, porcoes =", servings
        Graphics.goToPotAnimation(self.graphics)
        time.sleep(2)

    def getServingFromPot(self):
        #Barbaro pega uma porcao
        print "Barbaro", self.n, "esta se servindo"
        global servings
        servings = servings - 1
        if (servings == 0):
            Graphics.changePotSpriteToEmpty(self.graphics)
        time.sleep(2)
        
    def eat(self):
        #Barbaro come a comida
        print "Barbaro", self.n, "comeu e esta voltando para a fila"
        print ""
        Graphics.leavePot(self.graphics)
        time.sleep(2)
        #E volta para a fila

##Definicao da Thread Cozinheiro
class Cozinheiro(Thread):
    def __init__(self, graphics):
        Thread.__init__(self)
        self.graphics = graphics
        
    def run(self): #Funcao a ser executada pela Thread ao ser criada
        while True:
            emptyPot.acquire()
            self.putServingsInPot()
            fullPot.release()

    def putServingsInPot(self):
        #Cozinheiro anda ate o pote
        #Fica la um pouco
        print "(!) Cozinheiro esta botando comida, agora porcoes =", servings
        Graphics.refillPot(self.graphics)
        time.sleep(2)
        #E volta para sua posicao


## Inicio da execucao do programa

if(len(sys.argv) != 5):
    print "ERRO: Numero incorreto de parametros (Leia a documentacao)"
    sys.exit(1)

graphicsAreInitialized = False

# Criacao dos mutexes
mutex = Lock()
emptyPot = Lock()
fullPot = Lock()

# Criacao de variaveis
N = int(sys.argv[2]) # Numero de selvagens na cena
M = int(sys.argv[4]) #Numero de refeicoes maximo do pote
servings = M #Variavel que representa o pote

# Mutex de emptyPot e fullPot comecam trancados
emptyPot.acquire()
fullPot.acquire()

#os.system("cls") #limpaTela no windows
#os.system("clear") #limpaTela no Linux
print "** Jantar dos selvagens para", N, "barbaros e", M, "porcoes no pote **"
print ""
print "INICIO"
print "-------------------------"
print "Pote comeca com",M,"porcoes"
print "-------------------------"
print ""

# pygame
g = Graphics()
g.start()

print "Initializing Graphics"

while not graphicsAreInitialized:
    pass
print "Graphics Initialized"

# Criacao da thread cozinheiro
thr = Cozinheiro(g)
thr.start()

# Criacao de N threads do tipo Barbaro
for a in range(N):
    thr = Barbaro(a+1, g)
    thr.start()
