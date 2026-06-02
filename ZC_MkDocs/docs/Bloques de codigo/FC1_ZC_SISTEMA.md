---
title: FC1_ZC_SISTEMA
---
# FC FC1_ZC_SISTEMA

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 2.0<br>
    **Autor:** HCR

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función central para la gestión de marcas de sistema, temporizaciones generales, usuarios y resets del sistema. 
    
    En ella se realizan las siguientes acciones:
    
    - Cálculo dinámico del tiempo de ciclo del OB1 (en milisegundos) evaluando la variable auxiliar con la instrucción RUNTIME. 
    - Tratamiento y registro de trazabilidad de los 10 pulsadores de acuse de alarmas y del pulsador de modificación de fecha/hora mediante la función FC15026_ZC_PULSADOR. 
    - Consolidación del acuse general (ACK), agrupando las activaciones del PLC de todos los pulsadores de reconocimiento en una única marca. 
    - Generación de marcas estáticas (ON fijo y OFF fijo) y captura del primer ciclo de escáner tras el arranque. 
    - Creación de pulsos temporizados (100 ms, 1 s, 2 s, 5 s, 1 min, 1 h) y señales Flip-Flop a partir de las marcas de ciclo del hardware de la CPU. 
    - Lectura constante de la fecha y hora local (RD_LOC_T) y ejecución de la escritura en el sistema (WR_SYS_T) ante una orden del HMI. 
    - Escaneo continuo de las órdenes de selección para determinar y fijar el usuario actualmente activo en el sistema. 
    - Ejecución bajo demanda del reset general del array de entidades (solo aplicable con procesos parados), reinicializando sus variables a estados de disponibilidad, limpieza y vacío. 
    - Llamada a la rutina DB3_CHECKSUM para la validación y gestión de la suma de comprobación del programa.

!!! abstract "Dependencias Requeridas"
    **FC:** [FC15026_ZC_PULSADOR](../Bloques de codigo/FC15026_ZC_PULSADOR.md)
    **FC:** [FB3_ZC_CHECKSUM](../Bloques de codigo/FB3_ZC_CHECKSUM.md)
    **DB:** [DB1_SYS](../Estructura de datos/DB1_SYS.md)
    **DB:** [DB3_CHECKSUM](../Estructura de datos/DB3_CHECKSUM.md)
    **DB:** [DB6_ENTIDAD](../Estructura de datos/DB6_ENTIDAD.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `CPU_MarcasCiclo` | `Byte` | - | `-` | Byte Marca de ciclo CPU |
| `CPU_MarcasSistema` | `Byte` | - | `-` | Byte Marcas de sistema |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | Variable para bucles FOR |
| `t_RetVal` | `Int` | - | `-` | Variable temporal para su uso en programa |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC1_ZC_SISTEMA" : Void
TITLE = FC1_ZC_SISTEMA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : HCR
FAMILY : ZeusControl
VERSION : 2.0
//Funcion para gestion de marcas de sistema
   VAR_INPUT 
      CPU_MarcasCiclo : Byte;   // Byte Marca de ciclo CPU
      CPU_MarcasSistema : Byte;   // Byte Marcas de sistema
   END_VAR

   VAR_TEMP 
      for_i : Int;   // Variable para bucles FOR
      t_RetVal : Int;   // Variable temporal para su uso en programa
   END_VAR


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
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función central para la gestión de marcas de sistema, temporizaciones generales, usuarios y resets del sistema. 
	
	En ella se realizan las siguientes acciones:
	
	- Cálculo dinámico del tiempo de ciclo del OB1 (en milisegundos) evaluando la variable auxiliar con la instrucción RUNTIME. 
	- Tratamiento y registro de trazabilidad de los 10 pulsadores de acuse de alarmas y del pulsador de modificación de fecha/hora mediante la función FC15026_ZC_PULSADOR. 
	- Consolidación del acuse general (ACK), agrupando las activaciones del PLC de todos los pulsadores de reconocimiento en una única marca. 
	- Generación de marcas estáticas (ON fijo y OFF fijo) y captura del primer ciclo de escáner tras el arranque. 
	- Creación de pulsos temporizados (100 ms, 1 s, 2 s, 5 s, 1 min, 1 h) y señales Flip-Flop a partir de las marcas de ciclo del hardware de la CPU. 
	- Lectura constante de la fecha y hora local (RD_LOC_T) y ejecución de la escritura en el sistema (WR_SYS_T) ante una orden del HMI. 
	- Escaneo continuo de las órdenes de selección para determinar y fijar el usuario actualmente activo en el sistema. 
	- Ejecución bajo demanda del reset general del array de entidades (solo aplicable con procesos parados), reinicializando sus variables a estados de disponibilidad, limpieza y vacío. 
	- Llamada a la rutina DB3_CHECKSUM para la validación y gestión de la suma de comprobación del programa. 
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC15026_ZC_PULSADOR` |
	| FB   | `FB3_ZC_CHECKSUM` |
	| DB   | `DB1_SYS`, `DB3_CHECKSUM`, `DB6_ENTIDAD` |
	| UDT  | - |
	
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	|01.00.00  | 03.11.2022 | (HCR)   | Primera version. |
	|01.00.01  | 02.06.2023 | (ABH)   | Optimizacion de bloque para integrar en libreria. Se eliminan marcas no utilizadas. Se reorganizan las variables y se ponen bien los comentarios. |
	|01.00.02  | 24.04.2025 | (HCR)   | Se añade gestion de idioma. |
	|01.00.03  | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	|02.00.00  | 25.03.2026 | (ABH)   | Se cambia lenguaje a SCL. Se eliminan idiomas. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION TIEMPO_DE_CICLO
	    
	    //  Se almacena el tiempo de ciclo del OB1
	    "DB1_SYS".TiempoCiclo := LREAL_TO_REAL(RUNTIME("DB1_SYS".Aux.auxRuntime));
	    "DB1_SYS".TiempoCiclo := ("DB1_SYS".TiempoCiclo * 1000.0);
	    
	END_REGION TIEMPO_DE_CICLO
	
	
	//  ==========================================================================================================
	REGION GESTION_PULSADORES
	    
	    //  Gestion pulsadores de ack
	    "DB1_SYS".Pulsador.Ack[0].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_01",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[0]);
	    
	    "DB1_SYS".Pulsador.Ack[1].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_02",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[1]);
	    
	    "DB1_SYS".Pulsador.Ack[2].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_03",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[2]);
	    
	    "DB1_SYS".Pulsador.Ack[3].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_04",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[3]);
	    
	    "DB1_SYS".Pulsador.Ack[4].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_05",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[4]);
	    
	    "DB1_SYS".Pulsador.Ack[5].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_06",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[5]);
	    
	    "DB1_SYS".Pulsador.Ack[6].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_07",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[6]);
	    
	    "DB1_SYS".Pulsador.Ack[7].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_08",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[7]);
	    
	    "DB1_SYS".Pulsador.Ack[8].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_09",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[8]);
	    
	    "DB1_SYS".Pulsador.Ack[9].Permiso := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_ACK_10",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.Ack[9]);
	    
	    //  Gestion pulsador cambio de fecha y hora
	    "DB1_SYS".Pulsador.EscribirFechaHora.Permiso := TRUE;
	    "DB1_SYS".Pulsador.EscribirFechaHora.Visibilidad := TRUE;
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := "DB1_SYS".Pulso1seg,
	                          SP_Tiempo := 0,
	                          TrazaCategoria := "TRZ_CAT_1_SYS",
	                          TrazaIdProceso := 0,
	                          TrazaIdPulsador := "TRZ_SYS_PUL_FECHA",
	                          Usuario := "DB1_SYS".Usuario.Actual,
	                          FechaHoraActual := "DB1_SYS".FechaHoraActual,
	                          Pulsador := "DB1_SYS".Pulsador.EscribirFechaHora);
	    
	END_REGION GESTION_PULSADORES
	
	
	//  ==========================================================================================================
	REGION GESTION_ACUSE_GENERAL
	    
	    //  Activacion de marca de acuse general
	    "DB1_SYS".ACK :=
	    "DB1_SYS".Pulsador.Ack[0].Plc OR
	    "DB1_SYS".Pulsador.Ack[1].Plc OR
	    "DB1_SYS".Pulsador.Ack[2].Plc OR
	    "DB1_SYS".Pulsador.Ack[3].Plc OR
	    "DB1_SYS".Pulsador.Ack[4].Plc OR
	    "DB1_SYS".Pulsador.Ack[5].Plc OR
	    "DB1_SYS".Pulsador.Ack[6].Plc OR
	    "DB1_SYS".Pulsador.Ack[7].Plc OR
	    "DB1_SYS".Pulsador.Ack[8].Plc OR
	    "DB1_SYS".Pulsador.Ack[9].Plc;
	    
	END_REGION GESTION_ACUSE_GENERAL
	
	
	//  ==========================================================================================================
	REGION GESTION_MARCAS_GENERALES_Y_FLANCOS
	    
	    
	    //  ==========================================================================================================
	    //  Marca siempre a ON
	    "DB1_SYS".OFF := FALSE;
	    
	    //  Marca siempre a OFF
	    "DB1_SYS".ON := TRUE;
	    
	    //  Marca primer arranque
	    "DB1_SYS".ARRANQUE := #CPU_MarcasSistema.%X0;
	    
	    //  ==========================================================================================================
	    //  Pulso por 100 ms
	    "DB1_SYS".Pulso100ms := #CPU_MarcasCiclo.%X0 AND NOT "DB1_SYS".Aux.P_Trig_Pulso100ms;
	    
	    //  Pulso por 1 segundo
	    "DB1_SYS".Pulso1seg := #CPU_MarcasCiclo.%X5 AND NOT "DB1_SYS".Aux.P_Trig_Pulso1Seg;
	    
	    //  Pulso por 2 segundos
	    "DB1_SYS".Pulso2seg := FALSE;
	    IF "DB1_SYS".Pulso1seg THEN
	        "DB1_SYS".Aux.Contador2seg += 1;
	        IF "DB1_SYS".Aux.Contador2seg >= 2 THEN
	            "DB1_SYS".Pulso2seg := TRUE;
	            "DB1_SYS".Aux.Contador2seg := 0;
	        END_IF;
	    END_IF;
	    
	    //  Pulso por 5 segundos
	    "DB1_SYS".Pulso5seg := FALSE;
	    IF "DB1_SYS".Pulso1seg THEN
	        "DB1_SYS".Aux.Contador5seg += 1;
	        IF "DB1_SYS".Aux.Contador5seg >= 5 THEN
	            "DB1_SYS".Pulso5seg := TRUE;
	            "DB1_SYS".Aux.Contador5seg := 0;
	        END_IF;
	    END_IF;
	    
	    //  Pulso por 1 minuto
	    "DB1_SYS".Pulso1min := FALSE;
	    IF "DB1_SYS".Pulso1seg THEN
	        "DB1_SYS".Aux.Contador1min += 1;
	        IF "DB1_SYS".Aux.Contador1min >= 60 THEN
	            "DB1_SYS".Pulso1min := TRUE;
	            "DB1_SYS".Aux.Contador1min := 0;
	        END_IF;
	    END_IF;
	    
	    //  Pulso por 1 hora
	    "DB1_SYS".Pulso1h := FALSE;
	    IF "DB1_SYS".Pulso1seg THEN
	        "DB1_SYS".Aux.Contador1h += 1;
	        IF "DB1_SYS".Aux.Contador1h >= 3600 THEN
	            "DB1_SYS".Pulso1h := TRUE;
	            "DB1_SYS".Aux.Contador1h := 0;
	        END_IF;
	    END_IF;
	    
	    //  ==========================================================================================================
	    //  Flip Flop 1 segundo
	    IF "DB1_SYS".Pulso1seg AND NOT "DB1_SYS".FlipFlop1seg THEN
	        "DB1_SYS".FlipFlop1seg := TRUE;
	    ELSIF "DB1_SYS".Pulso1seg AND "DB1_SYS".FlipFlop1seg THEN
	        "DB1_SYS".FlipFlop1seg := FALSE;
	    END_IF;
	    
	    //  Flip Flop 2 segundos
	    IF "DB1_SYS".Pulso2seg AND NOT "DB1_SYS".FlipFlop2seg THEN
	        "DB1_SYS".FlipFlop2seg := TRUE;
	    ELSIF "DB1_SYS".Pulso2seg AND "DB1_SYS".FlipFlop2seg THEN
	        "DB1_SYS".FlipFlop2seg := FALSE;
	    END_IF;
	    
	    //  Flip Flop 5 segundos
	    IF "DB1_SYS".Pulso5seg AND NOT "DB1_SYS".FlipFlop5seg THEN
	        "DB1_SYS".FlipFlop5seg := TRUE;
	    ELSIF "DB1_SYS".Pulso5seg AND "DB1_SYS".FlipFlop5seg THEN
	        "DB1_SYS".FlipFlop5seg := FALSE;
	    END_IF;
	    
	    //  ==========================================================================================================
	    //  Estados anteriores
	    "DB1_SYS".Aux.P_Trig_Pulso100ms := #CPU_MarcasCiclo.%X0;
	    "DB1_SYS".Aux.P_Trig_Pulso1Seg := #CPU_MarcasCiclo.%X5;
	    
	END_REGION GESTION_MARCAS_GENERALES_Y_FLANCOS
	
	
	//  ==========================================================================================================
	REGION FECHA_Y_HORA
	    
	    //  Lectura de fecha y hora actual
	    #t_RetVal := RD_LOC_T("DB1_SYS".FechaHoraActual);
	    
	    //  Escritura de fecha y hora nueva
	    IF "DB1_SYS".Pulsador.EscribirFechaHora.Plc THEN
	        #t_RetVal := WR_SYS_T("DB1_SYS".FechaHoraNueva);
	    END_IF;
	    
	END_REGION FECHA_Y_HORA
	
	
	//  ==========================================================================================================
	REGION USUARIOS
	    
	    //  Gestion de usuario actual para trazas
	    FOR #for_i := 0 TO 9 DO
	        IF "DB1_SYS".Usuario.Seleccion[#for_i].Orden THEN
	            "DB1_SYS".Usuario.Actual := "DB1_SYS".Usuario.Seleccion[#for_i].Usuario;
	            "DB1_SYS".Usuario.Seleccion[#for_i].Orden := FALSE;
	            EXIT;
	        END_IF;
	    END_FOR;
	    
	END_REGION USUARIOS
	
	
	//  ==========================================================================================================
	REGION RESET_ENTIDADES
	    
	    //  Reset todas las entidades
	    //  CUIDADO!!!!!!!!
	    //          TIENEN QUE ESTAR TODOS LOS PROCESOS PARADOS!!!!!!
	    IF "DB1_SYS".ResetEntidades THEN
	        FOR #for_i := 1 TO "N_MAX_ENTIDAD" DO
	            
	            "DB6_ENTIDAD".ENT[#for_i].Estado.EnProduccion :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.EnCIP :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.EnSIP :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.ConProducto :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.ConAgua :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.Vacia :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.Sucia := FALSE;
	            
	            "DB6_ENTIDAD".ENT[#for_i].Habilitar :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.Disponible :=
	            "DB6_ENTIDAD".ENT[#for_i].Estado.Limpia := TRUE;
	            
	            "DB6_ENTIDAD".ENT[#for_i].Estado.CodEstado := 0;
	            "DB6_ENTIDAD".ENT[#for_i].Asignacion := 0;
	            
	            "DB6_ENTIDAD".ENT[#for_i].ID := #for_i;
	            
	        END_FOR;
	        
	        "DB1_SYS".ResetEntidades := FALSE;
	    END_IF;
	    
	END_REGION USUARIOS
	
	
	//  ==========================================================================================================
	REGION CHECKSUM
	    
	    //  Gestion de checksum del programa
	    "DB3_CHECKSUM"();
	    
	END_REGION USUARIOS
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>