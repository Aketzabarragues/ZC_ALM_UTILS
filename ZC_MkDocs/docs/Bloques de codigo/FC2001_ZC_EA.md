---
title: FC2001_ZC_EA
---
# FC FC2001_ZC_EA

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Entrada Analogica.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se realiza la lectura de la entrada de manera indirecta si esta habilitada.
    - Se gestiona el escalado si esta habilitado.
    - Se gestiona el estado del dispositivo
    - Se gestiona la trazabilidad de las manualizaciones del dispositivo

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **DB:** [DB2001_EA](../Estructura de datos/DB2001_EA.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1seg` | `Bool` | - | `-` | Pulso de 1 segundo |
| `Simulacion` | `Bool` | - | `-` | Simulacion |
| `Arranque` | `Bool` | - | `-` | Primer arranque |
| `Ack` | `Bool` | - | `-` | Acuse general |
| `UsuarioActual` | `String` | - | `-` | Usuario actual |
| `FechaHoraActual` | `DTL` | - | `-` | Fecha y hora actual |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |
| `for_mux` | `Int` | - | `-` | - |
| `t_x1` | `Real` | - | `-` | - |
| `t_y1` | `Real` | - | `-` | - |
| `t_ValorTarjeta` | `Int` | - | `-` | - |
| `t_LecturaRealizada` | `Bool` | - | `-` | - |
| `t_Index` | `Int` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TIPO_ACCESO_INDIRECTO_ESCALADO` | `SInt` | - | `0` | - |
| `TIPO_ACCESO_INDIRECTO_WORD_SIN_ESCALADO` | `SInt` | - | `2` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2001_ZC_EA" : Void
TITLE = FC2001_EA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo entrada analogica
   VAR_INPUT 
      Pulso1seg : Bool;   // Pulso de 1 segundo
      Simulacion : Bool;   // Simulacion
      Arranque : Bool;   // Primer arranque
      Ack : Bool;   // Acuse general
      UsuarioActual : String;   // Usuario actual
      FechaHoraActual {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
   END_VAR

   VAR_TEMP 
      for_i : Int;
      for_mux_cambios : Int;
      for_mux : Int;
      t_x0 : Real;
      t_x1 : Real;
      t_y0 : Real;
      t_y1 : Real;
      t_x : Real;
      t_ValorTarjeta : Int;
      t_ErrorGeneral : Bool;
      t_LecturaRealizada : Bool;
      t_SubError : Real;
      t_Index : Int;
      t_oldIndex : Int;
   END_VAR

   VAR CONSTANT 
      TIPO_ACCESO_INDIRECTO_ESCALADO : SInt := 0;
      TIPO_ACCESO_PLC : SInt := 1;
      TIPO_ACCESO_INDIRECTO_WORD_SIN_ESCALADO : SInt := 2;
      TIPO_ACCESO_INDIRECTO_DWORD_SIN_ESCALADO : SInt := 3;
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
	
	Funcion para la gestion de dispositivo de tipo Entrada Analogica.
	
	En ella se realizan las siguientes acciones:
	
	- Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
	- Se realiza la lectura de la entrada de manera indirecta si esta habilitada.
	- Se gestiona el escalado si esta habilitado.
	- Se gestiona el estado del dispositivo
	- Se gestiona la trazabilidad de las manualizaciones del dispositivo
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC8_ZC_TRAZA_REGISTRO` |
	| FB   | - |
	| DB   | `DB2001_EA` |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.00 | 15.10.2020 | (ABH)   | Primera versión. |
	| 00.00.01 | 26.04.2022 | (HCR)   | Cambio en la organizacion del UDT en base al tipo de funcion.Se añade seguridad en el escalado. |
	| 00.00.02 | 27.04.2022 | (ABH)   | Se añaden auxiliares de estado anterior del modo manual y automatico para poder registrar las trazas. |
	| 00.00.06 | 29.04.2022 | (HCR)   | Cambio del estado de la señal, se agrega señal estado por prioridades. Cambio de las condiciones de para error de configuración. Cambio en la programaciíon de alarmas. Cambio en los límites de la señal |
	| 00.00.07 | 08.11.2022 | (ABH)   | Se añade trazabilidad manualizaciones |
	| 00.00.08 | 20.12.2022 | (HCR)   | Se añade trazabilidad de escalado y offset   |
	| 00.00.09 | 22.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado) |
	| 00.00.10 | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado.nSe añade movimiento de EA[0] a multiplexado en caso de que el indice sea 0. |
	| 00.00.11 | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores. |
	| 00.00.12 | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro. |
	| 00.00.13 | 24.04.2025 | (HCR)   | Se añade gestion de idioma    |
	| 00.00.14 | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion.   |
	| 00.00.15 | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision. |
	| 00.00.16 | 14.05.2026 | (ABH)   | Se modifica UDT para añadir tipo de lectura. |
	| 01.00.00 | 18.05.2026 | (ABH)   | Se añade variable `Config_TipoAcceso` para uso de direccionamiento indirecto o uso directo en PLC. |
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2001_EA".Mux[#for_mux].Index :=
	            "DB2001_EA".Mux[#for_mux].oldIndex := 0;
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
	            IF "DB2001_EA".Mux[#for_mux].Index < 0 THEN
	                "DB2001_EA".Mux[#for_mux].Index := 0;
	            END_IF;
	            IF "DB2001_EA".Mux[#for_mux].Index > "N_MAX_DISP_EA" THEN
	                "DB2001_EA".Mux[#for_mux].Index := "N_MAX_DISP_EA";
	            END_IF;
	            IF "DB2001_EA".Mux[#for_mux].Index >= "N_MAX_DISP_EA" THEN
	                "DB2001_EA".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2001_EA".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2001_EA".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2001_EA".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2001_EA".Mux[#for_mux].oldIndex := #t_Index;
	        
	        IF "DB2001_EA".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2001_EA".Mux[#for_mux].EA := "DB2001_EA".EA[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	                
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2001_EA".Mux[#for_mux].EA.Hmi_Estado := "DB2001_EA".EA[#t_Index].Hmi_Estado;
	                    IF NOT "DB2001_EA".EA[#t_Index].Estado_AutoMan THEN
	                        "DB2001_EA".Mux[#for_mux].EA.Orden_ConsignaManual := "DB2001_EA".EA[#t_Index].Orden_ConsignaManual;
	                    END_IF;
	                    "DB2001_EA".Mux[#for_mux].EA.Estado_ValorIngenieria := "DB2001_EA".EA[#t_Index].Estado_ValorIngenieria;
	                    "DB2001_EA".Mux[#for_mux].EA.Estado_ValorTarjeta := "DB2001_EA".EA[#t_Index].Estado_ValorTarjeta;
	                    "DB2001_EA".Mux[#for_mux].EA.Alarmas_General := "DB2001_EA".EA[#t_Index].Alarmas_General;
	                    "DB2001_EA".Mux[#for_mux].EA.Alarmas_HiloRoto := "DB2001_EA".EA[#t_Index].Alarmas_HiloRoto;
	                    "DB2001_EA".Mux[#for_mux].EA.Alarmas_Lectura := "DB2001_EA".EA[#t_Index].Alarmas_Lectura;
	                    "DB2001_EA".Mux[#for_mux].EA.Alarmas_Max := "DB2001_EA".EA[#t_Index].Alarmas_Max;
	                    "DB2001_EA".Mux[#for_mux].EA.Alarmas_Min := "DB2001_EA".EA[#t_Index].Alarmas_Min;
	                    "DB2001_EA".Mux[#for_mux].EA.Alarmas_Parametros := "DB2001_EA".EA[#t_Index].Alarmas_Parametros;
	                    "DB2001_EA".Mux[#for_mux].EA.Aux_Estado := "DB2001_EA".EA[#t_Index].Aux_Estado;
	                    "DB2001_EA".Mux[#for_mux].EA.Aux_oldAlarma := "DB2001_EA".EA[#t_Index].Aux_oldAlarma;
	                    "DB2001_EA".Mux[#for_mux].EA.Aux_oldAutoMan := "DB2001_EA".EA[#t_Index].Aux_oldAutoMan;
	                    "DB2001_EA".Mux[#for_mux].EA.Config_GrupoAlarma := "DB2001_EA".EA[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2001_EA".Mux[#for_mux].ExisteCambio := false;
	                    
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2001_EA".Mux[#for_mux].EA.Estado_AutoMan <> "DB2001_EA".EA[#t_Index].Estado_AutoMan THEN
	                        "DB2001_EA".EA[#t_Index].Estado_AutoMan := "DB2001_EA".Mux[#for_mux].EA.Estado_AutoMan;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2001_EA".Mux[#for_mux].EA.Orden_ConsignaManual <> "DB2001_EA".EA[#t_Index].Orden_ConsignaManual THEN
	                        "DB2001_EA".EA[#t_Index].Orden_ConsignaManual := "DB2001_EA".Mux[#for_mux].EA.Orden_ConsignaManual;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_DireccionEntradaByte <> "DB2001_EA".EA[#t_Index].Config_DireccionEntradaByte THEN
	                        "DB2001_EA".EA[#t_Index].Config_DireccionEntradaByte := "DB2001_EA".Mux[#for_mux].EA.Config_DireccionEntradaByte;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMaxHisteresis <> "DB2001_EA".EA[#t_Index].Config_ErrorMaxHisteresis THEN
	                        "DB2001_EA".EA[#t_Index].Config_ErrorMaxHisteresis := "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMaxHisteresis;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMaxIngenieria <> "DB2001_EA".EA[#t_Index].Config_ErrorMaxIngenieria THEN
	                        "DB2001_EA".EA[#t_Index].Config_ErrorMaxIngenieria := "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMaxIngenieria;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMinHisteresis <> "DB2001_EA".EA[#t_Index].Config_ErrorMinHisteresis THEN
	                        "DB2001_EA".EA[#t_Index].Config_ErrorMinHisteresis := "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMinHisteresis;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMinIngenieria <> "DB2001_EA".EA[#t_Index].Config_ErrorMinIngenieria THEN
	                        "DB2001_EA".EA[#t_Index].Config_ErrorMinIngenieria := "DB2001_EA".Mux[#for_mux].EA.Config_ErrorMinIngenieria;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMaxIngenieria <> "DB2001_EA".EA[#t_Index].Config_EscaladoMaxIngenieria THEN
	                        "DB2001_EA".EA[#t_Index].Config_EscaladoMaxIngenieria := "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMaxIngenieria;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMaxTarjeta <> "DB2001_EA".EA[#t_Index].Config_EscaladoMaxTarjeta THEN
	                        "DB2001_EA".EA[#t_Index].Config_EscaladoMaxTarjeta := "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMaxTarjeta;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMinIngenieria <> "DB2001_EA".EA[#t_Index].Config_EscaladoMinIngenieria THEN
	                        "DB2001_EA".EA[#t_Index].Config_EscaladoMinIngenieria := "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMinIngenieria;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMinTarjeta <> "DB2001_EA".EA[#t_Index].Config_EscaladoMinTarjeta THEN
	                        "DB2001_EA".EA[#t_Index].Config_EscaladoMinTarjeta := "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoMinTarjeta;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoOffset <> "DB2001_EA".EA[#t_Index].Config_EscaladoOffset THEN
	                        "DB2001_EA".EA[#t_Index].Config_EscaladoOffset := "DB2001_EA".Mux[#for_mux].EA.Config_EscaladoOffset;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_Habilitar <> "DB2001_EA".EA[#t_Index].Config_Habilitar THEN
	                        "DB2001_EA".EA[#t_Index].Config_Habilitar := "DB2001_EA".Mux[#for_mux].EA.Config_Habilitar;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_HabilitarAlarmaMax <> "DB2001_EA".EA[#t_Index].Config_HabilitarAlarmaMax THEN
	                        "DB2001_EA".EA[#t_Index].Config_HabilitarAlarmaMax := "DB2001_EA".Mux[#for_mux].EA.Config_HabilitarAlarmaMax;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_HabilitarAlarmaMin <> "DB2001_EA".EA[#t_Index].Config_HabilitarAlarmaMin THEN
	                        "DB2001_EA".EA[#t_Index].Config_HabilitarAlarmaMin := "DB2001_EA".Mux[#for_mux].EA.Config_HabilitarAlarmaMin;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_TipoAcceso <> "DB2001_EA".EA[#t_Index].Config_TipoAcceso THEN
	                        "DB2001_EA".EA[#t_Index].Config_TipoAcceso := "DB2001_EA".Mux[#for_mux].EA.Config_TipoAcceso;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2001_EA".Mux[#for_mux].EA.Config_HisteresisTipo <> "DB2001_EA".EA[#t_Index].Config_HisteresisTipo THEN
	                        "DB2001_EA".EA[#t_Index].Config_HisteresisTipo := "DB2001_EA".Mux[#for_mux].EA.Config_HisteresisTipo;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2001_EA".Mux[#for_mux].ExisteCambio THEN
	                        
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2001_EA".Mux[#for_mux_cambios].Index THEN
	                                    "DB2001_EA".Mux[#for_mux_cambios].EA := "DB2001_EA".EA[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2001_EA".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la EA[0] que no se usa para escribir el index.
	                "DB2001_EA".Mux[#for_mux].EA := "DB2001_EA".EA[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            //  Multiplexado no habilitado
	            "DB2001_EA".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2001_EA".Mux[#for_mux].Index :=
	            "DB2001_EA".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	        
	    END_FOR;
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2001_EA".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2001_EA".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_EA" DO
	        
	        
	        REGION LIMITE_GRUPO_ALARMA
	            
	            IF "DB2001_EA".EA[#for_i].Config_GrupoAlarma < 0 THEN
	                "DB2001_EA".EA[#for_i].Config_GrupoAlarma := 0;
	            END_IF;
	            IF "DB2001_EA".EA[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                "DB2001_EA".EA[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	            END_IF;
	            
	        END_REGION LIMITE_GRUPO_ALARMA
	        
	        #t_LecturaRealizada := FALSE;
	        #t_ErrorGeneral := FALSE;
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2001_EA".EA[#for_i].Config_Habilitar THEN
	            
	            REGION LECTURA
	                
	                CASE "DB2001_EA".EA[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO_ESCALADO:
	                        REGION LECTURA_VALORES_DE_LA_TARJETA
	                            
	                            IF "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte > 0 THEN
	                                
	                                // =============================================================================
	                                //  LECTURA DE LA SEÑAL DE ENTRADA - PEEK_WORD (area) 16#1 para CPU 1500; 16#81 para CPU 1200
	                                #t_ValorTarjeta := WORD_TO_INT(PEEK_WORD(area := 16#81, dbNumber := 0, byteOffset := "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte));
	                                // =============================================================================
	                                //  COMPROBAMOS LOCALARMASENTE LA LECTURA CORRECTA DE LA ENTRADA ANALOGICA
	                                REGION DESCRIPCION_GET_ERR_ID()
	                                    // La instrucción "Consultar ID de error locALARMASente" consulta si se han producido errores en un bloque. Suele tratarse de un error de acceso.
	                                    // si al ejecutar el bloque el sistema notifica errores de ejecución desde que se ejecutó La instrucción por última vez, la instrucción emite la ID del primer error ocurrido.
	                                    // La ID de error solo se puede guardar en operandos del tipo de datos WORD. Si se producen varios errores en el bloque, la instrucción soluciona el primer error ocurrido,
	                                    // y solo entonces la instrucción emite la ID de error del siguiente error ocurrido.
	                                    // 0      0  Ningún error
	                                    // 2503 9475 Puntero no válido
	                                    // 2520 9504 STRING no válido
	                                    // 2522 9506 Error de lectura: operando fuera del rango válido
	                                    // 2523 9507 Error de escritura: operando fuera del rango válido
	                                    // 2524 9508 Error de lectura: operando no válido
	                                    // 2525 9509 Error de escritura: operando no válido
	                                    // 2528 9512 Error de lectura: alineación de datos
	                                    // 2529 9513 Error de escritura: alineación de datos
	                                    // 252C 9516 Puntero no válido
	                                    // 2530 9520 Error de escritura: Bloque de datos
	                                    // 2533 9523 Referencia usada no válida
	                                    // 2538 9528 Error de acceso: el DB no existe
	                                    // 2539 9529 Error de acceso: se ha utilizado un DB incorrecto
	                                    // 253A 9530 El bloque de datos global no existe
	                                    // 253C 9532 Indicación errónea o la función no existe
	                                    // 253D 9533 La función de sistema no existe
	                                    // 253E 9534 Indicación errónea o el bloque de función no existe
	                                    // 253F 9535 El bloque de sistema no existe
	                                    // 2550 9552 Error de acceso: el DB no existe
	                                    // 2551 9553 Error de acceso: se ha utilizado un DB incorrecto
	                                    // 2575 9589 Error en la profundidad de anidamiento del programa
	                                    // 2576 9590 Error en la distribución de datos locales
	                                    // 2577 9591 La propiedad de bloque "Alimentación de parámetros a través de registros" no está activada.
	                                    // 25A0 9632 Error interno en TP
	                                    // 25A1 9633 Variable protegida contra escritura
	                                    // 25A2 9634 Valor numérico no válido de la variable
	                                    // 2942 10562 Error de lectura: entrada
	                                    // 2943 10563 Error de escritura: salida
	                                END_REGION
	                                
	                                "DB2001_EA".EA[#for_i].Estado_Lectura := GET_ERR_ID();
	                                #t_LecturaRealizada := ("DB2001_EA".EA[#for_i].Estado_Lectura = 0);
	                                "DB2001_EA".EA[#for_i].Estado_ValorTarjeta := #t_ValorTarjeta;
	                            ELSE
	                                
	                                "DB2001_EA".EA[#for_i].Estado_ValorTarjeta := 0;
	                                #t_LecturaRealizada := TRUE;
	                            END_IF;
	                            
	                        END_REGION LECTURA_VALORES_DE_LA_TARJETA
	                        
	                        
	                        REGION CALCULO_VALOR
	                            
	                            IF "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte > 0 THEN
	                                
	                                IF "DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria > "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria AND
	                                    "DB2001_EA".EA[#for_i].Config_EscaladoMaxTarjeta > "DB2001_EA".EA[#for_i].Config_EscaladoMinTarjeta THEN
	                                    
	                                    #t_x0 := INT_TO_REAL("DB2001_EA".EA[#for_i].Config_EscaladoMinTarjeta);
	                                    #t_x1 := INT_TO_REAL("DB2001_EA".EA[#for_i].Config_EscaladoMaxTarjeta);
	                                    #t_x := DINT_TO_REAL("DB2001_EA".EA[#for_i].Estado_ValorTarjeta);
	                                    #t_y0 := "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria;
	                                    #t_y1 := "DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria;
	                                    
	                                    // =============================================================================
	                                    //  DETECCIÓN DE FALLO EN EL CANAL
	                                    IF ("DB2001_EA".EA[#for_i].Estado_ValorTarjeta > -32768) AND ("DB2001_EA".EA[#for_i].Estado_ValorTarjeta < 32767) AND #t_LecturaRealizada THEN
	                                        
	                                        IF ("DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria <> "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria)
	                                            AND
	                                            ("DB2001_EA".EA[#for_i].Config_EscaladoMaxTarjeta <> "DB2001_EA".EA[#for_i].Config_EscaladoMinTarjeta)
	                                        THEN
	                                            "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := ((#t_x - #t_x0) * ((#t_y1 - #t_y0) / (#t_x1 - #t_x0))) + #t_y0;
	                                            
	                                            // =============================================================================
	                                            //  LÍMITES
	                                            IF "DB2001_EA".EA[#for_i].Estado_ValorIngenieria > "DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria THEN
	                                                "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := "DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria;
	                                            END_IF;
	                                            IF "DB2001_EA".EA[#for_i].Estado_ValorIngenieria < "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria THEN
	                                                "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria;
	                                            END_IF;
	                                            
	                                            // =============================================================================
	                                            //  OFFSET
	                                            "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := "DB2001_EA".EA[#for_i].Estado_ValorIngenieria + "DB2001_EA".EA[#for_i].Config_EscaladoOffset;
	                                        ELSE
	                                            "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := 0.0;
	                                        END_IF;
	                                        "DB2001_EA".EA[#for_i].Alarmas_HiloRoto := FALSE;
	                                    ELSE
	                                        "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := 0.0;
	                                        "DB2001_EA".EA[#for_i].Alarmas_HiloRoto := TRUE; //  Error del canal
	                                    END_IF;
	                                ELSE
	                                    "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := 0.0;
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_REGION CALCULO_VALOR
	                        
	                        
	                    #TIPO_ACCESO_INDIRECTO_WORD_SIN_ESCALADO:
	                        REGION LECTURA_VALORES_DE_LA_TARJETA
	                            "DB2001_EA".EA[#for_i].Estado_ValorTarjeta := 0;
	                            
	                            IF "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte > 0 THEN
	                                
	                                // =============================================================================
	                                //  LECTURA DE LA SEÑAL DE ENTRADA - PEEK_WORD (area) 16#1 para CPU 1500; 16#81 para CPU 1200
	                                "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := DINT_TO_REAL(WORD_TO_DINT(PEEK_WORD(area := 16#81, dbNumber := 0, byteOffset := "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte)));
	                                
	                                // =============================================================================
	                                //  COMPROBAMOS LOCALARMASENTE LA LECTURA CORRECTA DE LA ENTRADA ANALOGICA
	                                "DB2001_EA".EA[#for_i].Estado_Lectura := GET_ERR_ID();
	                                #t_LecturaRealizada := ("DB2001_EA".EA[#for_i].Estado_Lectura = 0);
	                            ELSE
	                                "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := 0;
	                                #t_LecturaRealizada := TRUE;
	                            END_IF;
	                        END_REGION LECTURA_VALORES_DE_LA_TARJETA
	                        
	                        
	                    #TIPO_ACCESO_INDIRECTO_DWORD_SIN_ESCALADO:
	                        REGION LECTURA_VALORES_DE_LA_TARJETA
	                            "DB2001_EA".EA[#for_i].Estado_ValorTarjeta := 0;
	                            
	                            IF "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte > 0 THEN
	                                
	                                // =============================================================================
	                                //  LECTURA DE LA SEÑAL DE ENTRADA - PEEK_WORD (area) 16#1 para CPU 1500; 16#81 para CPU 1200
	                                "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := DINT_TO_REAL(DWORD_TO_DINT(PEEK_DWORD(area := 16#81, dbNumber := 0, byteOffset := "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte)));
	                                
	                                // =============================================================================
	                                //  COMPROBAMOS LOCALARMASENTE LA LECTURA CORRECTA DE LA ENTRADA ANALOGICA
	                                "DB2001_EA".EA[#for_i].Estado_Lectura := GET_ERR_ID();
	                                #t_LecturaRealizada := ("DB2001_EA".EA[#for_i].Estado_Lectura = 0);
	                            ELSE
	                                "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := 0;
	                                #t_LecturaRealizada := TRUE;
	                            END_IF;
	                        END_REGION LECTURA_VALORES_DE_LA_TARJETA
	                        
	                        
	                    #TIPO_ACCESO_PLC:
	                        #t_LecturaRealizada := TRUE;
	                        
	                END_CASE;
	                
	            END_REGION LECTURA
	
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                //  FORZADO DE LA SEÑAL
	                IF "DB2001_EA".EA[#for_i].Estado_AutoMan THEN
	                    "DB2001_EA".Agrup["DB2001_EA".EA[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := "DB2001_EA".EA[#for_i].Orden_ConsignaManual;
	                ELSE
	                    "DB2001_EA".EA[#for_i].Orden_ConsignaManual := "DB2001_EA".EA[#for_i].Estado_ValorIngenieria;
	                END_IF;
	                
	                
	            END_REGION
	            
	            
	            REGION ERRORES
	                
	                #t_SubError := "DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria - "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria;
	                // =============================================================================
	                //  ALARMA NIVEL MÍNIMO
	                IF "DB2001_EA".EA[#for_i].Config_HabilitarAlarmaMin THEN
	                    IF "DB2001_EA".EA[#for_i].Estado_ValorIngenieria < "DB2001_EA".EA[#for_i].Config_ErrorMinIngenieria THEN
	                        "DB2001_EA".EA[#for_i].Alarmas_Min := TRUE;
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  RESET DE ALARMA CON HISTÉRESIS EN UNIDADES DE INGENIERÍA
	                    IF NOT ("DB2001_EA".EA[#for_i].Config_HisteresisTipo) AND ("DB2001_EA".EA[#for_i].Estado_ValorIngenieria >= ("DB2001_EA".EA[#for_i].Config_ErrorMinIngenieria + "DB2001_EA".EA[#for_i].Config_ErrorMinHisteresis)) THEN
	                        "DB2001_EA".EA[#for_i].Alarmas_Min := FALSE;
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  RESET DE ALARMA CON HISTÉRESIS EN %
	                    IF "DB2001_EA".EA[#for_i].Config_HisteresisTipo AND ("DB2001_EA".EA[#for_i].Estado_ValorIngenieria >= "DB2001_EA".EA[#for_i].Config_ErrorMinIngenieria + ("DB2001_EA".EA[#for_i].Config_ErrorMinHisteresis / 100.0) * #t_SubError) THEN
	                        "DB2001_EA".EA[#for_i].Alarmas_Min := FALSE;
	                    END_IF;
	                ELSE
	                    "DB2001_EA".EA[#for_i].Alarmas_Min := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ALARMA NIVEL MÁXIMO
	                IF "DB2001_EA".EA[#for_i].Config_HabilitarAlarmaMax THEN
	                    IF "DB2001_EA".EA[#for_i].Estado_ValorIngenieria > "DB2001_EA".EA[#for_i].Config_ErrorMaxIngenieria THEN
	                        "DB2001_EA".EA[#for_i].Alarmas_Max := TRUE;
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  RESET DE ALARMA CON HISTÉRESIS EN UNIDADES DE INGENIERÍA
	                    IF NOT ("DB2001_EA".EA[#for_i].Config_HisteresisTipo) AND ("DB2001_EA".EA[#for_i].Estado_ValorIngenieria <= ("DB2001_EA".EA[#for_i].Config_ErrorMaxIngenieria - "DB2001_EA".EA[#for_i].Config_ErrorMaxHisteresis)) THEN
	                        "DB2001_EA".EA[#for_i].Alarmas_Max := FALSE;
	                    END_IF;
	                    
	                    // =============================================================================
	                    //  RESET DE ALARMA CON HISTÉRESIS EN %
	                    IF "DB2001_EA".EA[#for_i].Config_HisteresisTipo AND ("DB2001_EA".EA[#for_i].Estado_ValorIngenieria <= "DB2001_EA".EA[#for_i].Config_ErrorMaxIngenieria - ("DB2001_EA".EA[#for_i].Config_ErrorMaxHisteresis / 100.0) * #t_SubError) THEN
	                        "DB2001_EA".EA[#for_i].Alarmas_Max := FALSE;
	                    END_IF;
	                ELSE
	                    "DB2001_EA".EA[#for_i].Alarmas_Max := FALSE;
	                END_IF;
	                
	                #t_ErrorGeneral := "DB2001_EA".EA[#for_i].Alarmas_HiloRoto OR "DB2001_EA".EA[#for_i].Alarmas_Max OR "DB2001_EA".EA[#for_i].Alarmas_Min;
	                "DB2001_EA".EA[#for_i].Alarmas_General := #t_ErrorGeneral;
	                
	                IF #t_ErrorGeneral THEN
	                    "DB2001_EA".Agrup["DB2001_EA".EA[#for_i].Config_GrupoAlarma].AlgunaAlarma := TRUE;
	                END_IF;
	                
	                
	                "DB2001_EA".EA[#for_i].Alarmas_Lectura := NOT #t_LecturaRealizada;
	                
	                
	            END_REGION
	            
	            
	            REGION ESTADO
	                
	                //  Estado normal
	                "DB2001_EA".EA[#for_i].Aux_Estado := 1;
	                
	                //  Error de configuración
	                IF ("DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria = "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria) OR
	                    ("DB2001_EA".EA[#for_i].Config_EscaladoMaxTarjeta = "DB2001_EA".EA[#for_i].Config_EscaladoMinTarjeta)
	                THEN
	                    "DB2001_EA".EA[#for_i].Aux_Estado := 6; 
	                END_IF;
	                
	                //  Error de configuración
	                IF ("DB2001_EA".EA[#for_i].Config_EscaladoMaxIngenieria < "DB2001_EA".EA[#for_i].Config_EscaladoMinIngenieria) OR
	                    ("DB2001_EA".EA[#for_i].Config_EscaladoMaxTarjeta < "DB2001_EA".EA[#for_i].Config_EscaladoMinTarjeta)
	                THEN
	                    "DB2001_EA".EA[#for_i].Aux_Estado := 6;
	                END_IF;
	                
	                //  Error del canal
	                IF "DB2001_EA".EA[#for_i].Config_TipoAcceso = #TIPO_ACCESO_INDIRECTO_ESCALADO AND
	                    ("DB2001_EA".EA[#for_i].Estado_ValorTarjeta <= -32766) OR
	                    ("DB2001_EA".EA[#for_i].Estado_ValorTarjeta >= 32766)
	                THEN
	                    "DB2001_EA".EA[#for_i].Aux_Estado := 3;
	                END_IF;
	                
	                //  Señal en alarma
	                IF "DB2001_EA".EA[#for_i].Config_HabilitarAlarmaMin THEN
	                    IF "DB2001_EA".EA[#for_i].Estado_ValorIngenieria < "DB2001_EA".EA[#for_i].Config_ErrorMinIngenieria
	                    THEN
	                        "DB2001_EA".EA[#for_i].Aux_Estado := 4;
	                    END_IF;
	                END_IF;
	                
	                //  Señal en alarma
	                IF "DB2001_EA".EA[#for_i].Config_HabilitarAlarmaMax THEN
	                    IF "DB2001_EA".EA[#for_i].Estado_ValorIngenieria > "DB2001_EA".EA[#for_i].Config_ErrorMaxIngenieria
	                    THEN
	                        "DB2001_EA".EA[#for_i].Aux_Estado := 5;
	                    END_IF;
	                END_IF;
	                
	                //  Error de lectura
	                IF NOT #t_LecturaRealizada THEN
	                    "DB2001_EA".EA[#for_i].Aux_Estado := 7;
	                END_IF;
	                
	                // EA no direccionada
	                IF ("DB2001_EA".EA[#for_i].Config_TipoAcceso = #TIPO_ACCESO_INDIRECTO_ESCALADO  OR "DB2001_EA".EA[#for_i].Config_TipoAcceso = #TIPO_ACCESO_INDIRECTO_ESCALADO)
	                    AND
	                    "DB2001_EA".EA[#for_i].Config_DireccionEntradaByte <= 0
	                THEN
	                    "DB2001_EA".EA[#for_i].Aux_Estado := 8;
	                END_IF;
	                
	                //  Señal forzada
	                IF "DB2001_EA".EA[#for_i].Estado_AutoMan THEN
	                    "DB2001_EA".EA[#for_i].Aux_Estado := 2;
	                END_IF;
	                
	            END_REGION
	            
	            
	            REGION TRAZABILIDAD
	                
	                IF "DB2001_EA".EA[#for_i].Estado_AutoMan AND NOT "DB2001_EA".EA[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_11_DISP_EA",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_EA",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2001_EA".EA[#for_i].Estado_AutoMan AND "DB2001_EA".EA[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_11_DISP_EA",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_EA",
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
	            "DB2001_EA".EA[#for_i].Aux_oldAutoMan := "DB2001_EA".EA[#for_i].Estado_AutoMan;
	            
	        ELSE
	            // =============================================================================
	            // DISPOSITIVO NO HABILITADO
	            // =============================================================================
	            "DB2001_EA".EA[#for_i].Estado_ValorTarjeta := 0;
	            "DB2001_EA".EA[#for_i].Hmi_Estado := 0;   //  Canal deshabilitado
	            "DB2001_EA".EA[#for_i].Aux_Estado := 0;   //  Canal deshabilitado
	            "DB2001_EA".EA[#for_i].Estado_ValorIngenieria := 0.0;
	            "DB2001_EA".EA[#for_i].Alarmas_Max := FALSE;
	            "DB2001_EA".EA[#for_i].Alarmas_Min := FALSE;
	            "DB2001_EA".EA[#for_i].Alarmas_HiloRoto := FALSE;
	            "DB2001_EA".EA[#for_i].Alarmas_General := FALSE;
	            "DB2001_EA".EA[#for_i].Estado_AutoMan := FALSE;
	            
	        END_IF;
	        
	        REGION GESTION_HMI
	            
	            // =============================================================================
	            //  GESTION BITS PARA VISUALIZACION
	            //  Bit     0   Habilitacion
	            //  Bit     1   ManualAutomatico
	            //  Bit     2   Reserva
	            //  Bit     3   Reserva
	            //  Bit     4   Reserva
	            //  Bit     5   Reserva
	            //  Bit     6   Reserva
	            //  Bit     7   Reserva
	            //  Bit     8   Alarma Hilo Roto
	            //  Bit     9   Alarma Alta
	            //  Bit     10  Alarma Baja
	            //  Bit     11  Alarma 3
	            //  Bit     12  Alarma 4
	            //  Bit     13  Alarma 5
	            //  Bit     14  Reserva
	            //  Bit     15  Reserva
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X0 := "DB2001_EA".EA[#for_i].Config_Habilitar;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X1 := "DB2001_EA".EA[#for_i].Estado_AutoMan;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X2 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X3 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X4 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X8 := "DB2001_EA".EA[#for_i].Alarmas_HiloRoto;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X9 := "DB2001_EA".EA[#for_i].Alarmas_Max;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X10 := "DB2001_EA".EA[#for_i].Alarmas_Min;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X13 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2001_EA".EA[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION
	        
	        REGION GESTION_NUEVA_ALARMA
	            
	            // =============================================================================
	            //  DETECCION DE NUEVA ALARMA
	            IF "DB2001_EA".EA[#for_i].Alarmas_General AND NOT "DB2001_EA".EA[#for_i].Aux_oldAlarma THEN
	                "DB2001_EA".Agrup["DB2001_EA".EA[#for_i].Config_GrupoAlarma].NuevaAlarma := TRUE;
	            END_IF;
	            
	            //  Estado anterior de las alarmas
	            "DB2001_EA".EA[#for_i].Aux_oldAlarma := "DB2001_EA".EA[#for_i].Alarmas_General;
	            
	        END_REGION
	        
	    END_FOR;
	    
	    
	    // =============================================================================
	    //  ACUSE DE NUEVAS ALARMAS
	    IF #Ack THEN
	        FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	            "DB2001_EA".Agrup[#for_i].NuevaAlarma := FALSE;
	        END_FOR;
	    END_IF;
	    
	END_REGION
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>