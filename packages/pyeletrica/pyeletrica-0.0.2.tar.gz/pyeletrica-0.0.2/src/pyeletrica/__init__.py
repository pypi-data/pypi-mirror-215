# Version of pyeletrica package
__version__ = "0.0.2"

import numpy as np
import matplotlib.pyplot as plt

def sind(angle):
    '''
    Compute sine of angle, where angle is in degrees.

    Parameters
    ----------
    angle : float
        Angle in degrees.

    Returns
    -------
    out: float
         Sine of angle.
    '''
    return np.sin(np.deg2rad(angle))

def cosd(angle):
    '''
    Compute cosine of angle, where angle is in degrees.

    Parameters
    ----------
    angle : float
        Angle in degrees.

    Returns
    -------
    out: float
         Cosine of angle.
    '''
    return np.cos(np.deg2rad(angle))

def tand(angle):
    '''
    Compute tangent of angle, where angle is in degrees.

    Parameters
    ----------
    angle : float
        Angle in degrees.

    Returns
    -------
    out: float
         Tangent of angle.
    '''
    return np.tan(np.deg2rad(angle))


def Zparallel(arr):
    '''
    Calculate impedance/reactance/resistance in parallel.

    Parameters
    ----------
    arr : array_like
        Impedance list.

    Returns
    -------
    out: float
         Equivalent impedance/reactance/resistance in ohms.
    '''
    return (sum([i**-1 for i in arr]))**-1

def ZIbase(S, V):
    '''
    Calculate base impedance in ohms and base current in ampere.

    Parameters
    ----------
    S: float
        Power (watts).
    V : float
        Voltage (volts).
    
    Returns
    -------
    out : array-like
        (base impedance (ohms), base current in (amps))
    '''

    Zb = S / (np.sqrt(3) * V)
    Ib = V**2 / S

    return (Zb, Ib)

def divI(I, z1, z2, ndigits = 3):
    '''
    Calculate currents in ampere passing in two impedances in parallel.

    Parameters
    ----------
    I: float
        Total current.
    z1 : float
        Impedance branch 1.
    z2 : float
        Impedance branch 2.
    ndigits: int
            Precision in decimal digits.
    Returns
    -------
    out : array-like
          (Current of branch 1 (ampere), Current of branch 2 (ampere))
    '''
    
    return round(I * z2 / (z1 + z2), ndigits), round(I * z1 / (z1 + z2), ndigits)

def polar(v, ndigits=3):
    '''
    Calculate module and angle of a complex number.

    parameters
    ----------
    v : complex
        Complex number in format r + i j, where r is the real number
        and i the imaginary number of the complex number.
    ndigits: int
            Precision in decimal digits.
    Returns
    -------
    output : array-like
            [intensity, angle in degrees]
    '''
    return [round(abs(v), ndigits), round(np.rad2deg(np.angle(v)), ndigits)]

def rect(v, ndigits=8):
    '''
    Calculate complex number based on module and angle of number in
    polar form.

    Parameters
    ----------
    v : array-like
       [module, angle (degrees)]
    ndigits: int
            Precision in decimal digits.
    Returns
    -------
    out: complex
         Complex number in format r + i j, where r is the real number
         and i the imaginary number of the complex number.

    '''
    return round(v[0] * np.exp(np.deg2rad(v[1])*1j), ndigits)

α = np.exp(np.deg2rad(120)*1j)
A = np.array([[1,  1,    1   ],
              [1,  α**2, α   ],
              [1,  α    ,α**2]])

def to_symcomp(Va, Vb, Vc, ndigits = 3):  
    '''
    Calculate symmetric component vector from line vector.

    parameters
    ----------
    Va: array-like
        [module, angle (degrees)]
    Vb: array-like
        [module, angle (degrees)]
    Vc: array-like
        [module, angle (degrees)]
    ndigits: int
            Precision in decimal digits.
     
    Returns
    -------
    output : array-like
           (V1, V2, V0), each vector being in array format with
           [module, angle in degrees], where V1 is positive sequence,
           V2 negative sequence and V0 zero sequence.
    '''
    Vline = [rect(Va),
             rect(Vb),
             rect(Vc)]

    Vcomp = np.linalg.solve(A, Vline)
    V0, V1, V2 = Vcomp

    V0 = polar(V0, ndigits)
    V1 = polar(V1, ndigits)
    V2 = polar(V2, ndigits)

    V0 = [0,0] if V0[0] < 1e-10 else V0
    V0[1] = 0 if V0[1] < 1e-5 else V0[1] 

    V1 = [0,0] if V1[0] < 1e-10 else V1
    V1[1] = 0 if V1[1] < 1e-5 else V1[1] 

    V2= [0,0] if V2[0] < 1e-10 else V2
    V2[1] = 0 if V2[1] < 1e-5 else V2[1] 
    
    return V1,V2,V0

def to_linecomp(V1, V2, V0, ndigits = 3):
    '''
   Calculate line vector  from symmetric component vector.

   Parameters
    ----------
    V1: array-like
        [module, angle (degrees)]
    V2: array-like
        [module, angle (degrees)]
    V0: array-like
        [module, angle (degrees)]
    ndigits: int
            Precision in decimal digits.
     
    Returns
    -------
    output : array-like
           (Va, Vb, Vc), each vector being in array format with
           [module, angle (degrees)].
    '''
    Vcomp = [rect(V0),
             rect(V1),
             rect(V2)]
    
    Vline = A @ np.array(Vcomp)
    Va, Vb, Vc = Vline
    
    Va = polar(Va, ndigits)
    Vb = polar(Vb, ndigits)
    Vc = polar(Vc, ndigits)
    
    Va = [0,0] if Va[0] < 1e-10 else Va
    Va[1] = 0 if Va[1] < 1e-5 else Va[1] 

    Vb = [0,0] if Vb[0] < 1e-10 else Vb
    Vb[1] = 0 if Vb[1] < 1e-5 else Vb[1] 

    Vc= [0,0] if Vc[0] < 1e-10 else Vc
    Vc[1] = 0 if Vc[1] < 1e-5 else Vc[1] 

    return Va, Vb, Vc  

def plot3vectors(V, labels=['a','b','c']):
    '''
    plot three vectors array in polar graph.

    Parameters
    ----------
    V : array-like
        Vector V in format (Va, Vb, Vc), each vector in format
        of array with [module, angle (degrees)].
    labels: array-like
        Array of size 3 with string variables describing name
        of each vector to be plotted.
    '''

    plt.polar([0, np.deg2rad(V[0][1])], [0, V[0][0]], label=labels[0], marker='o')
    plt.polar([0, np.deg2rad(V[1][1])], [0, V[1][0]], label=labels[1], marker='o')
    plt.polar([0, np.deg2rad(V[2][1])], [0, V[2][0]], label=labels[2], marker='o')
    plt.legend()
    plt.show()

def overcurrent_time(I, Is , TD, standard='iec', curva='si'):
    '''
    Tempo de atuação da função de sobrecorrente.

    Parâmetros
    ----------
    I: float
        Measured current (Ampere)
    Is: float
        Setting current (Ampere)
    TD: float
        time adjustment
    standard: string
        'iec', 'ieee' or 'us'  
    standard: string
        Curve type according to standard.
        For 'iec':
            'si': Standard inverse
            'vi': Very inverse
            'ei': Extremely inverse
            'ltef': Long land missing
        For 'ieee':
            'mi': Inverse
            'vi': Very inverse
            'ei': Extremely inverse
        For 'us':
            'co8': US CO8 Inverse
            'co2': US CO2 Inverse short time
    Returns
    -------
    out: float
         Operating time (seconds).
    '''
    Ir = I/Is
    if standard=='iec':
        if curva=='si':
            return TD * (0.14 / ((Ir**0.02) - 1)) # Inversa Padrão
        if curva=='vi':
            return TD * (13.5 / (Ir - 1)) # Muito Inversa
        if curva=='ei':
            return TD * (80 / ((Ir**2) - 1)) # Extremamente Inversa
        if curva=='ltef':
            return TD * (80 / (Ir - 1)) # Falta a terra Longo

    if standard=='ieee':
        curva = 'mi' if curva == 'si' else curva 
        if curva=='mi':
            return (TD / 7) * ((0.0515 / ((Ir**0.02) - 1)) + 0.114) # Inversa
        if curva=='vi':
            return (TD / 7) * ((19.61 / ((Ir**2) - 1)) + 0.491) # Muito Inversa
        if curva=='ei':
            return (TD / 7) * ((28.2 / ((Ir**2) - 1)) + 0.1217) # Extremamente Inversa

    if standard=='us':
        curva = 'co8' if curva == 'si' else curva 
        if curva=='co8':
            return (TD / 7) * ((5.95 / ((Ir**2) - 1)) + 0.18) # US CO8 Inverso
        if curva=='co2':
            return (TD / 7) * ((0.02394 / ((Ir**0.02) - 1)) + 0.01694) # US CO2 Inverso tempo curto