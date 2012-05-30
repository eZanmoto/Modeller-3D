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
    def __init__( self, size, observer, position = None ):
        self.font_colour = ( 0, 0, 0 )
        self.width, self.height = size
        if None == position:
            self.position = Point( 0, 0, 0 )
        else:
            self.position = position
        self.observer = observer
        self.grid = self.make_squares( 10, ( 0, 0 ), ( self.width, self.width ), 10 )
        self.mag = 10
        self.font = pygame.font.SysFont( "monospace", 12 )

    def move( self, move_function ):
        x, y, z = self.position.as_tuple()
        new_position = move_function( x, y, z )
        return Model( ( self.width, self.height ), self.observer, new_position )

    def move_up( self ):
        return self.move( lambda x, y, z: Point( x, y - self.mag, z ) )

    def move_right( self ):
        return self.move( lambda x, y, z: Point( x + self.mag, y, z ) )

    def move_down( self ):
        return self.move( lambda x, y, z: Point( x, y + self.mag, z ) )

    def move_left( self ):
        return self.move( lambda x, y, z: Point( x - self.mag, y, z ) )

    def move_forward( self ):
        return self.move( lambda x, y, z: Point( x, y, z + self.mag ) )

    def move_back( self ):
        return self.move( lambda x, y, z: Point( x, y, z - self.mag ) )

    def update_observer( self, observer ):
        return Model( ( self.width, self.height ), observer, self.position )

    def output( self, screen, mode, polygons ):
        # TODO polygons also need colour
        screen.fill( 0 )
        self.output_polygons( screen, self.grid, 1 )
        self.output_polygons( screen, polygons, 0 )
        # TODO highlight most recent mark
        if len( polygons ) > 0 and polygons[ -1 ].num_points() > 0:
            last = polygons[ -1 ]
            p = last.get_points()[ -1 ]
            x, y = Point( p.x - self.position.x, p.y - self.position.y, p.z - self.position.z ).rel_to( self.observer )
            colour = ( 255, 0, 0 ) if last.is_open() else ( 0, 255, 0 )
            pygame.draw.line( screen, colour, ( x - 2, y - 2 ), ( x + 2, y + 2 ), 1 )
            pygame.draw.line( screen, colour, ( x + 2, y - 2 ), ( x - 2, y + 2 ), 1 )
        self.output_toolbar( screen, mode )
        pygame.display.flip()

    def output_polygons( self, screen, polygons, w ):
        for polygon in polygons:
            points = []
            for p in polygon.get_points():
                points.append( Point( p.x - self.position.x, p.y - self.position.y, p.z - self.position.z ).rel_to( self.observer ) )
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
            squares.append( self.make_square( top_left, bottom_right, i * separation + self.position.z ) )
        return squares

    def output_toolbar( self, screen, mode ):
        modestr = ""
        if 2 == mode: modestr = "-- OBSERVE --"
        pygame.draw.rect( screen, ( 205, 205, 205 ), ( ( 0, 400 ), ( 400, 440 ) ), 0 )
        text = self.font.render( modestr, True, self.font_colour )
        screen.blit( text, ( 5, 405 ) )
        text = self.font.render( str( self.observer ), True, self.font_colour )
        screen.blit( text, ( 5, 425 ) )
        text = self.font.render( str( self.position ), True, self.font_colour )
        screen.blit( text, ( 125, 425 ) )
        text = self.font.render( str( pygame.mouse.get_pos() ), True, self.font_colour )
        screen.blit( text, ( 245, 425 ) )

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

COMMAND = 0
INSERT  = 1
OBSERVE = 2
VISUAL  = 3
VISUAL_BATCH = 4

if '__main__' == __name__:
    mode = COMMAND
    pygame.init()
    running = True
    width, height = 400, 400
    observer = Point( width / 2, height / 2, 100 )
    model   = Model( ( width, height ), observer )
    screen  = pygame.display.set_mode( ( width, height + 40 ) )
    objects = [ ]
    actions = Actions()
    leftClick = rightClick = False
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
                    mode = COMMAND
                elif len( objects ) > 0 and K_RETURN == event.key:
                    actions.do( \
                        ( objects[ -1 ].close, [] ), \
                        ( objects[ -1 ].open, [] ) \
                    )
                elif K_UP    == event.key: model = model.move_up()
                elif K_RIGHT == event.key: model = model.move_right()
                elif K_DOWN  == event.key: model = model.move_down()
                elif K_LEFT  == event.key: model = model.move_left()
                elif K_j     == event.key: model = model.move_forward()
                elif K_k     == event.key: model = model.move_back()
                elif K_o     == event.key: mode  = OBSERVE
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
                            ( objects[ -1 ].add, [ Point( x, y, model.position.z ) ] ), \
                            ( objects[ -1 ].remove, [ Point( x, y, model.position.z ) ] ) \
                        )
                    else:
                        actions.do( \
                            ( lambda a: objects.append( a ), [ Polygon( ( 100, 100, ( 200 + model.position.z * 2 ) % 255 ) ).add( Point( x, y, model.position.z ) ) ] ), \
                            ( objects.pop, [] ) \
                        )
                elif rightClick and len( objects ) > 0 and objects[ -1 ].is_open():
                    actions.do( \
                        ( lambda a: objects[ -1 ].add( a ).close(), [ Point( x, y, model.position.z ) ] ), \
                        ( lambda a: objects[ -1 ].remove( a ).open(), [ Point( x, y, model.position.z ) ] ) \
                    )
        leftClick, _, rightClick = pygame.mouse.get_pressed()
        model.output( screen, mode, objects )
