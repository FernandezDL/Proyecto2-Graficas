from math import pi, atan2, acos, sqrt, cos, sin 
import mathLib as ml
import ml2

class Intercept(object):
    def __init__(self, distance, point, normal, obj, texcoords):
        self.distance = distance
        self.point =point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None
    
class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        L = ml.vector_subtraction(self.position, orig) 
        lengthL = ml.vector_normal(L)
        tca = ml.dot_product(L, dir)
        d = sqrt(lengthL ** 2 - tca ** 2)

        if d > self.radius:
            return None
        
        thc = sqrt(self.radius ** 2 - d ** 2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 <= 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = ml.add_vector_scaled(orig, t0, dir)
        normal = ml.vector_subtraction(P, self.position)
        normal_length = ml.vector_normal(normal)
        normal = [normal[i] / normal_length for i in range(3)]

        u = (atan2(normal[2], normal[0]) / (2*pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance= t0,
                         point= P,
                         normal= normal,
                         texcoords= (u,v),
                         obj= self)

class OvalSphere(Sphere):
    def __init__(self, position, radius_x, radius_y, material):
        self.radius_x = radius_x
        self.radius_y = radius_y
        super().__init__(position, (radius_x + radius_y) / 2, material)
    
    def ray_intersect(self, orig, dir):
        L = ml.vector_subtraction(self.position, orig) 
        lengthL = ml.vector_normal(L)
        tca = ml.dot_product(L, dir)
        d = sqrt(lengthL ** 2 - tca ** 2)

        if d > max(self.radius_x, self.radius_y):
            return None
        
        thc_x = sqrt(self.radius_x ** 2 - d ** 2)
        thc_y = sqrt(self.radius_y ** 2 - d ** 2)

        t0_x = tca - thc_x
        t1_x = tca + thc_x
        t0_y = tca - thc_y
        t1_y = tca + thc_y

        # Encuentra la intersección más cercana en cada eje
        t0 = min(t0_x, t1_x, t0_y, t1_y)
        t1 = max(t0_x, t1_x, t0_y, t1_y)

        if t0 <= 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = ml.add_vector_scaled(orig, t0, dir)

        # Calcula la normal en función de las coordenadas de la esfera ovalada
        normal = [
            (P[0] - self.position[0]) / self.radius_x ** 2,
            (P[1] - self.position[1]) / self.radius_y ** 2,
            (P[2] - self.position[2]) / self.radius_x ** 2  # Puedes ajustar según la forma deseada
        ]

        normal_length = ml.vector_normal(normal)
        normal = [normal[i] / normal_length for i in range(3)]

        u = (atan2(normal[2], normal[0]) / (2*pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=(u, v),
                         obj=self)

class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = ml.normalize_vector(normal)
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        #Distancia = (planePos - origRay) o normal) / (dirRay o normal)
        
        denom = ml.dot_product(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = ml.dot_product(ml.vector_subtraction(self.position, orig), self.normal)
        t = num/denom
        
        if t<0:
            return None
        
        p = ml.vector_addition(orig, ml.multiply_scalar_array(t, dir))
        
        return Intercept(distance = t,
                         point = p,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)
    
    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)
        
        if planeIntersect is None:
            return None
        
        # contactDistance = np.subtract(planeIntersect.point, self.position)
        # contactDistance = np.linalg.norm(contactDistance)
        contactDistance = ml.vector_subtraction(planeIntersect.point, self.position)
        contactDistance = ml.vector_normal(contactDistance)
        
        if contactDistance > self.radius:
            return None
        
        return Intercept(distance = planeIntersect.distance,
                         point = planeIntersect.point,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class AABB(Shape):
    #Axis Aligned Bounding Box
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes=[]
            
        leftPlane= Plane(ml.vector_addition(self.position, (-size[0]/ 2,0,0)), (-1,0,0), material)
        rigthPlane= Plane(ml.vector_addition(self.position, (size[0]/ 2,0,0)), (1,0,0), material)
            
        bottomPlane= Plane(ml.vector_addition(self.position, (0,-size[1]/ 2,0)), (0,-1,0), material)
        topPlane= Plane(ml.vector_addition(self.position, (0,size[1]/ 2,0)), (0,1,0), material)

        backPlane= Plane(ml.vector_addition(self.position, (0,0, -size[2]/ 2)), (0,0,-1), material)
        frontPlane= Plane(ml.vector_addition(self.position, (0,0, size[2]/ 2)), (0,0,1), material)

        self.planes.append(leftPlane)
        self.planes.append(rigthPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        #Bounds
        self.boundsMin= [0,0,0]
        self.boundsMax= [0,0,0]

        bias= 0.001

        for i in range(3):
            self.boundsMin[i]= self.position[i] - (bias + size[i] / 2)
            self.boundsMax[i]= self.position[i] + (bias + size[i] / 2)
    
    def ray_intersect(self, orig, dir):
        intersect= None
        t= float('inf')

        u= 0
        v= 0

        for plane in self.planes:
            planeIntersect= plane.ray_intersect(orig, dir)

            if planeIntersect is not None:
                planePoint= planeIntersect.point

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t= planeIntersect.distance
                                intersect= planeIntersect

                                #Generar las uvs
                                if abs(plane.normal[0]) > 0:
                                    #Estoy en X, usamos Y y Z para crear las uvs
                                    u= (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v= (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)

                                elif abs(plane.normal[1]) > 0:
                                    #Estoy en Y, usamos X y Z para crear las uvs
                                    u= (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)

                                elif abs(plane.normal[2]) > 0:
                                    #Estoy en X, usamos Y y Z para crear las uvs
                                    u= (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None
        
        return Intercept(distance= t,
                         point= intersect.point,
                         normal= intersect.normal,
                         texcoords= (u, v),
                         obj= self)

class Triangle(Shape):
    def __init__(self, vertices, material):
        self.vertices = vertices

        v0 = ml.vector_subtraction(self.vertices[1], self.vertices[0])
        v1 = ml.vector_subtraction(self.vertices[2],self.vertices[0])
        self.normal = ml.normalize_vector(ml.cross_product(v0,v1))

        x = (vertices[0][0] + vertices[1][0]+vertices[2][0])/3
        y = (vertices[0][1] + vertices[1][1]+vertices[2][1])/3
        z = (vertices[0][2] + vertices[1][2]+vertices[2][2])/3

        super().__init__((x,y,z), material)

    def ray_intersect(self, orig, dir):
        denom = ml.dot_product(dir, self.normal)
                
        if abs(denom)<=0.0001:
            return None
        
        d = -1 * ml.dot_product(self.normal, self.vertices[0])
        num = -1 * (ml.dot_product(self.normal, orig) + d)

        t = num/denom 

        if t < 0:
            return None
        
        P = ml.vector_addition(orig, ml.multiply_scalar_array(t,dir))

        #edge 0
        edge0 = ml.vector_subtraction(self.vertices[1],self.vertices[0]) #v1 - v0; 
        vp0 = ml.vector_subtraction(P,self.vertices[0]) #Vec3f vp0 = P - v0;
        C = ml.cross_product(edge0,vp0)
        
        if ml.dot_product(self.normal,C)<0: 
            return None
        
        #edge 1
        edge1 = ml.vector_subtraction(self.vertices[2], self.vertices[1])    #Vec3f edge1 = v2 - v1; 
        vp1 = ml.vector_subtraction(P, self.vertices[1])    #Vec3f vp1 = P - v1;
        C = ml.cross_product(edge1,vp1);
        
        if ml.dot_product(self.normal, C) < 0:    
            return None
    
        #edge 2
        edge2 = ml.vector_subtraction(self.vertices[0],self.vertices[2]) #v0 - v2; 
        vp2 = ml.vector_subtraction(P,self.vertices[2]) #Vec3f vp2 = P - v2;
        C = ml.cross_product(edge2,vp2);
        
        if ml.dot_product(self.normal, C) < 0:   
            return None 
        
        u,v,w = ml.barycentricCoords(self.vertices[0], self.vertices[1], self.vertices[2], P)

        
        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=(u,v),
                         obj=self)  
    
#Ovalo
class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        self.radii = radii
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        
        l = ml.vector_subtraction(orig,self.position)
        l = ml.vector_division(l,self.radii)
        dir = ml.vector_division(dir,self.radii)
        
        a = ml.dot_product(dir, dir)
        b = 2.0 * ml.dot_product(dir, l)
        c = ml.dot_product(l, l) - 1.0
        
        dis = (b**2) - (4*a*c)
    
        if dis < 0:
            return None
        
        t1 = (-b + sqrt(dis)) / (2 * a)
        t2 = (-b - sqrt(dis)) / (2 * a)
        
        if t1 < 0 and t2 <0:
            return None
        
        if t1 < t2:
            t = t1
        else:
            t = t2
            
        p = ml.vector_addition(orig, ml.VxE(dir, t))
        
        normal = ml.vector_subtraction(p, self.position)
        normal = ml.vector_division(normal, self.radii)
        normal = ml.normalize_vector(normal)
        
        u = 1-((atan2(normal[2], normal[0])+pi)/(2*pi))
        v = ((acos(normal[1])+pi)/2)/pi
        
        return Intercept(distance = t,
                         point = p,
                         normal = normal,
                         texcoords= (u,v),
                         obj = self)

#Cilindro  
class Cylinder(Shape):
    def __init__(self, position, height, radius, material, direction=(0, 1, 0)):
        self.height = height
        self.radius = radius
        self.direction = ml.normalize_vector(direction)
        self.base1 = Disk(position, direction, radius, material)
        self.base2 = Disk(ml.vector_addition(position, [direction[i] * height for i in range(3)]), direction, radius, material)
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        min_distance = float('inf')
        closest_intersect = None

        for base in [self.base1, self.base2]:
            intersect = base.ray_intersect(orig, dir)
            if intersect is not None and intersect.distance < min_distance:
                min_distance = intersect.distance
                closest_intersect = intersect

        ao = ml.vector_subtraction(orig, self.position)
        delta = ml.dot_product(dir, self.direction)
        a = ml.dot_product(dir, dir) - delta ** 2
        b = 2 * (ml.dot_product(dir, ao) - delta * ml.dot_product(ao, self.direction))
        c = ml.dot_product(ao, ao) - ml.dot_product(ao, self.direction) * 2 - self.radius * 2
        discriminant = b ** 2 - 4 * a * c

        if discriminant > 0:
            t0 = (-b - sqrt(discriminant)) / (2 * a)
            t1 = (-b + sqrt(discriminant)) / (2 * a)
            t = min(t0, t1)

            if t > 0 and t < min_distance:
                P = ml.add_vector_scaled(orig, t, dir)
                normal = ml.vector_subtraction(P, self.position)
                normal = ml.vector_subtraction(normal, [self.direction[i] * ml.dot_product(normal, self.direction) for i in range(3)])
                normal_length = ml.vector_normal(normal)
                normal = [normal[i] / normal_length for i in range(3)]

                height_intersect = ml.dot_product(ml.vector_subtraction(P, self.position), self.direction)
                if 0 <= height_intersect <= self.height:
                    return Intercept(distance=t, 
                                     point=P, 
                                     normal=normal, 
                                     texcoords=None, 
                                     obj=self)

        return closest_intersect
    
class Rectangle(Shape):
    def __init__(self, position, normal, width, height, material):
        self.normal = ml.normalize_vector(normal)
        self.width = width
        self.height = height
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        denom = ml.dot_product(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = ml.dot_product(ml.vector_subtraction(self.position, orig), self.normal)
        t = num / denom
        
        if t < 0:
            return None
        
        p = ml.vector_addition(orig, ml.multiply_scalar_array(t, dir))
        
        # Verificar si el punto de intersección está dentro del rectángulo
        to_intersect_point = ml.vector_subtraction(p, self.position)
        half_width = self.width / 2
        half_height = self.height / 2
        
        if (
            -half_width <= to_intersect_point[0] <= half_width and
            -half_height <= to_intersect_point[1] <= half_height
        ):
            return Intercept(
                distance=t,
                point=p,
                normal=self.normal,
                texcoords=None,
                obj=self
            )
        else:
            return None
