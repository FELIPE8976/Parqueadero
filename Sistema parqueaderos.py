import copy  #Copiar estructuras complejas
import json  #Manejo de archivos .json

# Funciones para cargar las estructuras donde se guardarán los datos
def cargarUsuarios(archivo,listaUsuarios):

    """ Carga todos los usuarios que se encuentren dentro del archivo indicado """

    try:
        with open(archivo,encoding='utf-8-sig') as file: #Se abre el archivo
            data = json.load(file) # Se leen los datos
            for datosUsuarios in data['usuarios']:
                info = {}
                info[datosUsuarios[1]] = {'nombre':datosUsuarios[0],  # Se guardan los datos dentro del dict correspondiente
                                        'tipoUsuario':datosUsuarios[2],
                                        'placa':datosUsuarios[3],
                                        'tipoVehiculo':datosUsuarios[4],
                                        'planPago':datosUsuarios[5]}
                listaUsuarios.append(info) #Se añade el usuario a la lista de usuarios
        print("Archivo cargado exitosamente...")
    except:
        print("Hubo un error en la carga del archivo...")       

def cargarTiposParqueadero(archivo,dictEspacios):

    """ Carga el archivo .json que contiene el tipo de parqueadero utilizado """

    try:
        with open(archivo,encoding='utf-8-sig') as file: #Se abre el archivo
            data = json.load(file) # Se leen los datos
            for datos in data.keys():
                dictEspacios[datos] = data[datos] # Se guardan los datos dentro del dict correspondiente
        print("Archivo cargado exitosamente...")
        ###print(dictEspacios)
    except:
        print("Hubo un error en la carga del archivo...")


def crearUsuariosEnParqueadero():

    """ Genera un diccionario donde se guardarán los usuarios parqueados """

    usuariosParqueadero = {}
    return usuariosParqueadero


def generarEspaciosParqueo(matriz):

    """ Recorre cada uno de los espacios y le asigna un estado (X,O) """

    matrizEspaciosLibres = copy.deepcopy(matriz) #Copiamos la matriz original (con números)
    filas = len(matriz)
    columnas = len(matriz[0])
    for i in range(filas):
        for j in range(columnas):
            matrizEspaciosLibres[i][j] = "O" # Se le asigna el valor "disponible" a cada posición
    ###print(matrizEspaciosLibres)
    return matrizEspaciosLibres

def cargarEspaciosParqueo(archivo):

    """ Carga los espacios de parqueo (matriz) """ 

    espacios = {} # Diccionario de matrices con los lugares asignados
    espaciosLibres = {} # Diccionario de matrices con los lugares libres

    cargarTiposParqueadero(archivo,espacios)

    piso1Libre = generarEspaciosParqueo(espacios['Piso1'])
    piso2Libre = generarEspaciosParqueo(espacios['Piso2'])
    piso3Libre = generarEspaciosParqueo(espacios['Piso3'])
    piso4Libre = generarEspaciosParqueo(espacios['Piso4'])
    piso5Libre = generarEspaciosParqueo(espacios['Piso5'])
    piso6Libre = generarEspaciosParqueo(espacios['Piso6'])

    # Se guardan las matrices en el dict para lugares libres
    espaciosLibres['Piso1'] = piso1Libre
    espaciosLibres['Piso2'] = piso2Libre
    espaciosLibres['Piso3'] = piso3Libre
    espaciosLibres['Piso4'] = piso4Libre
    espaciosLibres['Piso5'] = piso5Libre
    espaciosLibres['Piso6'] = piso6Libre
    ###print(espacios)
    ###print(espaciosLibres)
    return espacios,espaciosLibres

def iniciarUsuarios():
    """ Creamos una lista vacía donde se guardarán los usuarios """
    usuarios = []
    return usuarios

########################################################

# Funciones para verificar datos
def verificarDuplicados(identificacion,listaUsuarios):

    """ Verifica la existencia de un usuario en el sistema """

    for usuario in listaUsuarios: #Recorremos la lista de usuarios
        if identificacion in usuario.keys(): # Verificamos si la ID está en la lista
            return -1
        else:
            return 0

def verificarRegistroPlaca(placa,listaUsuarios):

    """ Verifica si la placa ya se encuentra registrada dentro del sistema """

    encontro = False
    for usuario in listaUsuarios: # Recorremos la lista de usuarios
        if encontro: # Bandera
                break
        for key in usuario.keys(): #Recorremos los datos del usuario
            info = usuario[key]  
            if placa == info['placa']: # Verificamos coincidencia
                print("El vehículo se encuentra registrado")
                encontro = True
    if encontro:
        return 0
    else:
        return -1

def verificarPlacaParqueada(placa,usuariosEnParqueadero):

    """ Verifica si la placa ingresada corresponde a un vehículo parqueado """

    encontro = False
    resultado = None
    for placas in usuariosEnParqueadero.keys(): #Recorremos el diccionario con los usuarios parqueados
        if encontro: # Centinela
            break
        if placa == placas: # Verificamos coincidencia
            encontro = True
            resultado = usuariosEnParqueadero[placas]
    return resultado

def verificarParqueaderosDisponibles(tipoVehiculo,espaciosParqueadero,espaciosLibres):

    """ Verifica la disponibilidad de parqueaderos para el tipo de vehículo que desea ingresar """

    espaciosTotales = 0 # Verifica la cantidad de espacios disponibles
    totalEspaciosPisos = {} # Lleva la cuenta de espacios en cada uno de los pisos
    posicionesLibresPiso = {} # Contiene las posiciones libres (x,y) en cada uno de los pisos
    for piso in espaciosParqueadero.keys():
        espaciosPiso = espaciosParqueadero[piso]
        espaciosLibresPiso = espaciosLibres[piso]
        totalEspaciosPisos[piso] = 0
        posicionesLibresPiso[piso] = []
        filas = len(espaciosPiso)
        columnas = len(espaciosPiso[0])
        for i in range(filas):
            for j in range(columnas):
                if tipoVehiculo == "Automóvil" and espaciosPiso[i][j] == 1 and espaciosLibresPiso[i][j] == "O":
                    espaciosTotales += 1
                    totalEspaciosPisos[piso] += 1
                    posicionesLibresPiso[piso].append((i,j))
                if tipoVehiculo == "Automóvil eléctrico" and espaciosPiso[i][j] == 1 or espaciosPiso[i][j] == 2 and espaciosLibresPiso[i][j] == "O":
                    espaciosTotales += 1
                    totalEspaciosPisos[piso] += 1
                    posicionesLibresPiso[piso].append((i,j))
                if tipoVehiculo == "Motocicleta" and espaciosPiso[i][j] == 3 and espaciosLibresPiso[i][j] == "O":
                    espaciosTotales += 1
                    totalEspaciosPisos[piso] += 1
                    posicionesLibresPiso[piso].append((i,j))
                if tipoVehiculo == "Discapacitado" and espaciosPiso[i][j] == 1 or espaciosPiso[i][j] == 4 and espaciosLibresPiso[i][j] == "O":
                    espaciosTotales += 1
                    totalEspaciosPisos[piso] += 1
                    posicionesLibresPiso[piso].append((i,j))
    if espaciosTotales > 0:
        return True,totalEspaciosPisos,posicionesLibresPiso
    else:
        return False,totalEspaciosPisos,posicionesLibresPiso

#########################################################

# Funciones para obtener datos
def traerTipoVehiculoSegunPlaca(placa,listaUsuarios):

    """ Obtiene el tipo del vehículo a partir de su placa """

    encontro = False
    tipo = None
    for usuario in listaUsuarios: #Recorremos la lista de usuarios
        if encontro: #Centinela
            break
        for key in usuario.keys(): #Recorremos los datos del usuario
            info = usuario[key]
            if placa == info['placa']: #Verificamos si la placa coincide
                encontro = True
                tipo = info['tipoVehiculo']
    if encontro:
        return tipo
    else:
        return None

def traerTipoUsuarioSegunPlaca(placa,listaUsuarios):

    """ Obtiene el tipo de usuario según la placa ingresada """

    encontro = False
    tipo = None
    for usuario in listaUsuarios: #Recorremos la lista de usuarios
        if encontro: #Centinela
            break
        for key in usuario.keys(): #Recorremos los datos del usuario
            info = usuario[key]
            if placa == info['placa']: #Verificamos si la placa coincide
                encontro = True
                tipo = info['tipoUsuario']
    if encontro:
        return tipo
    else:
        return None

def traerPlanPagoSegunPlaca(placa,listaUsuarios):

    """ Obtiene el plan de pago del usuario a partir de la placa ingresada """

    encontro = False
    plan = None
    for usuario in listaUsuarios: #Recorremos la lista de usuarios
        if encontro: #Centinela
            break
        for key in usuario.keys(): #Recorremos los datos del usuario
            info = usuario[key]
            if placa == info['placa']: #Verificamos si la placa coincide
                encontro = True
                plan = info['planPago']
    if encontro:
        return plan
    else:
        return None





def registrarUsuario(nombreCompleto,identificacion,tipoUsuario,placa,tipoVehiculo,planPago,listaUsuarios):

    """ Registra un nuevo usuario dentro de la base de datos """

    result = verificarDuplicados(identificacion,listaUsuarios)
    if result == -1:
        print("El usuario que trata de registrar ya cuenta con un vehículo registrado anteriormente")
    else:
        usuario = {} # Registramos los datos del usuario
        usuario[identificacion] = {'nombre':nombreCompleto,
                                    'tipoUsuario':tipoUsuario,
                                    'placa':placa,
                                    'tipoVehiculo':tipoVehiculo,
                                    'planPago':planPago}
        listaUsuarios.append(usuario) #Se añade a la lista que contiene los demás usuarios





def asignarEspacio(piso,posicionesLibresPiso,espaciosLibres,placa,usuariosEnParqueadero,tipoUsuario,tipoVehiculo,planPago):

    """ Asigna un auto al espacio elegido por el usuario teniendo en cuenta las restricciones """

    preguntar = True
    while preguntar: #Mientras no sea una posición válida, preguntamos
        x = int(input("Ingrese la fila que desea (Se cuenta a partir de 1): ")) #Fila
        y = int(input("Ingrese la columna que desea (Se cuenta a partir de 1): ")) #Columna
        posicion = (x-1,y-1) #Restamos 1 porque en Python la cuenta empieza en 0
        if posicion in posicionesLibresPiso[piso]:
            preguntar = False
            espaciosPiso = espaciosLibres[piso]
            espaciosPiso[x-1][y-1] = "X"
            #Añadimos el usuario a un diccionario que contiene la info de los estacionados actualmente
            usuariosEnParqueadero[placa] = {'posicion':posicion,'piso':piso,'tipoUsuario':tipoUsuario,'tipoVehiculo':tipoVehiculo,'planPago':planPago}
            removerPosicionOcupada(posicion,piso,posicionesLibresPiso)
            print("Vehículo ingresado al parqueadero exitosamente...")
        else: #Posición no válida u ocupada
            print("Esta posición no admite su tipo de vehículo. Por favor ingrese otra...")

def removerPosicionOcupada(posicionASalir,piso,posicionesLibresPiso):

    """ Remueve la posición que ocupó el usuario """

    posiciones = posicionesLibresPiso[piso]
    posiciones.remove(posicionASalir) #Elimina la posición correspondiente en la lista que la contiene



# Funciones para retirar un vehículo del parqueadero
def retirarVehiculoDeParqueadero(posicion,piso,horas,tipoUsuario,planPago,espaciosLibres,usuariosEnParqueadero,placa):

    """ Retira al usuario del parqueadero """

    aniadirPosicionLibre(posicion,piso,espaciosLibres,usuariosEnParqueadero,placa)
    calcularCobro(horas,tipoUsuario,planPago)
    print("Vehículo retirado del parqueadero exitosamente...")
    

def calcularCobro(horas,tipoUsuario,planPago):

    """ Calcula el cobro a realizar según el tipo de usuario y plan de pago """

    if planPago == "Mensualidad": #Verificamos si el usuario tiene plan Mensual
        print("No debe realizar pago alguno. Buen día")
    else: # Verificamos el costo de la hora según el usuario
        if tipoUsuario == "Estudiante":
            costoHora = 1000
        elif tipoUsuario == "Profesor":
            costoHora = 2000
        elif tipoUsuario == "Personal Administrativo":
            costoHora = 1500
        elif tipoUsuario == "Visitante":
            costoHora = 3000

        total = horas * costoHora # Se calcula el costo total
        print("El costo a pagar por estar " + str(horas) + " horas es de $" + str(total))

def aniadirPosicionLibre(posicionAEntrar,piso,espaciosLibres,usuariosEnParqueadero,placa):

    """ Actualiza las estructuras informando que un usuario abandonó el parqueadero """

    x,y = posicionAEntrar #Posición donde se encuentra el auto
    espaciosPiso = espaciosLibres[piso]
    espaciosPiso[x][y] = "O" #Actualizamos la posición de "X" a "O"
    del usuariosEnParqueadero[placa] #Eliminamos al usuario del diccionario de usuarios





def cantidadDeVehiculosSegunTipoUsuario(usuariosEnParqueadero):

    """ Genera el reporte de la cantidad de vehículos categorizada
    según el tipo de usuario """

    resultados = {'Visitante':0, #Estructura para llevar el conteo de los tipos de usuario
                  'Estudiante':0,
                  'Profesor':0,
                  'Personal Administrativo':0}

    for placa in usuariosEnParqueadero.keys(): # Recorremos el diccionario con los usuarios dentro del parqueadero
        infoUsuario = usuariosEnParqueadero[placa]
        tipoUsuario = infoUsuario['tipoUsuario']
        if tipoUsuario in resultados.keys(): # Si encontramos coincidencia, aumenta el número
            resultados[tipoUsuario] += 1

    #Escritura en el archivo
    file = open("reporteVehiculosSegunTipoUsuario.txt",'w')
    file.write("Cantidad de vehículos según el tipo de usuario\n")
    file.write("----------------------------------------\n")
    for tipo in resultados.keys():
        mensaje = tipo + ": " + str(resultados[tipo]) + "\n"
        file.write(mensaje)
    file.write("----------------------------------------\n")
    file.close()

def cantidadVehiculosSegunTipoVehiculo(usuariosEnParqueadero):

    """ Genera el reporte de la cantidad de vehículos categorizada
    según el tipo de vehículo """

    resultados = {'Automóvil':0,    #Estructura para llevar el conteo de los autos
                  'Automóvil Eléctrico':0,
                  'Motocicleta':0,
                  'Discapacitado':0}

    for placa in usuariosEnParqueadero.keys(): # Recorremos el diccionario con los usuarios dentro del parqueadero
        infoUsuario = usuariosEnParqueadero[placa]
        tipoVehiculo = infoUsuario['tipoVehiculo']
        if tipoVehiculo in resultados.keys(): # Si encontramos coincidencia, aumenta el número
            resultados[tipoVehiculo] += 1

    #Escritura en el archivo
    file = open("reporteVehiculosSegunTipoVehiculo.txt",'w')
    file.write("Cantidad de vehículos según el tipo de vehículo\n")
    file.write("----------------------------------------\n")
    for tipo in resultados.keys():
        mensaje = tipo + ": " + str(resultados[tipo]) + "\n"
        file.write(mensaje)
    file.write("----------------------------------------\n")
    file.close()
        
def porcentajeOcupacion(usuariosEnParqueadero):

    """ Genera el reporte del porcentaje de ocupación """

    espaciosTotales = 550 #Espacios totales en el parqueadero
    espaciosHastaCinco = 100 #Espacios en cada uno de los pisos (1-5)
    espaciosPisoSeis = 50 #Espacios en el piso 6
    ocupacionPisos = {'Piso1':0,    #Estructura para llevar el conteo de la ocupación
                      'Piso2':0,
                      'Piso3':0,
                      'Piso4':0,
                      'Piso5':0,
                      'Piso6':0}

    porcentajeGlobal = round((len(usuariosEnParqueadero)/espaciosTotales)*100,2) # Porcentaje global de ocupación

    for placa in usuariosEnParqueadero.keys(): # Recorremos el diccionario con los usuarios dentro del parqueadero
        infoUsuario = usuariosEnParqueadero[placa]
        piso = infoUsuario['piso']
        if piso in ocupacionPisos.keys(): # Si encontramos coincidencia, aumenta el número
            ocupacionPisos[piso] += 1 

    #Porcentaje por cada piso
    porcentajeP1 = round((ocupacionPisos['Piso1']/espaciosHastaCinco)*100,2) 
    porcentajeP2 = round((ocupacionPisos['Piso2']/espaciosHastaCinco)*100,2)
    porcentajeP3 = round((ocupacionPisos['Piso3']/espaciosHastaCinco)*100,2)
    porcentajeP4 = round((ocupacionPisos['Piso4']/espaciosHastaCinco)*100,2)
    porcentajeP5 = round((ocupacionPisos['Piso5']/espaciosHastaCinco)*100,2)
    porcentajeP6 = round((ocupacionPisos['Piso6']/espaciosPisoSeis)*100,2)

    #Escritura en el archivo
    file = open("reportePorcentajeOcupacion.txt",'w')
    file.write("Porcentaje de ocupación global\n")
    file.write("----------------------------------------\n")
    file.write(str(porcentajeGlobal)+"%\n\n")
    file.write("----------------------------------------\n")
    file.write("Porcentaje de ocupación por cada piso\n")
    file.write("----------------------------------------\n")
    file.write("Piso 1: " + str(porcentajeP1)+"\n")
    file.write("Piso 2: " + str(porcentajeP2)+"\n")
    file.write("Piso 3: " + str(porcentajeP3)+"\n")
    file.write("Piso 4: " + str(porcentajeP4)+"\n")
    file.write("Piso 5: " + str(porcentajeP5)+"\n")
    file.write("Piso 6: " + str(porcentajeP6)+"\n")
    file.write("----------------------------------------\n")


def crearReportes(usuariosEnParqueadero):

    """ Llama a las funciones encargadas de crear los reportes """
    
    cantidadDeVehiculosSegunTipoUsuario(usuariosEnParqueadero)
    cantidadVehiculosSegunTipoVehiculo(usuariosEnParqueadero)
    porcentajeOcupacion(usuariosEnParqueadero)

# Funciones varias

def imprimirMatrizLibres(piso,dictEspaciosLibres):

    """ Imprime las plazas del piso seleccionado por el usuario """

    print("Estas son las plazas para el piso seleccionado\nO (Libre) --- X (Ocupado)")
    for espacios in dictEspaciosLibres[piso]: #Imprimimos cada lista para un mejor efecto visual
        print(espacios)

espaciosParqueadero, espaciosLibres = None, None            ########################################
usuarios = iniciarUsuarios()                                #Variables donde se guardarán los datos#
usuariosEnParqueadero = crearUsuariosEnParqueadero()     ########################################

def cargarInfoParquedero(archivo):

    """ Carga los espacios de parqueo (matriz) """ 

    matrizEspacios, matrizLibres = cargarEspaciosParqueo(archivo)
    return matrizEspacios, matrizLibres

def imprimirMenu():

    ### Imprime el menú de la consola para interactuar con el usuario 

    print("Bienvenido al Sistema de Parqueadero de la Universidad Javeriana\n ¿Qué desea hacer?")
    print("1- Cargar archivo de tipos de parqueadero.")
    print("2- Cargar archivo de usuarios.")
    print("3- Realizar registro de usuario.")
    print("4- Ingresar vehículo al parqueadero.")
    print("5- Retirar vehículo")
    print("6- Generar reportes")
    print("7- Salir")

def iniciarAplicacion():

    """ Inicia la aplicación """

    continuar = True
    while continuar:
        imprimirMenu()
        inputUser = int(input("Ingrese la opción: "))
        if inputUser == 7:
            continuar = False
        
        elif inputUser == 1:
            archivo = input("Por favor ingrese el nombre del archivo a cargar indicando la extensión: ") ### Se solicita el nombre del archivo
            espaciosParqueadero,espaciosLibres=cargarInfoParquedero(archivo) 
        elif inputUser == 2:
            archivo = input("Por favor ingrese el nombre del archivo a cargar indicando la extensión: ") ### Se solicita el nombre del archivo
            cargarUsuarios(archivo,usuarios)

        elif inputUser == 3:
            preguntarTipoUsuario = True ### Bandera
            preguntarTipoVehiculo = True ### Bandera
            preguntarPlanPago = True ### Bandera
            nombre = input("Ingrese su nombre: ") ### Solicita el nombre del usuario
            identificacion = int(input("Ingrese su identificación: ")) ### Solicita el numero de identificacion del usuario
            while preguntarTipoUsuario:
                inputTipoUsuario = int(input("Soy\n 1. Estudiante\n 2. Profesor\n 3. Personal Administrativo\n")) ### Pide un numero dependiendo de la opcion que desee el usuario
                if inputTipoUsuario == 1:
                    tipoUsuario = "Estudiante" ### Se asigna valor a la variable 
                    preguntarTipoUsuario = False ### Bandera en false para detener el ciclo
                elif inputTipoUsuario == 2:
                    tipoUsuario = "Profesor" ### Se asigna valor a la variable 
                    preguntarTipoUsuario = False ### Bandera en false para detener el ciclo
                elif inputTipoUsuario == 3:
                    tipoUsuario = "Personal Administrativo" ### Se asigna valor a la variable 
                    preguntarTipoUsuario = False ### Bandera en false para detener el ciclo
                else:
                    print("Por favor ingrese una opción válida...") ### mensaje en caso de que el usuario digite algo incorrecto.
            placa = input("Ingrese la placa del vehículo: ") ### Se solicita placa del vehiculo
            while preguntarTipoVehiculo:
                inputTipoVehiculo = int(input("Mi vehículo es\n 1. Automóvil\n 2. Automóvil eléctrico\n 3. Motocicleta\n 4. Para discapacitados\n")) ### Pide un numero dependiendo de la opcion que desee el usuario
                if inputTipoVehiculo == 1:
                    tipoVehiculo = "Automóvil" ### Se asigna valor a la variable 
                    preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                elif inputTipoVehiculo == 2:
                    tipoVehiculo = "Automóvil eléctrico" ### Se asigna valor a la variable 
                    preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                elif inputTipoVehiculo == 3:
                    tipoVehiculo = "Motocicleta" ### Se asigna valor a la variable 
                    preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                elif inputTipoVehiculo == 4:
                    tipoVehiculo = "Discapacitado" ### Se asigna valor a la variable 
                    preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                else:
                    print("Por favor ingrese una opción válida...") ### mensaje en caso de que el usuario digite algo incorrecto.
            while preguntarPlanPago:
                inputPlan = int(input("Mi plan de pago es\n 1. Mensual\n 2. Diario\n")) ### Pide un numero dependiendo de la opcion que desee el usuario
                if inputPlan == 1:
                    planPago = "Mensual" ### Se asigna valor a la variable
                    preguntarPlanPago = False ### Bandera en false para detener el ciclo
                elif inputPlan == 2:
                    planPago = "Diario" ### Se asigna valor a la variable
                    preguntarPlanPago = False ### Bandera en false para detener el ciclo
                else:
                    print("Por favor ingrese una opción válida...") ### mensaje en caso de que el usuario digite algo incorrecto.  
            registrarUsuario(nombre,identificacion,tipoUsuario,placa,tipoVehiculo,planPago,usuarios) ### se utiliza la funcion con los datos proporcionados

        elif inputUser == 4:
            
            preguntarTipoVehiculo = True ### Bandera
            placa = input("Ingrese la placa del vehículo: ") ### Solicita la placa del vehiculo
            verificacion = verificarRegistroPlaca(placa,usuarios) ### se utiliza la funcion para verificar si la placa se encuentra registrada
            if verificacion == 0:
                tipo = traerTipoVehiculoSegunPlaca(placa,usuarios) ### se le asigna el tipo de vehiculo en caso de que la placa este registrada
                if tipo != None:
                    hayDisponibles, cantidad, posiciones = verificarParqueaderosDisponibles(tipo,espaciosParqueadero,espaciosLibres) ### se utiliza la funcion para verificar si hay diponibilidad, la cantidad y las coordenadas de los parqueaderos vacios
                    if hayDisponibles:
                        print("Estos son los espacios disponibles para " + tipo +" en cada piso:") ### imprime una frase
                        for piso in cantidad.keys():
                            print(piso,":",cantidad[piso]) ### imprimi cada piso y la cantidad de disponibles
                        preguntaPiso = input("¿Qué piso desea escoger? (1,2,3,4,5,6)\n") ### se le solicita al usuario el piso deseado
                        pisoEscogido = "Piso"+preguntaPiso ### se unen la palabra piso y el numero brindado por el usuario esto para usarse como una llave
                        tipoUsuarioHallado = traerTipoUsuarioSegunPlaca(placa,usuarios) ### utiliza la funcion para retornar el tipo de usuario
                        planPagoUsuario = traerPlanPagoSegunPlaca(placa,usuarios) ### utiliza la funcion para retornar el plan de pago del usuario 
                        imprimirMatrizLibres(pisoEscogido,espaciosLibres) ### imprime la matriz que muestra los espacios libres
                        asignarEspacio(pisoEscogido,posiciones,espaciosLibres,placa,usuariosEnParqueadero,tipoUsuarioHallado,tipo,planPagoUsuario) ### funcion para que el usuario seleccione donde desea estacionar
                    else:
                        print("No hay plazas de parqueo libres para este tipo de vehículo...") ### Esto ocurre cuando para un tipo de vehiculo ya no hay espacios para estacionar
            else:
                while preguntarTipoVehiculo:
                    inputTipoVehiculo = int(input("Mi vehículo es\n 1. Automóvil\n 2. Automóvil eléctrico\n 3. Motocicleta\n 4. Para discapacitados\n")) ### Solicita el tipo de vehiculo
                    if inputTipoVehiculo == 1:
                        tipoVehiculo = "Automóvil" ### Se asigna valor a la variable
                        preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                    elif inputTipoVehiculo == 2:
                        tipoVehiculo = "Automóvil eléctrico" ### Se asigna valor a la variable
                        preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                    elif inputTipoVehiculo == 3:
                        tipoVehiculo = "Motocicleta" ### Se asigna valor a la variable
                        preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                    elif inputTipoVehiculo == 4:
                        tipoVehiculo = "Discapacitado" ### Se asigna valor a la variable
                        preguntarTipoVehiculo = False ### Bandera en false para detener el ciclo
                    else:
                        print("Por favor ingrese una opción válida...")  ### mensaje en caso de que el usuario digite algo incorrecto.
                registrarUsuario("","","Visitante",placa,tipoVehiculo,"Diario",usuarios) ### utiliza la funcion de registrar usuario
                hayDisponibles, cantidad, posiciones = verificarParqueaderosDisponibles(tipoVehiculo,espaciosParqueadero,espaciosLibres) ### se utiliza la funcion para verificar si hay diponibilidad, la cantidad y las coordenadas de los parqueaderos vacios
                if hayDisponibles:
                    print("Estos son los espacios disponibles para " + tipoVehiculo +" en cada piso:") ### imprime una frase
                    for piso in cantidad.keys():
                        print(piso,":",cantidad[piso]) ### imprimi cada piso y la cantidad de disponibles
                    preguntaPiso = input("¿Qué piso desea escoger? (1,2,3,4,5,6)\n") ### se le solicita al usuario el piso deseado
                    pisoEscogido = "Piso"+preguntaPiso ### se unen la palabra piso y el numero brindado por el usuario esto para usarse como una llave
                    imprimirMatrizLibres(pisoEscogido,espaciosLibres) ### imprime la matriz que muestra los espacios libres
                    asignarEspacio(pisoEscogido,posiciones,espaciosLibres,placa,usuariosEnParqueadero,"Visitante",tipoVehiculo,'Diario') ### funcion para que el usuario seleccione donde desea estacionar
                else:
                    print("No hay plazas de parqueo libres para este tipo de vehículo...") ### Esto ocurre cuando para un tipo de vehiculo ya no hay espacios para estacionar

        elif inputUser == 5:
            placaIngresada = input("Ingrese la placa del vehículo que desea retirar: ") ### se le pide al usuario la placa del vehiculo estacionado
            numHorasParqueado = int(input("Ingrese el número de horas que estuvo parqueado el vehículo: ")) ### se le pide al usuario la cantidad de horas que estuvo estacionado
            resultadoBusqueda = verificarPlacaParqueada(placaIngresada,usuariosEnParqueadero) ### se utiliza la funcion para verificar que el vehiculo se encuentre el el parqueadero
            if resultadoBusqueda != None:
                posicionOcupada = resultadoBusqueda['posicion'] ### Se asigna valor a la variable
                pisoOcupado = resultadoBusqueda['piso'] ### Se asigna valor a la variable
                tipoUsuarioPlaca = resultadoBusqueda['tipoUsuario'] ### Se asigna valor a la variable
                planPagoPlaca = resultadoBusqueda['planPago'] ### Se asigna valor a la variable
                retirarVehiculoDeParqueadero(posicionOcupada,pisoOcupado,numHorasParqueado,tipoUsuarioPlaca,planPagoPlaca,espaciosLibres,usuariosEnParqueadero,placaIngresada) ### se usa la funcion para eliminar del registro al usuario estacionado
            else:
                print("La placa que ingresó no se encuentra en el parqueadero...") ### se imprime el mensaje en caso de que la placa no se encuentre el el parqueadero o sea incorrecta
        
        elif inputUser == 6:
            crearReportes(usuariosEnParqueadero) ### utiliza la funcion para generar los reportes
        elif inputUser == 8:
            print(usuarios) ### funcion ajena al usuario que permite ver la lista de usuarios registrados

iniciarAplicacion()

