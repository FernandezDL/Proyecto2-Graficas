import math

#Multiplicación de dos matrices de 4*4
def multi4x4matrix(matrix1, matrix2):
    resultado = [
        [0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0]]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                resultado[i][j] += matrix1[i][k] * matrix2[k][j]
    return resultado

#Multiplicación de una matriz con un vector 
def multimatrixvec(matrix, vect):
    resultado = [0.0, 0.0, 0.0, 0.0]

    for i in range(4):
        for j in range(4):
            resultado[i] += matrix[i][j] * vect[j]

    return resultado

#Multiplicación de vector y escalar
def multiply_scalar_array(scalar, array):
    result = []
    for i in range(len(array)):
        result.append(scalar * array[i])

    return tuple(result)

#Suma de vector y escalar
def add_scalar_array(scalar, array):
    result = []
    for i in range(len(array)):
        result.append(scalar + array[i])

    return tuple(result)

def add_vector_scaled(v1, scalar, v2):
    return [v1[i] + scalar * v2[i] for i in range(3)]

def multiply_vector_scalar(v, scalar):
    return [scalar * v[i] for i in range(3)]

#Producto cruz de dos vectores
def cross_product(vector_a, vector_b):
    if len(vector_a) != 3 or len(vector_b) != 3:
        raise ValueError("Los vectores tienen que ser de tres elementos")
    
    result = [0, 0, 0]
    
    result[0] = vector_a[1] * vector_b[2] - vector_a[2] * vector_b[1]
    result[1] = vector_a[2] * vector_b[0] - vector_a[0] * vector_b[2]
    result[2] = vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0]
    
    return result

#Producto punto de dos vectores
def dot_product(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores tienen que ser del mismo tamaño")
    
    result = 0
    for i in range(len(vector_a)):
        result += vector_a[i] * vector_b[i]
    
    return result

#Transpuesta de una matriz
def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    
    return transposed

def matrix_minor(matrix, row, col):
    return [row[:col] + row[col+1:] for row in (matrix[:row] + matrix[row+1:])]

#Determinante de una matriz
def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    
    det = 0
    for col in range(len(matrix)):
        det += ((-1) ** col) * matrix[0][col] * determinant(matrix_minor(matrix, 0, col))
    
    return det

#Matriz inverza
def matrix_inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("El determinante es 0, no se puede calcular la inversa.")
    
    rows = len(matrix)
    cols = len(matrix[0])
    adjugate = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            minor = matrix_minor(matrix, i, j)
            cofactor = ((-1) ** (i + j)) * determinant(minor)
            adjugate[j][i] = cofactor / det
    
    return adjugate

#Magnitud de un vector
def vector_magnitude(vector):
    return sum(component ** 2 for component in vector) ** 0.5

#Normalización de un vector
def normalize_vector(vector):
    magnitude = vector_magnitude(vector)
    normalized = [component / magnitude for component in vector]
    return normalized

#Saca la normal de un vector
def vector_normal(vector):
    square = sum(componente ** 2 for componente in vector)
    norma = square ** 0.5

    return norma

#Resta de dos vectores
def vector_subtraction(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores tienen que ser del mismo tamaño")
    
    result = [vector_a[i] - vector_b[i] for i in range(len(vector_a))]
    return result

#Suma de dos vectores
def vector_addition(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores tienen que ser del mismo tamaño")
    
    result = [vector_a[i] - vector_b[i] for i in range(len(vector_a))]
    return result

#División de dos vectores
def vector_division(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Se necesitan vectores de la misma magnitud.")

    r = [v1[i] / v2[i] for i in range(len(v1))]
    return r

def reflect(incident, normal):
    dot_product_result = 2 * dot_product(incident, normal)
    reflected = [incident[i] - dot_product_result * normal[i] for i in range(len(incident))]
    return reflected

def interpolate_colors(color1, color2, t):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int((1 - t) * r1 + t * r2)
    g = int((1 - t) * g1 + t * g2)
    b = int((1 - t) * b1 + t * b2)
    return r, g, b

def scalar_multiply(scalar, vector):
    result = [scalar * component for component in vector]
    return result

def VxE(v, e):
    r = [e*v[i] for i in range(len(v))]
    return r
    
def reflectVector(normal, direction):
    reflect = 2* dot_product(normal, direction)
    reflect = multiply_scalar_array(reflect, normal)
    reflect = vector_subtraction(reflect, direction)
    reflect = normalize_vector(reflect)
    
    return reflect

def producto_punto(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma longitud")

    product = sum(x * y for x, y in zip(vector1, vector2))
    return product

def totalInternalreflection(incident, normal, n1, n2):
    c1 = dot_product(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = [i * -1 for i in normal]
        n1, n2 = n2, n1

    if n1 < n2:
        return False
    
    theta1 = math.acos(c1)
    thetaC = math.asin(n2/n1)
    
    return theta1 >= thetaC

def refract_vector(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = [i * -1 for i in normal]
        n1, n2 = n2, n1
    
    n = n1 / n2

    escalar = (1 - n**2 * (1 - c1**2)) ** 0.5
    v1 = multiply_vector_scalar(add_vector_scaled(incident, c1, normal), n) 
    v2 =  multiply_vector_scalar(normal, escalar)
    T = vector_subtraction(v1, v2)
    T =  normalize_vector(T)
    return T

def fresnel(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1
    
    s2 = (n1 * (1 - c1**2) **0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5

    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt

def add_vector_scaled(v1, scalar, v2):
    return [v1[i] + scalar * v2[i] for i in range(3)]

def transform_vector(matrix, vector):
    # La matriz debe ser una lista de listas que representa una matriz 3x3 de transformación
    # El vector es una lista de tres elementos (las coordenadas x, y, z del vector)
    result = [0, 0, 0]

    for i in range(3):
        result[i] = sum(matrix[j] * vector[j] for j in range(3))

    return result


def barycentricCoords(A, B, C, P):
    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                 (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    # Si el área del triángulo es 0, retornar nada para
    # prevenir división por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas bariocéntricas dividiendo el 
    # área de cada subtriángulo por el área del triángulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada está entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son válidas.
    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and math.isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None