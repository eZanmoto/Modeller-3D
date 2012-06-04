from line import *
from point import *

def odd( n ):
    return n % 2 == 1

def within( n, lo, hi ):
    return within( n, hi, lo ) if lo > hi else n > lo and n < hi

class Polygon:
    """Mutable"""
    def __init__( self, colour, width = 0 ):
        self._points = []
        self._colour = colour
        self._isopen = True
        self._width  = width
        self._selected = False

    def select( self ):
        self._selected = True
        return self

    def deselect( self ):
        self._selected = False
        return self

    def is_selected( self ):
        return self._selected

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

    def contains( self, model, point ):
        horizontal, vertical = Line.horizontal( point ), Line.vertical( point )
        left_of_x = right_of_x = left_of_y = right_of_y = 0
        projection = self.project( model ) 
        for l in self.lines( projection ):
            line = Line.from_point( l[ 0 ], l[ 1 ] )
            x, y = relative_to( point, line )
            if within( point[ 0 ], l[ 0 ][ 0 ], l[ 1 ][ 0 ] ):
                if y == Ordering.LT:
                    left_of_y += 1
                elif y != None:
                    right_of_y += 1
            if within( point[ 1 ], l[ 0 ][ 1 ], l[ 1 ][ 1 ] ):
                if x == Ordering.LT:
                    left_of_x += 1
                elif x != None:
                    right_of_x += 1
        return  odd( left_of_x ) and odd( right_of_x ) \
            and odd( left_of_y ) and odd( right_of_y )

    def within( self, n, lo, hi ):
        return self.within( n, hi, lo ) if lo > hi else n > lo and n < hi

    def project( self, model ):
        points = [ ]
        for i in range( 0, len( self._points ) ):
            p = self._points[ i ]
            x, y, z = p.x - model.position.x, p.y - model.position.y, p.z - model.position.z
            if z < model.observer.z:
                points.append( Point( x, y, z ).rel_to( model.observer ) )
            else:
                points = [ ]
                break
        return points

    def lines( self, points2d ):
        lines = [ ]
        for i in range( 0, len( points2d ) ):
            lines.append( ( points2d[ i - 1 ], points2d[ i ] ) )
        return lines

    def write( self ):
        c = self.get_colour()
        output = [ str( c[ 0 ] ) + ' ' + str( c[ 1 ] ) + ' ' + str( c[ 2 ] ), str( self.num_points() ) ]
        for p in self._points:
            output.append( str( p.x ) + ' ' + str( p.y ) + ' ' + str( p.z ) )
        return output
