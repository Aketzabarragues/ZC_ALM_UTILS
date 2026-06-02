---
title: FC15_ZC_GEST_PREAL
---
# FC FC15_ZC_GEST_PREAL

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! warning "Restricciones"
    DB Optimizado.

## Descripción Funcional
Función principal para la gestión de trazabilidad de los parámetros **reales** del proceso. 
    
    Su objetivo principal es detectar cambios de valor en el array de parámetros y lanzar un registro de traza cuando esto sucede.
    
    El bloque opera de la siguiente manera:
    
        1. Calcula dinámicamente los límites superior e inferior del array de entrada.
        2. Si es el primer ciclo de ejecución de la CPU, inicializa los valores "anteriores" con los valores "actuales" para evitar falsos registros de traza iniciales.
        3. En ciclos normales, compara el valor actual de cada parámetro con su valor guardado en el ciclo anterior.
        4. Si detecta una diferencia, llama a la función `FC8_ZC_TRAZA_REGISTRO` para registrar el cambio y actualiza el valor anterior.

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **DB:** [UDT_ZC_PREAL](../Estructura de datos/UDT_ZC_PREAL.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `PrimerCiclo` | `Bool` | - | `-` | Marca de primer ciclo de arranque de la CPU |
| `FechaHora` | `DTL` | - | `-` | Fecha y hora actual |
| `Usuario` | `String` | - | `-` | Usuario actual |
| `PReal` | `Array[*] of UDT_ZC_PREAL` | - | `-` | Array de parametro real |
| `IndexTraza` | `Int` | - | `-` | Indice de texto parametro para trazabilidad |

### Entrada/Salida
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `ValorAnterior` | `Array[*] of Real` | - | `-` | Array de valores anteriores |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `DInt` | - | `-` | Variable para bucles FOR |
| `t_IndiceSuperior` | `DInt` | - | `-` | Indice superior del array |
| `t_IndiceInferior` | `DInt` | - | `-` | Indice inferior del array |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15_ZC_GEST_PREAL" : Void
TITLE = FC15_ZC_GEST_PREAL
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
   VAR_INPUT 
      PrimerCiclo : Bool;   // Marca de primer ciclo de arranque de la CPU
      FechaHora {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
      Usuario : String;   // Usuario actual
      PReal : Array[*] of "UDT_ZC_PREAL";   // Array de parametro real
      IndexTraza : Int;   // Indice de texto parametro para trazabilidad
   END_VAR

   VAR_IN_OUT 
      ValorAnterior : Array[*] of Real;   // Array de valores anteriores
   END_VAR

   VAR_TEMP 
      for_i : DInt;   // Variable para bucles FOR
      t_IndiceSuperior : DInt;   // Indice superior del array
      t_IndiceInferior : DInt;   // Indice inferior del array
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2026 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** DB Optimizado.
	
	---
	### Descripción Funcional
	
	Función principal para la gestión de trazabilidad de los parámetros **reales** del proceso. 
	
	Su objetivo principal es detectar cambios de valor en el array de parámetros y lanzar un registro de traza cuando esto sucede.
	
	El bloque opera de la siguiente manera:
	
	    1. Calcula dinámicamente los límites superior e inferior del array de entrada.
	    2. Si es el primer ciclo de ejecución de la CPU, inicializa los valores "anteriores" con los valores "actuales" para evitar falsos registros de traza iniciales.
	    3. En ciclos normales, compara el valor actual de cada parámetro con su valor guardado en el ciclo anterior.
	    4. Si detecta una diferencia, llama a la función `FC8_ZC_TRAZA_REGISTRO` para registrar el cambio y actualiza el valor anterior.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC8_ZC_TRAZA_REGISTRO` |
	| FB   | - |
	| DB   | - |
	| UDT  | `UDT_ZC_PREAL` |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 01.00.00 | 2026-03-20 | (ABH) | Primera version. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION CALCULO_LIMITES_ARRAY
	    
	    //  Calculo de los limites del array, ya que la entrada del array de parametros es variable.
	    #t_IndiceInferior := LOWER_BOUND(ARR := #PReal, DIM := 1);
	    #t_IndiceSuperior := UPPER_BOUND(ARR := #PReal, DIM := 1);
	    
	END_REGION CALCULO_LIMITES_ARRAY
	
	
	//  ==========================================================================================================
	REGION PRIMER_ARRANQUE
	    
	    //  En el primer arranque de la CPU, recorremos el array completo y almacenamos los valores actuales como valores anteriores en el arranque de la CPU.
	    //  Esto se realiza ya que los valores anteriores no son remanentes, para optimizar la memoria del PLC.
	    IF #PrimerCiclo THEN
	        
	        FOR #for_i := #t_IndiceInferior TO #t_IndiceSuperior DO
	            #ValorAnterior[#for_i] := #PReal[#for_i].Valor;
	        END_FOR;
	        
	        //  Salimos inmediatamente de la funcion, para realizar la gestion de los parametros con la CPU arrancada
	        RETURN;
	        
	    END_IF;
	    
	END_REGION PRIMER_ARRANQUE
	
	
	//  ==========================================================================================================
	REGION GESTION_PARAMETROS
	    
	    //  Gestion de los cambios de valor de los parametros. Si detecta un cambio, lanza la traza
	    //  y actualiza el valor anterior.
	    FOR #for_i := #t_IndiceInferior TO #t_IndiceSuperior DO
	        
	        //  En caso de detectar cambio de valor
	        IF #PReal[#for_i].Valor <> #ValorAnterior[#for_i] THEN
	            
	            //  Lanzamos la trazabilidad
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHora,
	                                    Registrar := 1,
	                                    Categoria := "TRZ_CAT_25_PREAL",
	                                    User := #Usuario,
	                                    CodInt_1 := #IndexTraza + DINT_TO_INT(#for_i),
	                                    CodInt_2 := "TRZ_SYS_PAR_VAL_ANT",
	                                    CodInt_3 := "TRZ_SYS_PAR_VAL_NUE",
	                                    CodInt_4:= 0,
	                                    CodInt_5:= 0,
	                                    CodReal_1 := #ValorAnterior[#for_i],
	                                    CodReal_2 := #PReal[#for_i].Valor);
	            
	            //  Actualizamos el valor anterior
	            #ValorAnterior[#for_i] := #PReal[#for_i].Valor;
	            
	        END_IF;
	        
	    END_FOR;
	    
	END_REGION GESTION_PARAMETROS
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>