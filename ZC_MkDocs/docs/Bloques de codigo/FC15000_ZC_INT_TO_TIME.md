---
title: FC15000_ZC_INT_TO_TIME
---
# FC FC15000_ZC_INT_TO_TIME

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
| `Valor` | `Int` | - | `-` | Valor INT |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `BASE_TIEMPO` | `Int` | - | `1000` | Base de tiempo para conversion |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15000_ZC_INT_TO_TIME" : Time
TITLE = FC15000_ZC_INT_TO_TIME
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : HCR
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para conversion INT a TIME
   VAR_INPUT 
      Valor : Int;   // Valor INT
   END_VAR

   VAR CONSTANT 
      BASE_TIEMPO : Int := 1000;   // Base de tiempo para conversion
   END_VAR


BEGIN
	(*  
	ZEUS CONTROL, S.A.
	(c)Copyright (2023) All Rights Reserved
	--------------------------------------------------------------------------------------
	
	Software:       TIA Portal 15.1
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC15000_ZC_INT_TO_TIME
	Descripcion:    Funcion para conversion de INT a TIME
	
	Dependencias:
	    FC:         -
	    FB:         -
	    DB:         -
	    UDT:        -
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    10.05.2023  (HCR)               Primera versión 
	    
	    
	//=====================================================================================
	*)
	
	#FC15000_ZC_INT_TO_TIME := DINT_TO_TIME(IN := INT_TO_DINT(IN := #Valor)) * #BASE_TIEMPO;
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>