import pygame
from pygame.locals import *
from random import randint
from screen import *
import time

class Point:
    def __init__( self, x, y, z ):
        self.__str__ = lambda: "(%s, %s, %s)" % ( x, y, z )
        self.x = x
        self.y = y
        self.z = z

    def rel_to( self, point ):
        x = self.move( point.z, point.x, self.z, self.x )
        y = self.move( point.z, point.y, self.z, self.y )
        return ( x, y )

    def move( self, viewer_d, displacement, object_d, object_h ):
        over  = object_h * viewer_d + object_d * displacement
        under = object_d + viewer_d + 1
        return over / under

def make_square( top_left, bottom_right, z ):
    ( a, b ) = top_left
    ( c, d ) = bottom_right
    return [ Point( a, b, z ), Point( b, c, z ), Point( c, d, z ), Point( d, a, z ) ]

def make_squares( top_left, bottom_right, separation ):
    squares = []
    for i in range( 0, 10 ):
        squares.append( make_square( top_left, bottom_right, i * separation ) )
    return squares

def output( screen, p, xss ):
    screen.fill( 0 )
    for xs in xss:
        ps = []
        for x in xs:
            ps.append( x.rel_to( p ) )
        pygame.draw.polygon( screen, ( 255, 255, 255 ), ps, 1 )
    output_toolbar( screen )
    pygame.display.flip()

pygame.init()

my_font = pygame.font.SysFont( pygame.font.get_default_font(), 20 )

def output_toolbar( screen ):
    global my_font
    pygame.draw.rect( screen, ( 205, 205, 205 ), ( ( 0, 400 ), ( 400, 440 ) ), 0 )
    text = my_font.render( str( pygame.mouse.get_pos() ), True, ( 0, 0, 0 ) )
    screen.blit( text, ( 300, 410 ) )

if '__main__' == __name__:
    running = True
    width, height = 400, 440
    screen = pygame.display.set_mode( ( width, height ) )
    update = pygame.display.flip
    all_sqs = make_squares( ( 0, 0 ), ( width, width ), 10 )
    origin = Point( width / 2, height / 2, 100 )
    while running:
        for event in pygame.event.get():
            if QUIT == event.type:
                running = False
        pressed, _, _ = pygame.mouse.get_pressed()
        if pressed:
            x, y = pygame.mouse.get_pos()
            all_sqs.append( [ Point( x, y, 0 ), Point( x, y, 0 ) ] )
        # output( screen, pygame.mouse.get_pos(), all_sqs )
        output( screen, origin, all_sqs )
