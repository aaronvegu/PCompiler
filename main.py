'''
Compiler for custom language
Version 2.0
Created by Aaron Vegu 24/mar/23
'''

# Constantes para estado aceptor y estado error
ERR = -1
ACP = 99

# Indice de la matriz
idx = 0

# bandera de errores
codeErr = False

# bandera de principal, para indicar si tiene funcion principal o main
mainFlag = False

# bandera de constante
constantFlag = False

# Tokens y lexemas
token = ''
lexema = ''

# Variables de linea y renglon para indicar posicion de errores
line = 1
col = 0

# Tipos del lenguaje
types = ['nulo', 'entero', 'decimal', 'palabra', 'logico']

# Tokens de Constantes del lenguaje
constTokens = ['Ent', 'Dec', 'CtA', 'CtL']

# Operadores logicos
logicOp = ['no', 'y', 'o']

# Constantes binarias
logicConst = ['verdadero', 'falso']

# Palabras reservadas del lenguaje FALTAN POR COMPLETAR
keywords = ['desde', 'si', 'hasta', 'entero', 'decimal', 'palabra', 'logico', 'nulo', 'sino', 'constante', 
            'mientras', 'regresa', 'hacer', 'incr', 'imprime', 'imprimenl', 'lee', 'repite', 'que']

# Operadores aritmeticos
AritOp = ['+', '-', '*', '/', '%', '^']

# Delimitadores
delimiters = [';', ',', '(', ')', '{', '}', '[', ']', ':']

# Operadores relacionales
relationals = ['<', '>', '<=', '>=', '<>']

# Delimitadores universales
univDelimit = [' ', '\t', '\n']

# la entrada por el momento sera una cadena vacia
inp = ''

## ##
# INICIO Analizadores Semanticos
## ##

linCod = 1

# Conversiones de Tipos permitidas (Semantica)
convTypes = [
    "E=E", "A=A", "R=R", "L=L", "R=E",
    "E+E", "E+R", "R+E", "R+R", "A+A",
    "E-E", "E-R", "R-E", "R-R",
    "E*E", "E*R", "R*E", "R*R",
    "E/E", "E/R", "R/E", "R/R",
    "E\37E", "-E", "-R",
    "LyL", "LoL", "noL",
    "E>E", "R>E", "E>R", "R>R",
    "E<E", "R<E", "E<R", "R<R",
    "E>=E", "R>=E", "E>=R", "R>=R",
    "E<=E", "R<=E", "E<=R", "R<=R",
    "E<>E", "R<>E", "E<>R", "R<>R", "A<>A",
    "E==E", "R==E", "E==R", "R==R", "A==A"
]

# Resultados de las conversiones
typesR = [
    "",  "",  "",  "",  "",
    "E", "R", "R", "R", "A",
    "E", "R", "R", "R",
    "E", "R", "R", "R",
    "R", "R", "R", "R",
    "E", "E", "R",
    "L", "L", "L",
    "L", "L", "L", "L",
    "L", "L", "L", "L",
    "L", "L", "L", "L",
    "L", "L", "L", "L",
    "L", "L", "L", "L", "L",
    "L", "L", "L", "L", "L"
]

def searchType(c):
    for i in range(55):
        if convTypes[i] == c: return i
    return -1

class objPrgm():
    def __init__(self, nom, cls, tip, dim1, dim2, apv) -> None:
        self.nombre = nom
        self.clase = cls
        self.tipo = tip
        self.dim1 = dim1
        self.dim2 = dim2
        self.apv = apv

class TabSimb():
    arreglo = []
    def inserSimbolo(self, nom, cls, tip, dim1, dim2, apv):
        obj = objPrgm(nom, cls, tip, dim1, dim2, apv)
        self.arreglo.append( obj )

    def buscaSimbolo(self, ide):
        for x in self.arreglo:
            if x.nom == ide: return x
        return None
    
    def grabaTabla(self, archSal):
        with open(archSal, 'r') as aSal:
            if aSal == None: return 

        with open(archSal, 'w') as aSal:
            for x in tabSimb:
                aSal.write(x.nom +',' + x.clas + ',' + x.tip + ',' + \
                           x.dim1 + ','+ x.dim2 + ',#')
            aSal.close()
        return

class codigo():
    def __init__(self, mnem, dir1, dir2):
        self.mnemo = mnem
        self.dir1 = dir1
        self.dir2 = dir2
    
class Programa():
    cod = []
    def insCodigo(self, mnemo, dir1, dir2):
        global linCod
        x = codigo(mnemo, dir1, dir2)
        self.cod[linCod] = x
        linCod = linCod + 1

tabSimb = TabSimb()  

prgmCode = Programa()

pilaTipos = []

## ##
# INICIO Analizadores Semanticos
## ##


# Funcion de error
def throwErr(errType, descript):
    global line, col
    global codeErr
    print('[' + str(line) + ']' + '[' + str(col) + ']', errType, descript)
    codeErr = True

# Matriz de estado
matran = [
        #let  dig  de   OpA   <     >   =    .    "
        [1,    2,   6,   5,   10,   8,  7,  ERR,   12], # 0
        [1,    1,  ACP, ACP, ACP, ACP, ACP, ACP,  ACP], # 1
        [ACP,  2,  ACP, ACP, ACP, ACP, ACP,   3,  ACP], # 2
        [ERR,  4,  ERR, ERR, ERR, ERR, ERR, ERR,  ACP], # 3
        [ACP,  4,  ACP, ACP, ACP, ACP, ACP, ACP,  ACP], # 4
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  ACP], # 5
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  ACP], # 6
        [ACP, ACP, ACP, ACP, ACP, ACP,   9, ACP,  ACP], # 7
        [ACP, ACP, ACP, ACP, ACP, ACP,   9, ACP,  ACP], # 8
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  ACP], # 9
        [ACP, ACP, ACP, ACP, ACP,  11,   9, ACP,  ACP], # 10
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  ACP], # 11
        [ 12,  12,  12,  12,  12,  12,  12,  12,   13], # 12
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,  ACP]  # 13
    ]
    
# Funcion para aceptar y procesar cada columna de nuestra matriz (caracteres)
def colChar(x):
    # Si el caracter recibido es una letra o underscore
    if x == '_' or x.isalpha(): return 0
    # Si el caracter es un digito
    if x.isdigit(): return 1
    # si el caracter es un delimitador
    if x in delimiters: return 2
    # si el caracter es un operador aritmetico
    if x in AritOp: return 3
    # si el caracter es un <
    if x == '<': return 4
    # si el caracter es un >
    if x == '>': return 5
    # si el caracter es un =
    if x == '=': return 6
    # si el caracter es un .
    if x == '.': return 7
    # si el caracter es un "
    if x == '"': return 8
    # si hay un delimitador universal, solo no procesamos sin error
    if x in univDelimit: return 15
    # si el caracter no es ninguno de los aceptados, regresa error
    throwErr('Error Lexico ', x + ' Simbolo no valido en Alfabeto')
    return ERR
    
# Funcion que regresa el token y el lexema // Analizador Lexico - Scanner
def scanner():
    global inp, ACP, ERR, idx, line, col
    
    state = 0
    lexema = ''
    c = ''
    column = 0

    while idx < len(inp) and state != ERR and state != ACP:
        c = inp[idx]
        idx = idx + 1

        # Si hay salto de linea, reiniciamos conteo de col y lin para errores
        if c == '\n':
            col = 0
            line = line + 1

        column = colChar(c)

        if state == 0 and column == 15:
            continue
        
        if column >= 0 and column <= 8 or column == 15:
            if column == 15 and state != 12:
                state = ACP
            if column >= 0 and column <= 8:
                state = matran[state][column]
            if state != ERR and state != ACP and column != 15 or column == 15 and state == 12:
                prevState = state
                lexema = lexema + c
            if c != '\n': col = col + 1
                
    if state != ACP and state != ERR: prevState = state

    # Variable de nuestro token a regresar
    token = 'Ntk'

    # Regresamos un estado para ir al simbolo que no fue concatenado - unget
    if state == ACP and column != 15:
        idx = idx - 1
        col = col - 1
    
    if state != ERR and state != ACP:
        prevState = state
    
    ### REVISAR ASIGNACIONS DE TOKENS
    # Si el lexema es una palabra reservada
    if lexema in keywords: token = 'Res'
    # Si el lexema es un operador logico
    elif lexema in logicOp: token = 'OpL'
    # Si el lexema es una constante logica
    elif lexema in logicConst: token = 'CtL'
    # Sino, se trata de un identificador
    else: token = 'Ide'

    # Estados aceptores del automata
    if prevState == 2: token = 'Ent'
    elif prevState == 4: token = 'Dec'
    elif prevState == 5: token = 'OpA'
    elif prevState == 6: token = 'Del'
    elif prevState == 7: token = 'OpS'
    elif prevState in [8, 9, 10, 11]: token = 'OpR'
    elif prevState == 13: token = 'CtA'
    
    # Si el token sigue indefinido
    if token == 'Ntk': print('Estado Anterior =', prevState, '| Estado=', state)
    
    return token, lexema

### Analizadores sintacticos de los comandos del lenguaje, en espaniol para evitar usar keywords de Python
def leer():
    global token, lexema
    # verificamos recibir keywork lee
    if lexema != 'lee': throwErr('Error de sintaxis', 'Se esperaba palabra reservada lee y llego ' + lexema)
    # avanzamos
    token, lexema = scanner()
    # Verificamos que se haya abierto parentesis
    if lexema != '(': throwErr('Error de sintaxis', 'Se esperaba ( y llego' + lexema)
    # avanzamos
    token, lexema = scanner()
    # verificamos recibir un identificador
    if token != 'Ide': throwErr('Error de Sintaxis', 'Se esperaba cadena a imprimir y llego ' + lexema)
    # avanzamos
    token, lexema = scanner()
    # dimension (opcional)
    if lexema == '[':
            token, lexema = scanner()
            expr()
            if lexema != ']':
                throwErr('Error de Sintaxis', 'Se esperaba cerrar ] y llego ' + lexema)
    # verificamos cierre de parentesis
    if lexema != ')': throwErr('Error de sintaxis', 'Se esperaba cierre de parentesis y llego ' + lexema)

def imprime():
    global token, lexema
    # Verificamos que se haya abierto parentesis
    if lexema != '(': throwErr('Error de sintaxis', 'Se esperaba ( y llego' + lexema)
    # avanzamos
    token, lexema = scanner()
    if lexema != '(': expressionGroup()
    if lexema != '(': token, lexema = scanner()
    # Verificamos que se haya abierto parentesis
    if lexema != ')': throwErr('Error de sintaxis', 'Se esperaba ) y llego' + lexema)
    # insertamos codigo en la maquina virtual
    prgmCode.insCodigo('OPR', '0', '20')

def imprimenl():
    global token, lexema, prgmCode
    token, lexema = scanner()
    # Verificamos que se haya abierto parentesis
    if lexema != '(': throwErr('Error de sintaxis', 'Se esperaba ( y llego ' + lexema)
    # avanzamos
    token, lexema = scanner()
    if lexema != ')': expressionGroup()
    if lexema != ')': token, lexema = scanner()
    # Verificamos que se haya abierto parentesis
    if lexema != ')': throwErr('Error de sintaxis', 'Se esperaba ) y llego ' + lexema)
    # insertamos codigo en la maquina virtual
    prgmCode.insCodigo('OPR', '0', '21')

def desde(): pass
def mientras(): pass
def si(): pass
def repite(): pass
def lmp(): pass # lmp = limpia pantalla
def regresa(): pass

## INICIA REGLAS DEL EVALUADOR DE EXPRESIONES

## Tecnica de implementacion: Descenso Recursivo Iterativo

##  Tabla de prioridades
##  +  ^^
##     || ()
##     || - (unitario)
##     || ^
##     || *, /, %
##     || +, -
##     || <, >, <=, >=, <>
##     || no
##     || y
##  -  || o

# Termino evalua parentesis
def termino():
    global token, lexema
    # Se espera () o un identificador
    if lexema != '(' and token not in constTokens and token != 'Ide':
        token, lexema = scanner()
    if lexema == '(':
        token, lexema = scanner()
        expr()
        if lexema != ')':
            throwErr('Error de Sintaxis', 'Se esperaba ) y llego ' + lexema)
    elif token == 'Ide': # Si llega un identificador

        nomIde = lexema

        token, lexema = scanner()
        if lexema == '[':
            token, lexema = scanner()
            expr()
            if lexema != ']':
                throwErr('Error de Sintaxis', 'Se esperaba cerrar ] y llego ' + lexema)
        elif lexema == '(': pass

        oIde = tabSimb.buscaSimbolo(nomIde)
        if oIde != None:
            pilaTipos.append(oIde.tip)
        else:
            throwErr('Error de Semantica', 'Identificador no declarado ' + nomIde)
            pilaTipos('I')
    elif token in constTokens:
        const()
    if lexema != ')':
        token, lexema = scanner()

# Regla de Negacion unitaria: manda a llamar a la ultima regla de termino
def signo():
    global token, lexema
    if lexema == '-': # Si se esta negando (opcional)
        token, lexema = scanner()
    termino()

# Regla de Operador de potencia: manda a llamar a regla de signo
def exPo():
    global token, lexema
    opr = '^' # obligamos que entre al while
    while opr == '^':
        signo() # Multiplicativo manda a llamar a signo o negacion unitaria
        opr = lexema

# Regla de Operadores multiplicativos: manda a llamar exponencial
def multi():
    global token, lexema
    opr = '*' # obligamos que entre al while
    while opr == '*' or opr == '/' or opr == '%':
        exPo() # Multiplicativo manda a llamar a potencia o exponencial
        opr = lexema

# Regla deOperadores de suma y resta: manda a llamar a Multiplicativos
def suma():
    global token, lexema
    opr = '+' # obligamos que entre al while
    while opr == '+' or opr == '-':
        multi() # Suma manda a llamar a operadores multiplicativos
        opr = lexema

# Regla del Operador RELACIONAL: manda a llamar a operadores de SUMA
def oprel():
    global token, lexema
    opr = '<' # obligamos que entre al while
    while opr in relationals:
        suma()
        opr = lexema

# Regla del Operador NO: manda a llamar a operador RELACIONAL
def opno():
    global token, lexema
    if lexema == 'no':
        token, lexema = scanner()
    oprel()

# Regla del Operador Y: manda a llamar al Operador NO
def opy():
    global token, lexema
    opr = 'y'
    while opr == 'y':
        opno()
        opr = lexema

# Se inicia el analisis de la expresion y manda a llamar al Operador O
def expr():
    global token, lexema
    opr = 'o'
    while opr == 'o':
        opy()
        opr = lexema

## TERMINA REGLAS DEL EVALUADOR DE EXPRESIONES

def const():
    global token, lexema, prgmCode
    # Si no es una constante definida
    if not(token in constTokens):
        throwErr('Error de Sintaxis', 'Se esperaba Cte y llego ' + lexema)
    else: # Si recibimos un token definido en nuestras constantes
        # clasificamos el tipo de constante
        # Si es constante, entero o decimal, insertamos con LIT, valor, 0
        if token == 'CtA' or token == 'Ent' or token == 'Dec':
            prgmCode.insCodigo('LIT', lexema, '0')
        # Si es una constante logico
        if token == 'CtL':
            # Si es verdadero: LIT, V, 0
            if lexema == 'verdadero': prgmCode.insCodigo('LIT', 'V', 0)
            # si es falso: LIT, F, 0
            elif lexema == 'falso': prgmCode.insCodigo('LIT', 'F', 0)

## POR IMPLEMENTAR
# Analizador sintactico de constantes y variables
def constVars():
    global inp, idx, token, lexema
    # avanzamos
    token, lexema = scanner()
    # # Analizamos si se nos da dimension o no
    # if lexema == '[': dims()

# Analizador sintactico de dimension de la variable
def dims():
    global inp, idx, token, lexema
    # avanzamos, ya recibimos [ como lexema de entrada a Dims
    token, lexema = scanner()
    # verificamos que llegue un Entero para definir la dimension
    if token != 'Ent':
        throwErr('Error de Sintaxis', 'Se espera numero entero para definir dimension, se recibio: ' + lexema)
    # avanzamos
    token, lexema = scanner()
    # verificamos recibir la cerradura de la dimension con ]
    if lexema != ']':
        throwErr('Error de Sintaxis', 'Se esperaba ] y llego ' + lexema)
    # avanzamos
    token, lexema = scanner()

## POR IMPLEMENTAR
# Analizador sintactico de parametros de funcion
def params():
    global inp, token, lexema
    # Leemos token y lexema a evaluar
    token, lexema = scanner()

# Analizador de expresiones que queremos llamar con una funcion como imprime o imprimenl
def expressionGroup():
    global token, lexema, prgmCode
    if lexema != ')':
        delim = ','
        while delim == ',':
            if lexema == ',':
                token, lexema = scanner()
                prgmCode.insCodigo('OPR', '0', '20')
            expr()
            delim = lexema
            #if delim == ',':
                #genCod(linea, 'OPR 0, 20')

def asigLfunc(): pass

# Comando
def statement():
    global token, lexema
    # Dependiendo la palabra que recibamos, pasamos al sintactico de ese comando
    if token == 'Ide': asigLfunc()
    if lexema == 'lee': leer()
    elif lexema == 'imprime': imprime()
    elif lexema == 'imprimenl': imprimenl()
    elif lexema == 'desde': desde()
    elif lexema == 'mientras': mientras()
    elif lexema == 'si': si()
    elif lexema == 'repite': repite()
    elif lexema == 'lmp': lmp()
    elif lexema == 'regresa': regresa()
    # Si no es ningun comando, enviar error
    else: throwErr('Error de Sintaxis', lexema + ' NO es un comando definido en el lenguaje')
    token, lexema = scanner()

# Analizador sintactico del grupo de comandos
def blockStatement():
    global token, lexema
    token, lexema = scanner()
    if lexema != ';' and lexema != '{': 
        statement()
        token, lexema = scanner()
        if lexema != ';': throwErr('Error de Sintaxis', 'se esperaba ; y llego ' + lexema)
    elif lexema == '{':
        instructions()
        if lexema != '}': throwErr('Error de Sintaxis', 'se esperaba cerrar block \"}\" y llego ' + lexema)

# Analizador sintactico del grupo de instrucciones de la funcion
def instructions():
    global token, lexema
    cbk = '{'
    while cbk != '}':
        # Si no tenemos punto y coma, leemos comando
        if lexema != ';': statement()
        # Si no hay ;, aventamos error
        if lexema != ';': throwErr('Error de Sintaxis', 'Se esperaba ; y llego ' + lexema)
        # Siempre debe haber un ; despues de un comando, y avanzamos
        token, lexema = scanner()
        # de no haber error, avanzamos
        cbk = lexema

# Analizador sintactico del bloque de instrucciones de funcion
def functBlock():
    global token, lexema
    # Bloque de instrucciones debe iniciar con llave
    if lexema != '{': throwErr('Error de Sintaxis', 'Se esperaba llave de apertura \"{\"')
    # avanzamos
    token, lexema = scanner()
    # esperamos instrucciones de la funcion, y leemos de no encontrar llave de cerradura
    if lexema != '}': instructions()
    # debemos recibir cerradura de la funcion
    if lexema != '}': throwErr('Error de Sintaxis', 'Se esperaba llave de cerradura \"}\"')

### DEPRECATED ??
# Encabezado de function y variable, analiza si se trata de la def de una var/const o una funcion
def VarFuncHeader():
    global inp, idx, token, lexema, constantFlag, mainFlag

    # Leemos para saber si viene Constante o tipo de datos para variable
    token, lexema = scanner()

    if lexema == 'constante': # Registramos si llega una constante
        constantFlag = True
        token, lexema = scanner()
    # Si lexema no esta en los tipos del lenguaje, lanzar error
    if not lexema in types:
        throwErr('Error sintactico', 'Se esperaba tipo ' + str(types))
    # Avanzamos en scanner (leemos)
    token, lexema = scanner()
    # Si el siguiente token no es un Identificador
    if token != 'Ide':
        throwErr('Error de Sintaxis', 'Se esperaba Nombre Funcion y llego ' + lexema)
    # Si llega una funcion Main o Principal, solo puede haber una main definida
    if mainFlag: throwErr('Error de Semantica', 'La funcion Principal ya esta definida')
    # Aqui captamos la funcion principal
    if lexema == 'principal': mainFlag = True
    # avanzamos
    token, lexema = scanner()
    # Si llega parentesis de apertura, procesamos funcion
    if lexema == "(": functions() 
    else: constVars() # Sino, es constante o variable


# Analizador sintactico de las funciones
def functions():
    global inp, idx, token, lexema, types, mainFlag

    #print('Programa entra a Functions')    

    # Si lexema no esta en los tipos del lenguaje, lanzar error
    if not(lexema in types):
        throwErr('Error sintactico', 'Se esperaba tipo ' + str(types))
    # Avanzamos en scanner (leemos)
    token, lexema = scanner()
    # Si el siguiente token no es un Identificador
    if token != 'Ide': throwErr('Error de Sintaxis', 'Se esperaba Nombre Funcion y llego ' + lexema)
    # Si llega una funcion Main o Principal, solo puede haber una main definida
    if mainFlag: throwErr('Error de Semantica', 'La funcion Principal ya esta definida')
    # Aqui captamos la funcion principal
    if lexema == 'principal': mainFlag = True
    # avanzamos
    token, lexema = scanner()
    # evaluamos apertura de parentesis
    if lexema != '(': throwErr('Error de Sintaxis', 'Se esperaba \"(\" y llego ' + lexema)
    # avanzamos
    token, lexema = scanner()
    # leemos parametros
    if lexema != ')': params()
    # evaluamos cerradura de parentesis
    if lexema != ')': throwErr('Error de Sintaxis', 'Se esperaba \")\" y llego ' + lexema)
    # avanzamos
    token, lexema = scanner()
    # esperamos el bloque de instrucciones de la funcion
    functBlock()

# Analizador sintantico de la estructura principal del programa
def prgm():
    while len(inp) > 0 and idx < len(inp):
        constVars()
        functions() # Para saber si es una constante/variable o funcion

# Analizador sintactico principal (Parser)
def parser():
    global inp, idx, token, lexema
    prgm()

# main
if __name__ == '__main__':
    # Pedimos archivo de entrada a procesar
    arche = input('Archivo (.icc) [.]=salir: ')
    if arche == '.': exit()
    # Carga archivo de entrada
    archivo = open(arche, 'r')

    inp = ''

    # Lectura del archivo linea por linea
    for linea in archivo:
        inp += linea

    # Imprimos entrada de archivo
    print(inp)
    # Llamamos a nuestro analizador sintactico general
    parser()

    # Si no hubo error tras el analisis sintactico
    if not codeErr: print('Programa COMPILO con exito!')