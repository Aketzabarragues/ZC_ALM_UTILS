---
title: FC2005_ZC_SD
---
# FC FC2005_ZC_SD

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Salida Digital.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se gestiona el estado del dispositivo
    - Se gestiona la orden de activacion y activacion retardada    
    - Se gestiona la trazabilidad de las manualizaciones del dispositivo

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1seg` | `Bool` | - | `-` | Pulso de 1 segundo |
| `Simulacion` | `Bool` | - | `-` | Simulacion |
| `Arranque` | `Bool` | - | `-` | Primer arranque |
| `Ack` | `Bool` | - | `-` | Acuse general |
| `SeguridadesOK` | `Bool` | - | `-` | Seguridades Ok |
| `UsuarioActual` | `String` | - | `-` | Usuario actual |
| `FechaHoraActual` | `DTL` | - | `-` | Fecha y hora actual |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |
| `for_mux` | `Int` | - | `-` | - |
| `t_oldIndex` | `Int` | - | `-` | - |
| `t_ActivarConRetardo` | `Bool` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TIPO_ACCESO_INDIRECTO` | `SInt` | - | `0` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2005_ZC_SD" : Void
TITLE = FC2005_SD
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo salida digital
   VAR_INPUT 
      Pulso1seg : Bool;   // Pulso de 1 segundo
      Simulacion : Bool;   // Simulacion
      Arranque : Bool;   // Primer arranque
      Ack : Bool;   // Acuse general
      SeguridadesOK : Bool;   // Seguridades Ok
      UsuarioActual : String;   // Usuario actual
      FechaHoraActual {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
   END_VAR

   VAR_TEMP 
      for_i : Int;
      for_mux_cambios : Int;
      for_mux : Int;
      t_Index : Int;
      t_oldIndex : Int;
      t_Activar : Bool;
      t_ActivarConRetardo : Bool;
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
	
	Funcion para la gestion de dispositivo de tipo Salida Digital.
	
	En ella se realizan las siguientes acciones:
	
	- Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
	- Se gestiona el estado del dispositivo
	- Se gestiona la orden de activacion y activacion retardada    
	- Se gestiona la trazabilidad de las manualizaciones del dispositivo
	
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
	| 00.00.01 | 26.04.2022 | (HCR)   | Primera version. Cambio en la organizacion del UDT. Se organiza en estructuras en base al tipo de funcion que realizan los datos. |
	| 00.00.02 | 27.04.2022 | (ABH)   | Se añaden auxiliares de estado anterior del modo manual y automatico para poder registrar las trazas. |
	| 00.00.03 | 08.11.2022 | (ABH)   | Se añade trazabilidad manualizaciones |
	| 00.00.03 | 08.11.2022 | (HCR)   | Se añade trazabilidad de activación manual |
	| 00.00.04 | 20.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado) |
	| 00.00.05 | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado Se añade movimiento de ED[0] a multiplexado en caso de que el indice sea 0.  |
	| 00.00.07 | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores. |
	| 00.00.08 | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro. |
	| 00.00.09 | 24.04.2025 | (HCR)   | Se añade gestion de idioma |
	| 00.00.10 | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	| 00.00.11 | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision. |
	| 00.00.12 | 14.05.2026 | (ABH)   | Se modifica UDT para añadir tipo de lectura. |
	| 01.00.00 | 18.05.2026 | (ABH)   | Se añade variable `Config_TipoAcceso` para uso de direccionamiento indirecto o uso directo en PLC. |
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2005_SD".Mux[#for_mux].Index :=
	            "DB2005_SD".Mux[#for_mux].oldIndex := 0;
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
	            IF "DB2005_SD".Mux[#for_mux].Index > "N_MAX_DISP_SD" THEN
	                "DB2005_SD".Mux[#for_mux].Index := "N_MAX_DISP_SD";
	            END_IF;
	            IF "DB2005_SD".Mux[#for_mux].Index >= "N_MAX_DISP_SD" THEN
	                "DB2005_SD".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2005_SD".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2005_SD".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2005_SD".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2005_SD".Mux[#for_mux].oldIndex := #t_Index;
	        
	        IF "DB2005_SD".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2005_SD".Mux[#for_mux].SD := "DB2005_SD".SD[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	                
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2005_SD".Mux[#for_mux].SD.Hmi_Estado := "DB2005_SD".SD[#t_Index].Hmi_Estado;
	                    IF NOT "DB2005_SD".SD[#t_Index].Estado_AutoMan THEN
	                        "DB2005_SD".Mux[#for_mux].SD.Orden_ActivarManual := "DB2005_SD".SD["DB2005_SD".Mux[#for_mux].Index].Orden_ActivarManual;
	                    END_IF;
	                    "DB2005_SD".Mux[#for_mux].SD.Estado_Activado := "DB2005_SD".SD[#t_Index].Estado_Activado;
	                    "DB2005_SD".Mux[#for_mux].SD.Estado_Enclavado := "DB2005_SD".SD[#t_Index].Estado_Enclavado;
	                    "DB2005_SD".Mux[#for_mux].SD.Orden_ActivarAuto := "DB2005_SD".SD[#t_Index].Orden_ActivarAuto;
	                    "DB2005_SD".Mux[#for_mux].SD.Tiempos_TiempoAct := "DB2005_SD".SD[#t_Index].Tiempos_TiempoAct;
	                    "DB2005_SD".Mux[#for_mux].SD.Tiempos_TiempoDes := "DB2005_SD".SD[#t_Index].Tiempos_TiempoDes;
	                    "DB2005_SD".Mux[#for_mux].SD.Aux_oldActivado := "DB2005_SD".SD[#t_Index].Aux_oldActivado;
	                    "DB2005_SD".Mux[#for_mux].SD.Aux_oldAutoMan := "DB2005_SD".SD[#t_Index].Aux_oldAutoMan;
	                    "DB2005_SD".Mux[#for_mux].SD.Config_GrupoAlarma := "DB2005_SD".SD[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2005_SD".Mux[#for_mux].ExisteCambio := false;
	                    
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2005_SD".Mux[#for_mux].SD.Estado_AutoMan <> "DB2005_SD".SD[#t_Index].Estado_AutoMan THEN
	                        "DB2005_SD".SD[#t_Index].Estado_AutoMan := "DB2005_SD".Mux[#for_mux].SD.Estado_AutoMan;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2005_SD".Mux[#for_mux].SD.Orden_ActivarAuto <> "DB2005_SD".SD[#t_Index].Orden_ActivarAuto THEN
	                        "DB2005_SD".SD[#t_Index].Orden_ActivarAuto := "DB2005_SD".Mux[#for_mux].SD.Orden_ActivarAuto;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Orden_ActivarManual <> "DB2005_SD".SD[#t_Index].Orden_ActivarManual THEN
	                        "DB2005_SD".SD[#t_Index].Orden_ActivarManual := "DB2005_SD".Mux[#for_mux].SD.Orden_ActivarManual;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_DireccionSalidaBit <> "DB2005_SD".SD[#t_Index].Config_DireccionSalidaBit THEN
	                        "DB2005_SD".SD[#t_Index].Config_DireccionSalidaBit := "DB2005_SD".Mux[#for_mux].SD.Config_DireccionSalidaBit;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_DireccionSalidaByte <> "DB2005_SD".SD[#t_Index].Config_DireccionSalidaByte THEN
	                        "DB2005_SD".SD[#t_Index].Config_DireccionSalidaByte := "DB2005_SD".Mux[#for_mux].SD.Config_DireccionSalidaByte;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_Habilitar <> "DB2005_SD".SD[#t_Index].Config_Habilitar THEN
	                        "DB2005_SD".SD[#t_Index].Config_Habilitar := "DB2005_SD".Mux[#for_mux].SD.Config_Habilitar;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_HabilitarInvertir <> "DB2005_SD".SD[#t_Index].Config_HabilitarInvertir THEN
	                        "DB2005_SD".SD[#t_Index].Config_HabilitarInvertir := "DB2005_SD".Mux[#for_mux].SD.Config_HabilitarInvertir;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_HabilitarRetardoAct <> "DB2005_SD".SD[#t_Index].Config_HabilitarRetardoAct THEN
	                        "DB2005_SD".SD[#t_Index].Config_HabilitarRetardoAct := "DB2005_SD".Mux[#for_mux].SD.Config_HabilitarRetardoAct;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_HabilitarRetardoDes <> "DB2005_SD".SD[#t_Index].Config_HabilitarRetardoDes THEN
	                        "DB2005_SD".SD[#t_Index].Config_HabilitarRetardoDes := "DB2005_SD".Mux[#for_mux].SD.Config_HabilitarRetardoDes;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2005_SD".Mux[#for_mux].SD.Config_TipoAcceso <> "DB2005_SD".SD[#t_Index].Config_TipoAcceso THEN
	                        "DB2005_SD".SD[#t_Index].Config_TipoAcceso := "DB2005_SD".Mux[#for_mux].SD.Config_TipoAcceso;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Tiempos
	                    IF "DB2005_SD".Mux[#for_mux].SD.Tiempos_SetPointTiempoAct <> "DB2005_SD".SD[#t_Index].Tiempos_SetPointTiempoAct THEN
	                        "DB2005_SD".SD[#t_Index].Tiempos_SetPointTiempoAct := "DB2005_SD".Mux[#for_mux].SD.Tiempos_SetPointTiempoAct;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    IF "DB2005_SD".Mux[#for_mux].SD.Tiempos_SetPointTiempoDes <> "DB2005_SD".SD[#t_Index].Tiempos_SetPointTiempoDes THEN
	                        "DB2005_SD".SD[#t_Index].Tiempos_SetPointTiempoDes := "DB2005_SD".Mux[#for_mux].SD.Tiempos_SetPointTiempoDes;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2005_SD".Mux[#for_mux].ExisteCambio THEN
	                        
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2005_SD".Mux[#for_mux_cambios].Index THEN
	                                    "DB2005_SD".Mux[#for_mux_cambios].SD := "DB2005_SD".SD[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2005_SD".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la SD[0] que no se usa para escribir el index.
	                "DB2005_SD".Mux[#for_mux].SD := "DB2005_SD".SD[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            "DB2005_SD".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2005_SD".Mux[#for_mux].Index :=
	            "DB2005_SD".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	        
	    END_FOR;
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2005_SD".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2005_SD".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_SD" DO
	        
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2005_SD".SD[#for_i].Config_Habilitar THEN
	            
	            REGION LIMITE_GRUPO_ALARMA
	                
	                IF "DB2005_SD".SD[#for_i].Config_GrupoAlarma < 0 THEN
	                    "DB2005_SD".SD[#for_i].Config_GrupoAlarma := 0;
	                END_IF;
	                IF "DB2005_SD".SD[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                    "DB2005_SD".SD[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	                END_IF;
	                
	            END_REGION LIMITE_GRUPO_ALARMA
	            
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                //  MANUAL
	                IF "DB2005_SD".SD[#for_i].Estado_AutoMan THEN
	                    
	                    "DB2005_SD".Agrup["DB2005_SD".SD[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    #t_Activar := "DB2005_SD".SD[#for_i].Orden_ActivarManual AND NOT "DB2005_SD".SD[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2005_SD".SD[#for_i].Estado_SeguridadOk;
	                    
	                ELSE
	                    // =============================================================================
	                    //  AUTO
	                    "DB2005_SD".SD[#for_i].Orden_ActivarManual := FALSE;
	                    
	                    IF "DB2005_SD".SD[#for_i].Config_HabilitarInvertir THEN
	                        #t_Activar := NOT "DB2005_SD".SD[#for_i].Orden_ActivarAuto AND NOT "DB2005_SD".SD[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2005_SD".SD[#for_i].Estado_SeguridadOk;
	                    ELSE
	                        #t_Activar := "DB2005_SD".SD[#for_i].Orden_ActivarAuto AND NOT "DB2005_SD".SD[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2005_SD".SD[#for_i].Estado_SeguridadOk;
	                    END_IF;
	                END_IF;
	                
	            END_REGION MODOS_DE_TRABAJO
	            
	            
	            REGION ESTADO_DEL_DISPOSITIVO
	                
	                // =============================================================================
	                //  SALIDA SIMULADA
	                IF NOT #Simulacion THEN
	                    IF "DB2005_SD".SD[#for_i].Orden_ActivarManual = TRUE THEN
	                        #t_Activar := TRUE;
	                    ELSE
	                        #t_Activar := FALSE;
	                    END_IF;
	                END_IF;
	                
	                
	                IF NOT "DB2005_SD".SD[#for_i].Estado_AutoMan AND NOT #Simulacion THEN
	                    
	                    // =============================================================================
	                    //  RETARDO A LA ACTIVACIÓN AUTOMÁTICO
	                    IF #t_Activar AND "DB2005_SD".SD[#for_i].Config_HabilitarRetardoAct THEN
	                        
	                        IF #Pulso1seg AND "DB2005_SD".SD[#for_i].Tiempos_TiempoAct < "DB2005_SD".SD[#for_i].Tiempos_SetPointTiempoAct THEN
	                            "DB2005_SD".SD[#for_i].Tiempos_TiempoAct += 1;
	                        END_IF;
	                        
	                        IF "DB2005_SD".SD[#for_i].Tiempos_TiempoAct >= "DB2005_SD".SD[#for_i].Tiempos_SetPointTiempoAct THEN
	                            #t_ActivarConRetardo := TRUE;
	                        ELSE
	                            #t_ActivarConRetardo := FALSE;
	                        END_IF;
	                        
	                    ELSIF #t_Activar THEN
	                        #t_ActivarConRetardo := TRUE;
	                    ELSE
	                        "DB2005_SD".SD[#for_i].Tiempos_TiempoAct := 0;
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  RETARDO A LA DESACTIVACIÓN AUTOMÁTICO
	                    IF NOT #t_Activar AND "DB2005_SD".SD[#for_i].Config_HabilitarRetardoDes THEN
	                        
	                        IF #Pulso1seg AND "DB2005_SD".SD[#for_i].Tiempos_TiempoDes < "DB2005_SD".SD[#for_i].Tiempos_SetPointTiempoDes THEN
	                            "DB2005_SD".SD[#for_i].Tiempos_TiempoDes += 1;
	                        END_IF;
	                        
	                        IF "DB2005_SD".SD[#for_i].Tiempos_TiempoDes >= "DB2005_SD".SD[#for_i].Tiempos_SetPointTiempoDes THEN
	                            #t_ActivarConRetardo := FALSE;
	                        ELSE
	                            #t_ActivarConRetardo := TRUE;
	                        END_IF;
	                        
	                    ELSIF NOT #t_Activar THEN
	                        #t_ActivarConRetardo := FALSE;
	                    ELSE
	                        "DB2005_SD".SD[#for_i].Tiempos_TiempoDes := 0;
	                    END_IF;
	                    
	                ELSE
	                    
	                    #t_ActivarConRetardo := #t_Activar;
	                    
	                END_IF;
	                
	            END_REGION ESTADO_DEL_DISPOSITIVO
	            
	            
	            REGION ESCRITURA_SALIDA
	                
	                CASE "DB2000_ED".ED[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        // =============================================================================
	                        //  ESCRITURA VALORES DE LA TARJETA
	                        IF "DB2005_SD".SD[#for_i].Config_DireccionSalidaByte >= 0 THEN
	                            IF #t_ActivarConRetardo OR #t_Activar THEN
	                                "DB2005_SD".SD[#for_i].Estado_Activado := TRUE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2005_SD".SD[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2005_SD".SD[#for_i].Config_DireccionSalidaBit,
	                                          value := TRUE);
	                            ELSE
	                                "DB2005_SD".SD[#for_i].Estado_Activado := FALSE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2005_SD".SD[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2005_SD".SD[#for_i].Config_DireccionSalidaBit,
	                                          value := FALSE);
	                            END_IF;
	                        END_IF;
	                        
	                    #TIPO_ACCESO_PLC:
	                        // =============================================================================
	                        //  ESCRITURA VALORES DE LA TARJETA
	                        IF #t_ActivarConRetardo OR #t_Activar THEN
	                            "DB2005_SD".SD[#for_i].Estado_Activado := TRUE;
	                        ELSE
	                            "DB2005_SD".SD[#for_i].Estado_Activado := FALSE;
	                        END_IF;
	                        
	                END_CASE;
	                
	            END_REGION ESCRITURA_SALIDA
	            
	            
	            // =============================================================================
	            //  RESET ORDEN ACTIVAR EN AUTO
	            "DB2005_SD".SD[#for_i].Orden_ActivarAuto := FALSE;
	            
	            
	            REGION TRAZABILIDAD_MANUALIZACION
	                
	                IF "DB2005_SD".SD[#for_i].Estado_AutoMan AND NOT "DB2005_SD".SD[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_12_DISP_SD",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_SD",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2005_SD".SD[#for_i].Estado_AutoMan AND "DB2005_SD".SD[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_12_DISP_SD",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_SD",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2005_SD".SD[#for_i].Estado_AutoMan AND "DB2005_SD".SD[#for_i].Estado_Activado AND NOT "DB2005_SD".SD[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_12_DISP_SD",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_SD",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_ON",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2005_SD".SD[#for_i].Estado_AutoMan AND NOT "DB2005_SD".SD[#for_i].Estado_Activado AND "DB2005_SD".SD[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_12_DISP_SD",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_SD",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_OFF",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                
	                
	            END_REGION
	            
	            
	            // =============================================================================
	            // Estado anterior manual/automatico
	            "DB2005_SD".SD[#for_i].Aux_oldAutoMan := "DB2005_SD".SD[#for_i].Estado_AutoMan;
	            
	        ELSE
	            
	            // =============================================================================
	            // DISPOSITIVO HABILITADO
	            // =============================================================================
	            "DB2005_SD".SD[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2005_SD".SD[#for_i].Tiempos_TiempoAct := 0;
	            "DB2005_SD".SD[#for_i].Tiempos_TiempoDes := 0;
	            
	        END_IF;
	        
	        
	        REGION GESTION_HMI
	            
	            // =============================================================================
	            //  GESTION BITS PARA VISUALIZACION
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
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X0 := "DB2005_SD".SD[#for_i].Config_Habilitar;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X1 := "DB2005_SD".SD[#for_i].Estado_AutoMan;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X2 := "DB2005_SD".SD[#for_i].Estado_Enclavado;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X3 := "DB2005_SD".SD[#for_i].Estado_Activado;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X4 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X8 := FALSE;;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X9 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X10 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X13 := FALSE;;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2005_SD".SD[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION
	        
	        
	    END_FOR;
	    
	END_REGION
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>