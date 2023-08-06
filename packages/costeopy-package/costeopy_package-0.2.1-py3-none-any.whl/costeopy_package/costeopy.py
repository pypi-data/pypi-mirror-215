import math

# Librerías para importar padrón de ESCALE

import pandas as pd
import httplib2
from bs4 import BeautifulSoup
import wget
import zipfile
import os
from dbfread import DBF

# Datos para agregar documentación

from pandas import DataFrame

# Ejemplos

def mancha(num1,num2):
    return num1+num2

def leo(num1,num2):
    return num1-num2

def vaca(num1,num2):
    return num1*num2

def mila(num1,num2):
    return num1/num2

def michi():
    print(" /\\_/\\")
    print("( o.o )")
    print(" > ^ <")

# Lista de meses

mes_13=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic','anual']
mes_12=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
mes_10=['mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
mes_inactivo_2=['ene','feb']
mes_agui_2=['jul','dic']
mes_noagui_2=['ene','feb','mar','abr','may','jun','ago','sep','oct','nov']

'''
        ETAPA 2: Definir funciones

'''

# CAS

def cas(base: DataFrame, nombre_perfil: str, meses_perfil: int, monto_perfil: int) -> DataFrame:

    '''
    Calcula el monto anual y mensual de la remuneración de un perfil en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre_perfil: str
        Nombre o abreviatura del perfil cuyo monto se quiere calcular.

    meses_perfil: int
        Número de meses de actividad del perfil.

    monto_perfil: int
        Monto de la remuneración del perfil.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con columnas adicionales que representan la remuneración anual y mensual del perfil.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.cas(bint, 'mant_12', 12, 2500)

    '''

    base['cas_'+nombre_perfil+'_anual'] = base[nombre_perfil]*meses_perfil*monto_perfil

    if meses_perfil == 12:

        for mes in mes_12:
            base['cas_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*monto_perfil

    elif meses_perfil == 10:

        for mes in mes_10:
            base['cas_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*monto_perfil

        for mes in mes_inactivo_2:
            base['cas_'+nombre_perfil+'_'+mes] = 0

# Aguinaldo

def aguinaldo(base: DataFrame, nombre_perfil: str, veces_agui: int, monto_agui: int) -> DataFrame:

    '''
    Calcula el monto anual y mensual del aguinaldo de un perfil en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre_perfil: str
        Nombre o abreviatura del perfil cuyo aguinaldo se quiere calcular.

    veces_agui: int
        Número de veces al año que recibe aguinaldo el perfil.

    monto_agui: int
        Monto del aguinaldo.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con columnas adicionales que representan el aguinaldo anual y mensual del perfil.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.aguinaldo(bint, 'mant_12', 2, 300)

    '''

    base['agui_'+nombre_perfil+'_anual'] = base[nombre_perfil]*veces_agui*monto_agui

    for mes in mes_agui_2:
        base['agui_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*monto_agui

    for mes in mes_noagui_2:
        base['agui_'+nombre_perfil+'_'+mes] = 0

# Tope de Essalud

def tope(UIT_porc: float, UIT: int) -> int:

    '''
    Calcula el monto de aporte máximo a EsSalud referente a la tasa aplicable del 9% sobre su remuneración.

    Parámetros
    ----------

    UIT_porc: float
        Base imponible máxima para calcular el aporte a EsSalud, expresada como un porcentaje. Para los años 2022 y 2023 es el 45% de la UIT vigente.

    UIT: int
        Monto de la UIT vigente.

    Resultado
    --------

    int
        Retorna el monto máximo de aporte a EsSalud. Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    -----

    >>> monto_tope=ct.tope(0.45, 5300)

    '''

    tope_max=math.ceil(0.09*UIT_porc*UIT)

    return tope_max

#monto_tope=tope(0.55,4600)

# Aporte individual a EsSalud

def aporte_essalud(base: DataFrame, nombre_perfil: str, monto_perfil: int, monto_tope: int) -> DataFrame:

    '''
    Calcula el monto del aporte a EsSalud respecto de la remuneración del perfil en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre_perfil: str
        Nombre o abreviatura del perfil cuyo monto máximo del aporte a EsSalud se quiere calcular.

    monto_perfil: int
        Monto de la remuneración del perfil.

    monto_tope: int
        Monto máximo de aporte a EsSalud, que es el resultado de la función tope().

    Resultado
    --------

    DataFrame
        Devuelve la base intermedia actualizada con una columna adicional que representa el aporte a EsSalud, el cual es el 9% del monto de la remuneración del perfil y tiene como límite al monto máximo de aporte a EsSalud.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.aporte_essalud(bint, 'mant_12', 2500, 201)

    '''

    base['ess_'+nombre_perfil] = min(math.ceil(0.09*monto_perfil),monto_tope)

# EsSalud

# nombre_perfil: nombre del perfil, entre comillas
# meses_perfil: número de meses activos del perfil

def essalud(base: DataFrame, nombre_perfil: str, meses_perfil: int) -> DataFrame:

    '''
    Calcula el monto anual y mensual del aporte a EsSalud de un perfil en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre_perfil: str
        Nombre o abreviatura del perfil cuyo aporte a EsSalud se quiere calcular.

    meses_perfil: int
        Número de meses de actividad del perfil.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con columnas adicionales que reflejan el monto anual y mensual del aporte a EsSalud correspondiente al perfil especificado.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.essalud(bint, 'mant_12', 12)

    '''

    base['essalud_'+nombre_perfil+'_anual'] = base[nombre_perfil]*meses_perfil*base['ess_'+nombre_perfil]

    if meses_perfil == 12:

        for mes in mes_12:
            base['essalud_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*base['ess_'+nombre_perfil]

    elif meses_perfil == 10:

        for mes in mes_10:
            base['essalud_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*base['ess_'+nombre_perfil]

        for mes in mes_inactivo_2:
            base['essalud_'+nombre_perfil+'_'+mes] = 0

# Total por perfil

def total_perfil(base: DataFrame, nombre: str, nombre_perfil: str, continuidad: int) -> DataFrame:

    '''
    Calcula el monto total de la remuneración, aporte a EsSalud o aguinaldo de un perfil en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre: str
        Indica el tipo de monto a calcular. Puede tomar los siguientes valores:

        - cas: para calcular la remuneración.
        - essalud: para calcular el aporte a EsSalud.
        - agui: para calcular el aguinaldo.

    nombre_perfil: str
        Nombre o abreviatura del perfil cuyo monto total se quiere calcular.

    continuidad: int
        Indica la continuidad del contrato del perfil:

        - 1: Perfil con contrato de 12 meses o 10 meses exclusivamente.
        - 2: Perfil con contrato de 12 meses y 10 meses.
        - 3: Perfil con contrato exclusivamente de 12 meses.
        - 4: Perfil con contrato exclusivamente de 10 meses.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con una columna adicional que refleja el monto total de la remuneración, aporte a EsSalud o aguinaldo correspondiente al perfil especificado.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.total_perfil(bint, 'cas', 'mant_12', 3)

    '''

    if continuidad == 1:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_anual']

    elif continuidad == 2:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_anual']+base[nombre+'_'+nombre_perfil+'_10_anual']

    elif continuidad == 3:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_anual']

    elif continuidad == 4:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_10_anual']

# Total por perfil por meses

def total_perfil_mes(base: DataFrame, nombre: str, nombre_perfil: str, continuidad: int) -> DataFrame:

    '''
    Calcula el monto total por mes de la remuneración, aporte a EsSalud o aguinaldo de un perfil en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre: str
        Indica el tipo de monto a calcular. Puede tomar los siguientes valores:

        - cas: para calcular la remuneración.
        - essalud: para calcular el aporte a EsSalud.
        - agui: para calcular el aguinaldo.

    nombre_perfil: str
        Nombre o abreviatura del perfil cuyo monto total se quiere calcular.

    continuidad: int
        Indica la continuidad del contrato del perfil:

        - 1: Perfil con contrato de 12 meses o 10 meses exclusivamente.
        - 2: Perfil con contrato de 12 meses y 10 meses.
        - 3: Perfil con contrato exclusivamente de 12 meses.
        - 4: Perfil con contrato exclusivamente de 10 meses.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con columnas adicionales que representan el monto total mensual del perfil especificado, en relación a la remuneración, el aporte a EsSalud o el aguinaldo.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.total_perfil(bint, 'essalud', 'mant_10', 4)

    '''

    if continuidad == 1:
        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_'+mes]

    elif continuidad == 2:
        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_'+mes]+base[nombre+'_'+nombre_perfil+'_10_'+mes]

    elif continuidad == 3:
        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_'+mes]

    elif continuidad == 4:
        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_10_'+mes]

# Totales

def total(base: DataFrame, nombre: str) -> DataFrame:

    '''
    Calcula el monto total de la remuneración, aporte a EsSalud o aguinaldo de todos los perfiles en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre: str
        Indica el tipo de monto a calcular. Puede tomar los siguientes valores:

        - cas: para calcular la remuneración.
        - essalud: para calcular el aporte a EsSalud.
        - agui: para calcular el aguinaldo.
        - costo: para calcular la suma de la remuneración, el aporte a EsSalud y el aguinaldo.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con una columna adicional que refleja el monto total relacionado con la remuneración, el aporte a EsSalud, el aguinaldo o la suma de estos conceptos.

    Nota
    ----

    Para evitar errores al utilizar el valor 'costo', se deben haber ingresado previamente los valores correspondientes a 'cas', 'essalud' y 'agui' en el parámetro 'nombre'.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.total_perfil(bint, 'costo')

    '''

    if nombre == 'cas':
        base['total_'+nombre+'_admin'] = base[base.columns[[x.startswith('cas_') for x in base.columns]].tolist()].sum(axis=1)
    elif nombre == 'essalud':
        base['total_'+nombre+'_admin'] = base[base.columns[[x.startswith('essalud_') for x in base.columns]].tolist()].sum(axis=1)
    elif nombre == 'agui':
        base['total_'+nombre+'_admin'] = base[base.columns[[x.startswith('agui_') for x in base.columns]].tolist()].sum(axis=1)
    elif nombre == 'costo':
        base[nombre+'_cas_admin'] = base[base.columns[[x.startswith('total_') for x in base.columns]].tolist()].sum(axis=1)

# Total por mes

# nombre: puede tomar los valores = cas, essalud, agui
# cas: costo total de CAS de todos los perfiles por mes
# ess: costo total de EsSalud de todos los perfiles por mes
# agui: costo total de aguinaldo de todos los perfiles por mes

def total_mes(base: DataFrame, nombre: str) -> DataFrame:

    '''
    Calcula el monto total de la remuneración, aporte a EsSalud o aguinaldo de todos los perfiles en la base de datos.

    Parámetros
    ----------

    base: DataFrame
        Base intermedia.

    nombre: str
        Indica el tipo de monto a calcular. Puede tomar los siguientes valores:

        - cas: para calcular la remuneración.
        - essalud: para calcular el aporte a EsSalud.
        - agui: para calcular el aguinaldo.

    Resultado
    --------

    DataFrame
        Retorna la base intermedia con columnas adicionales que representan el monto total mensual de todos los perfiles, en relación a la remuneración, el aporte a EsSalud o el aguinaldo.

    Referencias
    ----------
    Para obtener información adicional sobre la base intermedia y cómo ha sido estimada, consulta el siguiente `gráfico <https://drive.google.com/file/d/1Am0O3OyeCj6og7RjZuQzyEa1EPmRhu-L/view?usp=sharing>`_.

    Ejm:
    -----

    >>> ct.total_mes(bint, 'agui')

    '''

    if nombre == 'cas':
        bcas = base[base.columns[[x.startswith('cas_') for x in base.columns]].tolist()]
        base['cas_admin_ene'] = bcas[bcas.columns[[x.endswith('_ene') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_feb'] = bcas[bcas.columns[[x.endswith('_feb') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_mar'] = bcas[bcas.columns[[x.endswith('_mar') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_abr'] = bcas[bcas.columns[[x.endswith('_abr') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_may'] = bcas[bcas.columns[[x.endswith('_may') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_jun'] = bcas[bcas.columns[[x.endswith('_jun') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_jul'] = bcas[bcas.columns[[x.endswith('_jul') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_ago'] = bcas[bcas.columns[[x.endswith('_ago') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_sep'] = bcas[bcas.columns[[x.endswith('_sep') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_oct'] = bcas[bcas.columns[[x.endswith('_oct') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_nov'] = bcas[bcas.columns[[x.endswith('_nov') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_dic'] = bcas[bcas.columns[[x.endswith('_dic') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_anual'] = bcas[bcas.columns[[x.endswith('_anual') for x in bcas.columns]].tolist()].sum(axis=1)

    elif nombre == 'essalud':
        bcas = base[base.columns[[x.startswith('essalud_') for x in base.columns]].tolist()]
        base['essalud_admin_ene'] = bcas[bcas.columns[[x.endswith('_ene') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_feb'] = bcas[bcas.columns[[x.endswith('_feb') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_mar'] = bcas[bcas.columns[[x.endswith('_mar') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_abr'] = bcas[bcas.columns[[x.endswith('_abr') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_may'] = bcas[bcas.columns[[x.endswith('_may') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_jun'] = bcas[bcas.columns[[x.endswith('_jun') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_jul'] = bcas[bcas.columns[[x.endswith('_jul') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_ago'] = bcas[bcas.columns[[x.endswith('_ago') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_sep'] = bcas[bcas.columns[[x.endswith('_sep') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_oct'] = bcas[bcas.columns[[x.endswith('_oct') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_nov'] = bcas[bcas.columns[[x.endswith('_nov') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_dic'] = bcas[bcas.columns[[x.endswith('_dic') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_anual'] = bcas[bcas.columns[[x.endswith('_anual') for x in bcas.columns]].tolist()].sum(axis=1)

    elif nombre == 'agui':
        bcas = base[base.columns[[x.startswith('agui_') for x in base.columns]].tolist()]
        base['agui_admin_ene'] = bcas[bcas.columns[[x.endswith('_ene') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_feb'] = bcas[bcas.columns[[x.endswith('_feb') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_mar'] = bcas[bcas.columns[[x.endswith('_mar') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_abr'] = bcas[bcas.columns[[x.endswith('_abr') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_may'] = bcas[bcas.columns[[x.endswith('_may') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_jun'] = bcas[bcas.columns[[x.endswith('_jun') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_jul'] = bcas[bcas.columns[[x.endswith('_jul') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_ago'] = bcas[bcas.columns[[x.endswith('_ago') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_sep'] = bcas[bcas.columns[[x.endswith('_sep') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_oct'] = bcas[bcas.columns[[x.endswith('_oct') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_nov'] = bcas[bcas.columns[[x.endswith('_nov') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_dic'] = bcas[bcas.columns[[x.endswith('_dic') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_anual'] = bcas[bcas.columns[[x.endswith('_anual') for x in bcas.columns]].tolist()].sum(axis=1)

def padron_web(ruta: str, almacenar: bool = True) -> DataFrame:

    '''
    Descarga y devuelve la versión más reciente del Padrón de Instituciones Educativas y Programas de ESCALE.

    Parámetros
    ----------

    ruta: str
        Directorio de descarga, es la ubicación donde se guardan los archivos descargados.

    almacenar: bool, opcional
        Indica si se deben conservar las versiones anteriores del Padrón de Instituciones Educativas y Programas. Por defecto, es True.

    Resultado
    --------

    DataFrame
        Retorna el Padrón de Instituciones Educativas y Programas más actualizado.

    Notas
    -----

    - El Padrón de Instituciones Educativas y Programas se descarga desde el portal de ESCALE y se guarda en la ubicación especificada por 'ruta'.
    - Si 'almacenar' es True, se conservarán todas las versiones anteriores del Padrón de Instituciones Educativas y Programas en la carpeta especificada por 'ruta'.
    - Si 'almacenar' es False, solo se conservará solo la última versión del Padrón de Instituciones Educativas y Programas.
    - El resultado de la función se devuelve como un DataFrame de Pandas. Asegúrese de asignar el resultado a una variable para su posterior uso.
    - El DataFrame devuelto es la versión más actual del Padrón de Instituciones Educativas y Programas de ESCALE, proporcionando información actualizada y detallada sobre las instituciones educativas y los programas registrados.

    Referencias
    ----------
    Para obtener información adicional sobre cómo utilizar los datos del Padrón de Instituciones Educativas y Programas, puedes consultar el siguiente `Tablero <https://app.powerbi.com/view?r=eyJrIjoiMmNjNjgzZDgtNzkzMy00YzhlLWE0NWEtNTAwNjdiMjZiNTk0IiwidCI6IjE3OWJkZGE4LWQ5NjQtNDNmZi1hZDNiLTY3NDE4NmEyZmEyOCIsImMiOjR9>`_.

    El tablero contiene:

        - Información actualizada del Padrón de Instituciones Educativas y Programas de ESCALE.
        - Definiciones de las principales variables que identifican a las instituciones educativas y programas, como el código local, el código modular y el anexo.
        - Cuadros estadísticos de instituciones educativas y programas según nivel modular.
        - Información detallada de una institución educativa o programa según su nivel modular.

    Ejm:
    -----

    >>> padron = ct.padron_web('D:\eder', True)

    '''

    if almacenar == True:

        # Definir ruta

        #ruta='D:\eder'

        # Creación de carpeta

        dir = os.path.join(ruta, 'padron_web')

        if not os.path.exists(dir):
            os.mkdir(dir)

        else:
            print('Ya existe la carpeta')

        # Extración de enlaces del portal de ESCALE

        url = 'http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881'

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        enlace_1 = links [26:30]

        # Establecer enlace con fecha más actual

        l1=enlace_1[0]
        l2=enlace_1[1]
        l3=enlace_1[2]
        l4=enlace_1[3]

        n1=l1[76:81]
        n2=l2[76:81]
        n3=l3[76:81]
        n4=l4[76:81]

        mayor=max(n1,n2,n3,n4)

        enlace_2='http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881/'+mayor+';jsessionid=28cf9ab9d37f6fed3dfe4cea19d6?_110_INSTANCE_GMv7_redirect=http%3A%2F%2Fescale.minedu.gob.pe%2Fuee%2F-%2Fdocument_library_display%2FGMv7%2Fview%2F958881%3Bjsessionid%3D28cf9ab9d37f6fed3dfe4cea19d6'

        # Extraer zip del enlace con fecha más actual

        url = enlace_2

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        enlace_3 = links [32:33]

        # Enlace zip con fecha más actual

        e1=enlace_3[0]
        e2=e1[62:70]

        file = 'padron_web\Padron_web_'+e2+'.zip'

        # Extracción del padrón web en formato dbf

        path = os.path.join(ruta, file)

        if not os.path.exists(path):
            wget.download(enlace_3[0], ruta+'\padron_web')
            path2=os.path.join(ruta, '\padron_web\Padron_web.dbf')

            if not os.path.exists(path2):
                fantasy_zip = zipfile.ZipFile(ruta+'\padron_web\Padron_web_'+e2+'.zip')
                fantasy_zip.extract('Padron_web.dbf', ruta+'\padron_web')
                path3 = ruta+'/padron_web/'
                os.rename(path3+'Padron_web.dbf', path3+'Padron_web_'+e2+'.dbf')

            else:
                print('Ya existe el Padron_web.dbf')

        else:
            print('Ya existe el Padron_web_'+e2+'.zip')

        # Importar Padrón web con fecha más actual a Python

        # Generar DBF

        b_dbf=DBF(ruta+'\padron_web\Padron_web_'+e2+'.dbf')

        # Generar dataframe

        padweb = pd.DataFrame(iter(b_dbf))

        return padweb

    elif almacenar == False:

        # Creación de carpeta

        dir = os.path.join(ruta, 'padron_web')

        if not os.path.exists(dir):
            os.mkdir(dir)

        else:
            print('Ya existe la carpeta')

        # Eliminar todos los padrones

        dir = ruta+'\padron_web'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        # Extración de enlaces del portal de ESCALE

        url = 'http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881'

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        enlace_1 = links [26:30]

        # Establecer enlace con fecha más actual

        l1=enlace_1[0]
        l2=enlace_1[1]
        l3=enlace_1[2]
        l4=enlace_1[3]

        n1=l1[76:81]
        n2=l2[76:81]
        n3=l3[76:81]
        n4=l4[76:81]

        mayor=max(n1,n2,n3,n4)

        enlace_2='http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881/'+mayor+';jsessionid=28cf9ab9d37f6fed3dfe4cea19d6?_110_INSTANCE_GMv7_redirect=http%3A%2F%2Fescale.minedu.gob.pe%2Fuee%2F-%2Fdocument_library_display%2FGMv7%2Fview%2F958881%3Bjsessionid%3D28cf9ab9d37f6fed3dfe4cea19d6'

        # Extraer zip del enlace con fecha más actual

        url = enlace_2

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        enlace_3 = links [32:33]

        # Enlace zip con fecha más actual

        e1=enlace_3[0]
        e2=e1[62:70]

        file = 'padron_web\Padron_web_'+e2+'.zip'

        # Extracción del padrón web en formato dbf

        path = os.path.join(ruta, file)

        if not os.path.exists(path):
            wget.download(enlace_3[0], ruta+'\padron_web')
            path2=os.path.join(ruta, '\padron_web\Padron_web.dbf')

            if not os.path.exists(path2):
                fantasy_zip = zipfile.ZipFile(ruta+'\padron_web\Padron_web_'+e2+'.zip')
                fantasy_zip.extract('Padron_web.dbf', ruta+'\padron_web')
                path3 = ruta+'/padron_web/'
                os.rename(path3+'Padron_web.dbf', path3+'Padron_web_'+e2+'.dbf')

            else:
                print('Ya existe el Padron_web.dbf')

        else:
            print('Ya existe el Padron_web_'+e2+'.zip')

        # Importar Padrón web con fecha más actual a Python

        # Generar DBF

        b_dbf=DBF(ruta+'\padron_web\Padron_web_'+e2+'.dbf')

        # Generar dataframe

        padweb = pd.DataFrame(iter(b_dbf))

        return padweb

def siga_obj(base: DataFrame, objeto: str) -> DataFrame:

    '''
    Esta función filtra una base de datos del SIGA y retorna los registros cuyo nombre de objeto coincide con los caracteres de búsqueda.

    Parámetros
    ----------

    base: DataFrame
        Base de datos del SIGA que se emplea para realizar el filtrado.

    objeto: str
        Caracteres de búsqueda en mayúsculas que corresponden al nombre del objeto.

    Resultado
    --------

    DataFrame
        Retorna la base de datos del SIGA filtrada que contiene únicamente los registros cuyo nombre de objeto coincide con los caracteres de búsqueda especificados en mayúsculas.

    Notas
    -----

    - El resultado de la función se devuelve como un DataFrame de Pandas.
    - Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    -----

    # Establecer un DataFrame para asignar la base de datos del SIGA.

    base_siga = pd.DataFrame(...)

    # Filtrar la base del SIGA para el objeto 'TABLET'.

    siga_tablet = siga_obj(base_siga, 'TABLET')

    '''

    base['GRUPO_BIEN'] = base['GRUPO_BIEN'].str.zfill(2)
    base['CLASE_BIEN'] = base['CLASE_BIEN'].str.zfill(2)
    base['FAMILIA_BIEN'] = base['FAMILIA_BIEN'].str.zfill(4)
    base['ITEM_BIEN'] = base['ITEM_BIEN'].str.zfill(4)

    sigaf=base.loc[(base['SECTOR'] != '01')]

    sigaf['verificar']=sigaf['NOMBRE_ITEM'].str.contains(objeto)

    sigaobj=sigaf.loc[(sigaf['verificar'] == True)]

    sigaobj['cod_siga'] = sigaobj['GRUPO_BIEN']+'.'+sigaobj['CLASE_BIEN']+'.'+sigaobj['FAMILIA_BIEN']+'.'+sigaobj['ITEM_BIEN']

    del sigaobj['verificar']

    return sigaobj

def precio_obj(siga_objeto: DataFrame) -> DataFrame:

    '''
    Esta función utiliza una base de datos filtrada del SIGA para un objeto específico y retorna los precios correspondientes.

    Parámetros
    ----------

    siga_objeto: DataFrame
        DataFrame resultante de la función siga_obj, que contiene la base de datos filtrada del SIGA correspondiente a un objeto específico.

    Resultado
    --------

    DataFrame
        Retorna un DataFrame que contiene la media, mediana, percentil 20 y percentil 80 de los precios correspondientes al objeto especificado.

    Notas
    -----

    - El resultado de la función se devuelve como un DataFrame de Pandas.
    - Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    -----

    # Establecer un DataFrame para asignar la base de datos del SIGA.

    base_siga = pd.DataFrame(...)

    # Filtrar la base de datos del SIGA para el objeto 'TABLET'.

    siga_tablet = siga_obj(base_siga, 'TABLET')

    # Obtener los precios para el objeto 'TABLET'.

    precio_tablet=ct.precio_obj(siga_tablet)

    '''

    siga_objeto['n'] = 1
    objetoa=siga_objeto[['NOMBRE_ITEM','cod_siga','n','PRECIO_UNIT']]

    cant=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['n']].sum().reset_index()
    cant.rename(columns={'n':'cantidad'},inplace=True)

    media=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].mean().reset_index()
    media.rename(columns={'PRECIO_UNIT':'media'},inplace=True)

    p20=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.20).reset_index()
    p20.rename(columns={'PRECIO_UNIT':'p20'},inplace=True)

    p50=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.50).reset_index()
    p50.rename(columns={'PRECIO_UNIT':'mediana'},inplace=True)

    p80=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.80).reset_index()
    p80.rename(columns={'PRECIO_UNIT':'p80'},inplace=True)

    media_cant=pd.merge(cant, media, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50=pd.merge(media_cant, p50, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20=pd.merge(media_cant_p50, p20, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20_80=pd.merge(media_cant_p50_20, p80, on =['NOMBRE_ITEM','cod_siga'], how ='inner')

    return media_cant_p50_20_80

def siga_cod(base: DataFrame, codigo: str) -> DataFrame:

    '''
    Esta función filtra una base de datos del SIGA y retorna el registro del código SIGA que coincide con los caracteres de búsqueda especificados.

    Parámetros
    ----------

    base: DataFrame
        Base de datos del SIGA que se emplea para realizar el filtrado.

    codigo: str
        Código SIGA que se desea encontrar.

    Resultado
    --------

    DataFrame
        Retorna la base de datos del SIGA filtrada que contiene únicamente el registro cuyo código SIGA coincide con los caracteres de búsqueda especificados.

    Notas
    -----

    - El resultado de la función se devuelve como un DataFrame de Pandas.
    - Se asume que el código SIGA de un objeto es único, por lo tanto, se espera que el resultado contenga un único registro.
    - Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    -----

    # Establecer un DataFrame para asignar la base de datos del SIGA.

    base_siga = pd.DataFrame(...)

    # Filtrar la base de datos del SIGA para el código SIGA 74.08.9493.0001.

    siga_7408=ct.siga_cod(base_siga,'74.08.9493.0001')

    '''

    base['GRUPO_BIEN'] = base['GRUPO_BIEN'].str.zfill(2)
    base['CLASE_BIEN'] = base['CLASE_BIEN'].str.zfill(2)
    base['FAMILIA_BIEN'] = base['FAMILIA_BIEN'].str.zfill(4)
    base['ITEM_BIEN'] = base['ITEM_BIEN'].str.zfill(4)

    sigaf=base.loc[(base['SECTOR'] != '01')]

    sigaf['cod_siga'] = sigaf['GRUPO_BIEN']+'.'+sigaf['CLASE_BIEN']+'.'+sigaf['FAMILIA_BIEN']+'.'+sigaf['ITEM_BIEN']

    sigaf['verificar']=sigaf['cod_siga'].str.contains(codigo)

    sigaobj=sigaf.loc[(sigaf['verificar'] == True)]

    del sigaobj['verificar']

    return sigaobj

def precio_cod(siga_codigo: DataFrame) -> DataFrame:

    '''
    Esta función utiliza una base de datos filtrada del SIGA para un código SIGA específico y retorna los precios correspondientes.

    Parámetros
    ----------

    siga_codigo: DataFrame
        DataFrame resultante de la función siga_cod, que contiene la base de datos filtrada del SIGA correspondiente a un código SIGA específico.

    Resultado
    --------

    DataFrame
        Retorna un DataFrame que contiene la media, mediana, percentil 20 y percentil 80 de los precios correspondientes al código SIGA especificado.

    Notas
    -----

    - El resultado de la función se devuelve como un DataFrame de Pandas.
    - Se asume que el código SIGA de un objeto es único, por lo tanto, se espera que el resultado contenga un único registro.
    - Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    -----

    # Establecer un DataFrame para asignar la base de datos del SIGA.

    base_siga = pd.DataFrame(...)

    # Filtrar la base de datos del SIGA para el código SIGA 74.08.9493.0001.

    siga_7408=ct.siga_cod(base_siga,'74.08.9493.0001')

    # Obtener el precio para el código SIGA '74.08.9493.0001'.

    precio_7408=ct.precio_cod(siga_7408)

    '''

    siga_codigo['n'] = 1
    codigoa=siga_codigo[['NOMBRE_ITEM','cod_siga','n','PRECIO_UNIT']]

    cant=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['n']].sum().reset_index()
    cant.rename(columns={'n':'cantidad'},inplace=True)

    media=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].mean().reset_index()
    media.rename(columns={'PRECIO_UNIT':'media'},inplace=True)

    p20=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.20).reset_index()
    p20.rename(columns={'PRECIO_UNIT':'p20'},inplace=True)

    p50=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.50).reset_index()
    p50.rename(columns={'PRECIO_UNIT':'mediana'},inplace=True)

    p80=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.80).reset_index()
    p80.rename(columns={'PRECIO_UNIT':'p80'},inplace=True)

    media_cant=pd.merge(cant, media, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50=pd.merge(media_cant, p50, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20=pd.merge(media_cant_p50, p20, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20_80=pd.merge(media_cant_p50_20, p80, on =['NOMBRE_ITEM','cod_siga'], how ='inner')

    return media_cant_p50_20_80

# Importar base de traslados

def traslados(ruta,base):

    if base == 'movccpp':

        t = pd.read_stata(ruta+'/MovCCPP.dta')

    elif base == 'moviiee':

        t = pd.read_stata(ruta+'/MovIIEE.dta')

    elif base == 'movugel':

        t = pd.read_stata(ruta+'/MovUGEL.dta')

    return t

# Renombrar meses

def remes(base):

    base.rename(columns={'13':'costo_anual'},inplace=True)
    base.rename(columns={'1':'enero'},inplace=True)
    base.rename(columns={'2':'febrero'},inplace=True)
    base.rename(columns={'3':'marzo'},inplace=True)
    base.rename(columns={'4':'abril'},inplace=True)
    base.rename(columns={'5':'mayo'},inplace=True)
    base.rename(columns={'6':'junio'},inplace=True)
    base.rename(columns={'7':'julio'},inplace=True)
    base.rename(columns={'8':'agosto'},inplace=True)
    base.rename(columns={'9':'septiembre'},inplace=True)
    base.rename(columns={'10':'octubre'},inplace=True)
    base.rename(columns={'11':'noviembre'},inplace=True)
    base.rename(columns={'12':'diciembre'},inplace=True)

def validar_padron(dire: DataFrame, padweb: DataFrame, ue: DataFrame, nivel: str) -> DataFrame:

    '''
    Realiza validaciones de los anexos: Padrón de Instituciones Educativas y Metas Físicas de Contratación de intervenciones pedagógicas.
    Verifica el Pliego, la Unidad Ejecutora, la UGEL, el código local y el nombre de la institución educativa utilizando los códigos modulares como datos de validación.
    Utiliza como insumos el Padrón de Instituciones Educativas y Programas de ESCALE y la Base de Unidades Ejecutoras.

    Parámetros
    ----------

    dire: DataFrame
        Anexo remitido por la dirección encargada de la intervención pedagógica.

    padweb : DataFrame
        Padrón de Instituciones Educativas y Programas de ESCALE. Se recomienda usar la versión más actual para realizar las validaciones.
        También se puede utilizar la función padron_web para obtener la versión más actual del Padrón de Instituciones Educativas y Programas.

    ue: DataFrame
        Base que contiene los Pliegos, Unidades Ejecutoras y UGELes de todo el Perú.

    nivel : str
        Indica el nivel de desagregación del anexo que se desea validar. Puede tomar los siguientes valores:
        - 'cod_mod': el anexo de la intervención está desagregado a nivel de código modular.
        - 'ugel': el anexo de la intervención está desagregado a nivel de UGEL.
        - 'militar_cod_mod': el anexo de la intervención está desagregado a nivel de código modular. Además, la intervención pedagógica se implementa en colegios militares.
        - 'militar_ugel': el anexo de la intervención está desagregado a nivel de UGEL. Además, la intervención pedagógica se implementa en colegios militares.

    Resultado
    --------

    DataFrame
        Retorna un DataFrame que contiene los códigos modulares del anexo de la intervención pedagógica, junto con columnas adicionales que comparan el Pliego, la Unidad Ejecutora, el código local y el nombre del centro educativo para cada código modular.

    Notas
    -----

    - El resultado de la función se devuelve como un DataFrame de Pandas.
    - Actualmente, el valor correspondiente al Anexo para cada código modular es cero en todas las intervenciones pedagógicas.
    - Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    ----

    >>> # Importar librerías
    >>> import pandas as pd
    >>> from costeopy_package import costeopy as ct

    >>> # Cargar anexo remitido por la dirección
    >>> dire = pd.read_excel(ruta_input+'/Anexo 1xx4 - Metas de Físicas de Contratación.xlsx',sheet_name='Metas')
    >>> # Cargar versión más reciente del Padrón de Instituciones Educativas y Programas de ESCALE
    >>> padweb = ct.padron_web('D:\\')
    >>> # Cargar base de Unidades Ejecutoras
    >>> ue = pd.read_excel(ruta_input+'/base_ue_ugel_ubigeo_2023_v2.xlsx',sheet_name='base')
    >>> # Validar el anexo de la intervención pedagógica a nivel de UGEL
    >>> metas_ugel = ct.validar_padron(dire, padweb, ue, 'UGEL')

    '''

    if nivel == 'cod_mod':

        # Cambio de formato para validación

        dire.cod_mod=dire.cod_mod.astype(int)
        dire.cod_local_dire=dire.cod_local_dire.astype(int)
        dire.anexo=dire.anexo.astype(int)

        # Filtrar para estado igual a activa IE

        padweb_a = padweb[padweb.D_ESTADO == 'Activa']

        # Establecer df con variables de interés

        padweb_i=padweb_a[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU','D_NIV_MOD']]

        # Verificar tipo de variables

        print(padweb_i.dtypes)

        # Pasar a integer

        padweb_i.COD_MOD=padweb_i.COD_MOD.astype(int)
        padweb_i.CODOOII=padweb_i.CODOOII.astype(int)
        padweb_i.ANEXO=padweb_i.ANEXO.astype(int)

        padweb_i.loc[(padweb_i['CODLOCAL'] == ''),'CODLOCAL'] = '0'

        padweb_i.CODLOCAL=padweb_i.CODLOCAL.astype(int)

        # Renombrar variables

        padweb_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
        padweb_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        padweb_i.rename(columns={'CODLOCAL':'cod_local'},inplace=True)
        padweb_i.rename(columns={'ANEXO':'anexo'},inplace=True)
        padweb_i.rename(columns={'CEN_EDU':'nombre_iiee'},inplace=True)
        padweb_i.rename(columns={'COD_CAR':'cod_car'},inplace=True)
        padweb_i.rename(columns={'DAREACENSO':'dareacenso'},inplace=True)
        padweb_i.rename(columns={'D_NIV_MOD':'nivel'},inplace=True)

        # Combinar bases

        dire_padweb=pd.merge(dire, padweb_i, on =['cod_mod','anexo'], how ='left',indicator=True)

        # variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire_padweb, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Variables de interés

        bint=dire_padweb_ue[['cod_mod','cod_ugel','cod_local_dire','cod_local','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel','nombre_iiee_dire','nombre_iiee','nivel']]

        # Comparar suma con el total; out: True

        bint['cod_local_ver'] = bint['cod_local_dire'].eq(bint['cod_local'])
        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])
        bint['nombre_iiee_ver'] = bint['nombre_iiee_dire'].eq(bint['nombre_iiee'])

        return bint

    elif nivel == 'ugel':

        # Variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Variables de interés

        bint=dire_padweb_ue[['cod_ugel','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel']]

        # Comparar; out: True

        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])

        return bint

    elif nivel == 'militar_cod_mod':

        # Cambio de formato para validación

        dire.cod_mod=dire.cod_mod.astype(int)
        dire.cod_local_dire=dire.cod_local_dire.astype(int)
        dire.anexo=dire.anexo.astype(int)

        # Filtrar para estado igual a activa IE

        padweb_a = padweb[padweb.D_ESTADO == 'Activa']

        # Establecer df con variables de interés

        padweb_i=padweb_a[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU','D_NIV_MOD']]

        # Verificar tipo de variables

        print(padweb_i.dtypes)

        # Pasar a integer

        padweb_i.COD_MOD=padweb_i.COD_MOD.astype(int)
        padweb_i.CODOOII=padweb_i.CODOOII.astype(int)
        padweb_i.ANEXO=padweb_i.ANEXO.astype(int)

        padweb_i.loc[(padweb_i['CODLOCAL'] == ''),'CODLOCAL'] = '0'

        padweb_i.CODLOCAL=padweb_i.CODLOCAL.astype(int)

        # Renombrar variables

        padweb_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
        padweb_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        padweb_i.rename(columns={'CODLOCAL':'cod_local'},inplace=True)
        padweb_i.rename(columns={'ANEXO':'anexo'},inplace=True)
        padweb_i.rename(columns={'CEN_EDU':'nombre_iiee'},inplace=True)
        padweb_i.rename(columns={'COD_CAR':'cod_car'},inplace=True)
        padweb_i.rename(columns={'DAREACENSO':'dareacenso'},inplace=True)
        padweb_i.rename(columns={'D_NIV_MOD':'nivel'},inplace=True)

        # Combinar bases

        dire_padweb=pd.merge(dire, padweb_i, on =['cod_mod','anexo'], how ='left',indicator=True)

        # variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire_padweb, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Arreglo para colegios militares

        dire_padweb_ue.loc[(dire_padweb_ue['nombre_iiee']=='MILITAR PEDRO RUIZ GALLO') & (dire_padweb_ue['cod_ugel']==200001),'nom_ue'] = '301. COLEGIO MILITAR PEDRO RUIZ GALLO'
        dire_padweb_ue.loc[(dire_padweb_ue['nombre_iiee']=='MILITAR LEONCIO PRADO') & (dire_padweb_ue['cod_ugel']==70101),'nom_ue'] = '301. COLEGIO MILITAR LEONCIO PRADO'

        # Variables de interés

        bint=dire_padweb_ue[['cod_mod','cod_ugel','cod_local_dire','cod_local','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel','nombre_iiee_dire','nombre_iiee','nivel']]

        # Comparar suma con el total; out: True

        bint['cod_local_ver'] = bint['cod_local_dire'].eq(bint['cod_local'])
        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])
        bint['nombre_iiee_ver'] = bint['nombre_iiee_dire'].eq(bint['nombre_iiee'])

        return bint

    elif nivel == 'militar_ugel':

        # Variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Arreglo para colegios militares

        dire_padweb_ue.loc[(dire_padweb_ue['nom_ue_dire']=='301. COLEGIO MILITAR PEDRO RUIZ GALLO'),'nom_ue'] = '301. COLEGIO MILITAR PEDRO RUIZ GALLO'
        dire_padweb_ue.loc[(dire_padweb_ue['nom_ue_dire']=='301. COLEGIO MILITAR LEONCIO PRADO'),'nom_ue'] = '301. COLEGIO MILITAR LEONCIO PRADO'

        # Variables de interés

        bint=dire_padweb_ue[['cod_ugel','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel']]

        # Comparar; out: True

        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])

        return bint

def validar_activo(dire: DataFrame, padweb: DataFrame) -> DataFrame:

    '''
    Realiza validaciones de los anexos: Padrón de Instituciones Educativas y Metas Físicas de Contratación de intervenciones pedagógicas.
    Verifica si el código modular esta activo y si el tipo de gestión es Pública de gestión directa o Pública de gestión privada utilizando los códigos modulares como datos de validación.
    Utiliza como insumo el Padrón de Instituciones Educativas y Programas de ESCALE.

    Parámetros
    ----------

    dire: DataFrame
        Anexo remitido por la dirección encargada de la intervención pedagógica.

    padweb : DataFrame
        Padrón de Instituciones Educativas y Programas de ESCALE. Se recomienda usar la versión más actual para realizar las validaciones.
        También se puede utilizar la función padron_web para obtener la versión más actual del Padrón de Instituciones Educativas y Programas.

    Resultado
    --------

    DataFrame
        Retorna un DataFrame que contiene los códigos modulares del anexo de la intervención pedagógica, junto con columnas adicionales que incluyen el Anexo, el código local, el código de UGEL, el nombre del centro educativo, el nivel modular, el total de alumnos y el total de docentes para cada código modular.

    Notas
    -----

    - El resultado de la función se devuelve como un DataFrame de Pandas.
    - Las columnas adicionales en el DataFrame resultante son obtenidas del Padrón de Instituciones Educativas y Programas de ESCALE.
    - Asegúrese de asignar el resultado a una variable para su posterior uso.

    Ejm:
    ----

    >>> # Importar librerías
    >>> import pandas as pd
    >>> from costeopy_package import costeopy as ct

    >>> # Cargar anexo remitido por la dirección
    >>> dire = pd.read_excel(ruta_input+'/Anexo 1xx5 - Padrón de Instituciones Educativas.xlsx',sheet_name='Padrón')
    >>> # Cargar versión más reciente del Padrón de Instituciones Educativas y Programas de ESCALE
    >>> padweb = ct.padron_web('D:\\')
    >>> # Validar el anexo de la intervención pedagógica
    >>> padron_activo = ct.validar_activo(dire, padweb)

    '''

    # Filtrar para estado igual a activa

    padweb_a = padweb[padweb.D_ESTADO == 'Activa']

    # Filtrar para instituciones educativas públicas

    padweb_a_p=padweb_a.loc[(padweb_a['GESTION']=='1')|(padweb_a['GESTION']=='2')]

    # Establecer df con variables de interés

    padweb_i=padweb_a_p[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU','D_NIV_MOD','TALUMNO','TDOCENTE']]

    # Verificar tipo de variables

    print(padweb_i.dtypes)

    # Pasar a integer

    padweb_i.COD_MOD=padweb_i.COD_MOD.astype(int)
    padweb_i.CODOOII=padweb_i.CODOOII.astype(int)
    padweb_i.ANEXO=padweb_i.ANEXO.astype(int)

    padweb_i.loc[(padweb_i['CODLOCAL'] == ''),'CODLOCAL'] = '0'

    padweb_i.CODLOCAL=padweb_i.CODLOCAL.astype(int)

    # Renombrar variables

    padweb_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
    padweb_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
    padweb_i.rename(columns={'CODLOCAL':'cod_local'},inplace=True)
    padweb_i.rename(columns={'ANEXO':'anexo'},inplace=True)
    padweb_i.rename(columns={'CEN_EDU':'nombre_iiee'},inplace=True)
    padweb_i.rename(columns={'D_NIV_MOD':'nivel'},inplace=True)
    padweb_i.rename(columns={'TALUMNO':'total_alumnos'},inplace=True)
    padweb_i.rename(columns={'TDOCENTE':'total_docentes'},inplace=True)

    # Combinar bases

    dire_padweb=pd.merge(dire, padweb_i, on =['cod_mod','anexo'], how ='left',indicator=True)

    # Variables de interés

    bint=dire_padweb[['cod_mod','anexo','cod_local','cod_ugel','nombre_iiee','nivel','total_alumnos','total_docentes','_merge']]

    return bint
