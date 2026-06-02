---
title: FC2000_ZC_ED
---
# FC FC2000_ZC_ED

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** HCR

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Entrada Digital.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se realiza la lectura de la entrada de manera indirecta si esta habilitada.
    - Se gestiona el estado del dispositivo
    - Se gestiona la trazabilidad de las manualizaciones del dispositivo

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **DB:** [DB2000_ED](../Estructura de datos/DB2000_ED.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1seg` | `Bool` | - | `-` | Pulso de 1 segundo |
| `Simulacion` | `Bool` | - | `-` | Simulacion |
| `Arranque` | `Bool` | - | `-` | Primer arranque |
| `UsuarioActual` | `String` | - | `-` | Usuario actual |
| `FechaHoraActual` | `DTL` | - | `-` | Fecha y hora actual |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |
| `for_mux` | `Int` | - | `-` | - |
| `t_oldIndex` | `Int` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TIPO_ACCESO_INDIRECTO` | `SInt` | - | `0` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2000_ZC_ED" : Void
TITLE = FC2000_ED
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : HCR
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo Entrada digital
   VAR_INPUT 
      Pulso1seg : Bool;   // Pulso de 1 segundo
      Simulacion : Bool;   // Simulacion
      Arranque : Bool;   // Primer arranque
      UsuarioActual : String;   // Usuario actual
      FechaHoraActual {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
   END_VAR

   VAR_TEMP 
      for_i : Int;
      for_mux_cambios : Int;
      for_mux : Int;
      t_Index : Int;
      t_oldIndex : Int;
   END_VAR

   VAR CONSTANT 
      TIPO_ACCESO_INDIRECTO : SInt := 0;
      TIPO_ACCESO_PLC : SInt := 1;
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
	
	Funcion para la gestion de dispositivo de tipo Entrada Digital.
	
	En ella se realizan las siguientes acciones:
	
	- Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
	- Se realiza la lectura de la entrada de manera indirecta si esta habilitada.
	- Se gestiona el estado del dispositivo
	- Se gestiona la trazabilidad de las manualizaciones del dispositivo
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC8_ZC_TRAZA_REGISTRO` |
	| FB   | - |
	| DB   | `DB2000_ED` |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.00 | 15.10.2020 | (ABH)   | Primera version. |
	| 00.00.01 | 26.04.2022 | (HCR)   | Cambio en la organizacion del UDT. Se organiza en estructuras en base al tipo de funcion que realizan los datos. |
	| 00.00.02 | 27.04.2022 | (ABH)   | Se añaden auxiliares de estado anterior del modo manual y automatico para poder registrar las trazas. |
	| 00.00.03 | 22.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado) |
	| 00.00.04 | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado. Se añade movimiento de SD[0] a multiplexado en caso de que el indice sea 0. |
	| 00.00.05 | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores. |
	| 00.00.06 | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro. |
	| 00.00.07 | 24.04.2025 | (HCR)   | Se añade gestion de idioma  |
	| 00.00.08 | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	| 00.00.09 | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT. Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision. |
	| 01.00.00 | 18.05.2026 | (ABH)   | Se añade variable `Config_TipoAcceso` para uso de direccionamiento indirecto o uso directo en PLC. |
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2000_ED".Mux[#for_mux].Index :=
	            "DB2000_ED".Mux[#for_mux].oldIndex := 0;
	        END_FOR;
	        RETURN;
	    END_IF;
	    
	    //  ===========================================================================================================
	    //  Gestion de multiplexado
	    FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	        
	        //  ===============================================================================================================
	        //  Antes de iniciar la logica del multiplexado, revisamos los limites
	        REGION LIMITES
	            
	            //  ===========================================================================================================
	            //  Limites
	            IF "DB2000_ED".Mux[#for_mux].Index < 0 THEN
	                "DB2000_ED".Mux[#for_mux].Index := 0;
	            END_IF;
	            IF "DB2000_ED".Mux[#for_mux].Index > "N_MAX_DISP_ED" THEN
	                "DB2000_ED".Mux[#for_mux].Index := "N_MAX_DISP_ED";
	            END_IF;
	            IF "DB2000_ED".Mux[#for_mux].Index >= "N_MAX_DISP_ED" THEN
	                "DB2000_ED".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2000_ED".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2000_ED".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2000_ED".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2000_ED".Mux[#for_mux].oldIndex := #t_Index;
	        
	        IF "DB2000_ED".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2000_ED".Mux[#for_mux].ED := "DB2000_ED".ED[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	                
	                
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2000_ED".Mux[#for_mux].ED.Hmi_Estado := "DB2000_ED".ED[#t_Index].Hmi_Estado;
	                    IF NOT "DB2000_ED".ED[#t_Index].Estado_AutoMan THEN
	                        "DB2000_ED".Mux[#for_mux].ED.Orden_ActivarManual := "DB2000_ED".ED[#t_Index].Orden_ActivarManual;
	                    END_IF;
	                    "DB2000_ED".Mux[#for_mux].ED.Estado_Activado := "DB2000_ED".ED[#t_Index].Estado_Activado;
	                    "DB2000_ED".Mux[#for_mux].ED.Estado_EntradaCanal := "DB2000_ED".ED[#t_Index].Estado_EntradaCanal;
	                    "DB2000_ED".Mux[#for_mux].ED.Aux_oldActivado := "DB2000_ED".ED[#t_Index].Aux_oldActivado;
	                    "DB2000_ED".Mux[#for_mux].ED.Aux_oldAutoMan := "DB2000_ED".ED[#t_Index].Aux_oldAutoMan;
	                    "DB2000_ED".Mux[#for_mux].ED.Tiempos_TiempoAct := "DB2000_ED".ED[#t_Index].Tiempos_TiempoAct;
	                    "DB2000_ED".Mux[#for_mux].ED.Tiempos_TiempoDes := "DB2000_ED".ED[#t_Index].Tiempos_TiempoDes;
	                    "DB2000_ED".Mux[#for_mux].ED.Config_GrupoAlarma := "DB2000_ED".ED[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2000_ED".Mux[#for_mux].ExisteCambio := false;
	                    
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2000_ED".Mux[#for_mux].ED.Estado_AutoMan <> "DB2000_ED".ED[#t_Index].Estado_AutoMan THEN
	                        "DB2000_ED".ED[#t_Index].Estado_AutoMan := "DB2000_ED".Mux[#for_mux].ED.Estado_AutoMan;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2000_ED".Mux[#for_mux].ED.Orden_ActivarManual <> "DB2000_ED".ED[#t_Index].Orden_ActivarManual THEN
	                        "DB2000_ED".ED[#t_Index].Orden_ActivarManual := "DB2000_ED".Mux[#for_mux].ED.Orden_ActivarManual;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_DirEntradaBit <> "DB2000_ED".ED[#t_Index].Config_DirEntradaBit THEN
	                        "DB2000_ED".ED[#t_Index].Config_DirEntradaBit := "DB2000_ED".Mux[#for_mux].ED.Config_DirEntradaBit;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_DirEntradaByte <> "DB2000_ED".ED[#t_Index].Config_DirEntradaByte THEN
	                        "DB2000_ED".ED[#t_Index].Config_DirEntradaByte := "DB2000_ED".Mux[#for_mux].ED.Config_DirEntradaByte;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_Habilitar <> "DB2000_ED".ED[#t_Index].Config_Habilitar THEN
	                        "DB2000_ED".ED[#t_Index].Config_Habilitar := "DB2000_ED".Mux[#for_mux].ED.Config_Habilitar;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_HabilitarInvertir <> "DB2000_ED".ED[#t_Index].Config_HabilitarInvertir THEN
	                        "DB2000_ED".ED[#t_Index].Config_HabilitarInvertir := "DB2000_ED".Mux[#for_mux].ED.Config_HabilitarInvertir;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_HabilitarRetardoAct <> "DB2000_ED".ED[#t_Index].Config_HabilitarRetardoAct THEN
	                        "DB2000_ED".ED[#t_Index].Config_HabilitarRetardoAct := "DB2000_ED".Mux[#for_mux].ED.Config_HabilitarRetardoAct;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_HabilitarRetardoDes <> "DB2000_ED".ED[#t_Index].Config_HabilitarRetardoDes THEN
	                        "DB2000_ED".ED[#t_Index].Config_HabilitarRetardoDes := "DB2000_ED".Mux[#for_mux].ED.Config_HabilitarRetardoDes;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2000_ED".Mux[#for_mux].ED.Config_TipoAcceso <> "DB2000_ED".ED[#t_Index].Config_TipoAcceso THEN
	                        "DB2000_ED".ED[#t_Index].Config_TipoAcceso := "DB2000_ED".Mux[#for_mux].ED.Config_TipoAcceso;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Tiempos
	                    IF "DB2000_ED".Mux[#for_mux].ED.Tiempos_SPTiempoAct <> "DB2000_ED".ED[#t_Index].Tiempos_SPTiempoAct THEN
	                        "DB2000_ED".ED[#t_Index].Tiempos_SPTiempoAct := "DB2000_ED".Mux[#for_mux].ED.Tiempos_SPTiempoAct;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    IF "DB2000_ED".Mux[#for_mux].ED.Tiempos_SPTiempoDes <> "DB2000_ED".ED[#t_Index].Tiempos_SPTiempoDes THEN
	                        "DB2000_ED".ED[#t_Index].Tiempos_SPTiempoDes := "DB2000_ED".Mux[#for_mux].ED.Tiempos_SPTiempoDes;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2000_ED".Mux[#for_mux].ExisteCambio THEN
	                        
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2000_ED".Mux[#for_mux_cambios].Index THEN
	                                    "DB2000_ED".Mux[#for_mux_cambios].ED := "DB2000_ED".ED[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2000_ED".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la ED[0] que no se usa para escribir el index.
	                "DB2000_ED".Mux[#for_mux].ED := "DB2000_ED".ED[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            //  Multiplexado no habilitado
	            "DB2000_ED".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2000_ED".Mux[#for_mux].Index :=
	            "DB2000_ED".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	        
	        
	    END_FOR;
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2000_ED".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2000_ED".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_ED" DO
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2000_ED".ED[#for_i].Config_Habilitar THEN
	            
	            REGION LIMITE_GRUPO_ALARMA
	                
	                IF "DB2000_ED".ED[#for_i].Config_GrupoAlarma < 0 THEN
	                    "DB2000_ED".ED[#for_i].Config_GrupoAlarma := 0;
	                END_IF;
	                IF "DB2000_ED".ED[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                    "DB2000_ED".ED[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	                END_IF;
	                
	            END_REGION LIMITE_GRUPO_ALARMA
	            
	            
	            REGION LECTURA_VALORES
	                
	                CASE "DB2000_ED".ED[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        IF "DB2000_ED".ED[#for_i].Config_DirEntradaByte >= 0 THEN
	                            (*
	                            AREA: Pueden seleccionarse las siguientes áreas: 
	                            16#81: Input, 
	                            16#82: Output, 
	                            16#83: Marcas, 
	                            16#84: DB, 
	                            16#1: Entrada de periferia (solo S7-1500)
	                            DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                            BYTEOFFSET: Dirección en la que se lee. Solo se utilizan los 16 bits menos significativos.*)
	                            "DB2000_ED".ED[#for_i].Estado_EntradaCanal := PEEK_BOOL(area := 16#81,
	                                                                                    dbNumber := 0,
	                                                                                    byteOffset := "DB2000_ED".ED[#for_i].Config_DirEntradaByte,
	                                                                                    bitOffset := "DB2000_ED".ED[#for_i].Config_DirEntradaBit);
	                            
	                            IF "DB2000_ED".ED[#for_i].Config_HabilitarInvertir THEN
	                                
	                                "DB2000_ED".ED[#for_i].Estado_EntradaCanal := NOT (PEEK_BOOL(area := 16#81,
	                                                                                             dbNumber := 0,
	                                                                                             byteOffset := "DB2000_ED".ED[#for_i].Config_DirEntradaByte,
	                                                                                             bitOffset := "DB2000_ED".ED[#for_i].Config_DirEntradaBit));
	                            END_IF;
	                            
	                        END_IF;
	                        
	                    #TIPO_ACCESO_PLC:
	                        ;
	                        
	                END_CASE;
	                
	            END_REGION LECTURA_VALORES
	            
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                //  MODO MANUAL
	                IF "DB2000_ED".ED[#for_i].Estado_AutoMan THEN
	                    
	                    "DB2000_ED".Agrup["DB2000_ED".ED[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    
	                    IF "DB2000_ED".ED[#for_i].Orden_ActivarManual THEN
	                        "DB2000_ED".ED[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2000_ED".ED[#for_i].Estado_Activado := FALSE;
	                        "DB2000_ED".ED[#for_i].Orden_ActivarManual := FALSE;
	                    END_IF;
	                    
	                ELSE
	                    "DB2000_ED".ED[#for_i].Orden_ActivarManual := "DB2000_ED".ED[#for_i].Estado_Activado;
	                END_IF;
	                
	            END_REGION MODOS_DE_TRABAJO
	            
	            
	            REGION ESTADO_DEL_DISPOSITIVO
	                
	                // =============================================================================
	                //  DETECTOR SIMULADO
	                IF #Simulacion THEN
	                    
	                    IF "DB2000_ED".ED[#for_i].Orden_ActivarManual THEN
	                        "DB2000_ED".ED[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2000_ED".ED[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                END_IF;
	                
	                
	                IF NOT "DB2000_ED".ED[#for_i].Estado_AutoMan AND NOT #Simulacion THEN
	                    
	                    // =============================================================================
	                    //  RETARDO A LA ACTIVACIÓN AUTOMÁTICO
	                    IF "DB2000_ED".ED[#for_i].Estado_EntradaCanal AND "DB2000_ED".ED[#for_i].Config_HabilitarRetardoAct THEN
	                        
	                        IF #Pulso1seg AND "DB2000_ED".ED[#for_i].Tiempos_TiempoAct < "DB2000_ED".ED[#for_i].Tiempos_SPTiempoAct THEN
	                            "DB2000_ED".ED[#for_i].Tiempos_TiempoAct += 1;
	                        END_IF;
	                        
	                        IF "DB2000_ED".ED[#for_i].Tiempos_TiempoAct >= "DB2000_ED".ED[#for_i].Tiempos_SPTiempoAct THEN
	                            "DB2000_ED".ED[#for_i].Estado_Activado := TRUE;
	                        END_IF;
	                        
	                    ELSIF "DB2000_ED".ED[#for_i].Estado_EntradaCanal THEN
	                        
	                        "DB2000_ED".ED[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2000_ED".ED[#for_i].Tiempos_TiempoAct := 0;
	                        
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  RETARDO A LA DESACTIVACIÓN AUTOMÁTICO
	                    IF NOT "DB2000_ED".ED[#for_i].Estado_EntradaCanal AND "DB2000_ED".ED[#for_i].Config_HabilitarRetardoDes THEN
	                        
	                        IF #Pulso1seg AND "DB2000_ED".ED[#for_i].Tiempos_TiempoDes < "DB2000_ED".ED[#for_i].Tiempos_SPTiempoDes THEN
	                            "DB2000_ED".ED[#for_i].Tiempos_TiempoDes += 1;
	                        END_IF;
	                        
	                        IF "DB2000_ED".ED[#for_i].Tiempos_TiempoDes >= "DB2000_ED".ED[#for_i].Tiempos_SPTiempoDes THEN
	                            "DB2000_ED".ED[#for_i].Estado_Activado := FALSE;
	                        END_IF;
	                        
	                    ELSIF NOT "DB2000_ED".ED[#for_i].Estado_EntradaCanal THEN
	                        
	                        "DB2000_ED".ED[#for_i].Estado_Activado := FALSE;
	                        
	                    ELSE
	                        
	                        "DB2000_ED".ED[#for_i].Tiempos_TiempoDes := 0;
	                        
	                    END_IF;
	                    
	                END_IF;
	                
	            END_REGION ESTADO_DEL_DISPOSITIVO
	            
	            
	            REGION TRAZABILIDAD_MANUALIZACION
	                
	                IF "DB2000_ED".ED[#for_i].Estado_AutoMan AND NOT "DB2000_ED".ED[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_10_DISP_ED",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_ED",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2000_ED".ED[#for_i].Estado_AutoMan AND "DB2000_ED".ED[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_10_DISP_ED",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_ED",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2000_ED".ED[#for_i].Estado_AutoMan AND "DB2000_ED".ED[#for_i].Estado_Activado AND NOT "DB2000_ED".ED[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_10_DISP_ED",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_ED",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_ON",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2000_ED".ED[#for_i].Estado_AutoMan AND NOT "DB2000_ED".ED[#for_i].Estado_Activado AND "DB2000_ED".ED[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_10_DISP_ED",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_ED",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_OFF",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                
	                
	            END_REGION TRAZABILIDAD_MANUALIZACION
	            
	            
	            // =============================================================================
	            // ESTADO ANTERIOR MANUAL/AUTOMÁTICO
	            "DB2000_ED".ED[#for_i].Aux_oldAutoMan := "DB2000_ED".ED[#for_i].Estado_AutoMan;
	            "DB2000_ED".ED[#for_i].Aux_oldActivado := "DB2000_ED".ED[#for_i].Estado_Activado;
	            
	        ELSE
	            
	            // =============================================================================
	            // DISPOSITIVO NO HABILITADO
	            // =============================================================================
	            "DB2000_ED".ED[#for_i].Estado_EntradaCanal := FALSE;
	            "DB2000_ED".ED[#for_i].Estado_Activado := FALSE;
	            "DB2000_ED".ED[#for_i].Tiempos_TiempoAct := 0;
	            "DB2000_ED".ED[#for_i].Tiempos_TiempoDes := 0;
	            
	        END_IF;
	        
	        REGION ESTADO_HMI
	            
	            // =============================================================================
	            //  ESTADO BITS PARA VISUALIZACION
	            //  Bit     0   Habilitacion
	            //  Bit     1   ManualAutomatico
	            //  Bit     2   Enclavado
	            //  Bit     3   Activado 1
	            //  Bit     4   Activado 2
	            //  Bit     5   Reserva
	            //  Bit     6   Reserva
	            //  Bit     7   Reserva
	            //  Bit     8   Alarma General
	            //  Bit     9   Alarma 1
	            //  Bit     10  Alarma 2
	            //  Bit     11  Alarma 3
	            //  Bit     12  Alarma 4
	            //  Bit     13  Alarma Mantenimiento
	            //  Bit     14  Reserva
	            //  Bit     15  Reserva
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X0 := "DB2000_ED".ED[#for_i].Config_Habilitar;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X1 := "DB2000_ED".ED[#for_i].Estado_AutoMan;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X2 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X3 := "DB2000_ED".ED[#for_i].Estado_Activado;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X4 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X8 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X9 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X10 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X13 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2000_ED".ED[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION ESTADO_HMI
	        
	    END_FOR;
	    
	END_REGION
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>