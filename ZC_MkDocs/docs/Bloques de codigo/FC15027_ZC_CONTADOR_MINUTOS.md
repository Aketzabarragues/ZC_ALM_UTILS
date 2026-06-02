---
title: FC15027_ZC_CONTADOR_MINUTOS
---
# FC FC15027_ZC_CONTADOR_MINUTOS

!!! info "Información del Sistema"
    **Hardware:** -<br>
    **Ingeniería:** -<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

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
| `Contador` | `UDT_ZC_CONTADOR_MINUTOS` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `MAX_MINUTOS` | `UDInt` | - | `10000000` | Valor maximo de minutos |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15027_ZC_CONTADOR_MINUTOS" : Void
TITLE = FC15027_ZC_CONTADOR_MINUTOS
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion contador de minutos
   VAR_INPUT 
      Pulso1seg : Bool;   // Pulso de 1 segundo
      Iniciar : Bool;   // Orden iniciar contador
      Reset : Bool;   // Reset contador
   END_VAR

   VAR_IN_OUT 
      Contador : "UDT_ZC_CONTADOR_MINUTOS";
   END_VAR

   VAR CONSTANT 
      MAX_MINUTOS : UDInt := 10000000;   // Valor maximo de minutos
   END_VAR


BEGIN
	(*  
	ZEUS CONTROL, S.A.
	(c)Copyright (2024) All Rights Reserved
	-----------------------------------------------------------------------------
	
	Software:       TIA Portal 18
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC15027_ZC_CONTADOR_MINUTOS
	Descripcion:    Funcion contador de minutos.
	
	Dependencias:
	    FC:         -
	    FB:         -
	    DB:         -
	    UDT:        ZC_CONTADOR_MINUTOS
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    13.05.2024  (ABH)               Primera version
	    
	//=====================================================================================
	*)
	
	
	REGION RESET_CONTADOR  
	    
	    IF #Reset OR #Contador.Minuto >= #MAX_MINUTOS THEN
	        #Contador.Minuto := #Contador.Segundo := 0;
	    END_IF;
	    
	END_REGION
	
	
	REGION GESTION_CONTADOR
	    
	    IF #Iniciar AND #Pulso1seg THEN
	        #Contador.#Segundo += 1;
	        IF #Contador.#Segundo >= 60 THEN
	            #Contador.#Segundo := 0;
	            #Contador.#Minuto += 1;
	        END_IF;
	    END_IF;
	    
	END_REGION
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>