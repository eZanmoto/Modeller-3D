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
    def __init__( self, size, observer, position = None, has_grid = False ):
        self.font_colour = ( 0, 0, 0 )
        self.width, self.height = size
        if None == position:
            self.position = Point( 0, 0, 0 )
        else:
            self.position = position
        self.observer = observer
        self.grid = self.make_squares( 10, ( 0, 0 ), ( self.width, self.width ), 10 )
        self.font = pygame.font.SysFont( "monospace", 12 )
        self.has_grid = has_grid
        if self.has_grid:
            self.front_grid = self.make_grid( ( self.width, self.width ), 50 )

    def make_grid( self, size, sep ):
        width, height = size
        grid = []
        for i in range( sep, width, sep ):
            grid.append( Polygon( ( 255, 255, 255 ) ).add( Point( i, 0, 0 ) ).add( Point( i, height, 0 ) ) )
        for i in range( sep, height, sep ):
            grid.append( Polygon( ( 255, 255, 255 ) ).add( Point( 0, i, 0 ) ).add( Point( width, i, 0 ) ) )
        return grid

    def set_grid( self, has_grid ):
        return Model( ( self.width, self.height ), self.observer, self.position, has_grid )

    def move( self, new_position ):
        return Model( ( self.width, self.height ), self.observer, new_position, self.has_grid )

    def move_up( self, n ):
        return self.move( self.position.move_up( n ) )

    def move_right( self, n ):
        return self.move( self.position.move_right( n ) )

    def move_down( self, n ):
        return self.move( self.position.move_down( n ) )

    def move_left( self, n ):
        return self.move( self.position.move_left( n ) )

    def move_forward( self, n ):
        return self.move( self.position.move_forward( n ) )

    def move_back( self, n ):
        return self.move( self.position.move_back( n ) )

    def update_observer( self, observer ):
        return Model( ( self.width, self.height ), observer, self.position, self.has_grid )

    def snap( self, pos ):
        a = 50
        b = 10
        p = pos % a
        if p < b:
            return pos - p
        elif p > a - b:
            return pos + ( a - p )
        else:
            return pos

    def output( self, screen, mode, polygons ):
        screen.fill( 0 )
        self.output_polygons( screen, self.grid, 1 )
        self.output_polygons( screen, polygons, 0 )
        if len( polygons ) > 0 and polygons[ -1 ].num_points() > 0:
            last = polygons[ -1 ]
            p = last.get_points()[ -1 ]
            if p.z - self.position.z < self.observer.z:
                x, y = Point( p.x - self.position.x, p.y - self.position.y, p.z - self.position.z ).rel_to( self.observer )
                colour = ( 255, 0, 0 ) if last.is_open() else ( 0, 255, 0 )
                pygame.draw.line( screen, colour, ( x - 2, y - 2 ), ( x + 2, y + 2 ), 1 )
                pygame.draw.line( screen, colour, ( x + 2, y - 2 ), ( x - 2, y + 2 ), 1 )
        x, y = pygame.mouse.get_pos()
        if self.has_grid:
            self.op( screen, self.front_grid, 1 )
            x, y = self.snap( x ), self.snap( y )
        colour = ( 0, 0, 255 )
        pygame.draw.line( screen, colour, ( x - 2, y - 2 ), ( x + 2, y + 2 ), 1 )
        pygame.draw.line( screen, colour, ( x + 2, y - 2 ), ( x - 2, y + 2 ), 1 )
        self.output_toolbar( screen, mode )
        pygame.display.flip()

    def op( self, screen, polygons, w ):
        for polygon in polygons:
            points = [ ]
            for p in polygon.get_points():
                points.append( ( p.x, p.y ) )
            if len( points ) == 1:
                screen.set_at( points[ 0 ], polygon.get_colour() )
            elif len( points ) == 2:
                pygame.draw.line( screen, polygon.get_colour(), points[ 0 ], points[ 1 ], 1 )
            else:
                pygame.draw.polygon( screen, polygon.get_colour(), points, polygon.get_width() )

    def output_polygons( self, screen, polygons, w ):
        for polygon in polygons:
            all_points = polygon.get_points()
            points = []
            for i in range( 0, len( all_points ) ):
                p = all_points[ i ]
                z = p.z - self.position.z
                if p.z - self.position.z < self.observer.z:
                    points.append( Point( p.x - self.position.x, p.y - self.position.y, z ).rel_to( self.observer ) )
                else:
                    points = [ ]
                    break
            if len( points ) == 1:
                screen.set_at( points[ 0 ], polygon.get_colour() )
            elif len( points ) == 2:
                pygame.draw.line( screen, polygon.get_colour(), points[ 0 ], points[ 1 ], 1 )
            elif len( points ) > 2:
                pygame.draw.polygon( screen, polygon.get_colour(), points, polygon.get_width() )

    def get_it_from( self, a, b ):
        return ( self.get_it( a.x, a.z, b.x, b.z ), self.get_it( a.y, a.z, b.x, b.z ) )

    def get_it( self, x1, y1, x2, y2 ):
        m = self.slope( x1, y1, x2, y2 )
        return ( m * x1 - y1 ) / 0.1 if m == 0 else m

    def slope( self, x1, y1, x2, y2 ):
        under = ( x2 - x1 )
        return ( y2 - y1 ) / 0.1 if under == 0 else under

    def make_square( self, top_left, bottom_right, z ):
        colour = 255 - z % 100
        a, b = top_left
        c, d = bottom_right
        square = Polygon( ( colour, colour, colour ) ).add( Point( a, b, z ) ) \
            .add( Point( b, c, z ) ).add( Point( c, d, z ) ) \
            .add( Point( d, a, z ) )
        square.set_width( 1 )
        return square

    def make_squares( self, n, top_left, bottom_right, separation ):
        squares = []
        for i in range( 0, n ):
            squares.append( self.make_square( top_left, bottom_right, self.position.z - i * separation ) )
        return squares

    def output_toolbar( self, screen, mode ):
        status = ""
        if 2 == mode: status = "-- OBSERVE --"
        pygame.draw.rect( screen, ( 205, 205, 205 ), ( ( 0, 400 ), ( 400, 440 ) ), 0 )
        text = self.font.render( status, True, self.font_colour )
        screen.blit( text, ( 5, 405 ) )
        text = self.font.render( str( self.observer ), True, self.font_colour )
        screen.blit( text, ( 5, 425 ) )
        text = self.font.render( str( self.position ), True, self.font_colour )
        screen.blit( text, ( 125, 425 ) )
        x, y = pygame.mouse.get_pos()
        if self.has_grid:
            x, y = self.snap( x ), self.snap( y )
        text = self.font.render( str( ( x, y ) ), True, self.font_colour )
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

class Command():
    EDIT  = 0
    POINT = 1
    SET   = 2
    WRITE = 3
    QUIT  = 4

def enter_command( screen ):
    running = True
    line = ":"
    command = ( -1, [ ] )
    while running:
        for event in pygame.event.get():
            if QUIT == event.type:
                running = False
                command = Command.QUIT
            elif KEYUP == event.type:
                if K_RETURN == event.key:
                    running = False
                    words = line[ 1 : ].split()
                    if 'e' == words[0]:
                        if len( words ) == 2:
                            command = ( Command.EDIT, [ words[ 1 ] ] )
                        else:
                            line = ":e[dit] takes exactly one argument"
                    elif 'p' == words[0]:
                        if len( words ) == 4:
                            command = ( Command.POINT, words[ 1 : ] )
                        else:
                            line = ":p[oint] takes exactly three arguments"
                    elif 'set' == words[0]:
                        if len( words ) > 1:
                            command = ( Command.SET, words[ 1 : ] )
                        else:
                            line = ":set expects an option"
                    elif 'w' == words[0]:
                        if len( words ) == 2:
                            command = ( Command.WRITE, [ words[ 1 ] ] )
                        else:
                            line = ":w[rite] takes exactly one argument"
                    elif 'q' == words[0]:
                        command = ( Command.QUIT, [] )
                        line = "Quitting..."
                    else:
                        line = "Don't recognize command '" + words[ 0 ] + "'"
                elif K_ESCAPE == event.key: running = False
                elif K_BACKSPACE == event.key:
                    if len( line ) == 1: running = False
                    else: line = line[ : -1 ]
                elif K_PERIOD == event.key: line += '.'
                elif K_SLASH  == event.key: line += '/'
                elif K_SPACE  == event.key: line += ' '
                elif K_0 == event.key: line += '0'
                elif K_1 == event.key: line += '1'
                elif K_2 == event.key: line += '2'
                elif K_3 == event.key: line += '3'
                elif K_4 == event.key: line += '4'
                elif K_5 == event.key: line += '5'
                elif K_6 == event.key: line += '6'
                elif K_7 == event.key: line += '7'
                elif K_8 == event.key: line += '8'
                elif K_9 == event.key: line += '9'
                elif K_a == event.key: line += 'a'
                elif K_b == event.key: line += 'b'
                elif K_c == event.key: line += 'c'
                elif K_d == event.key: line += 'd'
                elif K_e == event.key: line += 'e'
                elif K_f == event.key: line += 'f'
                elif K_g == event.key: line += 'g'
                elif K_h == event.key: line += 'h'
                elif K_i == event.key: line += 'i'
                elif K_j == event.key: line += 'j'
                elif K_k == event.key: line += 'k'
                elif K_l == event.key: line += 'l'
                elif K_m == event.key: line += 'm'
                elif K_n == event.key: line += 'n'
                elif K_o == event.key: line += 'o'
                elif K_p == event.key: line += 'p'
                elif K_q == event.key: line += 'q'
                elif K_r == event.key: line += 'r'
                elif K_s == event.key: line += 's'
                elif K_t == event.key: line += 't'
                elif K_u == event.key: line += 'u'
                elif K_v == event.key: line += 'v'
                elif K_w == event.key: line += 'w'
                elif K_x == event.key: line += 'x'
                elif K_y == event.key: line += 'y'
                elif K_z == event.key: line += 'z'
        screen.fill( ( 205, 205, 205 ), Rect( 5, 405, 390, 12 ) )
        text = pygame.font.SysFont( "monospace", 12 ).render( line, True, ( 0, 0, 0 ) )
        screen.blit( text, ( 5, 405 ) )
        pygame.display.update()
    return command

def snap( pos, grid_size, strength ):
    p = pos % grid_size
    if p < strength:
        return pos - p
    elif p > grid_size - strength:
        return pos + ( grid_size - p )
    else:
        return pos

COMMAND = 0
INSERT  = 1
OBSERVE = 2
VISUAL  = 3
VISUAL_BATCH = 4

if '__main__' == __name__:
    mode = COMMAND
    pygame.init()
    running = True
    snapgrid = False
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
                elif K_o == event.key: mode  = OBSERVE
                if K_COLON | KMOD_SHIFT == event.key and COMMAND == mode:
                    command = enter_command( screen )
                    if Command.EDIT == command[ 0 ]:
                        filename = command[ 1 ][ 0 ]
                        if not filename.endswith( '.3d' ):
                            filename += '.3d'
                        objects = load_objects( filename )
                        print "Loaded '" + filename + "'"
                    elif Command.POINT == command[ 0 ]:
                        p = command[ 1 ]
                        point = Point( int( p[ 0 ] ), int( p[ 1 ] ), int( p[ 2 ] ) )
                        if len( objects ) > 0 and objects[ -1 ].is_open():
                            actions.do( \
                                ( objects[ -1 ].add, [ point ] ), \
                                ( objects[ -1 ].remove, [ point ] ) \
                            )
                        else:
                            actions.do( \
                                ( lambda a: objects.append( a ), [ Polygon( ( 100, 100, ( 200 + model.position.z * 2 ) % 255 ) ).add( point ) ] ), \
                                ( objects.pop, [] ) \
                            )
                    elif Command.SET == command[ 0 ]:
                        option = command[ 1 ][ 0 ]
                        if 'g' == option:
                            model = model.set_grid( True )
                        elif 'nog' == option:
                            model = model.set_grid( False )
                        elif 'sg' == option:
                            snapgrid = True
                            model = model.set_grid( True )
                        elif 'nosg' == option:
                            snapgrid = False
                    elif Command.WRITE == command[ 0 ]:
                        filename = command[ 1 ][ 0 ]
                        if not filename.endswith( '.3d' ):
                            filename += '.3d'
                        write_objects( filename, objects )
                        print "Wrote '" + filename + "'"
                    elif Command.QUIT == command[ 0 ]:
                        running = False
                if OBSERVE == mode:
                    if K_UP      == event.key: observer = observer.move_up( 10 )
                    elif K_RIGHT == event.key: observer = observer.move_right( 10 )
                    elif K_DOWN  == event.key: observer = observer.move_down( 10 )
                    elif K_LEFT  == event.key: observer = observer.move_left( 10 )
                    elif K_j     == event.key: observer = observer.move_forward( 10 )
                    elif K_k     == event.key and observer.z > model.position.z: observer = observer.move_back( 10 )
                    model = model.update_observer( observer )
                else:
                    if K_UP      == event.key: model = model.move_up( 10 )
                    elif K_RIGHT == event.key: model = model.move_right( 10 )
                    elif K_DOWN  == event.key: model = model.move_down( 10 )
                    elif K_LEFT  == event.key: model = model.move_left( 10 )
                    elif K_j     == event.key and model.position.z < observer.z: model = model.move_forward( 10 )
                    elif K_k     == event.key: model = model.move_back( 10 )
            elif MOUSEBUTTONUP == event.type:
                x, y = pygame.mouse.get_pos()
                if snapgrid:
                    x = snap( x, 50, 10 )
                    y = snap( y, 50, 10 )
                point = Point( x + model.position.x, y + model.position.y, model.position.z )
                if leftClick:
                    if len( objects ) > 0 and objects[ -1 ].is_open():
                        actions.do( \
                            ( objects[ -1 ].add, [ point ] ), \
                            ( objects[ -1 ].remove, [ point ] ) \
                        )
                    else:
                        actions.do( \
                            ( lambda a: objects.append( a ), [ Polygon( ( 100, 100, ( 200 + model.position.z * 2 ) % 255 ) ).add( point ) ] ), \
                            ( objects.pop, [] ) \
                        )
                elif rightClick and len( objects ) > 0 and objects[ -1 ].is_open():
                    actions.do( \
                        ( lambda a: objects[ -1 ].add( a ).close(), [ point ] ), \
                        ( lambda a: objects[ -1 ].remove( a ).open(), [ point ] ) \
                    )
        leftClick, _, rightClick = pygame.mouse.get_pressed()
        model.output( screen, mode, objects )
