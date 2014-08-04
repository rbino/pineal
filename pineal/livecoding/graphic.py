from random import uniform
import pyglet.gl as gl
from color import Color, colorMode, fill, stroke, noFill, noStroke

import thirdparty.ezpyinline as ezpyinline


def _vec(*args):
    return (gl.GLfloat * len(args))(*args)


_ezc_utils = ezpyinline.C(r"""
    #include <GL/freeglut.h>
    #include <math.h>

    void rotate(double angx, double angy, double angz)
    {
        glRotatef(180.0*angx/M_PI, 1,0,0);
        glRotatef(180.0*angy/M_PI, 0,1,0);
        glRotatef(180.0*angz/M_PI, 0,0,1);
    }

    void translate(double x, double y, double z)
    {
        glTranslatef(x, y, z);
    }

    void scale(double x, double y, double z)
    {
        glScalef(x, y, z);
    }

    void push(void)
    {
        glPushMatrix();
    }

    void pop(void)
    {
        glPopMatrix();
    }
""")


def strokeWeight(w):
    gl.glLineWidth(w)


def rotateX(angle):
    rotate(angx = angle)


def rotateY(angle):
    rotate(angy = angle)


def rotateZ(angle):
    rotate(angz = angle)


def rotate(angz=0, angy=0, angx=0):
    _ezc_utils.rotate(angx,angy,angz)


def translate(x=0, y=0, z=0):
    _ezc_utils.translate(x, y, z)


def scale(x, y=None, z=1):
    if not y:
        y = x
    _ezc_utils.scale(x, y, z)

_matrix_stack = 0


def pushMatrix():
    global _matrix_stack
    if _matrix_stack<30:
        _ezc_utils.push()
        _matrix_stack += 1
    else:
        print "TOO many push()"
        raise Exception()


def popMatrix():
    global _matrix_stack
    if _matrix_stack>0:
        _ezc_utils.pop()
    else:
        print "TOO many pop()"
        raise Exception()
    _matrix_stack -= 1 # if goes to -1 i can handle it


def resetMatrix():
    global _matrix_stack
    _matrix_stack = 0
    gl.glLoadIdentity()


def random(a=0, b=1):
    """ uniform distribution """
    return uniform(a,b)


def noise(a=1):
    """ white noise (uniform distribution in [-a,+a]) """
    return uniform(-a,a)


# light
def ambient(amb):
    """ set ambiental light intensity """
    gl.glLightModelfv(
        gl.GL_LIGHT_MODEL_AMBIENT|gl.GL_LIGHT_MODEL_TWO_SIDE,
        _vec(amb,amb,amb, 1.0)
    )


def light(val):
    """ set light intensity """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, _vec(val, val, val, 1.0))


def light_pos(x,y,z):
    """ set light position """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, _vec(x,y,z, 3))
#

ezc_shapes = ezpyinline.C(r"""
    #include <GL/freeglut.h>
    #include <math.h>

    void cube(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glColor4f(fr, fg, fb, fa);
        glutSolidCube(r);
        glColor4f(sr, sg, sb, sa);
        glutWireCube(r);
    }

    void tetrahedron(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glPushMatrix();
        glScalef(r,r,r);

        glColor4f(fr, fg, fb, fa);
        glutSolidTetrahedron();
        glColor4f(sr, sg, sb, sa);
        glutWireTetrahedron();
        glPopMatrix();
    }

    void dodecahedron(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glPushMatrix();
        glScalef(r,r,r);

        glColor4f(fr, fg, fb, fa);
        glutSolidDodecahedron();
        glColor4f(sr, sg, sb, sa);
        glutWireDodecahedron();
        glPopMatrix();
    }

    void octahedron(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glPushMatrix();
        glScalef(r,r,r);

        glColor4f(fr, fg, fb, fa);
        glutSolidOctahedron();
        glColor4f(sr, sg, sb, sa);
        glutWireOctahedron();
        glPopMatrix();
    }

    void quad(
        double l,
        double x, double y, double z,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glColor4f(fr,fg,fb, fa);
        glBegin(GL_POLYGON);
        glVertex3f(x-l/2, y-l/2, z);
        glVertex3f(x-l/2, y+l/2, z);
        glVertex3f(x+l/2, y+l/2, z);
        glVertex3f(x+l/2, y-l/2, z);
        glEnd();

        glColor4f(sr,sg,sb, sa);
        glBegin(GL_LINE_LOOP);
        glVertex3f(x-l/2, y-l/2, z);
        glVertex3f(x-l/2, y+l/2, z);
        glVertex3f(x+l/2, y+l/2, z);
        glVertex3f(x+l/2, y-l/2, z);
        glEnd();
    }
""")


def cube(r=1):
    f = fill()
    s = stroke()
    ezc_shapes.cube(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def tetrahedron(r=1):
    f = fill()
    s = stroke()
    ezc_shapes.tetrahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def dodecahedron(r=1):
    f = fill()
    s = stroke()
    ezc_shapes.dodecahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def octahedron(r=1):
    f = fill()
    s = stroke()
    ezc_shapes.octahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


class Shape(object):
    def __init__(self):
        self._v = list()

    def vertex(self, x,y, z=0):
        self._v.append( (x,y,z) )


def createShape():
    return Shape()


def shape(s):
    s._draw()


def quad(l=1.0, x=0, y=0, z=0):
    f = fill()
    s = stroke()
    ezc_shapes.quad(l,x,y,z, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)