import copy
class MapNode:
    def __init__(self , key = None , aristas = None , distancia = None):
        self.key = key
        self.list = []    #Esta lista sirve para poner sus nodos adyacentes
        self.peso_minimo = None
        self.padre = None
        self.dijkstra = {}


class Node(MapNode): # clase creada para ser insertada a la lista de adyacencia
    def __init__(self , key = None, distancia = None):
        self.key = key
        self.distancia = distancia

        
class Ubicacion: # Nodo que representa una ubicacion fija
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion # forma direccion lista con 2 tuplas (<ex, d>, <ey, d>)
        self.list = []

class Movil(Ubicacion): # Nodo que representa una Persona o un Auto
    def __init__(self, nombre, direccion, monto):
        super().__init__(nombre, direccion)
        self.monto = monto
        
class NodoRanking:
    def __init__(self , auto , distancia_viaje , monto_auto):
        self.auto = auto
        self.distancia_viaje = distancia_viaje
        self.precio_viaje = (distancia_viaje + int(monto_auto))/4

class NodoShortPath:
    def __init__(self, esquinas, peso_camino):
        self.esquinas = esquinas
        self.peso_camino = peso_camino
        

class Map:
    def __init__(self , vertices = None , aristas = None):
        self.vertices = vertices
        self.aristas = aristas
        
    def createMap(self , vertices, aristas):
        dict = {}
        #Agrego las esquinas

        for key in vertices:
            dict[key] = MapNode(key)

        dict = self.connections(dict , aristas)

        return dict
    
    def insert(self, mapa, nodo, esquina_x , esquina_y): # Inserta nodo individual

        if esquina_x != None:
            v1_node = Node(esquina_x, nodo.direccion[0][1])
            mapa[nodo.nombre].list.append(v1_node)

        if esquina_y != None:
            v2_node = Node(esquina_y, nodo.direccion[1][1])
            mapa[nodo.nombre].list.append(v2_node)
    
    def delete(self, mapa, elemento): 

        # en caso de una direccion se va a crear e insertar un NodoViaje que va a tener su propia key
        
        if elemento in mapa:
            nodo = mapa[elemento]
        else:
            return "element don't exist"
        
        esquina_1 = nodo.direccion[0][0]
        esquina_2 = nodo.direccion[1][0]

        #elimino al nodo  de la lista de adyacencia de la primera esquina
        for adyacente in mapa[esquina_1].list:  
            if adyacente.key == nodo.nombre: # Node tiene atributo key, mientras que los Nodos Moviles y Fijos tienen atributo nombre(key)
                mapa[esquina_1].list.remove(adyacente)

        #elimino al nodo  de la lista de adyacencia de la segunda esquina
        for adyacente in mapa[esquina_2].list:  
            if adyacente.key == nodo.nombre:
                mapa[esquina_2].list.remove(adyacente)

        if nodo.nombre in mapa["autos"]:
            mapa["autos"].remove(nodo.nombre) # Si el objeto a eliminar es un auto, se elimina de la lista

        del mapa[nodo.nombre]


    def connections(self , dict , aristas):

        for (v1 , v2 , c) in aristas: # c es el peso de la arista
            if v1 != v2:
                
                node = Node(v2, int(c))

                dict[v1].list.append(node)
            else: 
                node = Node(v1, int(c))

                dict[v1].list.append(node)
        return dict
    
    def insert_fixed(self, mapa, nombre, direccion):

        if nombre in mapa:
            return print("Ubication already exist, won't be added")

        suma_aux = direccion[0][1] + direccion[1][1]

        node = Ubicacion(nombre, direccion)
        tupla_x = direccion[0] 
        tupla_y = direccion[1]

        v1 = tupla_x[0] 
        v2 = tupla_y[0]

        flag1 = False
        flag2 = False

        #La calle va de v2 a v1
        for objeto in mapa[v2].list:
            if objeto.key == v1:
                flag1 = True
                if suma_aux != objeto.distancia:
                    return print("La direccion ingresada no es válida")


        #La calle va de v1 a v2
        for objeto in mapa[v1].list:
            if objeto.key == v2:
                flag2 = True
                if suma_aux != objeto.distancia:
                    return print("La direccion ingresada no es válida")


        if flag1 == True and flag2 == True: ## la calle es doble mano
            
            mapa[node.nombre] = node # agregamos una nueva ubicacion en el mapa

            self.insert(mapa, node , v1 , v2) # Insertamos en la ubicacion las esquinas adyacentes y las distancias

            # Insertamos en las esquinas la nueva adyacencia
            aux = Node(node.nombre, tupla_x[1]) 
            mapa[v1].list.append(aux) 
            aux = Node(node.nombre, tupla_y[1]) 
            mapa[v2].list.append(aux)
            
        elif flag1 == True:     #La calle va de v2 a v1
            mapa[node.nombre] = node 
            self.insert(mapa , node , v1 , None)

            aux = Node(node.nombre , tupla_y[1])
            mapa[v2].list.append(aux)
        else:                   #La calle va de v1 a v2
            mapa[node.nombre] = node 
            self.insert(mapa , node , None , v2)

            aux = Node(node.nombre , tupla_x[1])
            mapa[v1].list.append(aux)


    def insert_movile(self, mapa, nombre, direccion, monto):

        if nombre in mapa:
            return print("El nombre de la ubicacion ya existe")

        suma_aux = direccion[0][1] + direccion[1][1]

        node = Movil(nombre, direccion, monto)
        tupla_x = direccion[0]  
        tupla_y = direccion[1]

        v1 = tupla_x[0] 
        v2 = tupla_y[0]

        flag1 = False
        flag2 = False

        #La calle va de v2 a v1
        for objeto in mapa[v2].list:
            if objeto.key == v1:
                flag1 = True
                if suma_aux != objeto.distancia:
                    return print("La direccion ingresada no es válida")


        #La calle va de v1 a v2
        for objeto in mapa[v1].list:
            if objeto.key == v2:
                flag2 = True
                if suma_aux != objeto.distancia:
                    return print("La direccion ingresada no es válida")


        if flag1 == True and flag2 == True: ## la calle es doble mano
            
            mapa[node.nombre] = node # agregamos una nueva ubicacion en el mapa

            self.insert(mapa, node , v1 , v2) # Insertamos en la ubicacion las esquinas adyacentes y las distancias

            # Insertamos en las esquinas la nueva adyacencia
            aux = Node(node.nombre, tupla_x[1]) 
            mapa[v1].list.append(aux) 
            aux = Node(node.nombre, tupla_y[1]) 
            mapa[v2].list.append(aux)
            
        elif flag1 == True:     #La calle va de v2 a v1
            mapa[node.nombre] = node 
            self.insert(mapa , node , v1 , None)

            aux = Node(node.nombre , tupla_y[1])
            mapa[v2].list.append(aux)
        else:                   #La calle va de v1 a v2
            mapa[node.nombre] = node 
            self.insert(mapa , node , None , v2)

            aux = Node(node.nombre , tupla_x[1])
            mapa[v1].list.append(aux)

    def doble_sentido(self , mapa , nombre_persona):
        persona = mapa[nombre_persona]
        esquina1 = persona.direccion[0][0]
        esquina2 = persona.direccion[1][0]

        #Listas de adyacencia de las esquinas
        adyacentes_1 = mapa[esquina1].list 
        adyacentes_2 = mapa[esquina2].list

        flag1 = False
        flag2 = False

        for nodo in adyacentes_1:
            if nodo.key == esquina2:
                flag1 = True #Dentro de la esquina 1 se encuentra la esquina 2

        for nodo in adyacentes_2:
            if nodo.key == esquina1:
                flag2 = True #Dentro de la esquina 2 se encuentra la esquina 1

        if flag1 == True and flag2 == True: #Si la calle es doble sentido entonces retorna true
            return True
        else:
            return False


    def initRelax(self, map, nodo_inicial): # Funcion para relajar cada MapNode (esquinas)

        for esquina in map:
            if esquina != nodo_inicial.key:
                map[esquina].peso_minimo = float('inf')
                map[esquina].padre = None
            else:
                map[nodo_inicial.key].peso_minimo = 0
        return map
    
    def Relax(self, esquina1, esquina2 , distancia_e2): # Funcion que actualiza el peso_minimo de cada nodo, excepto el de partida
        #Esquina 1 y esquina 2 son del tipo MapNode y distancia_e2 es la distancia entre la e1 a la e2

        if esquina2.peso_minimo > (esquina1.peso_minimo + distancia_e2):
            esquina2.peso_minimo = esquina1.peso_minimo + distancia_e2
            esquina2.padre = esquina1.key

    def Dijkstra(self, mapa, esquina_inicial):
        new_map = copy.deepcopy(mapa)  #Se crea una copia profunda de mapa, lo que garantiza que todos los objetos y estructuras de datos internos se copien correctamente sin compartir referencias
        self.initRelax(new_map, esquina_inicial)
        visited = set()
        lista_pesos = []
        for key in new_map:
            lista_pesos.append(new_map[key])

        lista_pesos = sorted(lista_pesos, key=lambda x: x.peso_minimo)

        while len(lista_pesos) > 0:
            current_node = lista_pesos.pop(0)
            visited.add(current_node)

            for adyacente in current_node.list:
                aux = new_map[adyacente.key]
                if aux not in visited:
                    self.Relax(current_node, aux, adyacente.distancia)

            lista_pesos = sorted(lista_pesos, key=lambda x: x.peso_minimo)

        return new_map
        

    def dijkstraInNodes(self, mapa):
        new_mapa = {}  # Crear un nuevo diccionario para almacenar los resultados

        for key in mapa:
            current_map = mapa.copy()  # Crear una copia independiente del mapa en cada iteración
            current_map[key].dijkstra = self.Dijkstra(current_map, current_map[key])
            new_mapa[key] = current_map  # Guardar el resultado en el nuevo diccionario

        return new_mapa
    
    def ranking_autos(self , mapa , persona):


        if persona not in mapa:
            return "Los datos ingresados no son válidos"
        
        direccion_persona = mapa[persona].direccion
        esquina_1 = direccion_persona[0][0]
        esquina_2 = direccion_persona[1][0]

        #Si esta en una calle doble sentido utilizo esquina_persona_1 y esquina_persona_2  , sino solo utilizo esquina_persona
        esquina_persona = None
        esquina_persona_1 = None #Uso dos esquinas para ver que camino es mas corto
        esquina_persona_2 = None

        if self.doble_sentido(mapa , persona) == False:
            for adyacente in mapa[persona].list:
                if adyacente.key == esquina_1: #Si apunta a la esquina 1 entonces me quedo con la esquina 2
                    esquina_persona = mapa[esquina_2].key 
                else: #Si apunta a la esquina 2 entonces me quedo con la esquina 1
                    esquina_persona = mapa[esquina_1].key
        else:
            """
            Me voy a fijar la menor distancia desde el auto hasta las esquinas
            pero me voy a quedar con la de menor peso
            """
            esquina_persona_1 = mapa[esquina_1].key
            esquina_persona_2 = mapa[esquina_2].key

        """
        Ahora hay que calcular la esquina desde donde se va a iniciar la verificacion 
        del camino mas corto hasta la esquina de la persona
        """
        #Si esta en una calle doble sentido utilizo esquina_inicial_dijkstra_1 y esquina_inicial_dijkstra_2 , sino solo utilizo esquina_inicial_dijkstra

        lista_autos = mapa["autos"]
        lista_ranking = []
        
        for auto in lista_autos:

            esquina_inicial_dijkstra = None  
            esquina_inicial_dijkstra_1 = None
            esquina_inicial_dijkstra_2 = None

            direccion_auto = mapa[auto].direccion
            esquina_1_auto = direccion_auto[0][0]
            esquina_2_auto = direccion_auto[1][0]

            if esquina_1_auto not in mapa or esquina_2_auto not in mapa:
                return "Datos invalidos"
            
            if esquina_1 == esquina_1_auto and esquina_2 == esquina_2_auto:
                for adyacente in mapa[esquina_1].list:
                    if adyacente.key == auto:
                        aux = adyacente.distancia
                    elif adyacente.key == persona:
                        aux2 = adyacente.distancia
                nodo_aux = NodoRanking(auto , abs(aux-aux2), mapa[auto].monto)
                lista_ranking.append(nodo_aux)
                continue


            if self.doble_sentido(mapa , auto) == False:

                esquinas_adyacente = mapa[auto].list[0] # Las esquinas adyacentes al auto
                if esquinas_adyacente.key == esquina_1_auto: 
                    esquina_inicial_dijkstra = esquina_1_auto # Sigo el sentido de la calle y a partir de esa esquina busco la esquina de la persona
                else:
                    esquina_inicial_dijkstra = esquina_2_auto #Lo mismo de arriba
            else:
                esquina_inicial_dijkstra_1 = esquina_1_auto # Uso las 2 esquinas como iniciales y me quedo con la que tenga menor peso para llegar a la esquina de la persona
                esquina_inicial_dijkstra_2 = esquina_2_auto
            

            #Armo el ranking dependiendo de los casos
            if esquina_inicial_dijkstra != None and esquina_persona != None:
                distancia_camino = mapa[esquina_inicial_dijkstra].dijkstra[esquina_persona].peso_minimo
                distancia_auto = mapa[auto].list[0].distancia #Distancia del auto hacia la esquina donde voy a iniciar el viaje

                for elemento in mapa[esquina_persona].list: #Busco la persona dentro de la lista de adyacencia de la esquina 
                    if elemento.key == persona:
                        distancia_total = distancia_camino + elemento.distancia + distancia_auto #Sumo la distancia de el auto-esquina , esquina-persona y esquina_auto-esquina_persona
                        nodo_aux = NodoRanking(auto , distancia_total, mapa[auto].monto)
                        lista_ranking.append(nodo_aux)
            
            elif esquina_inicial_dijkstra == None and esquina_persona != None:
                
                #Calculo para la primera esquina del auto
                distancia_camino_1 = mapa[esquina_inicial_dijkstra_1].dijkstra[esquina_persona].peso_minimo
                distancia_auto_1 = mapa[auto].list[0].distancia #Distancia del auto hacia la esquina donde voy a iniciar el viaje

                for elemento in mapa[esquina_persona].list: #Busco la persona dentro de la lista de adyacencia de la esquina 
                    if elemento.key == persona:
                        distancia_total_1 = distancia_camino_1 + elemento.distancia + distancia_auto_1 #Sumo la distancia de el auto-esquina , esquina-persona y esquina_auto-esquina_persona
                
                #Calculo para la segunda esquina del auto
                distancia_camino_2 = mapa[esquina_inicial_dijkstra_2].dijkstra[esquina_persona].peso_minimo
                distancia_auto_2 = mapa[auto].list[1].distancia #Distancia del auto hacia la esquina donde voy a iniciar el viaje

                for elemento in mapa[esquina_persona].list: #Busco la persona dentro de la lista de adyacencia de la esquina 
                    if elemento.key == persona:
                        distancia_total_2 = distancia_camino_2 + elemento.distancia + distancia_auto_2 #Sumo la distancia de el auto-esquina , esquina-persona y esquina_auto-esquina_persona
                
                if distancia_total_1 <= distancia_total_2:
                    nodo_aux = NodoRanking(auto , distancia_total_1, mapa[auto].monto)
                    lista_ranking.append(nodo_aux)
                else:
                    nodo_aux = NodoRanking(auto , distancia_total_2, mapa[auto].monto)
                    lista_ranking.append(nodo_aux)                   

            elif esquina_inicial_dijkstra != None and esquina_persona == None:

                #En este caso el nodo de inicio es el mismo pero el de destino cambia
                distancia_camino_1 = mapa[esquina_inicial_dijkstra].dijkstra[esquina_persona_1].peso_minimo
                distancia_camino_2 = mapa[esquina_inicial_dijkstra].dijkstra[esquina_persona_2].peso_minimo

                distancia_auto = mapa[auto].list[0].distancia #Distancia del auto hacia la esquina donde voy a iniciar el viaje

                for elemento in mapa[esquina_persona_1].list: #Busco la persona dentro de la lista de adyacencia de la esquina 
                    if elemento.key == persona:
                        distancia_total_1 = distancia_camino_1 + elemento.distancia + distancia_auto #Sumo la distancia de el auto-esquina , esquina-persona y esquina_auto-esquina_persona
                
                for elemento in mapa[esquina_persona_2].list: #Busco la persona dentro de la lista de adyacencia de la esquina 
                    if elemento.key == persona:
                        distancia_total_2 = distancia_camino_2 + elemento.distancia + distancia_auto #Sumo la distancia de el auto-esquina , esquina-persona y esquina_auto-esquina_persona

                if distancia_total_1 <= distancia_total_2:
                    nodo_aux = NodoRanking(auto , distancia_total_1, mapa[auto].monto)
                    lista_ranking.append(nodo_aux)
                else:
                    nodo_aux = NodoRanking(auto , distancia_total_2, mapa[auto].monto)
                    lista_ranking.append(nodo_aux)  

            else:

                lista_menores = []
                distancia_camino_1 = mapa[esquina_inicial_dijkstra_1].dijkstra[esquina_persona_1].peso_minimo
                distancia_camino_2 = mapa[esquina_inicial_dijkstra_1].dijkstra[esquina_persona_2].peso_minimo
                distancia_camino_3 = mapa[esquina_inicial_dijkstra_2].dijkstra[esquina_persona_1].peso_minimo
                distancia_camino_4 = mapa[esquina_inicial_dijkstra_2].dijkstra[esquina_persona_2].peso_minimo

                distancia_auto_1 = mapa[auto].list[0].distancia
                distancia_auto_2 = mapa[auto].list[1].distancia

                for elemento in mapa[esquina_persona_1].list:
                    if elemento.key == persona:
                        distancia_total_1 = elemento.distancia + distancia_camino_1 + distancia_auto_1
                        distancia_total_3 = elemento.distancia + distancia_camino_3 + distancia_auto_2

                for elemento in mapa[esquina_persona_2].list:
                    if elemento.key == persona:
                        distancia_total_2 = elemento.distancia + distancia_camino_2 + distancia_auto_1
                        distancia_total_4 = elemento.distancia + distancia_camino_4 + distancia_auto_2

                lista_menores.append(distancia_total_1)
                lista_menores.append(distancia_total_2)
                lista_menores.append(distancia_total_3)
                lista_menores.append(distancia_total_4)

                nodo_aux = NodoRanking(auto, min(lista_menores) , mapa[auto].monto)
                lista_ranking.append(nodo_aux)

        lista_ranking = sorted(lista_ranking, key=lambda x: x.precio_viaje)
        aux_list = []
        for nodo in lista_ranking:
            if int(mapa[persona].monto) >= nodo.precio_viaje:
                aux_list.append((nodo.auto , nodo.precio_viaje))
        if len(aux_list) > 3:
            aux_list = aux_list[:3]  #Tomo los 3 primeros
        return aux_list

    def exist_location(self, mapa , direccion):

        esquina_1 = direccion[0][0]
        esquina_2 = direccion[1][0]
        distancia_total = direccion[0][1] + direccion[1][1]

        if esquina_1 not in mapa or esquina_2 not in mapa:
            return False


        for adyacente in mapa[esquina_1].list:
            if adyacente.key == esquina_2:
                distancia_total = distancia_total - adyacente.distancia

        return distancia_total == 0
    
    def short_path(self , mapa , persona , ubicacion):
        #Ubicacion seria la key del NodoViaje que le paso ('Destino')
        #La funcion hace lo mismo que ranking_autos pero no hay q iterar los autos, solo me fijo en una direccion
        if persona not in mapa:
            return "Los datos ingresados no son válidos"
        
        direccion_persona = mapa[persona].direccion
        esquina_1 = direccion_persona[0][0]
        esquina_2 = direccion_persona[1][0]

        #Si esta en una calle doble sentido utilizo esquina_persona_1 y esquina_persona_2  , sino solo utilizo esquina_persona
        esquina_persona = None
        esquina_persona_1 = None #Uso dos esquinas para ver que camino es mas corto
        esquina_persona_2 = None

        if self.doble_sentido(mapa , persona) == False:
            for adyacente in mapa[persona].list: # quiero tomar la esquina que respete el sentido de la calle
                if adyacente.key == esquina_1: 
                    esquina_persona = mapa[esquina_1].key 
                else: 
                    esquina_persona = mapa[esquina_2].key
        else:
            esquina_persona_1 = mapa[esquina_1].key
            esquina_persona_2 = mapa[esquina_2].key

        # hago el mismo proceso pero para la ubicacion

        esquina_final_dijkstra = None  
        esquina_final_dijkstra_1 = None
        esquina_final_dijkstra_2 = None

        direccion = mapa[ubicacion].direccion
        esquina_1_direccion = direccion[0][0]
        esquina_2_direccion = direccion[1][0]

        lista_recorrido = []

        if esquina_1 == esquina_1_direccion and esquina_2 == esquina_2_direccion:
            lista_recorrido.append((persona , ubicacion))
            return lista_recorrido
            #Seria el caso donde esten en la misma calle la persona y la direccion de llegada

        if self.doble_sentido(mapa , ubicacion) == False:

            esquinas_adyacente = mapa[ubicacion].list[0] # Las esquinas adyacentes al auto
            if esquinas_adyacente.key == esquina_1_direccion: 
                esquina_final_dijkstra = esquina_2_direccion # Sigo el sentido de la calle y a partir de esa esquina busco la esquina de la persona
            else:
                esquina_final_dijkstra = esquina_1_direccion #Lo mismo de arriba
        else:
            esquina_final_dijkstra_1 = esquina_1_direccion # Uso las 2 esquinas como iniciales y me quedo con la que tenga menor peso para llegar a la esquina de la persona
            esquina_final_dijkstra_2 = esquina_2_direccion
        

        #Armo la lista dependiendo de los casos
        if esquina_final_dijkstra != None and esquina_persona != None:
            distancia_camino = mapa[esquina_persona].dijkstra[esquina_final_dijkstra].peso_minimo
            distancia_persona = mapa[persona].list[0].distancia #De persona a la esquina inicial de dijkstra

            for elemento in mapa[esquina_final_dijkstra].list: 
                if elemento.key == ubicacion:
                    distancia_total = distancia_camino + elemento.distancia + distancia_persona 
                    #Funcion que devuelva el camino empezando en mapa[esquina_persona].dijkstra hasta esquina_final_dijkstra
                    lista_recorrido = self.recorrido(mapa[esquina_persona].dijkstra, esquina_final_dijkstra, [])
                    lista_recorrido = self.hacer_tupla(persona, lista_recorrido, ubicacion)
                    break
            
            return lista_recorrido
        
        elif esquina_final_dijkstra == None and esquina_persona != None:
            
            distancia_camino_1 = mapa[esquina_persona].dijkstra[esquina_final_dijkstra_1].peso_minimo
            distancia_camino_2 = mapa[esquina_persona].dijkstra[esquina_final_dijkstra_2].peso_minimo
            distancia_persona = mapa[persona].list[0].distancia 

            for elemento in mapa[esquina_final_dijkstra_1].list:
                if elemento.key == ubicacion:
                    distancia_total_1 = distancia_persona + elemento.distancia + distancia_camino_1

            for elemento in mapa[esquina_final_dijkstra_2].list:
                if elemento.key == ubicacion:
                    distancia_total_2 = distancia_persona + elemento.distancia + distancia_camino_2

            if distancia_total_1 <= distancia_camino_2:
                #Funcion recursiva desde mapa[esquina_persona].dijkstra esquina_final_dijkstra_1
                lista_recorrido = self.recorrido(mapa[esquina_persona].dijkstra, esquina_final_dijkstra_1, [])
                lista_recorrido = self.hacer_tupla(persona, lista_recorrido, ubicacion)
            else:
                #Funcion recursiva desde mapa[esquina_persona].dijkstra esquina_final_dijkstra_2
                lista_recorrido = self.recorrido(mapa[esquina_persona].dijkstra, esquina_final_dijkstra_2, [])
                lista_recorrido = self.hacer_tupla(persona, lista_recorrido, ubicacion)

            return lista_recorrido
        
        elif esquina_final_dijkstra != None and esquina_persona == None:

            distancia_camino_1 = mapa[esquina_persona_1].dijkstra[esquina_final_dijkstra].peso_minimo
            distancia_camino_2 = mapa[esquina_persona_2].dijkstra[esquina_final_dijkstra].peso_minimo
            distancia_persona_1 = mapa[persona].direccion[0][1]
            distancia_persona_2 = mapa[persona].direccion[1][1]

            for elemento in mapa[esquina_final_dijkstra].list:
                if elemento.key == ubicacion:
                    distancia_total_1 = elemento.distancia + distancia_camino_1 + distancia_persona_1
                    distancia_total_2 = elemento.distancia + distancia_camino_2 + distancia_persona_2
                    
            if distancia_total_1 <= distancia_camino_2:
                #Funcion recursiva desde mapa[esquina persona_1].dijkstra hasta esquina_final_dijkstra
                lista_recorrido = self.recorrido(mapa[esquina_persona_1].dijkstra, esquina_final_dijkstra, [])
                lista_recorrido = self.hacer_tupla(persona, lista_recorrido, ubicacion)
            else:
                #Funcion recursiva desde mapa[esquina persona_2].dijkstra hasta esquina_final_dijkstra
                lista_recorrido = self.recorrido(mapa[esquina_persona_2].dijkstra, esquina_final_dijkstra, [])
                lista_recorrido = self.hacer_tupla(persona, lista_recorrido, ubicacion)

            return lista_recorrido
        
        elif esquina_final_dijkstra == None and esquina_persona == None:
            
            distancia_camino_1 = mapa[esquina_persona_1].dijkstra[esquina_final_dijkstra_1].peso_minimo
            distancia_camino_2 = mapa[esquina_persona_1].dijkstra[esquina_final_dijkstra_2].peso_minimo
            distancia_camino_3 = mapa[esquina_persona_2].dijkstra[esquina_final_dijkstra_1].peso_minimo
            distancia_camino_4 = mapa[esquina_persona_2].dijkstra[esquina_final_dijkstra_2].peso_minimo

            distancia_persona_1 = mapa[persona].direccion[0][1] #esquina_persona_1  distancia
            distancia_persona_2 = mapa[persona].direccion[1][1] #esquina_persona_2  distancia

            lista_camino_minimo = [] # lista de tuplas

            for elemento in mapa[esquina_final_dijkstra_1].list:
                if elemento.key == ubicacion:
                    distancia_total_1 = elemento.distancia + distancia_camino_1 + distancia_persona_1
                    nodo_path_1 = NodoShortPath((esquina_persona_1, esquina_final_dijkstra_1), distancia_total_1)
                    distancia_total_3 = elemento.distancia + distancia_camino_3 + distancia_persona_2
                    nodo_path_3 = NodoShortPath((esquina_persona_2, esquina_final_dijkstra_1), distancia_total_3)

            for elemento in mapa[esquina_final_dijkstra_2].list:
                if elemento.key == ubicacion:
                    distancia_total_2 = elemento.distancia + distancia_camino_2 + distancia_persona_1
                    nodo_path_2 = NodoShortPath((esquina_persona_1, esquina_final_dijkstra_2), distancia_total_2)
                    distancia_total_4 = elemento.distancia + distancia_camino_4 + distancia_persona_2
                    nodo_path_4 = NodoShortPath((esquina_persona_2, esquina_final_dijkstra_2), distancia_total_4)

            lista_camino_minimo.append(nodo_path_1)
            lista_camino_minimo.append(nodo_path_2)
            lista_camino_minimo.append(nodo_path_3)
            lista_camino_minimo.append(nodo_path_4)

            lista_camino_minimo = sorted(lista_camino_minimo, key = lambda x: x.peso_camino)

            caminoMasCorto = lista_camino_minimo[0].esquinas
            # Funcion recursiva desde mapa[caminoMasCorto[0]].dijkstra hasta caminoMasCorto[1]
            lista_recorrido = self.recorrido(mapa[caminoMasCorto[0]].dijkstra, caminoMasCorto[1] , [])
            lista_recorrido = self.hacer_tupla(persona, lista_recorrido, ubicacion)
            return lista_recorrido

    def recorrido(self, mapa_dijkstra, esquina_destino, lista):

        aux = mapa_dijkstra[esquina_destino] # Guardamos la esquina en un nodo auxiliar

        if aux.padre != None:
            lista.insert(0, aux.key)
            self.recorrido(mapa_dijkstra, aux.padre, lista)
        else:
            lista.insert(0, aux.key)
            return lista
        return lista
    
    def hacer_tupla(self, persona, lista, lugar):
        nuevaLista = []
        for i in range(len(lista)):
            if i==0:
                nuevaLista.append((persona,lista[i]))
            if i == len(lista)-1:
                nuevaLista.append((lista[i], lugar))
                break
            nuevaLista.append((lista[i], lista[i+1]))
        return nuevaLista
                                

