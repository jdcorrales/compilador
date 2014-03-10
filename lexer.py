# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
from ply.lex import TOKEN
'''
Diccionario de datos que contiene la lista de las
palabras reservadas

@var reserved diccionario
'''
reserved = {
  'class'    : 'CLASS',
  'extends'  : 'EXTENDS',
  'void'     : 'VOID',
  'int'      : 'INT',
  'boolean'  : 'BOOLEAN',
  'string'   : 'STRING',
  'return'   : 'RETURN',
  'if'       : 'IF',
  'else'     : 'ELSE',
  'while'    : 'WHILE',
  'break'    : 'BREAK',
  'continue' : 'CONTINUE',
  'this'     : 'THIS',
  'new'      : 'NEW',
  'length'   : 'LENGTH',
  'true'     : 'TRUE',
  'false'    : 'FALSE',
  'null'     : 'NULL'
}

'''
Lista que contiene los token's del lenguaje
a esta lista se le agrega el diccionario de
datos que contiene las palabras reservadas

@var token lista
'''
tokens = [
            'LNR',
            'NUMBER',
            'ENUMBER',
            'NUMBEREX',
            'ID',
            'NID',
            'BCOMMENT',
            'LCOMMENT',
            'ECOMMENT',
            'CSTRING',
            'ECSTRING',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'MODULE',
            'ME'
            'LPAREN',
            'RPAREN'
         ] + list(reserved.values())

'''
Lexema para LINEAS NO RECONOCIDAS
se crea por la necesidad de comentar dentro
del codigo fuente y que no aparesca en la consola

@function t_LNR
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
def t_LNR(t):
    r'\#\#.*'
    #print t.value
    return ''


'''
Apartir de esta linea se empieza a realizar la reglas(expresiones regulares)
que definen cada toke la cuales se llamaran lexemas.

Como estrategia se implementaran variables que contienen expresiones regulares
las cuales se contatenaran para cada caso, esto con el fin de poder hacer un
mejor seguimiento al codigo en caso de presentarse errores.


Conjunto de lexemas para reconocer numeros validos

Lexema que define el numero, debe reconocer lo siguiente
  233232
  54545
  04344
  0
'''
numero = r'[1-9]\d+|0[1-9]\d+|0'

'''
Lexema que define el numero con signo, debe reconocer lo siguiente
  -232
  -44
'''
numero_signo = r'\-'+numero+r''

'''
Lexema que define el numero con signo y punto flotante, debe reconocer lo siguiente
  454.767
  -290.8989
  -.44
  -0.4646
'''
numero_punto_flotante = r'\-?([1-9]\d+|0[1-9]\d+|0)\.\d+|\-?\.\d+'

'''
Lexema que define el numero con signo, punto flotante y exponencial, debe reconocer lo siguiente
  454.767
  -290.8989
  -.44
  -0.4646
'''

numero_exponencial = r'\-?\d+E[\-\+]?\d+|\-?\d+\.\d+E[\-\+]?\d+|\-?\.\d+E[\-\+]?\d+'

'''
Union de todos los lexemas que definen un numero
'''
number = r''+numero_exponencial+r'|'+numero_punto_flotante+r'|'+numero_signo+r'|'+numero+r''



'''
Conjunto de Lexemas para reconocer numeros no validos

Lexema que reconoce numeros que tengan 2 o mas ceros a la izquierda, debe reconocer lo
siguiente:

  00000000
  -000000
  000004545
  -000056
'''
no_ceros    = r'\-?(0{2,})\d+(\.\d*)?'

'''
Lexema que reconoce numeros que tengan 2 o mas signos negativos, debe reconocer lo
siguiente:

  -----000000
  ---56
  ---000056
  0---556
  00000---556
  000565600---55600
  000565600---00000--55600
'''
no_minus    = r'(\-{2,}\d+{\-2,}\d+)+|(\d+\-{2,}\d+)+|(\d+\-{2,})+|(\-{2,}\d+)+'

'''
Lexema que reconoce numeros que tengan 2 o mas puntos flotantes, debe reconocer lo
siguiente:

  ....32
  -...9776
  ----.78
  ----....90
  ----....000090
  545....5454
  676.65656.66565
  65656.
  87878.....
'''
no_punto = r'(\-{2,}|\-)?(\.{2,}\d+|\d+(\.{2,}\d+)+|\d+\.{2,})|\-{2,}\.\d+|\-\.{2,}\d+|\d+(\.+\d+\.+\d+)+'

'''
Lexema que reconoce numeros que tengan 2 o mas exponenciales, debe reconocer lo
siguiente:

  536-E
  5878-EEE
  58899---E
  58000---EEE
  -23443-E
  5878-EEE
  58899---E
  58000---EEE
  00000078-E
  5878-EEE
  58899---E
  58000---EEE
  ---3434-E
  ---00007575-E
'''
no_exponencial = r'\-*\d+(\.+\d+)*\-+E+([\+\-]*\d*\.*\d*)+'

nonumber = r''+no_exponencial+r'|'+no_punto+r'|'+no_ceros+r'|'+no_minus+r''


'''
Lexema para reconocer numeros en formato hexaesimal.

@function t_NUMBEREX
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''


def t_NUMBEREX(t):
    r'0x[0-9A-Fa-f]+'
    return t


'''
Lexema para reconocer numeros no validos.

@function t_ENUMBER
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
@TOKEN(nonumber)

def t_ENUMBER(t):
    print "ERROR: Numero '%s' invalido en la linea %d columna %d" % (t.value, t.lexer.lineno, obtener_columna(t.lexer.lexdata, t))
t_ENUMBER.__doc__ = nonumber

'''
Lexema para reconocer numeros.

@function t_NUMBER
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''

@TOKEN(number)

def t_NUMBER(t):
    return t
t_NUMBER.__doc__ = number

'''
Lexema para reconocer identificadores no validos.
Hace las siguientes validaciones:
  * Si existe una cadena de entrada que empieza con
    numeros saca el error de identificador invalido
@function t_NID
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
def t_NID(t):
    r'\d+[a-zA-Z_\-_]+[0-9\-_]*'
    print "ERROR: Identificador '%s' invalido en la linea %d columna %d" % (t.value, t.lexer.lineno, obtener_columna(t.lexer.lexdata, t))


'''
Lexema para reconocer identificadores.
Hace las siguientes validaciones:
  * Que el identificador no se encuentre
    entre las palabras reservadas
  * Si la longitud del identificador tiene
    mas de 20 caracteres devuelve los primeros
    20 caracteres
@function t_ID
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-\_]*'
    t.type = reserved.get(t.value,'ID')
    if len(t.value) > 20:
      t.value = t.value[0:20]
    return t

'''
Lexema para reconocer un string
debe reconocer las siguientes expresiones

  "esto es una cadena de caracteres"
  "esto es una cadena \" escapada\" "
'''
def t_CSTRING(t):
    r'"{1}([^\\"]|\\(.|\n))*"{1}'
    t.lexer.lineno += t.value.count("\n")
    return t

'''
Lexema para reconocer un string invalido
debe reconocer las siguientes expresiones

  "esto es una cadena de caracteres
  "esto es una cadena \" escapada\"
'''
def t_ECSTRING(t):
    r'"([^\\"]|\\(.|\n))*|"{2,}'
    print "FATAL ERROR: La cadena de caracteres '%s' no esta cerrada linea %d columna %d" % (t.value, t.lexer.lineno, obtener_columna(t.lexer.lexdata, t))
    exit(0)

'''
Lexema para reconocer lineas comentadas
@function t_LCOMMENT
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
def t_LCOMMENT(t):
    r'//(.)*'
    return t

'''
Lexema para reconocer bloques de lineas comentadas
@function t_BCOMMENT
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
def t_BCOMMENT(t):
    r'/\*(.|\n|\r|\t)*?\*/'
    t.lexer.lineno += t.value.count("\n")
    return t

'''
Lexema para reconocer error del no cierre del bloque
comentarios
@function t_ECOMMENT
@param  t (instancia del simbolo)
@return t (instancia del simbolo)
'''
def t_ECOMMENT(t):
    r'/\*(.|\n|\r|\t)*?'
    print "FATAL ERROR: El bloque de comentario '%s' no esta cerrado linea %d columna %d" % (t.value, t.lexer.lineno, obtener_columna(t.lexer.lexdata, t))
    exit(0)

'''
Lexemas para operadores unarios, binarios, aritmeticos y de agrupacion
'''

def t_PLUS(t):
  r'\+'
  return t

def t_MINUS(t):
  r'-'
  return t

def t_TIMES(t):
  r'\*'
  return t

def t_DIVIDE(t):
  r'/'
  return t

def t_MODULE(t):
  r'%'
  return t

def t_LPAREN(t):
  r'\('
  return t

def t_RPAREN(t):
  r'\)'
  return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

'''
Funcion para la gestion de errores

Los token's no encontrados los muestra como caracteres invalidos
lueog omite el error y continua con la ejecucion del programa
@function t_error
@param  t     (instancia del simbolo)
@return void
'''
def t_error(t):
    print "ERROR: Token '%s' no reconocido en la linea %d columna %d" % (t.value[0], t.lexer.lineno, obtener_columna(t.lexer.lexdata, t))
    t.lexer.skip(1)

'''
Funcion para leer el codigo funente desde un archivo
y pasar al lexer las cadenas de caracteres a analizar

@function leer_archivo
@param  void
@return void
'''
def leer_archivo():
    '''
    Abre el archivo y lee linea a linea poniendo las
    cadenas de caracteres de cada linea en la intrada
    del analizador lexico
    '''
    with open('archivos_prueba/tokens_simples.txt') as linea:
        datos = linea.read()
        lexer.input(datos)
    '''
    Loop infinido que muestra los token's reconocidos por
    el analizador lexico dando informacion de:
    tipo de token
    valor del token
    fila donde fue leido
    columna donde fue leido
    cuando no encuentra mas token's en la entrada termina
    la iteracion
    '''
    while True:
        tok = lexer.token()
        if not tok: break # Si no encuentra token's detiene las iteraciones
        print "Tipo: %s Valor '%s' Fila %d Columna %d" %(tok.type, tok.value, tok.lineno, obtener_columna(tok.lexer.lexdata, tok))

'''
Funcion para determinar la columna donde se encuentra
ubicado el token leido

@function obtener_columna
@param  cadena  (cadena de entrada)
@param  token   (instancia del simbolo)
@return columna (posicion de la columna donde empieza el token)
'''
def obtener_columna(cadena,token):
  ultimo_salto = cadena.rfind('\n',0,token.lexpos) #determina la posicion inmediatamente anterior del ultimo salto de linea que encuentre en la cadena
  '''
  token.lexpos posicion del primer caracter del token encontrado
  haciendo la resta en el token.lexpos - ultimo_salto se obtiene
  la posicion de la  columna en donde empieza el token
  '''
  columna = (token.lexpos - ultimo_salto)
  return columna


'''
Constructor del analizador lexico
'''
lexer = lex.lex()

'''
Llamada inicial para comenzar a leer los token's
del archivo
'''
leer_archivo()
