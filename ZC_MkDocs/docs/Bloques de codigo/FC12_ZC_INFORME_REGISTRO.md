---
title: FC12_ZC_INFORME_REGISTRO
---
# FC FC12_ZC_INFORME_REGISTRO

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función para el almacenamiento y estructuración masiva de registros de trazabilidad dentro del buffer de informes del sistema.
    
    En ella se realizan las siguientes acciones:
    
    - Comprobación de habilitación: Verificación de la variable de permiso `HabilitacionGeneral`; si no se encuentra activa, se omite la ejecución del bloque mediante un retorno anticipado.
    - Desplazamiento de datos (FIFO):
        - Ejecución de la instrucción de bloque para desplazar todos los registros existentes en el Buffer una posición hacia abajo.
        - Liberación del índice 0 del array para permitir la inserción del nuevo registro sin sobrescribir el histórico reciente.
    - Gestión e inserción del nuevo registro:
            - Generación y asignación de un identificador único (Id) transformando la fecha y hora actual del sistema a formato cadena.
            - Escritura de los metadatos de control y catalogación (Registrar, Tipo, Codigo) en la primera posición del buffer.
            - Procesamiento y validación de hasta 4 marcas de tiempo dinámicas (Fecha_1 a Fecha_4), forzando una fecha por defecto (01/01/1970) si el año recibido es 0.
            - Mapeo y transferencia masiva de todas las variables de proceso vinculadas al evento, incluyendo cadenas de texto (CodString_1 a 15), booleanos (Bool_1 a 32), reales (Real_1 a 20) y enteros (Int_1 a 20).

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Registrar` | `USInt` | - | `-` | Orden registrar (0= no registrar / 1= registrar) |
| `Tipo` | `Int` | - | `-` | Tipo |
| `Codigo` | `String` | - | `-` | Codigo produccion |
| `Fecha_1_Ano` | `UInt` | - | `-` | Fecha 1  Año |
| `Fecha_1_Mes` | `USInt` | - | `-` | Fecha 1  Mes |
| `Fecha_1_Dia` | `USInt` | - | `-` | Fecha 1  Dia |
| `Fecha_1_DiaSemana` | `USInt` | - | `-` | Fecha 1  Dia de la semana |
| `Fecha_1_Hora` | `USInt` | - | `-` | Fecha 1  Hora |
| `Fecha_1_Minuto` | `USInt` | - | `-` | Fecha 1  Minuto |
| `Fecha_1_Segundo` | `USInt` | - | `-` | Fecha 1  Segundo |
| `Fecha_1_NanoSegundo` | `UDInt` | - | `-` | Fecha 1  Nanosegundo |
| `Fecha_2_Ano` | `UInt` | - | `-` | Fecha 2 Año |
| `Fecha_2_Mes` | `USInt` | - | `-` | Fecha 2 Mes |
| `Fecha_2_Dia` | `USInt` | - | `-` | Fecha 2 Dia |
| `Fecha_2_DiaSemana` | `USInt` | - | `-` | Fecha 2 Dia de la semana |
| `Fecha_2_Hora` | `USInt` | - | `-` | Fecha 2 Hora |
| `Fecha_2_Minuto` | `USInt` | - | `-` | Fecha 2 Minuto |
| `Fecha_2_Segundo` | `USInt` | - | `-` | Fecha 2 Segundo |
| `Fecha_2_NanoSegundo` | `UDInt` | - | `-` | Fecha 2 Nanosegundo |
| `Fecha_3_Ano` | `UInt` | - | `-` | Fecha 3 Año |
| `Fecha_3_Mes` | `USInt` | - | `-` | Fecha 3 Mes |
| `Fecha_3_Dia` | `USInt` | - | `-` | Fecha 3 Dia |
| `Fecha_3_DiaSemana` | `USInt` | - | `-` | Fecha 3 Dia de la semana |
| `Fecha_3_Hora` | `USInt` | - | `-` | Fecha 3 Hora |
| `Fecha_3_Minuto` | `USInt` | - | `-` | Fecha 3 Minuto |
| `Fecha_3_Segundo` | `USInt` | - | `-` | Fecha 3 Segundo |
| `Fecha_3_NanoSegundo` | `UDInt` | - | `-` | Fecha 3 Nanosegundo |
| `Fecha_4_Ano` | `UInt` | - | `-` | Fecha 4 Año |
| `Fecha_4_Mes` | `USInt` | - | `-` | Fecha 4 Mes |
| `Fecha_4_Dia` | `USInt` | - | `-` | Fecha 4 Dia |
| `Fecha_4_DiaSemana` | `USInt` | - | `-` | Fecha 4 Dia de la semana |
| `Fecha_4_Hora` | `USInt` | - | `-` | Fecha 4 Hora |
| `Fecha_4_Minuto` | `USInt` | - | `-` | Fecha 4 Minuto |
| `Fecha_4_Segundo` | `USInt` | - | `-` | Fecha 4 Segundo |
| `Fecha_4_NanoSegundo` | `UDInt` | - | `-` | Fecha 4 Nanosegundo |
| `CodString_1` | `Int` | - | `-` | Codigo string 1 |
| `CodString_2` | `Int` | - | `-` | Codigo string 2 |
| `CodString_3` | `Int` | - | `-` | Codigo string 3 |
| `CodString_4` | `Int` | - | `-` | Codigo string 4 |
| `CodString_5` | `Int` | - | `-` | Codigo string 5 |
| `CodString_6` | `Int` | - | `-` | Codigo string 6 |
| `CodString_7` | `Int` | - | `-` | Codigo string 7 |
| `CodString_8` | `Int` | - | `-` | Codigo string 8 |
| `CodString_9` | `Int` | - | `-` | Codigo string 9 |
| `CodString_10` | `Int` | - | `-` | Codigo string 10 |
| `CodString_11` | `Int` | - | `-` | Codigo string 11 |
| `CodString_12` | `Int` | - | `-` | Codigo string 12 |
| `CodString_13` | `Int` | - | `-` | Codigo string 13 |
| `CodString_14` | `Int` | - | `-` | Codigo string 14 |
| `CodString_15` | `Int` | - | `-` | Codigo string 15 |
| `Bool_1` | `Bool` | - | `-` | Valor booleano 1 |
| `Bool_2` | `Bool` | - | `-` | Valor booleano 2 |
| `Bool_3` | `Bool` | - | `-` | Valor booleano 3 |
| `Bool_4` | `Bool` | - | `-` | Valor booleano 4 |
| `Bool_5` | `Bool` | - | `-` | Valor booleano 5 |
| `Bool_6` | `Bool` | - | `-` | Valor booleano 6 |
| `Bool_7` | `Bool` | - | `-` | Valor booleano 7 |
| `Bool_8` | `Bool` | - | `-` | Valor booleano 8 |
| `Bool_9` | `Bool` | - | `-` | Valor booleano 9 |
| `Bool_10` | `Bool` | - | `-` | Valor booleano 10 |
| `Bool_11` | `Bool` | - | `-` | Valor booleano 11 |
| `Bool_12` | `Bool` | - | `-` | Valor booleano 12 |
| `Bool_13` | `Bool` | - | `-` | Valor booleano 13 |
| `Bool_14` | `Bool` | - | `-` | Valor booleano 14 |
| `Bool_15` | `Bool` | - | `-` | Valor booleano 15 |
| `Bool_16` | `Bool` | - | `-` | Valor booleano 16 |
| `Bool_17` | `Bool` | - | `-` | Valor booleano 17 |
| `Bool_18` | `Bool` | - | `-` | Valor booleano 18 |
| `Bool_19` | `Bool` | - | `-` | Valor booleano 19 |
| `Bool_20` | `Bool` | - | `-` | Valor booleano 20 |
| `Bool_21` | `Bool` | - | `-` | Valor booleano 21 |
| `Bool_22` | `Bool` | - | `-` | Valor booleano 22 |
| `Bool_23` | `Bool` | - | `-` | Valor booleano 23 |
| `Bool_24` | `Bool` | - | `-` | Valor booleano 24 |
| `Bool_25` | `Bool` | - | `-` | Valor booleano 25 |
| `Bool_26` | `Bool` | - | `-` | Valor booleano 26 |
| `Bool_27` | `Bool` | - | `-` | Valor booleano 27 |
| `Bool_28` | `Bool` | - | `-` | Valor booleano 28 |
| `Bool_29` | `Bool` | - | `-` | Valor booleano 29 |
| `Bool_30` | `Bool` | - | `-` | Valor booleano 30 |
| `Bool_31` | `Bool` | - | `-` | Valor booleano 31 |
| `Bool_32` | `Bool` | - | `-` | Valor booleano 32 |
| `Real_1` | `Real` | - | `-` | Valor real 1 |
| `Real_2` | `Real` | - | `-` | Valor real 2 |
| `Real_3` | `Real` | - | `-` | Valor real 3 |
| `Real_4` | `Real` | - | `-` | Valor real 4 |
| `Real_5` | `Real` | - | `-` | Valor real 5 |
| `Real_6` | `Real` | - | `-` | Valor real 6 |
| `Real_7` | `Real` | - | `-` | Valor real 7 |
| `Real_8` | `Real` | - | `-` | Valor real 8 |
| `Real_9` | `Real` | - | `-` | Valor real 9 |
| `Real_10` | `Real` | - | `-` | Valor real 10 |
| `Real_11` | `Real` | - | `-` | Valor real 11 |
| `Real_12` | `Real` | - | `-` | Valor real 12 |
| `Real_13` | `Real` | - | `-` | Valor real 13 |
| `Real_14` | `Real` | - | `-` | Valor real 14 |
| `Real_15` | `Real` | - | `-` | Valor real 15 |
| `Real_16` | `Real` | - | `-` | Valor real 16 |
| `Real_17` | `Real` | - | `-` | Valor real 17 |
| `Real_18` | `Real` | - | `-` | Valor real 18 |
| `Real_19` | `Real` | - | `-` | Valor real 19 |
| `Real_20` | `Real` | - | `-` | Valor real 20 |
| `Int_1` | `Int` | - | `-` | Valor entero 1 |
| `Int_2` | `Int` | - | `-` | Valor entero 2 |
| `Int_3` | `Int` | - | `-` | Valor entero 3 |
| `Int_4` | `Int` | - | `-` | Valor entero 4 |
| `Int_5` | `Int` | - | `-` | Valor entero 5 |
| `Int_6` | `Int` | - | `-` | Valor entero 6 |
| `Int_7` | `Int` | - | `-` | Valor entero 7 |
| `Int_8` | `Int` | - | `-` | Valor entero 8 |
| `Int_9` | `Int` | - | `-` | Valor entero 9 |
| `Int_10` | `Int` | - | `-` | Valor entero 10 |
| `Int_11` | `Int` | - | `-` | Valor entero 11 |
| `Int_12` | `Int` | - | `-` | Valor entero 12 |
| `Int_13` | `Int` | - | `-` | Valor entero 13 |
| `Int_14` | `Int` | - | `-` | Valor entero 14 |
| `Int_15` | `Int` | - | `-` | Valor entero 15 |
| `Int_16` | `Int` | - | `-` | Valor entero 16 |
| `Int_17` | `Int` | - | `-` | Valor entero 17 |
| `Int_18` | `Int` | - | `-` | Valor entero 18 |
| `Int_19` | `Int` | - | `-` | Valor entero 19 |
| `Int_20` | `Int` | - | `-` | Valor entero 20 |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `t_dummy` | `Int` | - | `-` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC12_ZC_INFORME_REGISTRO" : Void
TITLE = FC12_ZC_INFORME_REGISTRO
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para almacenar una traza en el buffer de informes
   VAR_INPUT 
      Registrar : USInt;   // Orden registrar (0= no registrar / 1= registrar)
      Tipo : Int;   // Tipo
      Codigo : String;   // Codigo produccion
      Fecha_1_Ano : UInt;   // Fecha 1  Año
      Fecha_1_Mes : USInt;   // Fecha 1  Mes
      Fecha_1_Dia : USInt;   // Fecha 1  Dia
      Fecha_1_DiaSemana : USInt;   // Fecha 1  Dia de la semana
      Fecha_1_Hora : USInt;   // Fecha 1  Hora
      Fecha_1_Minuto : USInt;   // Fecha 1  Minuto
      Fecha_1_Segundo : USInt;   // Fecha 1  Segundo
      Fecha_1_NanoSegundo : UDInt;   // Fecha 1  Nanosegundo
      Fecha_2_Ano : UInt;   // Fecha 2 Año
      Fecha_2_Mes : USInt;   // Fecha 2 Mes
      Fecha_2_Dia : USInt;   // Fecha 2 Dia
      Fecha_2_DiaSemana : USInt;   // Fecha 2 Dia de la semana
      Fecha_2_Hora : USInt;   // Fecha 2 Hora
      Fecha_2_Minuto : USInt;   // Fecha 2 Minuto
      Fecha_2_Segundo : USInt;   // Fecha 2 Segundo
      Fecha_2_NanoSegundo : UDInt;   // Fecha 2 Nanosegundo
      Fecha_3_Ano : UInt;   // Fecha 3 Año
      Fecha_3_Mes : USInt;   // Fecha 3 Mes
      Fecha_3_Dia : USInt;   // Fecha 3 Dia
      Fecha_3_DiaSemana : USInt;   // Fecha 3 Dia de la semana
      Fecha_3_Hora : USInt;   // Fecha 3 Hora
      Fecha_3_Minuto : USInt;   // Fecha 3 Minuto
      Fecha_3_Segundo : USInt;   // Fecha 3 Segundo
      Fecha_3_NanoSegundo : UDInt;   // Fecha 3 Nanosegundo
      Fecha_4_Ano : UInt;   // Fecha 4 Año
      Fecha_4_Mes : USInt;   // Fecha 4 Mes
      Fecha_4_Dia : USInt;   // Fecha 4 Dia
      Fecha_4_DiaSemana : USInt;   // Fecha 4 Dia de la semana
      Fecha_4_Hora : USInt;   // Fecha 4 Hora
      Fecha_4_Minuto : USInt;   // Fecha 4 Minuto
      Fecha_4_Segundo : USInt;   // Fecha 4 Segundo
      Fecha_4_NanoSegundo : UDInt;   // Fecha 4 Nanosegundo
      CodString_1 : Int;   // Codigo string 1
      CodString_2 : Int;   // Codigo string 2
      CodString_3 : Int;   // Codigo string 3
      CodString_4 : Int;   // Codigo string 4
      CodString_5 : Int;   // Codigo string 5
      CodString_6 : Int;   // Codigo string 6
      CodString_7 : Int;   // Codigo string 7
      CodString_8 : Int;   // Codigo string 8
      CodString_9 : Int;   // Codigo string 9
      CodString_10 : Int;   // Codigo string 10
      CodString_11 : Int;   // Codigo string 11
      CodString_12 : Int;   // Codigo string 12
      CodString_13 : Int;   // Codigo string 13
      CodString_14 : Int;   // Codigo string 14
      CodString_15 : Int;   // Codigo string 15
      Bool_1 : Bool;   // Valor booleano 1
      Bool_2 : Bool;   // Valor booleano 2
      Bool_3 : Bool;   // Valor booleano 3
      Bool_4 : Bool;   // Valor booleano 4
      Bool_5 : Bool;   // Valor booleano 5
      Bool_6 : Bool;   // Valor booleano 6
      Bool_7 : Bool;   // Valor booleano 7
      Bool_8 : Bool;   // Valor booleano 8
      Bool_9 : Bool;   // Valor booleano 9
      Bool_10 : Bool;   // Valor booleano 10
      Bool_11 : Bool;   // Valor booleano 11
      Bool_12 : Bool;   // Valor booleano 12
      Bool_13 : Bool;   // Valor booleano 13
      Bool_14 : Bool;   // Valor booleano 14
      Bool_15 : Bool;   // Valor booleano 15
      Bool_16 : Bool;   // Valor booleano 16
      Bool_17 : Bool;   // Valor booleano 17
      Bool_18 : Bool;   // Valor booleano 18
      Bool_19 : Bool;   // Valor booleano 19
      Bool_20 : Bool;   // Valor booleano 20
      Bool_21 : Bool;   // Valor booleano 21
      Bool_22 : Bool;   // Valor booleano 22
      Bool_23 : Bool;   // Valor booleano 23
      Bool_24 : Bool;   // Valor booleano 24
      Bool_25 : Bool;   // Valor booleano 25
      Bool_26 : Bool;   // Valor booleano 26
      Bool_27 : Bool;   // Valor booleano 27
      Bool_28 : Bool;   // Valor booleano 28
      Bool_29 : Bool;   // Valor booleano 29
      Bool_30 : Bool;   // Valor booleano 30
      Bool_31 : Bool;   // Valor booleano 31
      Bool_32 : Bool;   // Valor booleano 32
      Real_1 : Real;   // Valor real 1
      Real_2 : Real;   // Valor real 2
      Real_3 : Real;   // Valor real 3
      Real_4 : Real;   // Valor real 4
      Real_5 : Real;   // Valor real 5
      Real_6 : Real;   // Valor real 6
      Real_7 : Real;   // Valor real 7
      Real_8 : Real;   // Valor real 8
      Real_9 : Real;   // Valor real 9
      Real_10 : Real;   // Valor real 10
      Real_11 : Real;   // Valor real 11
      Real_12 : Real;   // Valor real 12
      Real_13 : Real;   // Valor real 13
      Real_14 : Real;   // Valor real 14
      Real_15 : Real;   // Valor real 15
      Real_16 : Real;   // Valor real 16
      Real_17 : Real;   // Valor real 17
      Real_18 : Real;   // Valor real 18
      Real_19 : Real;   // Valor real 19
      Real_20 : Real;   // Valor real 20
      Int_1 : Int;   // Valor entero 1
      Int_2 : Int;   // Valor entero 2
      Int_3 : Int;   // Valor entero 3
      Int_4 : Int;   // Valor entero 4
      Int_5 : Int;   // Valor entero 5
      Int_6 : Int;   // Valor entero 6
      Int_7 : Int;   // Valor entero 7
      Int_8 : Int;   // Valor entero 8
      Int_9 : Int;   // Valor entero 9
      Int_10 : Int;   // Valor entero 10
      Int_11 : Int;   // Valor entero 11
      Int_12 : Int;   // Valor entero 12
      Int_13 : Int;   // Valor entero 13
      Int_14 : Int;   // Valor entero 14
      Int_15 : Int;   // Valor entero 15
      Int_16 : Int;   // Valor entero 16
      Int_17 : Int;   // Valor entero 17
      Int_18 : Int;   // Valor entero 18
      Int_19 : Int;   // Valor entero 19
      Int_20 : Int;   // Valor entero 20
   END_VAR

   VAR_TEMP 
      t_dummy : Int;
      t_fecha_vacia {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2024 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función para el almacenamiento y estructuración masiva de registros de trazabilidad dentro del buffer de informes del sistema.
	
	En ella se realizan las siguientes acciones:
	
	- Comprobación de habilitación: Verificación de la variable de permiso `HabilitacionGeneral`; si no se encuentra activa, se omite la ejecución del bloque mediante un retorno anticipado.
	- Desplazamiento de datos (FIFO):
	    - Ejecución de la instrucción de bloque para desplazar todos los registros existentes en el Buffer una posición hacia abajo.
	    - Liberación del índice 0 del array para permitir la inserción del nuevo registro sin sobrescribir el histórico reciente.
	- Gestión e inserción del nuevo registro:
	        - Generación y asignación de un identificador único (Id) transformando la fecha y hora actual del sistema a formato cadena.
	        - Escritura de los metadatos de control y catalogación (Registrar, Tipo, Codigo) en la primera posición del buffer.
	        - Procesamiento y validación de hasta 4 marcas de tiempo dinámicas (Fecha_1 a Fecha_4), forzando una fecha por defecto (01/01/1970) si el año recibido es 0.
	        - Mapeo y transferencia masiva de todas las variables de proceso vinculadas al evento, incluyendo cadenas de texto (CodString_1 a 15), booleanos (Bool_1 a 32), reales (Real_1 a 20) y enteros (Int_1 a 20).
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | - |
	| FB   | - |
	| DB   | - |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 01.00.01 | 30.07.2024 | (ABH)   | Primera version. |
	| 01.00.02 | 11.09.2024 | (ABH)   | Se elimina la generacion de ID, para que lo genere el gestor. |
	| 01.00.03 | 06.11.2025 | (ABH)   | Fix escritura de hora si año seleccionado es 0. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION COMPROBACION_HABILITACION
	    
	    //  Si no esta habilitado los informes, salimos de la funcion.
	    IF NOT "DB11_INFORMES".Gestion.HabilitacionGeneral THEN
	        RETURN;
	    END_IF;
	    
	END_REGION COMPROBACION_HABILITACION
	
	
	//  ==========================================================================================================
	REGION DESPLAZAMIENTO_DE_DATOS
	    
	    //  Desplazamos los datos del buffer una posicion hacia abajo
	    #t_dummy := MOVE_BLK_VARIANT(SRC := "DB11_INFORMES".Buffer, COUNT := INT_TO_UDINT(("N_MAX_INF_BUFFER")), SRC_INDEX := 0, DEST_INDEX := 1, DEST => "DB11_INFORMES".Buffer);
	    
	END_REGION DESPLAZAMIENTO_DE_DATOS
	
	
	//  ==========================================================================================================
	REGION GESTION_REGISTRO_INFORME
	    
	    //  Grabamos el nuevo registro
	    "DB11_INFORMES".Buffer[0].Registrar := #Registrar;
	    "DB11_INFORMES".Buffer[0].Id := "FC15006_ZC_DTL_TO_STRING"(FechaDTL := "DB1_SYS".FechaHoraActual, Formato := 3);
	    "DB11_INFORMES".Buffer[0].Tipo := #Tipo;
	    "DB11_INFORMES".Buffer[0].Codigo := #Codigo;
	    IF #Fecha_1_Ano = 0 THEN
	        "DB11_INFORMES".Buffer[0].Fecha_1.Ano := 1970;
	        "DB11_INFORMES".Buffer[0].Fecha_1.Mes := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_1.Dia := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_1.DiaSemana := 5;
	    ELSE
	        "DB11_INFORMES".Buffer[0].Fecha_1.Ano := #Fecha_1_Ano;
	        "DB11_INFORMES".Buffer[0].Fecha_1.Mes := #Fecha_1_Mes;
	        "DB11_INFORMES".Buffer[0].Fecha_1.Dia := #Fecha_1_Dia;
	        "DB11_INFORMES".Buffer[0].Fecha_1.DiaSemana := #Fecha_1_DiaSemana;
	    END_IF;
	    "DB11_INFORMES".Buffer[0].Fecha_1.Hora := #Fecha_1_Hora;
	    "DB11_INFORMES".Buffer[0].Fecha_1.Minuto := #Fecha_1_Minuto;
	    "DB11_INFORMES".Buffer[0].Fecha_1.Segundo := #Fecha_1_Segundo;
	    "DB11_INFORMES".Buffer[0].Fecha_1.NanoSegundo := #Fecha_1_NanoSegundo;
	    IF #Fecha_2_Ano = 0 THEN
	        "DB11_INFORMES".Buffer[0].Fecha_2.Ano := 1970;
	        "DB11_INFORMES".Buffer[0].Fecha_2.Mes := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_2.Dia := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_2.DiaSemana := 5;
	    ELSE
	        "DB11_INFORMES".Buffer[0].Fecha_2.Ano := #Fecha_2_Ano;
	        "DB11_INFORMES".Buffer[0].Fecha_2.Mes := #Fecha_2_Mes;
	        "DB11_INFORMES".Buffer[0].Fecha_2.Dia := #Fecha_2_Dia;
	        "DB11_INFORMES".Buffer[0].Fecha_2.DiaSemana := #Fecha_2_DiaSemana;
	    END_IF;
	    "DB11_INFORMES".Buffer[0].Fecha_2.Hora := #Fecha_2_Hora;
	    "DB11_INFORMES".Buffer[0].Fecha_2.Minuto := #Fecha_2_Minuto;
	    "DB11_INFORMES".Buffer[0].Fecha_2.Segundo := #Fecha_2_Segundo;
	    "DB11_INFORMES".Buffer[0].Fecha_2.NanoSegundo := #Fecha_2_NanoSegundo;
	    IF #Fecha_3_Ano = 0 THEN
	        "DB11_INFORMES".Buffer[0].Fecha_3.Ano := 1970;
	        "DB11_INFORMES".Buffer[0].Fecha_3.Mes := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_3.Dia := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_3.DiaSemana := 5;
	    ELSE
	        "DB11_INFORMES".Buffer[0].Fecha_3.Ano := #Fecha_3_Ano;
	        "DB11_INFORMES".Buffer[0].Fecha_3.Mes := #Fecha_3_Mes;
	        "DB11_INFORMES".Buffer[0].Fecha_3.Dia := #Fecha_3_Dia;
	        "DB11_INFORMES".Buffer[0].Fecha_3.DiaSemana := #Fecha_3_DiaSemana;
	    END_IF;
	    IF #Fecha_4_Ano = 0 THEN
	        "DB11_INFORMES".Buffer[0].Fecha_4.Ano := 1970;
	        "DB11_INFORMES".Buffer[0].Fecha_4.Mes := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_4.Dia := 1;
	        "DB11_INFORMES".Buffer[0].Fecha_4.DiaSemana := 5;
	    ELSE
	        "DB11_INFORMES".Buffer[0].Fecha_4.Ano := #Fecha_4_Ano;
	        "DB11_INFORMES".Buffer[0].Fecha_4.Mes := #Fecha_4_Mes;
	        "DB11_INFORMES".Buffer[0].Fecha_4.Dia := #Fecha_4_Dia;
	        "DB11_INFORMES".Buffer[0].Fecha_4.DiaSemana := #Fecha_4_DiaSemana;
	    END_IF;
	    "DB11_INFORMES".Buffer[0].Fecha_3.Hora := #Fecha_3_Hora;
	    "DB11_INFORMES".Buffer[0].Fecha_3.Minuto := #Fecha_3_Minuto;
	    "DB11_INFORMES".Buffer[0].Fecha_3.Segundo := #Fecha_3_Segundo;
	    "DB11_INFORMES".Buffer[0].Fecha_3.NanoSegundo := #Fecha_3_NanoSegundo;
	    "DB11_INFORMES".Buffer[0].CodString_1 := #CodString_1;
	    "DB11_INFORMES".Buffer[0].CodString_2 := #CodString_2;
	    "DB11_INFORMES".Buffer[0].CodString_3 := #CodString_3;
	    "DB11_INFORMES".Buffer[0].CodString_4 := #CodString_4;
	    "DB11_INFORMES".Buffer[0].CodString_5 := #CodString_5;
	    "DB11_INFORMES".Buffer[0].CodString_6 := #CodString_6;
	    "DB11_INFORMES".Buffer[0].CodString_7 := #CodString_7;
	    "DB11_INFORMES".Buffer[0].CodString_8 := #CodString_8;
	    "DB11_INFORMES".Buffer[0].CodString_9 := #CodString_9;
	    "DB11_INFORMES".Buffer[0].CodString_10 := #CodString_10;
	    "DB11_INFORMES".Buffer[0].CodString_11 := #CodString_11;
	    "DB11_INFORMES".Buffer[0].CodString_12 := #CodString_12;
	    "DB11_INFORMES".Buffer[0].CodString_13 := #CodString_13;
	    "DB11_INFORMES".Buffer[0].CodString_14 := #CodString_14;
	    "DB11_INFORMES".Buffer[0].CodString_15 := #CodString_15;
	    "DB11_INFORMES".Buffer[0].Bool_1 := #Bool_1;
	    "DB11_INFORMES".Buffer[0].Bool_2 := #Bool_2;
	    "DB11_INFORMES".Buffer[0].Bool_3 := #Bool_3;
	    "DB11_INFORMES".Buffer[0].Bool_4 := #Bool_4;
	    "DB11_INFORMES".Buffer[0].Bool_5 := #Bool_5;
	    "DB11_INFORMES".Buffer[0].Bool_6 := #Bool_6;
	    "DB11_INFORMES".Buffer[0].Bool_7 := #Bool_7;
	    "DB11_INFORMES".Buffer[0].Bool_8 := #Bool_8;
	    "DB11_INFORMES".Buffer[0].Bool_9 := #Bool_9;
	    "DB11_INFORMES".Buffer[0].Bool_10 := #Bool_10;
	    "DB11_INFORMES".Buffer[0].Bool_11 := #Bool_11;
	    "DB11_INFORMES".Buffer[0].Bool_12 := #Bool_12;
	    "DB11_INFORMES".Buffer[0].Bool_13 := #Bool_13;
	    "DB11_INFORMES".Buffer[0].Bool_14 := #Bool_14;
	    "DB11_INFORMES".Buffer[0].Bool_15 := #Bool_15;
	    "DB11_INFORMES".Buffer[0].Bool_16 := #Bool_16;
	    "DB11_INFORMES".Buffer[0].Bool_17 := #Bool_17;
	    "DB11_INFORMES".Buffer[0].Bool_18 := #Bool_18;
	    "DB11_INFORMES".Buffer[0].Bool_19 := #Bool_19;
	    "DB11_INFORMES".Buffer[0].Bool_20 := #Bool_20;
	    "DB11_INFORMES".Buffer[0].Bool_21 := #Bool_21;
	    "DB11_INFORMES".Buffer[0].Bool_22 := #Bool_22;
	    "DB11_INFORMES".Buffer[0].Bool_23 := #Bool_23;
	    "DB11_INFORMES".Buffer[0].Bool_24 := #Bool_24;
	    "DB11_INFORMES".Buffer[0].Bool_25 := #Bool_25;
	    "DB11_INFORMES".Buffer[0].Bool_26 := #Bool_26;
	    "DB11_INFORMES".Buffer[0].Bool_27 := #Bool_27;
	    "DB11_INFORMES".Buffer[0].Bool_28 := #Bool_28;
	    "DB11_INFORMES".Buffer[0].Bool_29 := #Bool_29;
	    "DB11_INFORMES".Buffer[0].Bool_30 := #Bool_30;
	    "DB11_INFORMES".Buffer[0].Bool_31 := #Bool_31;
	    "DB11_INFORMES".Buffer[0].Bool_32 := #Bool_32;
	    "DB11_INFORMES".Buffer[0].Real_1 := #Real_1;
	    "DB11_INFORMES".Buffer[0].Real_2 := #Real_2;
	    "DB11_INFORMES".Buffer[0].Real_3 := #Real_3;
	    "DB11_INFORMES".Buffer[0].Real_4 := #Real_4;
	    "DB11_INFORMES".Buffer[0].Real_5 := #Real_5;
	    "DB11_INFORMES".Buffer[0].Real_6 := #Real_6;
	    "DB11_INFORMES".Buffer[0].Real_7 := #Real_7;
	    "DB11_INFORMES".Buffer[0].Real_8 := #Real_8;
	    "DB11_INFORMES".Buffer[0].Real_9 := #Real_9;
	    "DB11_INFORMES".Buffer[0].Real_10 := #Real_10;
	    "DB11_INFORMES".Buffer[0].Real_11 := #Real_11;
	    "DB11_INFORMES".Buffer[0].Real_12 := #Real_12;
	    "DB11_INFORMES".Buffer[0].Real_13 := #Real_13;
	    "DB11_INFORMES".Buffer[0].Real_14 := #Real_14;
	    "DB11_INFORMES".Buffer[0].Real_15 := #Real_15;
	    "DB11_INFORMES".Buffer[0].Real_16 := #Real_16;
	    "DB11_INFORMES".Buffer[0].Real_17 := #Real_17;
	    "DB11_INFORMES".Buffer[0].Real_18 := #Real_18;
	    "DB11_INFORMES".Buffer[0].Real_19 := #Real_19;
	    "DB11_INFORMES".Buffer[0].Real_20 := #Real_20;
	    "DB11_INFORMES".Buffer[0].Int_1 := #Int_1;
	    "DB11_INFORMES".Buffer[0].Int_2 := #Int_2;
	    "DB11_INFORMES".Buffer[0].Int_3 := #Int_3;
	    "DB11_INFORMES".Buffer[0].Int_4 := #Int_4;
	    "DB11_INFORMES".Buffer[0].Int_5 := #Int_5;
	    "DB11_INFORMES".Buffer[0].Int_6 := #Int_6;
	    "DB11_INFORMES".Buffer[0].Int_7 := #Int_7;
	    "DB11_INFORMES".Buffer[0].Int_8 := #Int_8;
	    "DB11_INFORMES".Buffer[0].Int_9 := #Int_9;
	    "DB11_INFORMES".Buffer[0].Int_10 := #Int_10;
	    "DB11_INFORMES".Buffer[0].Int_11 := #Int_11;
	    "DB11_INFORMES".Buffer[0].Int_12 := #Int_12;
	    "DB11_INFORMES".Buffer[0].Int_13 := #Int_13;
	    "DB11_INFORMES".Buffer[0].Int_14 := #Int_14;
	    "DB11_INFORMES".Buffer[0].Int_15 := #Int_15;
	    "DB11_INFORMES".Buffer[0].Int_16 := #Int_16;
	    "DB11_INFORMES".Buffer[0].Int_17 := #Int_17;
	    "DB11_INFORMES".Buffer[0].Int_18 := #Int_18;
	    "DB11_INFORMES".Buffer[0].Int_19 := #Int_19;
	    "DB11_INFORMES".Buffer[0].Int_20 := #Int_20;
	    
	END_REGION GESTION_REGISTRO_INFORME
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>