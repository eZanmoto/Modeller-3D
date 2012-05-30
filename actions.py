class Actions:
    """ Mutable """

    def __init__( self ):
        """ Creates a new record of actions which may be undone. """
        self.undos = []
        self.redos = []

    def do( self, do, undo ):
        """
            Does the action specified by do, which may be undone.

              do - (  action, [ args ] )
            undo - ( inverse, [ args ] )
        """
        do[ 0 ]( *do[ 1 ] )
        self.undos.append( ( do, undo ) )
        self.redos = []

    def can_undo( self ):
        """ 'True' if an action can be undone. """
        return len( self.undos ) > 0

    def undo( self ):
        """ Undoes the most recent action. """
        if self.can_undo():
            action = self.undos.pop()
            _, undo = action
            undo[ 0 ]( *undo[ 1 ] )
            self.redos.append( action )

    def can_redo( self ):
        """ 'True' if an action can be redone. """
        return len( self.redos ) > 0

    def redo( self ):
        """ Redoes the most recent action. """
        if self.can_redo():
            action = self.redos.pop()
            redo, _ = action
            redo[ 0 ]( *redo[ 1 ] )
            self.undos.append( action )
