---
title: FC4_ZC_DISPONIBILIDAD_ENTIDAD
---
# FC FC4_ZC_DISPONIBILIDAD_ENTIDAD

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función encargada de evaluar y determinar la disponibilidad operativa de las entidades del sistema.
    
    Las tareas que realiza son las siguientes:
    
    - Calcular el estado de disponibilidad de la entidad correspondiente en función del valor recibido en la entrada `Entidad`.
    - Verificar y restringir, por motivos de seguridad, el valor de la entrada `Entidad` para garantizar que no exceda los límites definidos en el array de entidades.

!!! abstract "Dependencias Requeridas"
    **FC:** [FC4_ZC_DISPONIBILIDAD_ENTIDAD](../Bloques de codigo/FC4_ZC_DISPONIBILIDAD_ENTIDAD.md)
    **DB:** [DB6_ENTIDAD](../Estructura de datos/DB6_ENTIDAD.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Entidad` | `Int` | - | `-` | Numero de entidad a gestionar |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC4_ZC_DISPONIBILIDAD_ENTIDAD" : Bool
TITLE = FC4_ZC_DISPONIBILIDAD_ENTIDAD
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para comprobar disponibilidad de las entidades.
   VAR_INPUT 
      Entidad : Int;   // Numero de entidad a gestionar
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2025 - 2025
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función encargada de evaluar y determinar la disponibilidad operativa de las entidades del sistema.
	
	Las tareas que realiza son las siguientes:
	
	- Calcular el estado de disponibilidad de la entidad correspondiente en función del valor recibido en la entrada `Entidad`.
	- Verificar y restringir, por motivos de seguridad, el valor de la entrada `Entidad` para garantizar que no exceda los límites definidos en el array de entidades.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC4_ZC_DISPONIBILIDAD_ENTIDAD` |
	| FB   | - |
	| DB   | `DB6_ENTIDAD` |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 01.00.00 | 14.03.2025 | (ABH)   | Primera version. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION GESTION_DISPONIBILIDAD
	    
	    //  Comprobacion de limites de la entrada Entidad. En caso de estar fuera de indices, devolvemos un FALSE.
	    //  En caso de estar dentro de limites, devolvemos el estado de la entidad
	    IF #Entidad < 1 OR #Entidad > "N_MAX_ENTIDAD" THEN
	        #FC4_ZC_DISPONIBILIDAD_ENTIDAD := FALSE;
	    ELSE
	        #FC4_ZC_DISPONIBILIDAD_ENTIDAD := "DB6_ENTIDAD".ENT[#Entidad].Estado.Disponible;
	    END_IF;
	    
	END_REGION GESTION_DISPONIBILIDAD 
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>