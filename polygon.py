class Polygon:
    """Mutable"""
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
