import pygame
from pygame.locals import *
from random import randint
from screen import *
import time

class Polygon:
    def __init__( self, colour, width = 0 ):
        self._points = []
        self._colour = colour
        self._isopen = True
        self._width  = width

    def get_colour( self ):
        return self._colour

    def add( self, point ):
        self._points.append( point )
        return self

    def remove( self, point ):
        self._points.remove( point )
        return self

    def num_points( self ):
        return len( self._points )

    def get_points( self ):
        """ Returns a copy of the points in this vector as a list. """
        return self._points[:]

    def open( self ):
        self._isopen = True
        return self

    def close( self ):
        self._isopen = False
        return self

    def is_open( self ):
        return self._isopen

    def set_width( self, width ):
        self._width = width
        return self

    def get_width( self ):
        return self._width

    def is_filled( self ):
        return self._filled

    def write( self ):
        c = self.get_colour()
        output = [ str( c[ 0 ] ) + ' ' + str( c[ 1 ] ) + ' ' + str( c[ 2 ] ), str( self.num_points() ) ]
        for p in self._points:
            output.append( str( p.x ) + ' ' + str( p.y ) + ' ' + str( p.z ) )
        return output

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

    def __str__( self ):
        return "(%d, %d, %d)" % ( self.x, self.y, self.z )

    def __eq__( self, other ):
        return other != None and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__( self, other ):
        return not ( self == other )

class Model:
    # TODO implement immutability where possible
    def __init__( self, size, origin = None, z = 0 ):
        self.x, self.y = size
        self.grid = self.make_squares( 10, ( 0, 0 ), ( self.x, self.y ), 10 )
        self.origin = Point( self.x / 2, self.y / 2, 100 ) if None == origin else origin
        self.font = pygame.font.SysFont( pygame.font.get_default_font(), 20 )
        self.z = z

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
            squares.append( self.make_square( top_left, bottom_right, i * separation ) )
        return squares

    def output_toolbar( self, screen ):
        pygame.draw.rect( screen, ( 205, 205, 205 ), ( ( 0, 400 ), ( 400, 440 ) ), 0 )
        text = self.font.render( str( pygame.mouse.get_pos() ), True, ( 0, 0, 0 ) )
        screen.blit( text, ( 300, 410 ) )

class Actions:
    #TODO implement immutability where possible
    def __init__( self ):
        self.undos = []
        self.redos = []

    def do( self, do_steps, undo_steps ):
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
                    objects[ -1 ].close()
                elif K_UP    == event.key: model = model.nudge( ( 0, -10 ) )
                elif K_RIGHT == event.key: model = model.nudge( ( 10, 0 ) )
                elif K_DOWN  == event.key: model = model.nudge( ( 0, 10 ) )
                elif K_LEFT  == event.key: model = model.nudge( ( -10, 0 ) )
                elif K_q == event.key: model = Model( ( width, height ) )
                elif K_k == event.key:
                    model = model.forward( 10 )
                    z -= 10
                elif K_j == event.key:
                    model = model.back( 10 )
                    z += 10
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
                            [ lambda: objects[ -1 ].add( Point( x, y, z ) ) ], \
                            [ lambda: objects[ -1 ].remove( Point( x, y, z ) ) ] \
                        )
                    else:
                        actions.do( \
                            [ lambda: objects.append( Polygon( ( 100, 100, ( 200 + z * 2 ) % 255 ) ).add( Point( x, y, z ) ) ) ], \
                            [ lambda: objects.pop() ] \
                        )
                elif rightClick and objects[ -1 ].is_open():
                    actions.do( \
                        [ lambda: objects[ len( objects ) - 1 ].add( Point( x, y, z ) ).close() ], \
                        [ lambda: objects[ len( objects ) - 1 ].remove( Point( x, y, z ) ).open() ] \
                    )
        leftClick, _, rightClick = pygame.mouse.get_pressed()
        model.output( screen, objects )
