Specification for Modeller 3D
=============================

Sean Kelleher
-------------

### Modes

#### Command Mode

The default mode where commands are entered.

#### Insert Mode

Enter with `i`.

Left-clicking with the mouse inserts a vertex.

#### Observer Mode

Enter with `o`.

Allows you to move the viewpoint you see the model from using the mouse.

#### Visual Mode

Enter with `v`.

Left-clicking with the mouse selects the closest vertex. Click-and-drag with the
left mouse button creates a bounding box which selects all enclosed vertices.

#### Visual Batch Mode

Enter with `V`.

Left-clicking with the mouse selects the polygon underneath the cursor.
Click-and-drag with the left mouse button creates a bounding box which selects
all polygons which have an enclosed vertex.

### Commands

#### Edit

    :e[dit] filename

Loads a .3d model, or creates one if the specified file doesn't exist. The .3d
extension is appended to the filename if it is not specified.

#### Insert point

    :p[oint] x y z

Inserts a vertex at the position with co-ordinates (x, y, z).

#### Insert polygon

    :p[olygo]n [ x y z ]+

Creates a polygon using the vertices specified by a sequence of (x, y, z)
co-ordinates.

#### Save

    :w[rite] filename

Saves the model as a .3d file. The .3d extension is appended to the filename if
it is not specified.

#### Quit

    :q[uit]

Ends the program.

### Options

Options may be set with the `:set` command, and unset by prefixing the option
name with `no`, e.g.:

    :set grid
    :set nogrid

turns the grid option on and off. You may use `no` with the option's
abbreviation, e.g. the following turns off grid:

    :set nog

#### Grid option

    :set g[rid]

Shows a grid on the current layer.

#### Snap-to-grid option

    :set s[nap]g[rid]

Clicking near the grid sets a point on the grid line.

### 3d File Format

#### Header

The first line contains the version number of Modeller 3D that this file was
used to save this file.

#### Data

The first line of the data section contains the number of polygons, n. n
polygons follow.

The first line of a polygon contains its colour, in the form

    R G B

where R, G and B are decimals from 0 to 255 representing the colour of the
polygon. The next line contains the number of vertices the polygon has, v, and
v vertex definition lines follow. A vertex definition is a line of the form

    X Y Z

where X, Y and Z are integers which may be positive or negative.

### Key Mappings

#### Any Mode

ESC - exit to command mode

#### Command Mode

g - go to start position
i - insert mode
j - move model "away from" the screen
k - move model "towards" the screen
o - observer mode
p - paste
r - redo
s - delete and enter insert mode
u - undo
v - visual mode
v - visual batch mode
x - delete

#### Insert Mode

ENTER - close polygon

#### Observer Mode

j - move "away from" the screen
k - move "towards" the screen

#### Visual Mode

j - move object "away from" the screen
k - move object "towards" the screen
s - delete and enter insert mode
x - delete
y - yank

### Visual Aids

All vertices and lines that reside on the current layer are highlighted.

The perceived position of the observer, the position of the mouse cursor, and
the position of the model, are all displayed at the right-hand side of the
toolbar. The top-left corner of the model is considered to be its (x, y)
position.
