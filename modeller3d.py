import pygame
from pygame.locals import *
from random import randint
from screen import *
import time

from polygon import Polygon
from actions import Actions
from point import Point

class Model:
    """Immutable"""
    def __init__( self, size, origin = None, z = 0 ):
        self.x, self.y = size
        self.z = z
        self.grid = self.make_squares( 10, ( 0, 0 ), ( self.x, self.y ), 10 )
        self.origin = Point( self.x / 2, self.y / 2, 100 ) if None == origin else origin
        self.font = pygame.font.SysFont( pygame.font.get_default_font(), 20 )

    def forward( self, z ):
        return Model( ( self.x, self.y ), self.origin, self.z - z )

    def back( self, z ):
        return Model( ( self.x, self.y ), self.origin, self.z + z )

    def nudge( self, magnitude ):
        x_, y_ = magnitude
        x, y, z = self.origin.x, self.origin.y, self.origin.z
        return Model( ( self.x, self.y ), Point( x + x_, y + y_, z ), self.z )

    def output( self, screen, polygons ):
        # TODO polygons also need colour
        screen.fill( 0 )
        self.output_polygons( screen, self.grid, 1 )
        self.output_polygons( screen, polygons, 0 )
        # TODO highlight most recent mark
        if len( polygons ) > 0 and polygons[ -1 ].num_points() > 0:
            last = polygons[ -1 ]
            p = last.get_points()[ -1 ]
            x, y = Point( p.x, p.y, p.z - self.z ).rel_to( self.origin )
            colour = ( 255, 0, 0 ) if last.is_open() else ( 0, 255, 0 )
            pygame.draw.line( screen, colour, ( x - 2, y - 2 ), ( x + 2, y + 2 ), 1 )
            pygame.draw.line( screen, colour, ( x + 2, y - 2 ), ( x - 2, y + 2 ), 1 )
        self.output_toolbar( screen )
        pygame.display.flip()

    def output_polygons( self, screen, polygons, w ):
        for polygon in polygons:
            points = []
            for p in polygon.get_points():
                points.append( Point( p.x, p.y, p.z - self.z ).rel_to( self.origin ) )
            if len( points ) == 1:
                screen.set_at( points[ 0 ], polygon.get_colour() )
            elif len( points ) == 2:
                pygame.draw.line( screen, polygon.get_colour(), points[ 0 ], points[ 1 ], 1 )
            else:
                pygame.draw.polygon( screen, polygon.get_colour(), points, polygon.get_width() )

    def make_square( self, top_left, bottom_right, z ):
        a, b = top_left
        c, d = bottom_right
        square = Polygon( ( 255, 255, 255 ) ).add( Point( a, b, z ) ) \
            .add( Point( b, c, z ) ).add( Point( c, d, z ) ) \
            .add( Point( d, a, z ) )
        square.set_width( 1 )
        return square

    def make_squares( self, n, top_left, bottom_right, separation ):
        squares = []
        for i in range( 0, n ):
            squares.append( self.make_square( top_left, bottom_right, i * separation + self.z ) )
        return squares

    def output_toolbar( self, screen ):
        pygame.draw.rect( screen, ( 205, 205, 205 ), ( ( 0, 400 ), ( 400, 440 ) ), 0 )
        x, y = pygame.mouse.get_pos()
        text = self.font.render( str( ( x, y, self.z ) ), True, ( 0, 0, 0 ) )
        screen.blit( text, ( 300, 410 ) )

def write_objects( filename, objects ):
    with open( filename, 'w' ) as f:
        f.write( str( len( objects ) ) + "\n" )
        for polygon in objects:
            lines = polygon.write()
            for line in lines:
                f.write( line + "\n" )

def load_objects( filename ):
    polygons = []
    with open( filename, 'r' ) as f:
        lines = f.readlines()[ 1 : ] # ignore num_objects
        while len( lines ) > 0:
            c = lines.pop( 0 ).split()
            polygon = Polygon( ( int( c[ 0 ] ), int( c[ 1 ] ), int( c[ 2 ] ) ) )
            num_ps = int( lines.pop( 0 ) )
            for i in range( 0, num_ps ):
                magnitudes = map( int, lines.pop( 0 ).split() )
                polygon.add( Point( *magnitudes ) )
            polygons.append( polygon )
    return polygons

if '__main__' == __name__:
    pygame.init()
    running = True
    width, height = 400, 400
    model   = Model( ( width, height ) )
    screen  = pygame.display.set_mode( ( width, height + 40 ) )
    objects = [ ]
    actions = Actions()
    leftClick = rightClick = False
    z = 0
    while running:
        for event in pygame.event.get():
            if QUIT == event.type:
                running = False
            elif KEYUP == event.type:
                if K_u == event.key:
                    if actions.can_undo():
                        actions.undo()
                elif K_r == event.key:
                    if actions.can_redo():
                        actions.redo()
                elif K_ESCAPE == event.key:
                    running = False
                elif K_RETURN == event.key:
                    actions.do( \
                        ( objects[ -1 ].close, [] ), \
                        ( objects[ -1 ].open, [] ) \
                    )
                elif K_UP    == event.key: model = model.nudge( ( 0, -10 ) )
                elif K_RIGHT == event.key: model = model.nudge( ( 10, 0 ) )
                elif K_DOWN  == event.key: model = model.nudge( ( 0, 10 ) )
                elif K_LEFT  == event.key: model = model.nudge( ( -10, 0 ) )
                elif K_q == event.key: model = Model( ( width, height ) )
                elif K_k == event.key:
                    model = model.back( 10 )
                    z += 10
                elif K_j == event.key:
                    model = model.forward( 10 )
                    z -= 10
                elif K_w == event.key:
                    write_objects( '../out.3d', objects )
                    print "Written!"
                elif K_l == event.key:
                    objects = load_objects( '../out.3d' )
                    print "Loaded!"
            elif MOUSEBUTTONUP == event.type:
                x, y = pygame.mouse.get_pos()
                if leftClick:
                    if len( objects ) > 0 and objects[ -1 ].is_open():
                        actions.do( \
                            ( objects[ -1 ].add, [ Point( x, y, z ) ] ), \
                            ( objects[ -1 ].remove, [ Point( x, y, z ) ] ) \
                        )
                    else:
                        actions.do( \
                            ( lambda a: objects.append( a ), [ Polygon( ( 100, 100, ( 200 + z * 2 ) % 255 ) ).add( Point( x, y, z ) ) ] ), \
                            ( objects.pop, [] ) \
                        )
                elif rightClick and objects[ -1 ].is_open():
                    actions.do( \
                        ( lambda a: objects[ -1 ].add( a ).close(), [ Point( x, y, z ) ] ), \
                        ( lambda a: objects[ -1 ].remove( a ).open(), [ Point( x, y, z ) ] ) \
                    )
        leftClick, _, rightClick = pygame.mouse.get_pressed()
        model.output( screen, objects )
