---
title: FC8_ZC_TRAZA_REGISTRO
---
# FC FC8_ZC_TRAZA_REGISTRO

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función encargada de almacenar de forma secuencial un nuevo evento de trazabilidad dentro del buffer de registros.
    
    Las tareas que realiza son las siguientes:
    
    - Verifica que la gestión general de trazabilidad se encuentre habilitada en el sistema.
    - Desplaza el contenido actual del buffer de trazas una posición hacia abajo mediante la instrucción `MOVE_BLK_VARIANT`, liberando el primer índice.
    - Convierte la marca de tiempo de entrada (formato `DTL`) a una cadena de texto (`String`) haciendo uso de la función `FC15006_ZC_DTL_TO_STRING`.
    - Almacena los parámetros del nuevo registro (orden de registrar, marca de tiempo, categoría, códigos numéricos enteros y reales) en la posición inicial (índice 0) del buffer.
    - Valida la cadena de caracteres correspondiente al usuario: si se encuentra vacía, registra una cadena de espacios por defecto; en caso contrario, asigna el nombre de usuario proporcionado en la entrada.

!!! abstract "Dependencias Requeridas"
    **FC:** [FC15006_ZC_DTL_TO_STRING](../Bloques de codigo/FC15006_ZC_DTL_TO_STRING.md)
    **DB:** [DB7_TRAZA](../Estructura de datos/DB7_TRAZA.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `FechaHora` | `DTL` | - | `-` | Fecha y hora actual |
| `Registrar` | `USInt` | - | `-` | Registrar trazabilidad |
| `Categoria` | `Int` | - | `-` | Categoria de trazabilidad |
| `User` | `String` | - | `-` | Usuario actual |
| `CodInt_1` | `Int` | - | `-` | Codigo entero 1 |
| `CodInt_2` | `Int` | - | `-` | Codigo entero 2 |
| `CodInt_3` | `Int` | - | `-` | Codigo entero 3 |
| `CodInt_4` | `Int` | - | `-` | Codigo entero 4 |
| `CodInt_5` | `Int` | - | `-` | Codigo entero 5 |
| `CodReal_1` | `Real` | - | `-` | Codigo real 1 |
| `CodReal_2` | `Real` | - | `-` | Codigo real 2 |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `t_dummy` | `Int` | - | `-` | Variable temporal para su uso en programa |
| `t_TimeStamp` | `String[25]` | - | `-` | Fecha y hora actual en formato String |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC8_ZC_TRAZA_REGISTRO" : Void
TITLE = FC8_TRAZA_REGISTRO
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para almacenar una traza en el buffer de trazas.
   VAR_INPUT 
      FechaHora {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
      Registrar : USInt;   // Registrar trazabilidad
      Categoria : Int;   // Categoria de trazabilidad
      User : String;   // Usuario actual
      CodInt_1 : Int;   // Codigo entero 1
      CodInt_2 : Int;   // Codigo entero 2
      CodInt_3 : Int;   // Codigo entero 3
      CodInt_4 : Int;   // Codigo entero 4
      CodInt_5 : Int;   // Codigo entero 5
      CodReal_1 : Real;   // Codigo real 1
      CodReal_2 : Real;   // Codigo real 2
   END_VAR

   VAR_TEMP 
      t_dummy : Int;   // Variable temporal para su uso en programa
      t_TimeStamp : String[25];   // Fecha y hora actual en formato String
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2022 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función encargada de almacenar de forma secuencial un nuevo evento de trazabilidad dentro del buffer de registros.
	
	Las tareas que realiza son las siguientes:
	
	- Verifica que la gestión general de trazabilidad se encuentre habilitada en el sistema.
	- Desplaza el contenido actual del buffer de trazas una posición hacia abajo mediante la instrucción `MOVE_BLK_VARIANT`, liberando el primer índice.
	- Convierte la marca de tiempo de entrada (formato `DTL`) a una cadena de texto (`String`) haciendo uso de la función `FC15006_ZC_DTL_TO_STRING`.
	- Almacena los parámetros del nuevo registro (orden de registrar, marca de tiempo, categoría, códigos numéricos enteros y reales) en la posición inicial (índice 0) del buffer.
	- Valida la cadena de caracteres correspondiente al usuario: si se encuentra vacía, registra una cadena de espacios por defecto; en caso contrario, asigna el nombre de usuario proporcionado en la entrada.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC15006_ZC_DTL_TO_STRING` |
	| FB   | - |
	| DB   | `DB7_TRAZA` |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.01 | 31.08.2022 | (ABH)   | Primera version. |
	| 01.00.00 | 25.03.2026 | (ABH)   | Se añade datos nuevos de UDT. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION GESTION_REGISTRO_TRAZA
	    
	    //  Si la trazabilidad esta habilitada
	    IF "DB7_TRAZA".Gestion.HabilitacionGeneral THEN
	        
	        //  Desplazamos los datos una posicion hacia abajo
	        #t_dummy := MOVE_BLK_VARIANT(SRC := "DB7_TRAZA".Buffer, COUNT := INT_TO_UDINT((30)), SRC_INDEX := 0, DEST_INDEX := 1, DEST => "DB7_TRAZA".Buffer);
	        
	        //  Convertimos la fecha y hora actual a String
	        #t_TimeStamp := "FC15006_ZC_DTL_TO_STRING"(FechaDTL := #FechaHora,
	                                                   Formato := 0);
	        
	        //  Guardamos el nuevo registro en la primera posicion
	        "DB7_TRAZA".Buffer[0].Registrar := #Registrar;
	        "DB7_TRAZA".Buffer[0].TimeStamp := #t_TimeStamp;
	        "DB7_TRAZA".Buffer[0].Categoria := #Categoria;
	        "DB7_TRAZA".Buffer[0].CodInt_1 := #CodInt_1;
	        "DB7_TRAZA".Buffer[0].CodInt_2 := #CodInt_2;
	        "DB7_TRAZA".Buffer[0].CodInt_3 := #CodInt_3;
	        "DB7_TRAZA".Buffer[0].CodInt_4 := #CodInt_4;
	        "DB7_TRAZA".Buffer[0].CodInt_5 := #CodInt_5;
	        "DB7_TRAZA".Buffer[0].CodReal_1 := #CodReal_1;
	        "DB7_TRAZA".Buffer[0].CodReal_2 := #CodReal_2;
	        IF #User = '' THEN
	            "DB7_TRAZA".Buffer[0].User := '    ';
	        ELSE
	            "DB7_TRAZA".Buffer[0].User := #User;
	        END_IF;
	        
	    END_IF;
	    
	END_REGION GESTION_REGISTRO_TRAZA
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>