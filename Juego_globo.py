import pygame as pg
from pygame.locals import *
import sys, os
import random

_fps = 60

class Ball(pg.sprite.Sprite):
    w= 46
    h=46
    #color = (255, 255, 255)
    velocidad = 2
    diry = 1
    dirx = 1
    contador = 0
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.getcwd()+'/assets/globo3.png')
        self.rect = self.image.get_rect()

    def avanza2(self, pause):
        if pause == False:
            self.y += self.diry * self.velocidad


            if self.y <= 0:
                self.y = 0

            if self.y >= 800 - self.h:
                self.y = 800 - self.h  
        

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
    
    def movimientoRotacion(self, angulo, soporte, pause):
        if pause == False:
            if self.y+46 >= soporte.y and angulo == 0:
                self.y = soporte.y - 46
                self.contador = 0
                self.x += random.choice([-1,1])
                
            #pendiente hacia la izquierda
            if angulo >= 1 and angulo <2:
                self.x += -1
                self.contador += -0.025
                self.y = soporte.y - 44 - self.contador   
                
            
            if angulo >= 2 and angulo <3:
                self.x += -2
                self.contador += -0.070
                self.y = soporte.y - 44 - self.contador
                
            
            if angulo >= 3 and angulo <4:
                self.x += -3
                self.contador += -0.15
                self.y = soporte.y - 42 -self.contador  
              

            if angulo >= 4 and angulo <=5:
                self.x += -4
                self.contador += -0.3
                self.y = soporte.y - 40 -self.contador    
            
            #pendiente hacia la derecha
            if angulo <= 359 and angulo >358:
                self.x += 1
                self.contador += -0.025
                self.y = soporte.y - 44 - self.contador   
            
            if angulo <= 358 and angulo >357:
                self.x += 2
                self.contador += -0.070
                self.y = soporte.y - 44 -self.contador     

            if angulo <= 357 and angulo >356:
                self.x += 3
                self.contador += -0.15
                self.y = soporte.y - 42 -self.contador    
           
            if angulo <= 356 and angulo >=355:
                self.x += 4
                self.contador += -0.3
                self.y = soporte.y - 40 -self.contador   
             

class Soporte(pg.Surface):
    x = 0
    y = 700
    w= 650
    h= 10
    color = (255, 0, 0)
    velocidad = 20
    diry = 1
    rotation_angle = 0
    def __init__(self):
        pg.Surface.__init__(self, (self.w, self.h))
        self.fill(self.color)

    def setColor(self, color):
        self.color = color
        self.fill(self.color)
    
    def avanza(self, pause):
        if pause == False:
            self.y += self.diry * self.velocidad
            if self.y <= 0:
                self.y = 0

            if self.y >= 800 - self.h:
                self.y = 800 - self.h
            
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Game:
    clock = pg.time.Clock()
    winner = None
    pause = False
    conmutador = True
    conmutador2 = True
    aumento = 0
    nivel = 0
    contadorVidas = 3
    mensajeVidas = False
    final = False
    movimiento = 0
    comienzo = False

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display
        self.screen = self.display.set_mode(self.size)
        self.screen.fill((25, 158, 218))  
        self.display.set_caption('Mi juego')
        
        self.ball = Ball()

        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.ball) 
        self.equilibrador = Soporte()
        self.equilibrador = self.equilibrador.convert_alpha()
        self.equilibrador_copy = self.equilibrador.copy()
        self.equilibrador.setColor((255, 0, 0))
       
       
        #Fuentes títulos
        self.fuente = pg.font.Font(os.getcwd()+'/assets/fontUNO.ttf', 28) 
        self.fuente2 = pg.font.Font(os.getcwd()+'/assets/fontUNO.ttf', 20)
        self.fuente3 = pg.font.Font(os.getcwd()+'/assets/fontUNO.ttf', 36)
        self.fuente4 = pg.font.Font(os.getcwd()+'/assets/fontUNO.ttf', 55)
        self.inicioPartida()


    def inicioPartida(self):
        self.ball.x = 264
        self.ball.y = 500
        self.rotation_angle = 0
        self.equilibrador = Soporte()
        self.equilibrador = self.equilibrador.convert_alpha()
        self.equilibrador_copy = self.equilibrador.copy()
        self.equilibrador.x = 0
        self.equilibrador.y = 720
        self.final = False
        self.winner = False
        
    
    def recalculate(self):
        self.ball.movimientoRotacion(self.rotation_angle, self.equilibrador, self.pause)
     
    def win(self, bola, circulo, radio):         
        if bola.x+23 >= circulo.x +10 and bola.x+23 <= circulo.x+(2*radio)-10 and bola.y+23 >= circulo.y+10 and bola.y+23 <= circulo.y+(2*radio)-10:
            self.winner = True
            self.pause = True
            if self.nivel == 5:
                self.nivel = 6

    def gameover(self):
        pg.quit()
        sys.exit()

    def handleevent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.gameover()
            # Controles:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.equilibrador.diry = -1
                    self.equilibrador.velocidad =10
                    self.equilibrador.avanza(self.pause)
                    
                if event.key == K_DOWN:
                    self.equilibrador.diry = 1
                    self.equilibrador.velocidad =10
                    self.equilibrador.avanza(self.pause)
                
                if event.key == K_SPACE and self.winner == True :        #Siguiente nivel
                    self.nivel += 1
                    self.inicioPartida()
                    self.winner = False
                    self.pause = False
                    
                if event.key ==  K_RETURN and self.pause == True and self.mensajeVidas == True:       # 1 vida menos
                    self.contadorVidas += -1
                    self.inicioPartida()
                    self.mensajeVidas = False
                    self.pause = False
                    if self.contadorVidas == 0:
                        self.contadorVidas = 3
                
                if event.key == K_p and self.winner == False:           #Parar el juego
                    if self.pause == False:
                        self.pause = True
                    else:
                        self.pause = False
                if event.key == K_x:           #Salir del juego
                    self.gameover()

                if event.key == K_LEFT: 
                    if self.pause == False:
                        if self.rotation_angle < 5 or self.rotation_angle >= 355 : 
                            # aumenta el ángulo de rotación 1 grado
                            self.rotation_angle += 1
                            # mantiene el ángulo de rotación en el rango [0, 360)
                            self.rotation_angle %= 360
                            
                            
                            self.equilibrador_copy = pg.transform.rotate(self.equilibrador, self.rotation_angle)
                    
                if event.key == K_RIGHT:
                    if self.pause == False:
                        if self.rotation_angle <= 5 or self.rotation_angle > 355:
                            # aumenta el ángulo de rotación 1 grado
                            self.rotation_angle += -1
                            # mantiene el ángulo de rotación en el rango [0, 360)
                            self.rotation_angle %= 360
                            
                            self.equilibrador_copy = pg.transform.rotate(self.equilibrador, self.rotation_angle)


        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_UP]:
            self.equilibrador.diry = -1
            if self.equilibrador.velocidad <=10:
                self.equilibrador.velocidad += 1
                self.equilibrador.avanza(self.pause)
        
        if keys_pressed[K_DOWN]:
            self.equilibrador.diry = 1
            if self.equilibrador.velocidad <=10:
                self.equilibrador.velocidad += 1
                self.equilibrador.avanza(self.pause)        

    def pantallaPrincipal(self):
        self.ball.x = 264
        self.ball.y = 230
        self.comienzo = True
        self.winner = True
        self.final = True  #para que no aparezca el Pause en pantalla
        self.pause = True  #para desactivar movimientos


        text1= '          Intenta llevar el globo \rhasta el interior del círculo ROJO'
        y= 80
        for i in text1.split("\r"):
            self.screen.blit(self.fuente3.render(i, 1, (255,255,0)),(25,y))
            y += 30      

        self.mensajeFinal2 = self.fuente2.render('(Si te sales o chocas con otros círculos pierdes 1 vida)', 1, (255,0,0))
        self.screen.blit(self.mensajeFinal2, (36, 155))

        text= 'Flechas:\r - <<ARRIBA>>, subir soporte \r - <<ABAJO>>, bajar soporte\r - <<DERECHA>>, inclinar soporte hacia la derecha \r - <<IZQUIERDA>>, inclinar soporte hacia la izquierda\r\rOpciones:\r<<P>>, parar/reactivar el juego\r<<X>>, salir del juego'
        y= 350
        for i in text.split("\r"):
            self.screen.blit(self.fuente2.render(i, 1, (255,255,255)),(25,y))
            y += 30        
        self.mensajeFinal = self.fuente3.render('Pulsa <<SPACE>> para comenzar!!', 1, (255,255,0))
        self.screen.blit(self.mensajeFinal, (25, 650))


    def circulos(self):
        self.comienzo = False
        self.radius1 = 40
        self.radius2 = 60
        self.radius3 = 80
      
        self.verde1e = pg.draw.circle(self.screen, (0,250,0), [480, 400], self.radius3, 4)
        self.verde2e = pg.draw.circle(self.screen, (0,250,0), [140, 400], self.radius3, 4)   
        self.rojo = pg.draw.circle(self.screen, (250,0,0), [150, 200], self.radius1, 10)
        
        self.choque(self.ball, self.verde1e, self.radius3)
        self.choque(self.ball, self.verde2e, self.radius3)

    def circulos1(self):
        self.radius1 = 40
        self.radius2 = 60
        self.radius3 = 80

        if self.conmutador == True and self.pause == False:
            self.aumento += 1
            if self.aumento >=50:
                self.conmutador = False

        if self.conmutador == False and self.pause == False:
            self.aumento += -1
            if self.aumento <= 0:
                self.conmutador = True
        
        if self.conmutador2 == True and self.pause == False:
            self.movimiento += 1
            if self.movimiento >= 600:
                self.conmutador2 = False

        if self.conmutador2 == False and self.pause == False:
            self.movimiento += -1
            if self.movimiento <= 50:
                self.conmutador2 = True
        

        self.radiusVAR = self.radius1 + self.aumento
        subaja = 0 + self.movimiento
        self.azul3 = pg.draw.circle(self.screen, (0,250,0), [60, subaja], self.radius1, 4) 
        self.verde1 = pg.draw.circle(self.screen, (0,250,0), [190, 360], self.radius1, 4) 
        self.azul2 = pg.draw.circle(self.screen, (0,0,250), [340, 240], self.radiusVAR, 4)
        self.verde3 = pg.draw.circle(self.screen, (0,250,0), [140, 640], self.radius3, 4)
        self.azul1 = pg.draw.circle(self.screen, (0,0,250), [440, 480], self.radiusVAR, 4)   
        self.rojo = pg.draw.circle(self.screen, (250,0,0), [200, 270], self.radius1, 10)

        self.choque(self.ball, self.azul3, self.radius1)
        self.choque(self.ball, self.verde1, self.radius1)
        self.choque(self.ball, self.azul2, self.radiusVAR)
        self.choque(self.ball, self.verde3, self.radius3)
        self.choque(self.ball, self.azul1, self.radiusVAR)

    def circulos2(self):
        self.radius1 = 40
        self.radius2 = 60
        self.radius3 = 80
        
        if self.conmutador == True and self.pause == False:
            self.aumento += 1
            if self.aumento >=50:
                self.conmutador = False

        if self.conmutador == False and self.pause == False:
            self.aumento += -1
            if self.aumento <= 0:
                self.conmutador = True


        if self.conmutador2 == True and self.pause == False:
            self.movimiento += 2
            if self.movimiento >= 200:
                self.conmutador2 = False

        if self.conmutador2 == False and self.pause == False:
            self.movimiento += -2
            if self.movimiento <= -100:
                self.conmutador2 = True
        
        self.radiusVAR = self.radius1 + self.aumento
        self.subaja = 480 + self.movimiento

        self.verde5b = pg.draw.circle(self.screen, (0,0,250), [200+self.movimiento, 200], self.radius2, 4) 
        self.verde1b = pg.draw.circle(self.screen, (0,0,250), [140, 540], self.radius3, 4) 
        self.verde2b = pg.draw.circle(self.screen, (0,0,250), [340, 340], self.radius1, 4) 
        self.verde3b = pg.draw.circle(self.screen, (0,0,250), [440, self.subaja], self.radiusVAR, 4)
        self.verde4b = pg.draw.circle(self.screen, (0,0,250), [40, 240], self.radius3, 4)   
        self.rojo = pg.draw.circle(self.screen, (250,0,0), [200, 100], self.radius1, 10)

        self.choque(self.ball, self.verde5b, self.radius2)
        self.choque(self.ball, self.verde1b, self.radius3)
        self.choque(self.ball, self.verde2b, self.radius1)
        self.choque(self.ball, self.verde3b, self.radiusVAR)
        self.choque(self.ball, self.verde4b, self.radius3)
        
    def circulos3(self):
        self.radius1 = 40
        self.radius2 = 60
        self.radius3 = 80
        
        if self.conmutador == True and self.pause == False:
            self.aumento += 1
            if self.aumento >=40:
                self.conmutador = False

        if self.conmutador == False and self.pause == False:
            self.aumento += -1
            if self.aumento <= 0:
                self.conmutador = True
        
        if self.conmutador2 == True and self.pause == False:
            self.movimiento += 2
            if self.movimiento >= 200:
                self.conmutador2 = False

        if self.conmutador2 == False and self.pause == False:
            self.movimiento += -2
            if self.movimiento <= -100:
                self.conmutador2 = True

        self.radiusVAR = self.radius3 + self.aumento
        self.verde1a = pg.draw.circle(self.screen, (250,0,250), [110, 140+self.movimiento], self.radius2, 4)
        self.verde2a = pg.draw.circle(self.screen, (250,0,250), [240, 240], self.radiusVAR, 4)
        self.verde3a = pg.draw.circle(self.screen, (250,0,250), [340, 340], self.radiusVAR, 4)
        self.verde4a = pg.draw.circle(self.screen, (250,0,250), [440, 460+self.movimiento], self.radius2, 4) 
        self.rojo = pg.draw.circle(self.screen, (250,0,0), [200, 70], self.radius1, 10)

        self.choque(self.ball, self.verde1a, self.radius2)
        self.choque(self.ball, self.verde2a, self.radiusVAR)
        self.choque(self.ball, self.verde3a, self.radiusVAR)
        self.choque(self.ball, self.verde4a, self.radius2)

    def circulos4(self):
        self.radius1 = 40
        self.radius2 = 60
        self.radius3 = 80
        
        if self.conmutador == True and self.pause == False:
            self.aumento += 1
            if self.aumento >=50:
                self.conmutador = False

        if self.conmutador == False and self.pause == False:
            self.aumento += -1
            if self.aumento <= 0:
                self.conmutador = True
        
        if self.conmutador2 == True and self.pause == False:
            self.movimiento += 2
            if self.movimiento >= 200:
                self.conmutador2 = False

        if self.conmutador2 == False and self.pause == False:
            self.movimiento += -2
            if self.movimiento <= -100:
                self.conmutador2 = True

        self.radiusVAR = self.radius1 + self.aumento
        self.subaja = 400 + self.movimiento
        self.verde12 = pg.draw.circle(self.screen, (0,250,250), [140, 540], self.radius3, 4) 
        self.verde13 = pg.draw.circle(self.screen, (250,0,250), [340+self.movimiento, 340], self.radius1, 4) 
        self.verde14 = pg.draw.circle(self.screen, (255,233,0), [440, self.subaja], self.radiusVAR, 4)
        self.verde4 = pg.draw.circle(self.screen, (0,250,250), [340, 200], self.radius1, 4)
        self.verde8 = pg.draw.circle(self.screen, (0,0,250), [240, 340], self.radius1, 4) 
        self.verde9 = pg.draw.circle(self.screen, (0,0,250), [440, 480], self.radiusVAR, 4)
        self.verde10 = pg.draw.circle(self.screen, (0,0,250), [70, 360], self.radiusVAR, 4)
        self.verde11= pg.draw.circle(self.screen, (0,0,250), [40, 240], self.radius3, 4)   
        self.rojo = pg.draw.circle(self.screen, (250,0,0), [200, 70], self.radius1, 10)

        self.choque(self.ball, self.verde12, self.radius3)
        self.choque(self.ball, self.verde13, self.radius1)
        self.choque(self.ball, self.verde14, self.radiusVAR)
        self.choque(self.ball, self.verde4, self.radius1)
        self.choque(self.ball, self.verde8, self.radius1)
        self.choque(self.ball, self.verde9, self.radiusVAR)
        self.choque(self.ball, self.verde10, self.radiusVAR)
        self.choque(self.ball, self.verde11, self.radius3)  
    

    def pantallaFinal(self):
        self.mensajeFinal = self.fuente.render('Enhorabuena, has superado todos los niveles!', 1, (255,255,255))
        self.screen.blit(self.mensajeFinal, (5, 240))

        self.mensajeFinal2 = self.fuente2.render('Pulsa <<X>> para salir', 1, (255,255,255))
        self.screen.blit(self.mensajeFinal2, (195, 420))
        self.final = True
        self.pause = True
        self.ball6 = Ball()
        self.ball1 = Ball()
        self.ball2 = Ball()
        self.ball3 = Ball()
        self.ball4 = Ball()
        self.ball5 = Ball()

        self.allSprites.add(self.ball6)
        self.allSprites.add(self.ball1) 
        self.allSprites.add(self.ball2) 
        self.allSprites.add(self.ball3) 
        self.allSprites.add(self.ball4)  
        self.allSprites.add(self.ball5)

        self.ball6.x = 80
        self.ball1.x = 160
        self.ball2.x = 240
        self.ball3.x = 320
        self.ball4.x = 400
        self.ball5.x = 480
        
        self.ball6.y = 300
        self.ball1.y = 300
        self.ball2.y = 300
        self.ball3.y = 300
        self.ball4.y = 300
        self.ball5.y = 300

    def render(self):
        self.screen.fill((25, 158, 218))
        self.marcadorVidas = self.fuente.render('VIDAS: {}'.format(self.contadorVidas), 1, (255,255,255))
        caja = self.marcadorVidas.get_rect()
        self.screen.blit(self.marcadorVidas, ( 584 -caja.w, 8))

        if self.nivel <6:
            self.marcadorNivel = self.fuente.render('Nivel {}'.format(self.nivel), 1, (255,255,255))
            self.screen.blit(self.marcadorNivel, ( 16, 8))

        #sprites
        self.allSprites.update()    #solo Ball()
        self.allSprites.draw(self.screen)
       
        self.screen.blit(self.equilibrador_copy, (self.equilibrador.x, self.equilibrador.y))
        
        #NIVELES
        if self.nivel == 0:
            self.pantallaPrincipal()
        if self.nivel == 1:
            self.circulos()
        if self.nivel == 2:
            self.circulos1()
        if self.nivel == 3:
            self.circulos2()
        if self.nivel == 4:
            self.circulos3()
        if self.nivel == 5:
            self.circulos4()
        if self.nivel == 6:
            self.pantallaFinal()
        
        if self.nivel >= 1:
            self.win(self.ball, self.rojo, self.radius1)
        if self.pause == True and self.winner == False and self.mensajeVidas == False and self.final== False:
            self.parada = self.fuente.render('PAUSE', 1, (255,255,255))
            self.screen.blit(self.parada, ( 265, 230))
    
            text= 'Flechas:\r - <<ARRIBA>>, subir soporte \r - <<ABAJO>>, bajar soporte\r - <<DERECHA>>, inclinar soporte hacia la derecha \r - <<IZQUIERDA>>, inclinar soporte hacia la izquierda\r\r<<P>>, parar/reactivar el juego\r<<X>>, salir del juego'
            ya= 300
            for i in text.split("\r"):
                self.screen.blit(self.fuente2.render(i, 1, (255,255,255)),(25,ya))
                ya += 30 


        if self.winner and self.comienzo == False and self.nivel < 6:
            text= "                       Enhorabuena!!\rPulsa <<SPACE>> para ir al siguiente nivel"
            ya= 200
            for i in text.split("\r"):
                self.screen.blit(self.fuente.render(i, 1, (255,255,0)),(25,ya))
                ya += 40 

        self.ball.avanza2(self.pause)


    def choque(self, bola, circulo, radio):
        #if(bola.x+23 in range(circulo.x-radio-23,circulo.x+radio+23)) and (bola.y+23 in range(circulo.y-radio-23,circulo.y+radio+23)):       #no va
        #if bola.x+23 >= circulo.x-radio and bola.x+23 <= circulo.x+radio and bola.y+23 >= circulo.y-radio and bola.y+23 <= circulo.y+radio:  malo
        #if bola.x+23 >= circulo.x and bola.x+23 <= circulo.x+(2*radio) and bola.y+23 >= circulo.y and bola.y+23 <= circulo.y+(2*radio):
        #if (bola.x+23, bola.y+23) <= (circulo.x+radio+23, circulo.y+radio+23):
        #if between(bola.y+23, circulo.y-radio-23, circulo.y+radio+23) and between(bola.x+23, circulo.x-radio-23, circulo.x+radio+23):
        if bola.x <= -7:
                self.pause = True
                self.mensajeVidas = True
                

        if bola.x >= 607 - bola.h:
            self.pause = True
            self.mensajeVidas = True

        
        if bola.x+46 >= circulo.center[0]-(radio- radio/3) and bola.x <= circulo.center[0]+(radio- radio/3) and bola.y+46 >= circulo.center[1]-(radio- radio/3) and bola.y <= circulo.center[1]+(radio- radio/3):
        
            #print('X = {}, Y = {}'.format(bola.x, bola.y))
            #print('circulo +X = {}, +Y = {}'.format(circulo.center[0]+(radio- radio/10), circulo.center[1]+(radio- radio/10)))
            #print('circulo -X = {}, -Y = {}'.format(circulo.center[0]-(radio- radio/10), circulo.center[1]-(radio- radio/10)))
            #print(circulo)
            self.pause = True
            self.mensajeVidas = True
                       
    

    def comprobarChoque(self):
        '''
        if self.nivel == 1:
            self.choque(self.ball, self.verde1e, self.radius3)
            self.choque(self.ball, self.verde2e, self.radius3)
        if self.nivel == 2:
            self.choque(self.ball, self.azul3, self.radius1)
            self.choque(self.ball, self.verde1, self.radius1)
            self.choque(self.ball, self.azul2, self.radiusVAR)
            self.choque(self.ball, self.verde3, self.radius3)
            self.choque(self.ball, self.azul1, self.radiusVAR)
        if self.nivel == 3:
            self.choque(self.ball, self.verde5b, self.radius2)
            self.choque(self.ball, self.verde1b, self.radius3)
            self.choque(self.ball, self.verde2b, self.radius1)
            self.choque(self.ball, self.verde3b, self.radiusVAR)
            self.choque(self.ball, self.verde4b, self.radius3)
        if self.nivel == 4:
            self.choque(self.ball, self.verde1a, self.radiusVAR)
            self.choque(self.ball, self.verde2a, self.radiusVAR)
            self.choque(self.ball, self.verde3a, self.radiusVAR)
            self.choque(self.ball, self.verde4a, self.radiusVAR)
        if self.nivel == 5:
            self.choque(self.ball, self.verde12, self.radius3)
            self.choque(self.ball, self.verde13, self.radius1)
            self.choque(self.ball, self.verde14, self.radiusVAR)
            self.choque(self.ball, self.verde4, self.radius1)
            self.choque(self.ball, self.verde8, self.radius1)
            self.choque(self.ball, self.verde9, self.radiusVAR)
            self.choque(self.ball, self.verde10, self.radiusVAR)
            self.choque(self.ball, self.verde11, self.radius3)''' 
    
        if self.mensajeVidas == True and self.contadorVidas > 2:
            self.frase1 = self.fuente.render("Te quedan {} vidas,".format(self.contadorVidas-1), 1, (255,255,0))          
            self.screen.blit(self.frase1, (185,200))
            self.frase2 = self.fuente.render("Pulsa <<ENTER>> para continuar", 1, (255,255,0))
            self.screen.blit(self.frase2, (105,270))

        if self.mensajeVidas == True and self.contadorVidas == 2:
            self.frase3 = self.fuente.render("Te queda {} vida,".format(self.contadorVidas-1), 1, (255,255,0))
            self.screen.blit(self.frase3, (185,200))
            self.frase2 = self.fuente.render("pulsa <<ENTER>> para continuar", 1, (255,255,0))
            self.screen.blit(self.frase2, (105,270))

        if self.mensajeVidas == True and self.contadorVidas == 1:
            self.frase = self.fuente4.render("GAME OVER", 1, (255,255,0))
            self.screen.blit(self.frase, (150,100))

            text= "pulsa <<ENTER>> para empezar de nuevo\r                                 o \r             <<X>> para salir del juego"
            ya= 200
            for i in text.split("\r"):
                self.screen.blit(self.fuente.render(i, 1, (255,255,0)),(32,ya))
                ya += 40 

            self.nivel = 1
            

    def start(self):
        while True:
            self.clock.tick(_fps)
            self.render()
            self.recalculate()
            self.comprobarChoque()
            #controles
            self.handleevent()
            #bola dentro del ciruclo correcto
            self.display.flip()

if __name__ == '__main__':
    pg.init()
    game = Game(600, 800)
    game.start()