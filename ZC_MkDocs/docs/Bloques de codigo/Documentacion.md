---
title: Documentacion
---
# FC Documentacion

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 0.1<br>
    **Autor:** -

!!! warning "Restricciones"
    [!!! INDICA AQUÍ LIMITACIONES (O ESCRIBE "Ninguna") !!!]

## Descripción Funcional
[!!! ESCRIBE AQUÍ UN RESUMEN BREVE DEL BLOQUE (1 O 2 LÍNEAS) !!!]
    
    [!!! EXPLICA AQUÍ LOS DETALLES TÉCNICOS. POR EJEMPLO: !!!]
    A nivel secuencial, la función realiza las siguientes tareas: 
    
    - Tarea principal 1, destacando el uso de la entrada `NombreVariable`.
    - Tarea principal 2 evaluando el estado de **En Marcha**.
      - Condición secundaria o sub-tarea (usando dos espacios antes del guion).

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "Documentacion" : Void
{ S7_Optimized_Access := 'TRUE' }
VERSION : 0.1

BEGIN
	
	
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2020 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** [!!! INDICA AQUÍ LIMITACIONES (O ESCRIBE "Ninguna") !!!]
	
	---
	### Descripción Funcional
	[!!! ESCRIBE AQUÍ UN RESUMEN BREVE DEL BLOQUE (1 O 2 LÍNEAS) !!!]
	
	[!!! EXPLICA AQUÍ LOS DETALLES TÉCNICOS. POR EJEMPLO: !!!]
	A nivel secuencial, la función realiza las siguientes tareas: 
	
	- Tarea principal 1, destacando el uso de la entrada `NombreVariable`.
	- Tarea principal 2 evaluando el estado de **En Marcha**.
	  - Condición secundaria o sub-tarea (usando dos espacios antes del guion).
	
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
	| 00.00.01 | DD.MM.YYYY | (ZC)    | Primera versión. |
	
	*)
	END_REGION DESCRIPCION
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>