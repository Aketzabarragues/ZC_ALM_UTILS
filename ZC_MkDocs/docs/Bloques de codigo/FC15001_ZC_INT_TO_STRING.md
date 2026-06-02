---
title: FC15001_ZC_INT_TO_STRING
---
# FC FC15001_ZC_INT_TO_STRING

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
| `Valor` | `Int` | - | `-` | Valor INT |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15001_ZC_INT_TO_STRING" : String
TITLE = FC15001_ZC_INT_TO_STRING
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para convertir INT a STRING
   VAR_INPUT 
      Valor : Int;   // Valor INT
   END_VAR


BEGIN
	(*  
	ZEUS CONTROL, S.A.
	(c)Copyright (2023) All Rights Reserved
	--------------------------------------------------------------------------------------
	
	Software:       TIA Portal 16
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC1018_ZC_INT_TO_STRING
	Descripcion:    Funcion para conversion de INT a STRING
	
	Dependencias:
	    FC:         -
	    FB:         -
	    DB:         -
	    UDT:        -
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    15.03.2023  (ABH)               Primera version. 
	    
	    
	//=====================================================================================
	*)
	
	#FC15001_ZC_INT_TO_STRING := DELETE(IN := INT_TO_STRING(#Valor), L := 1, P := 1);
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>