---
title: FC15025_ZC_CONTADOR_TIEMPO
---
# FC FC15025_ZC_CONTADOR_TIEMPO

!!! info "Información del Sistema"
    **Hardware:** -<br>
    **Ingeniería:** -<br>
    **Versión:** 1.0<br>
    **Autor:** HCR

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1seg` | `Bool` | - | `-` | Pulso de 1 segundo |
| `Iniciar` | `Bool` | - | `-` | Orden iniciar contador |
| `Reset` | `Bool` | - | `-` | Reset contador |

### Entrada/Salida
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Contador` | `UDT_ZC_CONTADOR_TIEMPO` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `MAX_HORAS` | `UDInt` | - | `10000000` | Valor maximo de horas |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15025_ZC_CONTADOR_TIEMPO" : Void
TITLE = FC15025_ZC_CONTADOR_TIEMPO
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : HCR
FAMILY : ZeusControl
VERSION : 1.0
//Funcion contador de tiempo
   VAR_INPUT 
      Pulso1seg : Bool;   // Pulso de 1 segundo
      Iniciar : Bool;   // Orden iniciar contador
      Reset : Bool;   // Reset contador
   END_VAR

   VAR_IN_OUT 
      Contador : "UDT_ZC_CONTADOR_TIEMPO";
   END_VAR

   VAR CONSTANT 
      MAX_HORAS : UDInt := 10000000;   // Valor maximo de horas
   END_VAR


BEGIN
	(*  
	ZEUS CONTROL, S.A.
	(c)Copyright (2023) All Rights Reserved
	-----------------------------------------------------------------------------
	
	Software:       TIA Portal 15.1
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC15025_ZC_CONTADOR_TIEMPO
	Descripcion:    Funcion contador de tiempo.
	
	Dependencias:
	    FC:         -
	    FB:         -
	    DB:         -
	    UDT:        ZC_CONTADOR_TIEMPO
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    16.03.2023  (HCR)               Primera version
	    01.00.01    25.07.2023  (HCR)               Se añade valor maximo DINT para limitar contador horas. En caso de alcanzar valor maximo,
	                                                se resetea el contador de horas.
	    
	//=====================================================================================
	*)
	
	
	REGION RESET_CONTADOR  
	    
	    IF #Reset OR #Contador.Hora >= #MAX_HORAS THEN
	        #Contador.Hora := #Contador.Minuto := #Contador.Segundo := 0;
	    END_IF;
	    
	END_REGION
	
	
	REGION GESTION_CONTADOR
	    
	    IF #Iniciar AND #Pulso1seg THEN
	        #Contador.#Segundo += 1;
	        IF #Contador.#Segundo >= 60 THEN
	            #Contador.#Segundo := 0;
	            #Contador.#Minuto += 1;
	            IF #Contador.#Minuto >= 60 THEN
	                #Contador.#Minuto := 0;
	                #Contador.Hora += 1;
	            END_IF;
	        END_IF;
	    END_IF;
	    
	END_REGION
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>