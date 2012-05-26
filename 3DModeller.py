import pygame
from pygame.locals import *
from random import randint
from screen import *
import time

# TODO implement immutability

class Polygon:
    def __init__( self, colour ):
        self.points = []
        self.colour = colour
        self.isopen = True
        self.width  = 0

    def get_colour( self ):
        return self.colour

    def add( self, point ):
        self.points.append( point )
        return self

    def remove( self, point ):
        self.points.remove( point )
        return self

    def num_points( self ):
        return len( self.points )

    def get_points( self ):
        return self.points

    def open( self ):
        self.isopen = True

    def close( self ):
        self.isopen = False

    def is_open( self ):
        return self.isopen

    def set_width( self, width ):
        self.width = width

    def get_width( self ):
        return self.width

    def is_filled( self ):
        return self.filled

class Point:
    def __init__( self, x, y, z ):
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

class Model:
    def __init__( self, size, origin = None ):
        self.x, self.y = size
        self.grid = self.make_squares( 10, ( 0, 0 ), ( self.x, self.y ), 10 )
        self.origin = Point( self.x / 2, self.y / 2, 100 ) if None == origin else origin
        self.font = pygame.font.SysFont( pygame.font.get_default_font(), 20 )

    def nudge( self, magnitude ):
        x_, y_ = magnitude
        x, y, z = self.origin.x, self.origin.y, self.origin.z
        return Model( ( self.x, self.y ), Point( x + x_, y + y_, z ) )

    def output( self, screen, polygons ):
        # TODO polygons also need colour
        screen.fill( 0 )
        self.output_polygons( screen, self.grid, 1 )
        self.output_polygons( screen, polygons, 0 )
        # TODO highlight most recent mark
        if len( polygons ) > 0 and polygons[ -1 ].num_points() > 0:
            last = polygons[ -1 ]
            x, y = last.get_points()[ -1 ].rel_to( self.origin )
            colour = ( 255, 0, 0 ) if last.is_open() else ( 0, 255, 0 )
            pygame.draw.line( screen, colour, ( x - 2, y - 2 ), ( x + 2, y + 2 ), 1 )
            pygame.draw.line( screen, colour, ( x + 2, y - 2 ), ( x - 2, y + 2 ), 1 )
        self.output_toolbar( screen )
        pygame.display.flip()

    def output_polygons( self, screen, polygons, w ):
        for polygon in polygons:
            points = []
            for point in polygon.get_points():
                points.append( point.rel_to( self.origin ) )
            if len( points ) > 1:
                if len( points ) == 2:
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
            squares.append( self.make_square( top_left, bottom_right, i * separation ) )
        return squares

    def output_toolbar( self, screen ):
        pygame.draw.rect( screen, ( 205, 205, 205 ), ( ( 0, 400 ), ( 400, 440 ) ), 0 )
        text = self.font.render( str( pygame.mouse.get_pos() ), True, ( 0, 0, 0 ) )
        screen.blit( text, ( 300, 410 ) )

class Actions:
    def __init__( self ):
        self.undos = []
        self.redos = []

    def do( self, do_steps, undo_steps ):
        """ action is of the form ( [ do steps ], [ undo steps ] ) """
        for do_step in do_steps:
            do_step()
        self.undos.append( ( do_steps, undo_steps ) )
        self.redos = []

    def can_undo( self ):
        return len( self.undos ) > 0

    def undo( self ):
        if self.can_undo():
            action = self.undos.pop()
            _, undo_steps = action
            for undo_step in undo_steps:
                undo_step()
            self.redos.append( action )

    def can_redo( self ):
        return len( self.redos ) > 0

    def redo( self ):
        if self.can_redo():
            action = self.redos.pop()
            redo_steps, _ = action
            for redo_step in redo_steps:
                redo_step()
            self.undos.append( action )

class Bool:
    # TODO rename methods and attributes
    def __init__( self ):
        self.on = False

    def turn_on( self ):
        self.on = True

    def turn_off( self ):
        self.on = False

if '__main__' == __name__:
    pygame.init()
    running = True
    width, height = 400, 400
    model   = Model( ( width, height ) )
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
                    running = False
                elif K_RETURN == event.key:
                    objects[ -1 ].close()
                elif K_UP    == event.key: model = model.nudge( ( 0, -10 ) )
                elif K_RIGHT == event.key: model = model.nudge( ( 10, 0 ) )
                elif K_DOWN  == event.key: model = model.nudge( ( 0, 10 ) )
                elif K_LEFT  == event.key: model = model.nudge( ( -10, 0 ) )
                elif K_w  == event.key: model = Model( ( width, height ) )
            elif MOUSEBUTTONUP == event.type:
                x, y = pygame.mouse.get_pos()
                point = Point( x, y, 0 )
                if leftClick:
                    if len( objects ) > 0 and objects[ -1 ].is_open():
                        actions.do( \
                            [ lambda: objects[ -1 ].add( point ) ], \
                            # FIXME can't remove this way
                            [ lambda: objects[ -1 ].remove( point ) ] \
                        )
                    else:
                        actions.do( \
                            [ lambda: objects.append( Polygon( ( 255, 255, 255 ) ).add( point ) ) ], \
                            [ lambda: objects.pop() ] \
                        )
                elif rightClick and objects[ -1 ].is_open():
                    actions.do( \
                        [ lambda: objects[ len( objects ) - 1 ].add( point ).close() ], \
                        [ lambda: objects[ len( objects ) - 1 ].remove( point ).open() ] \
                    )
        leftClick, _, rightClick = pygame.mouse.get_pressed()
        model.output( screen, objects )
