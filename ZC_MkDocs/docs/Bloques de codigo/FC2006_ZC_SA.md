---
title: FC2006_ZC_SA
---
# FC FC2006_ZC_SA

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Salida Analogica.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se gestiona el estado del dispositivo
    - Se gestiona la orden de escritura
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
| `t_X1` | `Real` | - | `-` | - |
| `t_Y1` | `Real` | - | `-` | - |
| `t_ValorSalida` | `Real` | - | `-` | - |
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
﻿FUNCTION "FC2006_ZC_SA" : Void
TITLE = FC2006_SA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo salida analogica
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
      t_X0 : Real;
      t_X1 : Real;
      t_Y0 : Real;
      t_Y1 : Real;
      X : Real;
      t_ValorSalida : Real;
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
	
	Funcion para la gestion de dispositivo de tipo Salida Analogica.
	
	En ella se realizan las siguientes acciones:
	
	- Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
	- Se gestiona el estado del dispositivo
	- Se gestiona la orden de escritura
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
	| 00.00.00 | 15.10.2020 | (ABH)   | Primera version. |
	| 00.00.01 | 06.05.2021 | (ABH)   | Añadido bit de enclavamiento. Cuando Estado_Enclavado este a TRUE, la salida tiene el valor de Config_ConsignaEnclavado. |
	| 00.00.02 | 27.07.2021 | (ABH)   | Se añade que si la direccion de salida es igual a 0, no realiza ningun calculo ni intenta escribir la salida para que no salten errores. Se añade variable aux para almacenar el mensaje de error, para que a la hora de generar las alarmas se generen adecuadamente. |
	| 00.00.03 | 26.04.2022 | (HCR)   | Cambio en la organizacion del UDT. Se organiza en estructuras en base al tipo de funcion que realizan los datos. Se gestionan los BITs de visibilidad para Hmi. |
	| 00.00.04 | 27.04.2022 | (ABH)   | Se añaden auxiliares de estado anterior del modo manual y automatico para poder registrar las trazas.   |
	| 00.00.05 | 28.04.2022 | (HCR)   | Se mantiene la salida al pasar a modo manual. |
	| 00.00.06 | 29.04.2022 | (HCR)   | Cambio del estado de la señal por prioridades. Cambio de las condiciones de para error de configuración, poniendo parámetros de ingenería y de tarjeta. Cambio en Alarmas. |
	| 00.00.07 | 17.05.2022 | (BRM)   | Cambio en escritura canal - Funcion POKE area: 16#82 para CPU 1200. |
	| 00.00.08 | 08.11.2022 | (ABH)   | Se añade trazabilidad manualizaciones. |
	| 00.00.09 | 27.07.2023 | (ABH)   | Se añade trazabilidad cambio parametros. |
	| 00.00.10 | 18.09.2023 | (ABH)   | Se añade reset de valor SP auto al final de la gestion del dispositivo. |
	| 00.00.11 | 22.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado) |
	| 00.00.12 | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado. Se añade movimiento de SA[0] a multiplexado en caso de que el indice sea 0.  |
	| 00.00.12 | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores. |
	| 00.00.13 | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro. |
	| 00.00.14 | 24.04.2025 | (HCR)   | Se añade gestion de idioma  |
	| 00.00.15 | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	| 00.00.16 | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT.Se elimina nombre de UDT. Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision. |  
	| 01.00.00 | 18.05.2026 | (ABH)   | Se añade variable `Config_TipoAcceso` para uso de direccionamiento indirecto o uso directo en PLC. |
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2006_SA".Mux[#for_mux].Index :=
	            "DB2006_SA".Mux[#for_mux].oldIndex := 0;
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
	            IF "DB2006_SA".Mux[#for_mux].Index < 0 THEN
	                "DB2006_SA".Mux[#for_mux].Index := 0;
	            END_IF;
	            IF "DB2006_SA".Mux[#for_mux].Index > "N_MAX_DISP_SA" THEN
	                "DB2006_SA".Mux[#for_mux].Index := "N_MAX_DISP_SA";
	            END_IF;
	            IF "DB2006_SA".Mux[#for_mux].Index >= "N_MAX_DISP_SA" THEN
	                "DB2006_SA".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2006_SA".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2006_SA".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2006_SA".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2006_SA".Mux[#for_mux].oldIndex := #t_Index;
	        
	        IF "DB2006_SA".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2006_SA".Mux[#for_mux].SA := "DB2006_SA".SA[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	                
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2006_SA".Mux[#for_mux].SA.Hmi_Estado := "DB2006_SA".SA[#t_Index].Hmi_Estado;
	                    "DB2006_SA".Mux[#for_mux].SA.Estado_SeguridadOk := "DB2006_SA".SA[#for_i].Estado_SeguridadOk;
	                    IF NOT "DB2006_SA".SA[#t_Index].Estado_AutoMan THEN
	                        "DB2006_SA".Mux[#for_mux].SA.Orden_ConsignaManual := "DB2006_SA".SA[#t_Index].Orden_ConsignaManual;
	                    END_IF;
	                    "DB2006_SA".Mux[#for_mux].SA.Estado_ValorActual := "DB2006_SA".SA[#t_Index].Estado_ValorActual;
	                    "DB2006_SA".Mux[#for_mux].SA.Estado_ValorTarjeta := "DB2006_SA".SA[#t_Index].Estado_ValorTarjeta;
	                    "DB2006_SA".Mux[#for_mux].SA.Estado_Enclavado := "DB2006_SA".SA[#t_Index].Estado_Enclavado;
	                    "DB2006_SA".Mux[#for_mux].SA.Alarmas_Escritura := "DB2006_SA".SA[#t_Index].Alarmas_Escritura;
	                    "DB2006_SA".Mux[#for_mux].SA.Alarmas_General := "DB2006_SA".SA[#t_Index].Alarmas_General;
	                    "DB2006_SA".Mux[#for_mux].SA.Alarmas_Max := "DB2006_SA".SA[#t_Index].Alarmas_Max;
	                    "DB2006_SA".Mux[#for_mux].SA.Alarmas_Min := "DB2006_SA".SA[#t_Index].Alarmas_Min;
	                    "DB2006_SA".Mux[#for_mux].SA.Alarmas_Parametros := "DB2006_SA".SA[#t_Index].Alarmas_Parametros;
	                    "DB2006_SA".Mux[#for_mux].SA.Orden_ConsignaAuto := "DB2006_SA".SA[#t_Index].Orden_ConsignaAuto;
	                    "DB2006_SA".Mux[#for_mux].SA.Aux_Estado := "DB2006_SA".SA[#t_Index].Aux_Estado;
	                    "DB2006_SA".Mux[#for_mux].SA.Aux_oldAlarma := "DB2006_SA".SA[#t_Index].Aux_oldAlarma;
	                    "DB2006_SA".Mux[#for_mux].SA.Aux_oldAutoMan := "DB2006_SA".SA[#t_Index].Aux_oldAutoMan;
	                    "DB2006_SA".Mux[#for_mux].SA.Config_GrupoAlarma := "DB2006_SA".SA[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2006_SA".Mux[#for_mux].ExisteCambio := false;
	                    
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2006_SA".Mux[#for_mux].SA.Estado_AutoMan <> "DB2006_SA".SA[#t_Index].Estado_AutoMan THEN
	                        "DB2006_SA".SA[#t_Index].Estado_AutoMan := "DB2006_SA".Mux[#for_mux].SA.Estado_AutoMan;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2006_SA".Mux[#for_mux].SA.Orden_ConsignaManual <> "DB2006_SA".SA[#t_Index].Orden_ConsignaManual THEN
	                        "DB2006_SA".SA[#t_Index].Orden_ConsignaManual := "DB2006_SA".Mux[#for_mux].SA.Orden_ConsignaManual;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Orden_ConsignaEnclavado <> "DB2006_SA".SA[#t_Index].Orden_ConsignaEnclavado THEN
	                        "DB2006_SA".SA[#t_Index].Orden_ConsignaEnclavado := "DB2006_SA".Mux[#for_mux].SA.Orden_ConsignaEnclavado;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_DireccionSalidaByte <> "DB2006_SA".SA[#t_Index].Config_DireccionSalidaByte THEN
	                        "DB2006_SA".SA[#t_Index].Config_DireccionSalidaByte := "DB2006_SA".Mux[#for_mux].SA.Config_DireccionSalidaByte;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_ErrorMaxIngenieria <> "DB2006_SA".SA[#t_Index].Config_ErrorMaxIngenieria THEN
	                        "DB2006_SA".SA[#t_Index].Config_ErrorMaxIngenieria := "DB2006_SA".Mux[#for_mux].SA.Config_ErrorMaxIngenieria;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_ErrorMinIngenieria <> "DB2006_SA".SA[#t_Index].Config_ErrorMinIngenieria THEN
	                        "DB2006_SA".SA[#t_Index].Config_ErrorMinIngenieria := "DB2006_SA".Mux[#for_mux].SA.Config_ErrorMinIngenieria;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMaxIngenieria <> "DB2006_SA".SA[#t_Index].Config_EscaladoMaxIngenieria THEN
	                        "DB2006_SA".SA[#t_Index].Config_EscaladoMaxIngenieria := "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMaxIngenieria;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMaxTarjeta <> "DB2006_SA".SA[#t_Index].Config_EscaladoMaxTarjeta THEN
	                        "DB2006_SA".SA[#t_Index].Config_EscaladoMaxTarjeta := "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMaxTarjeta;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMinIngenieria <> "DB2006_SA".SA[#t_Index].Config_EscaladoMinIngenieria THEN
	                        "DB2006_SA".SA[#t_Index].Config_EscaladoMinIngenieria := "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMinIngenieria;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMinTarjeta <> "DB2006_SA".SA[#t_Index].Config_EscaladoMinTarjeta THEN
	                        "DB2006_SA".SA[#t_Index].Config_EscaladoMinTarjeta := "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoMinTarjeta;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoOffset <> "DB2006_SA".SA[#t_Index].Config_EscaladoOffset THEN
	                        "DB2006_SA".SA[#t_Index].Config_EscaladoOffset := "DB2006_SA".Mux[#for_mux].SA.Config_EscaladoOffset;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_Habilitar <> "DB2006_SA".SA[#t_Index].Config_Habilitar THEN
	                        "DB2006_SA".SA[#t_Index].Config_Habilitar := "DB2006_SA".Mux[#for_mux].SA.Config_Habilitar;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_HabilitarAlarmaMax <> "DB2006_SA".SA[#t_Index].Config_HabilitarAlarmaMax THEN
	                        "DB2006_SA".SA[#t_Index].Config_HabilitarAlarmaMax := "DB2006_SA".Mux[#for_mux].SA.Config_HabilitarAlarmaMax;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_HabilitarAlarmaMin <> "DB2006_SA".SA[#t_Index].Config_HabilitarAlarmaMin THEN
	                        "DB2006_SA".SA[#t_Index].Config_HabilitarAlarmaMin := "DB2006_SA".Mux[#for_mux].SA.Config_HabilitarAlarmaMin;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2006_SA".Mux[#for_mux].SA.Config_TipoAcceso <> "DB2006_SA".SA[#t_Index].Config_TipoAcceso THEN
	                        "DB2006_SA".SA[#t_Index].Config_TipoAcceso := "DB2006_SA".Mux[#for_mux].SA.Config_TipoAcceso;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2006_SA".Mux[#for_mux].ExisteCambio THEN
	                        
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2006_SA".Mux[#for_mux_cambios].Index THEN
	                                    "DB2006_SA".Mux[#for_mux_cambios].SA := "DB2006_SA".SA[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2006_SA".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la SA[0] que no se usa para escribir el index.
	                "DB2006_SA".Mux[#for_mux].SA := "DB2006_SA".SA[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            "DB2006_SA".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2006_SA".Mux[#for_mux].Index :=
	            "DB2006_SA".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	        
	    END_FOR;
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2006_SA".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2006_SA".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_SA" DO
	        
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2006_SA".SA[#for_i].Config_Habilitar THEN
	            
	            REGION LIMITE_GRUPO_ALARMA
	                
	                IF "DB2006_SA".SA[#for_i].Config_GrupoAlarma < 0 THEN
	                    "DB2006_SA".SA[#for_i].Config_GrupoAlarma := 0;
	                END_IF;
	                IF "DB2006_SA".SA[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                    "DB2006_SA".SA[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	                END_IF;
	                
	            END_REGION LIMITE_GRUPO_ALARMA
	            
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                // MODO MANUAL
	                IF "DB2006_SA".SA[#for_i].Estado_AutoMan THEN
	                    "DB2006_SA".Agrup["DB2006_SA".SA[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    "DB2006_SA".SA[#for_i].Estado_ValorActual := "DB2006_SA".SA[#for_i].Orden_ConsignaManual;
	                ELSE
	                    "DB2006_SA".SA[#for_i].Estado_ValorActual := "DB2006_SA".SA[#for_i].Orden_ConsignaAuto;
	                    "DB2006_SA".SA[#for_i].Orden_ConsignaManual := "DB2006_SA".SA[#for_i].Orden_ConsignaAuto;
	                END_IF;
	                
	            END_REGION MODOS_DE_TRABAJO
	            
	            
	            REGION ERRORES
	                
	                // =============================================================================
	                //  LIMITE INFERIOR
	                IF "DB2006_SA".SA[#for_i].Estado_ValorActual <= "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria THEN
	                    "DB2006_SA".SA[#for_i].Estado_ValorActual := "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria;
	                END_IF;
	                
	                // =============================================================================
	                //  LIMITE SUPERIOR
	                IF "DB2006_SA".SA[#for_i].Estado_ValorActual >= "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria THEN
	                    "DB2006_SA".SA[#for_i].Estado_ValorActual := "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR MÍNIMO
	                IF "DB2006_SA".SA[#for_i].Config_HabilitarAlarmaMin AND
	                    "DB2006_SA".SA[#for_i].Estado_ValorActual < "DB2006_SA".SA[#for_i].Config_ErrorMinIngenieria THEN
	                    "DB2006_SA".SA[#for_i].Alarmas_Min := TRUE;
	                ELSE
	                    "DB2006_SA".SA[#for_i].Alarmas_Min := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR MÁXIMO
	                IF "DB2006_SA".SA[#for_i].Config_HabilitarAlarmaMax AND
	                    "DB2006_SA".SA[#for_i].Estado_ValorActual > "DB2006_SA".SA[#for_i].Config_ErrorMaxIngenieria THEN
	                    "DB2006_SA".SA[#for_i].Alarmas_Max := TRUE;
	                ELSE
	                    "DB2006_SA".SA[#for_i].Alarmas_Max := FALSE;
	                END_IF;
	                
	                
	            END_REGION ERRORES
	            
	            
	            REGION SALIDA
	                
	                IF NOT "DB2006_SA".SA[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2006_SA".SA[#for_i].Estado_SeguridadOk THEN
	                    
	                    // =============================================================================
	                    //  CONVERSIÓN DE VALORES
	                    #t_Y0 := INT_TO_REAL("DB2006_SA".SA[#for_i].Config_EscaladoMinTarjeta);
	                    #t_Y1 := INT_TO_REAL("DB2006_SA".SA[#for_i].Config_EscaladoMaxTarjeta);
	                    #X := "DB2006_SA".SA[#for_i].Estado_ValorActual;
	                    #t_X0 := "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria;
	                    #t_X1 := "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria;
	                    
	                    // =============================================================================
	                    //  ESCALADO Y = (X-x0)*((y1-y0)/(x1-x0)) + y0
	                    IF "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria > "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria AND
	                        "DB2006_SA".SA[#for_i].Config_EscaladoMaxTarjeta > "DB2006_SA".SA[#for_i].Config_EscaladoMinTarjeta THEN
	                        
	                        #t_ValorSalida := ((#X - #t_X0) * ((#t_Y1 - #t_Y0) / (#t_X1 - #t_X0))) + #t_Y0;
	                        "DB2006_SA".SA[#for_i].Alarmas_Parametros := FALSE;
	                        #t_ValorSalida := #t_ValorSalida + "DB2006_SA".SA[#for_i].Config_EscaladoOffset;
	                    ELSE
	                        #t_ValorSalida := "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria;
	                        "DB2006_SA".SA[#for_i].Alarmas_Parametros := TRUE;
	                    END_IF;
	                    
	                ELSE
	                    
	                    // =============================================================================
	                    //  AJUSTE LIMITES CONSIGNA ENCLAVADO
	                    IF "DB2006_SA".SA[#for_i].Orden_ConsignaEnclavado > "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria THEN
	                        "DB2006_SA".SA[#for_i].Orden_ConsignaEnclavado := "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria;
	                    END_IF;
	                    IF "DB2006_SA".SA[#for_i].Orden_ConsignaEnclavado < "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria THEN
	                        "DB2006_SA".SA[#for_i].Orden_ConsignaEnclavado := "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria;
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  ESCRITURA SALIDA ENCLAVADA
	                    
	                    // =============================================================================
	                    //  CONVERSIÓN DE VALORES
	                    #t_Y0 := INT_TO_REAL("DB2006_SA".SA[#for_i].Config_EscaladoMinTarjeta);
	                    #t_Y1 := INT_TO_REAL("DB2006_SA".SA[#for_i].Config_EscaladoMaxTarjeta);
	                    #X := "DB2006_SA".SA[#for_i].Orden_ConsignaEnclavado;
	                    #t_X0 := "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria;
	                    #t_X1 := "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria;
	                    
	                    // =============================================================================
	                    //  ESCALADO Y = (X-x0)*((y1-y0)/(x1-x0)) + y0
	                    IF "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria > "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria AND
	                        "DB2006_SA".SA[#for_i].Config_EscaladoMaxTarjeta > "DB2006_SA".SA[#for_i].Config_EscaladoMinTarjeta THEN
	                        
	                        #t_ValorSalida := ((#X - #t_X0) * ((#t_Y1 - #t_Y0) / (#t_X1 - #t_X0))) + #t_Y0;
	                        "DB2006_SA".SA[#for_i].Alarmas_Parametros := FALSE;
	                    ELSE
	                        #t_ValorSalida := "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria;
	                        "DB2006_SA".SA[#for_i].Alarmas_Parametros := TRUE;
	                    END_IF;
	                    
	                END_IF;
	                
	                REGION ESCRITURA_SALIDA
	                    
	                    CASE "DB2006_SA".SA[#for_i].Config_TipoAcceso OF
	                            
	                        #TIPO_ACCESO_INDIRECTO:
	                            //  =============================================================================
	                            //  ESCRITURA DEL CANAL - POKE (area) 16#2 para CPU 1500 ; 16#82 para CPU 1200
	                            IF "DB2006_SA".SA[#for_i].Config_DireccionSalidaByte > 0 THEN
	                                
	                                "DB2006_SA".SA[#for_i].Estado_ValorTarjeta := REAL_TO_INT(#t_ValorSalida);
	                                
	                                POKE(area := 16#82,
	                                     dbNumber := 0,
	                                     byteOffset := "DB2006_SA".SA[#for_i].Config_DireccionSalidaByte,
	                                     value := INT_TO_WORD("DB2006_SA".SA[#for_i].Estado_ValorTarjeta));
	                                
	                                "DB2006_SA".SA[#for_i].Estado_Escritura := GET_ERR_ID();
	                                IF "DB2006_SA".SA[#for_i].Estado_Escritura <> 0 THEN
	                                    "DB2006_SA".SA[#for_i].Alarmas_Escritura := TRUE;
	                                ELSE
	                                    "DB2006_SA".SA[#for_i].Alarmas_Escritura := FALSE;
	                                END_IF;
	                                
	                            ELSE
	                                
	                                "DB2006_SA".SA[#for_i].Estado_ValorTarjeta := 0;
	                                
	                            END_IF;
	                            
	                        #TIPO_ACCESO_PLC:
	                            // =============================================================================
	                            //  ESCRITURA VALORES DE LA TARJETA
	                            "DB2006_SA".SA[#for_i].Estado_ValorTarjeta := REAL_TO_INT(#t_ValorSalida);
	                            
	                    END_CASE;
	                    
	                END_REGION ESCRITURA_SALIDA
	                
	            END_REGION SALIDA
	            
	            
	            REGION ESTADO
	                
	                //  Señal normal
	                "DB2006_SA".SA[#for_i].Aux_Estado := 1;   
	                
	                //  Límites alcanzados
	                IF "DB2006_SA".SA[#for_i].Estado_ValorActual < "DB2006_SA".SA[#for_i].Config_ErrorMinIngenieria AND
	                    "DB2006_SA".SA[#for_i].Config_HabilitarAlarmaMin THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 4;  
	                END_IF;
	                
	                //  Límites alcanzados
	                IF "DB2006_SA".SA[#for_i].Estado_ValorActual >= "DB2006_SA".SA[#for_i].Config_ErrorMaxIngenieria AND
	                    "DB2006_SA".SA[#for_i].Config_HabilitarAlarmaMax THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 5;  
	                END_IF;
	                
	                //  Señal forzada   
	                IF "DB2006_SA".SA[#for_i].Estado_AutoMan THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 2;   
	                END_IF;
	                
	                //  Enclavado
	                IF "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria > "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria AND
	                    "DB2006_SA".SA[#for_i].Config_EscaladoMaxTarjeta > "DB2006_SA".SA[#for_i].Config_EscaladoMinTarjeta AND
	                    "DB2006_SA".SA[#for_i].Estado_Enclavado THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 9;  
	                END_IF;
	                
	                //  Error parametros
	                IF "DB2006_SA".SA[#for_i].Config_EscaladoMaxIngenieria <= "DB2006_SA".SA[#for_i].Config_EscaladoMinIngenieria OR
	                    "DB2006_SA".SA[#for_i].Config_EscaladoMaxTarjeta <= "DB2006_SA".SA[#for_i].Config_EscaladoMinTarjeta THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 6;  
	                END_IF;
	                
	                //  Error de escritura
	                IF "DB2006_SA".SA[#for_i].Estado_Escritura <> 0 THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 10;  
	                END_IF;
	                
	                // SA no direccionada
	                IF "DB2006_SA".SA[#for_i].Config_DireccionSalidaByte <= 0 THEN
	                    "DB2006_SA".SA[#for_i].Aux_Estado := 8; 
	                END_IF;
	                
	            END_REGION
	            
	            
	            "DB2006_SA".SA[#for_i].Alarmas_General := FALSE;
	            IF "DB2006_SA".SA[#for_i].Alarmas_Max OR
	                "DB2006_SA".SA[#for_i].Alarmas_Min OR
	                "DB2006_SA".SA[#for_i].Alarmas_Parametros OR
	                "DB2006_SA".SA[#for_i].Alarmas_Escritura
	            THEN
	                "DB2006_SA".Agrup["DB2006_SA".SA[#for_i].Config_GrupoAlarma].AlgunaAlarma := TRUE;
	                "DB2006_SA".SA[#for_i].Alarmas_General := TRUE;
	            END_IF;
	            
	            
	            REGION TRAZABILIDAD
	                
	                IF "DB2006_SA".SA[#for_i].Estado_AutoMan AND NOT "DB2006_SA".SA[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_13_DISP_SA",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_SA",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2006_SA".SA[#for_i].Estado_AutoMan AND "DB2006_SA".SA[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_13_DISP_SA",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_SA",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	            END_REGION
	            
	            // =============================================================================
	            //  Estado anterior manual/automatico
	            "DB2006_SA".SA[#for_i].Aux_oldAutoMan := "DB2006_SA".SA[#for_i].Estado_AutoMan;
	            
	            
	            // =============================================================================
	            //  Reset de orden automatica
	            "DB2006_SA".SA[#for_i].Orden_ConsignaAuto := 0.0;
	            
	        ELSE
	            
	            // =============================================================================
	            // DISPOSITIVO NO HABILITADO
	            // =============================================================================
	            "DB2006_SA".SA[#for_i].Estado_ValorTarjeta := 0;
	            "DB2006_SA".SA[#for_i].Hmi_Estado := 0;   //  Canal deshabilitado
	            "DB2006_SA".SA[#for_i].Estado_ValorActual := 0.0;
	            "DB2006_SA".SA[#for_i].Estado_ValorTarjeta := 0;
	            "DB2006_SA".SA[#for_i].Orden_ConsignaAuto := 0.0;
	            "DB2006_SA".SA[#for_i].Orden_ConsignaManual := 0.0;
	            "DB2006_SA".SA[#for_i].Estado_AutoMan := FALSE;
	            "DB2006_SA".SA[#for_i].Alarmas_General := FALSE;
	            "DB2006_SA".SA[#for_i].Alarmas_Max := FALSE;
	            "DB2006_SA".SA[#for_i].Alarmas_Min := FALSE;
	            
	        END_IF;
	        
	        REGION GESTION_HMI
	            
	            // =============================================================================
	            //  GESTION BITS PARA VISUALIZACION
	            //  Bit     0   Habilitacion
	            //  Bit     1   ManualAutomatico
	            //  Bit     2   Reserva
	            //  Bit     3   Reserva
	            //  Bit     4   Enclavado
	            //  Bit     5   Reserva
	            //  Bit     6   Reserva
	            //  Bit     7   Reserva
	            //  Bit     8   Alarma General
	            //  Bit     9   Alarma 1
	            //  Bit     10  Alarma 2
	            //  Bit     11  Alarma 3
	            //  Bit     12  Alarma 4
	            //  Bit     13  Alarma 5
	            //  Bit     14  Reserva
	            //  Bit     15  Reserva
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X0 := "DB2006_SA".SA[#for_i].Config_Habilitar;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X1 := "DB2006_SA".SA[#for_i].Estado_AutoMan;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X2 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X3 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X4 := "DB2006_SA".SA[#for_i].Estado_Enclavado;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X8 := "DB2006_SA".SA[#for_i].Alarmas_General;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X9 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X10 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X13 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2006_SA".SA[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION
	        
	        REGION GESTION_NUEVA_ALARMA
	            
	            // =============================================================================
	            //  DETECCION DE NUEVA ALARMA
	            IF "DB2006_SA".SA[#for_i].Alarmas_General AND NOT "DB2006_SA".SA[#for_i].Aux_oldAlarma THEN
	                "DB2006_SA".Agrup["DB2006_SA".SA[#for_i].Config_GrupoAlarma].NuevaAlarma := TRUE;
	            END_IF;
	            
	            //  Estado anterior de las alarmas
	            "DB2006_SA".SA[#for_i].Aux_oldAlarma := "DB2006_SA".SA[#for_i].Alarmas_General;
	            
	        END_REGION
	        
	        
	    END_FOR;
	    
	    
	    // =============================================================================
	    //  ACUSE DE NUEVAS ALARMAS
	    IF #Ack THEN
	        FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	            "DB2006_SA".Agrup[#for_i].NuevaAlarma := FALSE;
	        END_FOR;
	    END_IF;
	    
	END_REGION
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>