---
title: FC20_SINCRONIZAR_FECHA_SCADA
---
# FC FC20_SINCRONIZAR_FECHA_SCADA

!!! info "Información del Sistema"
    **Hardware:** -<br>
    **Ingeniería:** -<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC20_SINCRONIZAR_FECHA_SCADA" : Void
TITLE = FC20_SINCRONIZAR_FECHA_SCADA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0

BEGIN
	(* 
	=============================================================================
	ZEUS CONTROL, S.A.
	 (c)Copyright (2024) All Rights Reserved
	 -----------------------------------------------------------------------------
	
	 Software:        TIA Portal 18
	 Restricciones:   PLC serie 1200/1500
	
	
	 Nombre:         SINCRONIZAR FECHA SCADA
	 Descripcion:    Funcion para sincronizacion de fecha desde SCADA
	 
	 Dependencias:
	    FC:         -
	    FB:         -
	    DB:         -
	    UDT:        -
	
	 Change log:
	 Version     Fecha       Tecnico a cargo
	
	    Version     Fecha       Tecnico a cargo     Observaciones
	    
	    01.00.00    15.17.2024  (ABH)               Primera version.
	   
	
	// =============================================================================
	*)
	
	
	IF "DB20_SINCRONIZAR_FECHA".Sincronizar THEN
	    "DB20_SINCRONIZAR_FECHA".RET_VAL := WR_LOC_T(LOCTIME := "DB20_SINCRONIZAR_FECHA".FechaHora, DST := TRUE);
	    "DB20_SINCRONIZAR_FECHA".Sincronizar := FALSE;
	END_IF;
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>