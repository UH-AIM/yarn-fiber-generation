from math import sin, cos, sqrt, pow, pi

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

def sqr(x):
    return x * x

def norm2(v):
    return sqr(v.x) + sqr(v.y) + sqr(v.z)

def norm(v):
    return sqrt(norm2(v))

def scale(c, v):
    cv = Vector3(c * v.x, c * v.y, c * v.z)
    return cv

def cross(u, v):
    w = Vector3()
    w.x = u.y * v.z - u.z * v.y
    w.y = u.z * v.x - u.x * v.z
    w.z = u.x * v.y - u.y * v.x
    return w

def yarnCurve(t, a, h, d):
    gamma_t = Vector3()
    gamma_t.x = t + a * sin(2.0 * t)
    gamma_t.y = h * cos(t)
    gamma_t.z = d * cos(2.0 * t)
    return gamma_t

def frenetFrame(t, a, h, d):
    e1 = Vector3()
    e2 = Vector3()

    u_t, v_t, x_t, y_t = 0.0, 0.0, 0.0, 0.0
    e1.x = 1.0 + 2.0 * a * cos(2.0 * t)
    e1.y = -h * sin(t)
    e1.z = -2.0 * d * sin(2.0 * t)
    u_t = norm2(e1)
    v_t = 2.0 * h * h * cos(t) * sin(t) + 16.0 * d * d * cos(2.0 * t) * sin(2.0 * t) - 8.0 * a * (1.0 + 2.0 * a * cos(2.0 * t)) * sin(2.0 * t)
    x_t = 1.0 / sqrt(u_t)
    y_t = v_t / (2.0 * pow(u_t, 3.0 / 2.0))
    e2.x = y_t * (-1.0 - 2.0 * a * cos(2.0 * t)) - x_t * 4.0 * a * sin(2.0 * t)
    e2.y = y_t * h * sin(t) - x_t * h * cos(t)
    e2.z = y_t * 2.0 * d * sin(2.0 * t) - x_t * 4.0 * d * cos(2.0 * t)
    e1 = scale(x_t, e1)
    e2 = scale(1.0 / norm(e2), e2)
    e3 = cross(e1, e2)
    return [e1, e2, e3]

def fiberCurve(t, a, h, d, r, omega, phi):
    gamma_t = yarnCurve(t, a, h, d)
    [e1, e2, e3] = frenetFrame(t, a, h, d)
    theta_t = t * omega - 2. * cos(t) + phi
    eta_t = Vector3(0, 0, 0)
    eta_t.x = gamma_t.x + r * (cos(theta_t) * e2.x + sin(theta_t) * e3.x)
    eta_t.y = gamma_t.y + r * (cos(theta_t) * e2.y + sin(theta_t) * e3.y)
    eta_t.z = gamma_t.z + r * (cos(theta_t) * e2.z + sin(theta_t) * e3.z)
    return eta_t



def writeYarnCurves(filename, nRows, rowOffset, nLoops, samplesPerLoop, a, h, d):
    '''
    Input
        str filename       output filename 
        int nRows          number of rows in wale direction 
        dbl rowOffset      row spacing in wale direction 
        int nLoops         number of loops in course direction 
        int samplesPerLoop sample points for each loop 
        dbl a              loop roundness 
        dbl h              loop height 
        dbl d              loop depth 
    '''
    
    def format_float(f):
        # Format the given float to scientific notation
        return "{:.8e}".format(f)

    # Open the output file for writing
    out = open(filename, "w")

    nPoints = 0
    dt = 2*pi / samplesPerLoop

    # Write vertices
    for row in range(nRows):
        y0 = rowOffset * row
        for loop in range(nLoops):
            t0 = 2*pi * loop
            for sample in range(samplesPerLoop):
                t = t0 + dt * sample
                gamma_t = yarnCurve(t, a, h, d)

                out.write("v {} {} {}\n".format(
                    format_float(gamma_t.x),
                    format_float(gamma_t.y + y0),
                    format_float(gamma_t.z)
                ))

    # Write polylines
    for row in range(nRows):
        out.write("l")
        for loop in range(nLoops):
            for sample in range(samplesPerLoop):
                out.write(" {}".format(nPoints + 1))
                nPoints += 1
        out.write("\n")

    # Close the output file
    out.close()



def writeFiberCurves(filename, nRows, rowOffset, nLoops, samplesPerLoop, a, h, d, r, omega, nFibers):

    '''
    Input
        str filename       output filename 
        int nRows          number of rows in wale direction 
        dbl rowOffset      row spacing in wale direction 
        int nLoops         number of loops in course direction 
        int samplesPerLoop sample points for each loop 
        dbl a              loop roundness 
        dbl h              loop height 
        dbl d              loop depth 
        dbl r              yarn radius
        dbl omega          amount of fiber twist
        int nFibers        number of fibers around yarn
    '''
    
    out = open(filename, "w")

    nPoints = 0
    dt = (2.0 * pi) / samplesPerLoop
    dphi = (2.0 * pi) / nFibers

    # write vertices
    for row in range(nRows):
        y0 = rowOffset * row
        for fiber in range(nFibers):
            phi = dphi * fiber
            for loop in range(nLoops):
                t0 = 2.0 * pi * loop
                for sample in range(samplesPerLoop):
                    t = t0 + dt * sample
                    eta_t = fiberCurve(t, a, h, d, r, omega, phi)
                    out.write(f"v {eta_t.x} {y0 + eta_t.y} {eta_t.z}\n")


    # write polylines
    for row in range(nRows):
        y0 = rowOffset * row
        for fiber in range(nFibers):
            out.write("l")
            for loop in range(nLoops):
                for sample in range(samplesPerLoop):
                    out.write(" {}".format(nPoints + 1))
                    nPoints += 1
            out.write("\n")
            
    out.close()
