---
title: FC2015_ZC_M
---
# FC FC2015_ZC_M

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Motor arranque directo.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se gestiona el estado del dispositivo
    - Se gestiona el tiempo en marcha
    - Se gestiona la orden de escritura
    - Se gestiona la trazabilidad de las manualizaciones del dispositivo

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **FC:** [FC15025_ZC_CONTADOR_TIEMPO](../Bloques de codigo/FC15025_ZC_CONTADOR_TIEMPO.md)
    **DB:** [DB2015_DISP_M](../Estructura de datos/DB2015_DISP_M.md)
    **DB:** [ZC_DISP_M](../Estructura de datos/ZC_DISP_M.md)
    **DB:** [ZC_DISP_MUX_M](../Estructura de datos/ZC_DISP_MUX_M.md)
    **DB:** [ZC_CONTADOR_TIEMPO](../Estructura de datos/ZC_CONTADOR_TIEMPO.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1seg` | `Bool` | - | `-` | Pulso de 1 segundo |
| `Simulacion` | `Bool` | - | `-` | Simulacion |
| `Arranque` | `Bool` | - | `-` | Primer arranque |
| `Ack` | `Bool` | - | `-` | Acuse general |
| `SeguridadesOK` | `Bool` | - | `-` | Seguridades OK |
| `UsuarioActual` | `String` | - | `-` | Usuario actual |
| `FechaHoraActual` | `DTL` | - | `-` | Fecha y hora actual |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |
| `for_mux` | `Int` | - | `-` | - |
| `t_ErrorTermico` | `Bool` | - | `-` | - |
| `t_Index` | `Int` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TIPO_ACCESO_INDIRECTO` | `SInt` | - | `0` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2015_ZC_M" : Void
TITLE = FC2015_M
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo motor
   VAR_INPUT 
      Pulso1seg : Bool;   // Pulso de 1 segundo
      Simulacion : Bool;   // Simulacion
      Arranque : Bool;   // Primer arranque
      Ack : Bool;   // Acuse general
      SeguridadesOK : Bool;   // Seguridades OK
      UsuarioActual : String;   // Usuario actual
      FechaHoraActual {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
   END_VAR

   VAR_TEMP 
      for_i : Int;
      for_mux_cambios : Int;
      for_mux : Int;
      t_Activar : Bool;
      t_ErrorTermico : Bool;
      t_ErrorConfMarcha : Bool;
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
	
	Funcion para la gestion de dispositivo de tipo Motor arranque directo.
	
	En ella se realizan las siguientes acciones:
	
	- Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
	- Se gestiona el estado del dispositivo
	- Se gestiona el tiempo en marcha
	- Se gestiona la orden de escritura
	- Se gestiona la trazabilidad de las manualizaciones del dispositivo
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC8_ZC_TRAZA_REGISTRO`, `FC15025_ZC_CONTADOR_TIEMPO` |
	| FB   | - |
	| DB   | `DB2015_DISP_M` |
	| UDT  | `ZC_DISP_M`, `ZC_DISP_MUX_M`, `ZC_CONTADOR_TIEMPO` |
	
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.01  | 15.10.2020 | (ABH)   | Primera version.
	| 00.00.02  | 28.11.2020 | (ABH)   | Añadidas alarmas mantenimiento
	| 00.00.03  | 26.10.2021 | (ABH)   | Se integra la gestion de directo/inverso
	| 00.00.04  | 26.04.2022 | (HCR)   | Cambio en la organizacion del UDT. Se organiza en estructuras en base al tipo de funcion que realizan los datos. Se quita el enclavamiento para orden manual.
	| 00.00.05  | 27.04.2022 | (ABH)   | Se añaden auxiliares de estado anterior del modo manual y automatico para poder registrar las trazas.  
	| 00.00.06  | 27.04.2022 | (HCR)   | Si no esta habilitado se quita orden manual y se quita el estado manual. Se agrega Ack para alarmas de confirmación de marcha. Se mantiene el estado cuando se pasa a manual. Cambio en lógica de errores. Cambio en la escritura de la salida. Cambio en laógica de modos
	| 00.00.07  | 08.11.2022 | (ABH)   | Se añade trazabilidad manualizaciones
	| 00.00.08  | 08.11.2022 | (HCR)   | Se añade trazabilidad de activación manual
	| 00.00.09  | 08.11.2022 | (HCR)   | Cambio lógica enclavamiento
	| 00.00.10  | 18.09.2023 | (ABH)   | Cambio en tipo de dato de horas de alarma. Se utiliza el tipo de dato ZC_CONTADOR_TIEMPO y el FC15025_ZC_CONTADOR_TIEMPO
	| 00.00.11  | 22.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado)
	| 00.00.12  | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado Se añade movimiento de M[0] a multiplexado en caso de que el indice sea 0. 
	| 00.00.13  | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores.
	| 00.00.14  | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro.
	| 00.00.15  | 24.04.2025 | (HCR)   | Se añade gestion de idioma 
	| 00.00.16  | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion.
	| 00.00.17  | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT. Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision.
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2015_M".Mux[#for_mux].Index :=
	            "DB2015_M".Mux[#for_mux].oldIndex := 0;
	        END_FOR;
	        RETURN;
	    END_IF;
	    
	    //  ===========================================================================================================
	    //  Gestion de multiplexado
	    FOR #for_mux := 0 TO "N_MAX_MUX_DISP"DO
	        
	        //  ===============================================================================================================
	        //  Antes de iniciar la logica del multiplexado, revisamos los limites
	        REGION LIMITES
	            
	            //  ===========================================================================================================
	            //  Limites
	            IF "DB2015_M".Mux[#for_mux].Index < 0 THEN
	                "DB2015_M".Mux[#for_mux].Index := 0;
	            END_IF;
	            IF "DB2015_M".Mux[#for_mux].Index > "N_MAX_DISP_M" THEN
	                "DB2015_M".Mux[#for_mux].Index := "N_MAX_DISP_M";
	            END_IF;
	            IF "DB2015_M".Mux[#for_mux].Index >= "N_MAX_DISP_M" THEN
	                "DB2015_M".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2015_M".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2015_M".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2015_M".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2015_M".Mux[#for_mux].oldIndex := #t_Index;
	        
	        IF "DB2015_M".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2015_M".Mux[#for_mux].M := "DB2015_M".M[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2015_M".Mux[#for_mux].M.Hmi_Estado := "DB2015_M".M[#t_Index].Hmi_Estado;
	                    "DB2015_M".Mux[#for_mux].M.Estado_SeguridadOk :=  "DB2015_M".M[#for_i].Estado_SeguridadOk;
	                    IF NOT "DB2015_M".M[#t_Index].Estado_AutoMan THEN
	                        "DB2015_M".Mux[#for_mux].M.Orden_ActivarManual := "DB2015_M".M[#t_Index].Orden_ActivarManual;
	                    ELSE
	                        IF NOT #SeguridadesOK OR NOT "DB2015_M".Mux[#for_mux].M.Estado_SeguridadOk OR "DB2015_M".M[#t_Index].Alarmas_Termico THEN
	                            "DB2015_M".Mux[#for_mux].M.Orden_ActivarManual :=
	                            "DB2015_M".M[#t_Index].Orden_ActivarManual := FALSE;
	                        END_IF;
	                    END_IF;
	                    "DB2015_M".Mux[#for_mux].M.Estado_Activado := "DB2015_M".M[#t_Index].Estado_Activado;
	                    "DB2015_M".Mux[#for_mux].M.Estado_Enclavado := "DB2015_M".M[#t_Index].Estado_Enclavado;
	                    "DB2015_M".Mux[#for_mux].M.Estado_Salida := "DB2015_M".M[#t_Index].Estado_Salida;
	                    "DB2015_M".Mux[#for_mux].M.Estado_EntradaTermico := "DB2015_M".M[#t_Index].Estado_EntradaTermico;
	                    "DB2015_M".Mux[#for_mux].M.Estado_EntradaConfMarcha := "DB2015_M".M[#t_Index].Estado_EntradaConfMarcha;
	                    "DB2015_M".Mux[#for_mux].M.Alarmas_ConfirmacionMarcha := "DB2015_M".M[#t_Index].Alarmas_ConfirmacionMarcha;
	                    "DB2015_M".Mux[#for_mux].M.Alarmas_General := "DB2015_M".M[#t_Index].Alarmas_General;
	                    "DB2015_M".Mux[#for_mux].M.Alarmas_Mantenimiento := "DB2015_M".M[#t_Index].Alarmas_Mantenimiento;
	                    "DB2015_M".Mux[#for_mux].M.Alarmas_Termico := "DB2015_M".M[#t_Index].Alarmas_Termico;
	                    "DB2015_M".Mux[#for_mux].M.Orden_ActivarAuto := "DB2015_M".M[#t_Index].Orden_ActivarAuto;
	                    "DB2015_M".Mux[#for_mux].M.Tiempos_Alarma := "DB2015_M".M[#t_Index].Tiempos_Alarma;
	                    "DB2015_M".Mux[#for_mux].M.Tiempos_Mantenimiento := "DB2015_M".M[#t_Index].Tiempos_Mantenimiento;
	                    "DB2015_M".Mux[#for_mux].M.Aux_oldActivado := "DB2015_M".M[#t_Index].Aux_oldActivado;
	                    "DB2015_M".Mux[#for_mux].M.Aux_oldAlarma := "DB2015_M".M[#t_Index].Aux_oldAlarma;
	                    "DB2015_M".Mux[#for_mux].M.Aux_oldAutoMan := "DB2015_M".M[#t_Index].Aux_oldAutoMan;
	                    "DB2015_M".Mux[#for_mux].M.Config_GrupoAlarma := "DB2015_M".M[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2015_M".Mux[#for_mux].ExisteCambio := false;
	
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2015_M".Mux[#for_mux].M.Estado_AutoMan <> "DB2015_M".M[#t_Index].Estado_AutoMan THEN
	                        "DB2015_M".M[#t_Index].Estado_AutoMan := "DB2015_M".Mux[#for_mux].M.Estado_AutoMan;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2015_M".Mux[#for_mux].M.Orden_ActivarManual <> "DB2015_M".M[#t_Index].Orden_ActivarManual THEN
	                        "DB2015_M".M[#t_Index].Orden_ActivarManual := "DB2015_M".Mux[#for_mux].M.Orden_ActivarManual;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Orden_ResetHoras <> "DB2015_M".M[#t_Index].Orden_ResetHoras THEN
	                        "DB2015_M".M[#t_Index].Orden_ResetHoras := "DB2015_M".Mux[#for_mux].M.Orden_ResetHoras;
	                        "DB2015_M".Mux[#for_mux].M.Orden_ResetHoras := FALSE;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2015_M".Mux[#for_mux].M.Config_DireccionRetConfMarchaBit <> "DB2015_M".M[#t_Index].Config_DireccionRetConfMarchaBit THEN
	                        "DB2015_M".M[#t_Index].Config_DireccionRetConfMarchaBit := "DB2015_M".Mux[#for_mux].M.Config_DireccionRetConfMarchaBit;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_DireccionRetConfMarchaByte <> "DB2015_M".M[#t_Index].Config_DireccionRetConfMarchaByte THEN
	                        "DB2015_M".M[#t_Index].Config_DireccionRetConfMarchaByte := "DB2015_M".Mux[#for_mux].M.Config_DireccionRetConfMarchaByte;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_DireccionRetTermicoBit <> "DB2015_M".M[#t_Index].Config_DireccionRetTermicoBit THEN
	                        "DB2015_M".M[#t_Index].Config_DireccionRetTermicoBit := "DB2015_M".Mux[#for_mux].M.Config_DireccionRetTermicoBit;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_DireccionRetTermicoByte <> "DB2015_M".M[#t_Index].Config_DireccionRetTermicoByte THEN
	                        "DB2015_M".M[#t_Index].Config_DireccionRetTermicoByte := "DB2015_M".Mux[#for_mux].M.Config_DireccionRetTermicoByte;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_DireccionSalidaBit <> "DB2015_M".M[#t_Index].Config_DireccionSalidaBit THEN
	                        "DB2015_M".M[#t_Index].Config_DireccionSalidaBit := "DB2015_M".Mux[#for_mux].M.Config_DireccionSalidaBit;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_DireccionSalidaByte <> "DB2015_M".M[#t_Index].Config_DireccionSalidaByte THEN
	                        "DB2015_M".M[#t_Index].Config_DireccionSalidaByte := "DB2015_M".Mux[#for_mux].M.Config_DireccionSalidaByte;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_Habilitar <> "DB2015_M".M[#t_Index].Config_Habilitar THEN
	                        "DB2015_M".M[#t_Index].Config_Habilitar := "DB2015_M".Mux[#for_mux].M.Config_Habilitar;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_HabilitarInvertirConfMarcha <> "DB2015_M".M[#t_Index].Config_HabilitarInvertirConfMarcha THEN
	                        "DB2015_M".M[#t_Index].Config_HabilitarInvertirConfMarcha := "DB2015_M".Mux[#for_mux].M.Config_HabilitarInvertirConfMarcha;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_HabilitarInvertirTermico <> "DB2015_M".M[#t_Index].Config_HabilitarInvertirTermico THEN
	                        "DB2015_M".M[#t_Index].Config_HabilitarInvertirTermico := "DB2015_M".Mux[#for_mux].M.Config_HabilitarInvertirTermico;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_HabilitarMantenimiento <> "DB2015_M".M[#t_Index].Config_HabilitarMantenimiento THEN
	                        "DB2015_M".M[#t_Index].Config_HabilitarMantenimiento := "DB2015_M".Mux[#for_mux].M.Config_HabilitarMantenimiento;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_HabilitarRetornoConfMarcha <> "DB2015_M".M[#t_Index].Config_HabilitarRetornoConfMarcha THEN
	                        "DB2015_M".M[#t_Index].Config_HabilitarRetornoConfMarcha := "DB2015_M".Mux[#for_mux].M.Config_HabilitarRetornoConfMarcha;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_HabilitarRetornoTermico <> "DB2015_M".M[#t_Index].Config_HabilitarRetornoTermico THEN
	                        "DB2015_M".M[#t_Index].Config_HabilitarRetornoTermico := "DB2015_M".Mux[#for_mux].M.Config_HabilitarRetornoTermico;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Config_TipoAcceso <> "DB2015_M".M[#t_Index].Config_TipoAcceso THEN
	                        "DB2015_M".M[#t_Index].Config_TipoAcceso := "DB2015_M".Mux[#for_mux].M.Config_TipoAcceso;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Tiempos
	                    IF "DB2015_M".Mux[#for_mux].M.Tiempos_SetPointTiempoAlarma <> "DB2015_M".M[#t_Index].Tiempos_SetPointTiempoAlarma THEN
	                        "DB2015_M".M[#t_Index].Tiempos_SetPointTiempoAlarma := "DB2015_M".Mux[#for_mux].M.Tiempos_SetPointTiempoAlarma;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2015_M".Mux[#for_mux].M.Tiempos_SetPointMantenimiento <> "DB2015_M".M[#t_Index].Tiempos_SetPointMantenimiento THEN
	                        "DB2015_M".M[#t_Index].Tiempos_SetPointMantenimiento := "DB2015_M".Mux[#for_mux].M.Tiempos_SetPointMantenimiento;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2015_M".Mux[#for_mux].ExisteCambio THEN
	                        
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2015_M".Mux[#for_mux_cambios].Index THEN
	                                    "DB2015_M".Mux[#for_mux_cambios].M := "DB2015_M".M[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2015_M".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la M[0] que no se usa para escribir el index.
	                "DB2015_M".Mux[#for_mux].M := "DB2015_M".M[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            "DB2015_M".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2015_M".Mux[#for_mux].Index := 
	            "DB2015_M".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	        
	    END_FOR;
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2015_M".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2015_M".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_M" DO
	        
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2015_M".M[#for_i].Config_Habilitar THEN
	            
	            REGION LIMITE_GRUPO_ALARMA
	                
	                IF "DB2015_M".M[#for_i].Config_GrupoAlarma < 0 THEN
	                    "DB2015_M".M[#for_i].Config_GrupoAlarma := 0;
	                END_IF;
	                IF "DB2015_M".M[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                    "DB2015_M".M[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	                END_IF;
	                
	            END_REGION LIMITE_GRUPO_ALARMA
	            
	            // =============================================================================
	            //  PUESTA A CERO DE LA SALIDA
	            #t_Activar := FALSE;
	            
	            REGION LECTURA_VALORES
	                
	                CASE "DB2015_M".M[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        (* AREA: Pueden seleccionarse las siguientes áreas: 16#81: Input, 16#82: Output, 16#83: Marcas, 16#84: DB, 16#1: Entrada de periferia (solo S7-1500)
	                        DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                        BYTEOFFSET: Dirección en la que se lee. Solo se utilizan los 16 bits menos significativos.*)
	                        
	                        // =============================================================================
	                        // RETORNO TERMICO
	                        IF "DB2015_M".M[#for_i].Config_DireccionRetTermicoByte >= 0 THEN
	                            "DB2015_M".M[#for_i].Estado_EntradaTermico := PEEK_BOOL(area := 16#81,
	                                                                                    dbNumber := 0,
	                                                                                    byteOffset := "DB2015_M".M[#for_i].Config_DireccionRetTermicoByte,
	                                                                                    bitOffset := "DB2015_M".M[#for_i].Config_DireccionRetTermicoBit);
	                            IF "DB2015_M".M[#for_i].Config_HabilitarInvertirTermico THEN
	                                "DB2015_M".M[#for_i].Estado_EntradaTermico := NOT (PEEK_BOOL(area := 16#81,
	                                                                                             dbNumber := 0,
	                                                                                             byteOffset := "DB2015_M".M[#for_i].Config_DireccionRetTermicoByte,
	                                                                                             bitOffset := "DB2015_M".M[#for_i].Config_DireccionRetTermicoBit));
	                            END_IF;
	                        END_IF;
	                        
	                        // =============================================================================
	                        // RETORNO CONFIRMACION DE MARCHA
	                        IF "DB2015_M".M[#for_i].Config_DireccionRetConfMarchaByte >= 0 THEN
	                            "DB2015_M".M[#for_i].Estado_EntradaConfMarcha := PEEK_BOOL(area := 16#81,
	                                                                                       dbNumber := 0,
	                                                                                       byteOffset := "DB2015_M".M[#for_i].Config_DireccionRetConfMarchaByte,
	                                                                                       bitOffset := "DB2015_M".M[#for_i].Config_DireccionRetConfMarchaBit);
	                            IF "DB2015_M".M[#for_i].Config_HabilitarInvertirConfMarcha THEN
	                                "DB2015_M".M[#for_i].Estado_EntradaConfMarcha := NOT (PEEK_BOOL(area := 16#81,
	                                                                                                dbNumber := 0,
	                                                                                                byteOffset := "DB2015_M".M[#for_i].Config_DireccionRetConfMarchaByte,
	                                                                                                bitOffset := "DB2015_M".M[#for_i].Config_DireccionRetConfMarchaBit));
	                            END_IF;
	                        END_IF;
	                        
	                        
	                    #TIPO_ACCESO_PLC:
	                        ;
	                        
	                END_CASE;
	                
	            END_REGION LECTURA_VALORES
	            
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                //  MODO MANUAL
	                IF "DB2015_M".M[#for_i].Estado_AutoMan THEN
	                    "DB2015_M".Agrup["DB2015_M".M[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    IF "DB2015_M".M[#for_i].Orden_ActivarManual = TRUE AND #SeguridadesOK AND "DB2015_M".M[#for_i].Estado_SeguridadOk AND NOT "DB2015_M".M[#for_i].Alarmas_Termico THEN // En caso de enclavar manual NOT "DB2036_TMF1_DISP_M".M[#i].Estado_Enclavado
	                        #t_Activar := TRUE;
	                    ELSE
	                        #t_Activar := FALSE;
	                        "DB2015_M".M[#for_i].Orden_ActivarManual := FALSE;
	                    END_IF;
	                ELSE
	                    "DB2015_M".M[#for_i].Orden_ActivarManual := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  MODO AUTO
	                IF NOT "DB2015_M".M[#for_i].Estado_AutoMan THEN
	                    IF "DB2015_M".M[#for_i].Orden_ActivarAuto = TRUE AND NOT "DB2015_M".M[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2015_M".M[#for_i].Estado_SeguridadOk AND NOT "DB2015_M".M[#for_i].Alarmas_Termico THEN
	                        #t_Activar := TRUE;
	                    ELSE
	                        #t_Activar := FALSE;
	                    END_IF;
	                    
	                    "DB2015_M".M[#for_i].Orden_ActivarManual := "DB2015_M".M[#for_i].Estado_Activado;
	                END_IF;
	                
	            END_REGION MODOS_DE_TRABAJO
	            
	            
	            REGION ESTADO_DEL_DISPOSITIVO
	                
	                // =============================================================================
	                //  MOTOR SIMULADO
	                IF #Simulacion THEN
	                    
	                    IF #t_Activar THEN
	                        "DB2015_M".M[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2015_M".M[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR RETORNO TERMICO Y CONFIRMACION DE MARCHA
	                IF NOT #Simulacion AND "DB2015_M".M[#for_i].Config_HabilitarRetornoTermico
	                    AND "DB2015_M".M[#for_i].Config_HabilitarRetornoConfMarcha
	                THEN
	                    
	                    IF NOT "DB2015_M".M[#for_i].Estado_EntradaTermico AND "DB2015_M".M[#for_i].Estado_EntradaConfMarcha THEN
	                        "DB2015_M".M[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2015_M".M[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR RETORNO SOLO TERMICO
	                IF NOT #Simulacion AND "DB2015_M".M[#for_i].Config_HabilitarRetornoTermico
	                    AND NOT "DB2015_M".M[#for_i].Config_HabilitarRetornoConfMarcha THEN
	                    
	                    IF NOT "DB2015_M".M[#for_i].Estado_EntradaTermico AND #t_Activar THEN
	                        "DB2015_M".M[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2015_M".M[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR RETORNO SOLO CONFIRMACION DE MARCHA
	                IF NOT #Simulacion AND NOT "DB2015_M".M[#for_i].Config_HabilitarRetornoTermico
	                    AND "DB2015_M".M[#for_i].Config_HabilitarRetornoConfMarcha THEN
	                    
	                    IF "DB2015_M".M[#for_i].Estado_EntradaConfMarcha THEN
	                        "DB2015_M".M[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2015_M".M[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR SIN RETORNOS
	                IF NOT (#Simulacion) AND NOT ("DB2015_M".M[#for_i].Config_HabilitarRetornoTermico)
	                    AND NOT ("DB2015_M".M[#for_i].Config_HabilitarRetornoConfMarcha) THEN
	                    
	                    IF #t_Activar THEN
	                        "DB2015_M".M[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2015_M".M[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	            END_REGION ESTADO_DEL_DISPOSITIVO
	            
	            
	            REGION ERRORES
	                
	                // =============================================================================
	                //  CHEQUEO RETORNO TERMICO
	                IF NOT #Simulacion AND "DB2015_M".M[#for_i].Config_HabilitarRetornoTermico
	                    AND "DB2015_M".M[#for_i].Estado_EntradaTermico THEN
	                    #t_ErrorTermico := TRUE;
	                ELSE
	                    #t_ErrorTermico := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  CHEQUEO RETORNO CONFIRMACION DE MARCHA
	                IF NOT #Simulacion AND "DB2015_M".M[#for_i].Config_HabilitarRetornoConfMarcha AND 
	                    (
	                    (#t_Activar AND NOT "DB2015_M".M[#for_i].Estado_EntradaConfMarcha)
	                    OR
	                    (NOT #t_Activar AND "DB2015_M".M[#for_i].Estado_EntradaConfMarcha)
	                    ) THEN
	                    #t_ErrorConfMarcha := TRUE;
	                ELSE
	                    #t_ErrorConfMarcha := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  TEMPORIZADO DE ERRORES
	                IF "DB2015_M".M[#for_i].Config_HabilitarRetornoConfMarcha
	                    AND #t_ErrorConfMarcha
	                    AND NOT "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha
	                    AND NOT "DB2015_M".M[#for_i].Alarmas_Termico
	                THEN
	                    IF NOT #Simulacion AND #Pulso1seg THEN
	                        "DB2015_M".M[#for_i].Tiempos_Alarma += 1;
	                    END_IF;
	                ELSE
	                    "DB2015_M".M[#for_i].Tiempos_Alarma := 0;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR TERMICO
	                IF #t_ErrorTermico THEN
	                    "DB2015_M".M[#for_i].Alarmas_Termico := TRUE;
	                END_IF;
	                IF NOT #t_ErrorTermico THEN
	                    "DB2015_M".M[#for_i].Alarmas_Termico := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR CONFIRMACION DE MARCHA
	                IF "DB2015_M".M[#for_i].Tiempos_Alarma >= "DB2015_M".M[#for_i].Tiempos_SetPointTiempoAlarma AND #t_ErrorConfMarcha THEN
	                    "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha := TRUE;
	                END_IF;
	                IF NOT #t_ErrorConfMarcha THEN
	                    "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR GLOBAL
	                IF  "DB2015_M".M[#for_i].Alarmas_Termico OR
	                    "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha
	                THEN
	                    "DB2015_M".M[#for_i].Alarmas_General := TRUE;
	                END_IF;
	                IF #Ack AND
	                    NOT "DB2015_M".M[#for_i].Alarmas_Termico AND
	                    NOT "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha
	                THEN
	                    "DB2015_M".M[#for_i].Alarmas_General := FALSE;
	                END_IF;
	                //"DB2015_M".M[#for_i].Alarmas_General := "DB2015_M".M[#for_i].Alarmas_Termico OR "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha;
	                
	                IF "DB2015_M".M[#for_i].Alarmas_General THEN
	                    "DB2015_M".Agrup["DB2015_M".M[#for_i].Config_GrupoAlarma].AlgunaAlarma := TRUE;
	                END_IF;
	                
	            END_REGION ERRORES
	            
	            
	            REGION DIAGNOSIS
	                
	                //  =============================================================================
	                //  CONTADOR DE HORAS DE FUNCIONAMIENTO
	                IF "DB2015_M".M[#for_i].Orden_ResetHoras THEN
	                    "DB2015_M".M[#for_i].Tiempos_Mantenimiento := 0.0;
	                    "DB2015_M".M[#for_i].Orden_ResetHoras := FALSE;
	                END_IF;
	                IF NOT #Simulacion AND #Pulso1seg AND "DB2015_M".M[#for_i].Estado_Activado THEN
	                    "DB2015_M".M[#for_i].Tiempos_Mantenimiento += 0.00027778;
	                END_IF;
	                //  =============================================================================
	                //  ALARMA HORAS PARA MANTENIMIENTO ALCANZADOS
	                "DB2015_M".M[#for_i].Alarmas_Mantenimiento := FALSE;
	                IF "DB2015_M".M[#for_i].Config_HabilitarMantenimiento
	                    AND
	                    "DB2015_M".M[#for_i].Tiempos_Mantenimiento > "DB2015_M".M[#for_i].Tiempos_SetPointMantenimiento
	                THEN
	                    "DB2015_M".M[#for_i].Alarmas_Mantenimiento := TRUE;
	                END_IF;
	                
	                
	            END_REGION DIAGNOSIS
	            
	            
	            REGION ESCRITURA_SALIDA
	                
	                CASE "DB2015_M".M[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        // =============================================================================
	                        // ESCRITURA SALIDA
	                        (* AREA: Pueden seleccionarse las siguientes áreas:16#81: Input, 16#82: Output, 16#83: Marcas, 16#84: DB, 16#2: Salida de periferia (solo S7-1500)      
	                        DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                        BYTEOFFSET: Dirección que se escribe, Solo se utilizan los 16 bits menos significativos. 
	                        BITOFFSET: Bit que se escribe, 
	                        VALUE: Valor que se escribe *)
	                        
	                        IF "DB2015_M".M[#for_i].Config_DireccionSalidaByte >= 0 THEN
	                            
	                            IF #t_Activar AND NOT "DB2015_M".M[#for_i].Alarmas_General THEN
	                                
	                                "DB2015_M".M[#for_i].Estado_Salida := TRUE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2015_M".M[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2015_M".M[#for_i].Config_DireccionSalidaBit,
	                                          value := TRUE);
	                            ELSE
	                                "DB2015_M".M[#for_i].Estado_Salida := FALSE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2015_M".M[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2015_M".M[#for_i].Config_DireccionSalidaBit,
	                                          value := FALSE);
	                            END_IF;
	                        END_IF;
	                        
	                    #TIPO_ACCESO_PLC:
	                        IF #t_Activar AND NOT "DB2015_M".M[#for_i].Alarmas_General THEN
	                            "DB2015_M".M[#for_i].Estado_Salida := TRUE;
	                        ELSE
	                            "DB2015_M".M[#for_i].Estado_Salida := FALSE;
	                        END_IF;
	                        
	                END_CASE;
	                
	            END_REGION ESCRITURA_SALIDA
	            
	            
	            // =============================================================================
	            //  RESET ORDEN ACTIVAR EN AUTO
	            "DB2015_M".M[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2015_M".M[#for_i].Estado_Enclavado := FALSE;
	            
	            REGION TRAZABILIDAD_MANUALIZACION
	                
	                IF "DB2015_M".M[#for_i].Estado_AutoMan AND NOT "DB2015_M".M[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_15_DISP_M",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2015_M".M[#for_i].Estado_AutoMan AND "DB2015_M".M[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_15_DISP_M",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2015_M".M[#for_i].Estado_AutoMan AND "DB2015_M".M[#for_i].Estado_Activado AND NOT "DB2015_M".M[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_15_DISP_M",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_ON",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2015_M".M[#for_i].Estado_AutoMan AND NOT "DB2015_M".M[#for_i].Estado_Activado AND "DB2015_M".M[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_15_DISP_M",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_OFF",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	            END_REGION TRAZABILIDAD_MANUALIZACION
	            
	            // =============================================================================
	            // Estado anterior manual/automatico
	            "DB2015_M".M[#for_i].Aux_oldAutoMan := "DB2015_M".M[#for_i].Estado_AutoMan;
	            "DB2015_M".M[#for_i].Aux_oldActivado := "DB2015_M".M[#for_i].Estado_Activado;
	            
	        ELSE
	            
	            // =============================================================================
	            // DISPOSITIVO NO HABILITADO
	            // =============================================================================
	            "DB2015_M".M[#for_i].Alarmas_General := FALSE;
	            "DB2015_M".M[#for_i].Alarmas_Termico := FALSE;
	            "DB2015_M".M[#for_i].Alarmas_ConfirmacionMarcha := FALSE;
	            "DB2015_M".M[#for_i].Alarmas_Mantenimiento := FALSE;
	            "DB2015_M".M[#for_i].Estado_EntradaTermico := FALSE;
	            "DB2015_M".M[#for_i].Estado_EntradaConfMarcha := FALSE;
	            "DB2015_M".M[#for_i].Estado_Enclavado := FALSE;
	            "DB2015_M".M[#for_i].Estado_Salida := FALSE;
	            "DB2015_M".M[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2015_M".M[#for_i].Estado_Activado := FALSE;
	            "DB2015_M".M[#for_i].Tiempos_Alarma := 0;
	            "DB2015_M".M[#for_i].Orden_ActivarManual := FALSE;
	            "DB2015_M".M[#for_i].Estado_AutoMan := FALSE;
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
	            //  Bit     8   alarmas General
	            //  Bit     9   alarmas 1
	            //  Bit     10  alarmas 2
	            //  Bit     11  alarmas 3
	            //  Bit     12  alarmas 4
	            //  Bit     13  alarmas Mantenimiento
	            //  Bit     14  Reserva
	            //  Bit     15  Reserva
	            "DB2015_M".M[#for_i].Hmi_Estado.%X0 := "DB2015_M".M[#for_i].Config_Habilitar;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X1 := "DB2015_M".M[#for_i].Estado_AutoMan;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X2 := "DB2015_M".M[#for_i].Estado_Enclavado;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X3 := "DB2015_M".M[#for_i].Estado_Activado;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X3 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X4 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X8 := "DB2015_M".M[#for_i].Alarmas_General;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X9 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X10 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X13 := "DB2015_M".M[#for_i].Alarmas_Mantenimiento;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2015_M".M[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION GESTION_HMI
	        
	        REGION GESTION_NUEVA_ALARMA
	            
	            // =============================================================================
	            //  DETECCION DE NUEVA alarmas
	            IF "DB2015_M".M[#for_i].Alarmas_General AND NOT "DB2015_M".M[#for_i].Aux_oldAlarma THEN
	                "DB2015_M".Agrup["DB2015_M".M[#for_i].Config_GrupoAlarma].NuevaAlarma := TRUE;
	            END_IF;
	            
	            //  Estado anterior de las alarmass
	            "DB2015_M".M[#for_i].Aux_oldAlarma := "DB2015_M".M[#for_i].Alarmas_General;
	            
	        END_REGION GESTION_NUEVA_ALARMA
	        
	        
	    END_FOR;
	    
	    
	    // =============================================================================
	    //  ACUSE DE NUEVAS ALARMAS
	    IF #Ack THEN
	        FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	            "DB2015_M".Agrup[#for_i].NuevaAlarma := FALSE;
	        END_FOR;
	    END_IF;
	    
	END_REGION LOGICA_DEL_DISPOSITIVO
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>