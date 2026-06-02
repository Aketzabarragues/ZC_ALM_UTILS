---
title: FC2010_ZC_V
---
# FC FC2010_ZC_V

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Valvula.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se gestiona el estado del dispositivo
    - Se gestiona el numero de activaciones
    - Se gestiona la orden de escritura
    - Se gestiona la trazabilidad de las manualizaciones del dispositivo

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **DB:** [DB1_SYS](../Estructura de datos/DB1_SYS.md)
    **DB:** [DB2010_V](../Estructura de datos/DB2010_V.md)

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
| `t_oldIndex` | `Int` | - | `-` | - |
| `t_ErrorReposo` | `Bool` | - | `-` | - |
| `t_ErrorDoble` | `Bool` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TIPO_ACCESO_INDIRECTO` | `SInt` | - | `0` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2010_ZC_V" : Void
TITLE = FC2010_V
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo vlvula
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
      t_Index : Int;
      t_oldIndex : Int;
      t_Activar : Bool;
      t_ErrorReposo : Bool;
      t_ErrorTrabajo : Bool;
      t_ErrorDoble : Bool;
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
	
	Funcion para la gestion de dispositivo de tipo Valvula.
	
	En ella se realizan las siguientes acciones:
	
	- Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
	- Se gestiona el estado del dispositivo
	- Se gestiona el numero de activaciones
	- Se gestiona la orden de escritura
	- Se gestiona la trazabilidad de las manualizaciones del dispositivo
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC8_ZC_TRAZA_REGISTRO` |
	| FB   | - |
	| DB   | `DB1_SYS`, `DB2010_V` |
	| UDT  | - |
	
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.01  | 15.10.2020 | (ABH)   | Primera version. |
	| 00.00.02  | 28.11.2020 | (ABH)   | Añadidas alarmas mantenimiento |
	| 00.00.03  | 28.07.2021 | (ABH)   | Añadidas alarmas en doble posicion / ninguna posicion |
	| 00.00.04  | 22.12.2021 | (ABH)   | Añadido bit de visibilidad, a traves de variable CFG_Hmi_ |
	| 00.00.05  | 26.04.2022 | (HCR)   | Cambio UDT |
	| 00.00.06  | 26.04.2022 | (HCR)   | BITs de visibilidad para HMI, quitar enclavamiento para orden manual |
	| 00.00.07  | 27.04.2022 | (HCR)   | Si no esta habilitado se quita orden manual y se quita el estado manual. Se agrega Ack para alarma de confirmación de marcha. Se mantiene el estado de válvula cuando se pasa a manual. Cambio en lógica de errores. Cambio en la escritura de la salida                                             |
	| 00.00.08  | 08.11.2022 | (ABH)   | Se añade trazabilidad manualizaciones  |
	| 00.00.09  | 08.11.2022 | (HCR)   | Se añade trazabilidad de activación manual |
	| 00.00.10  | 08.11.2022 | (HCR)   | Cambio lógica enclavamiento |
	| 00.00.11  | 22.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado) |
	| 00.00.12  | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado. Se añade movimiento de V[0] a multiplexado en caso de que el indice sea 0.  |
	| 00.00.13  | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores. |
	| 00.00.14  | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro. |
	| 00.00.15  | 24.04.2025 | (HCR)   | Se añade gestion de idioma  |
	| 00.00.16  | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	| 00.00.17  | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT. Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision. |
	| 01.00.00  | 18.05.2026 | (ABH)   | Se añade variable `Config_TipoAcceso` para uso de direccionamiento indirecto o uso directo en PLC. |
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2010_V".Mux[#for_mux].Index :=
	            "DB2010_V".Mux[#for_mux].oldIndex := 0;
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
	            IF "DB2010_V".Mux[#for_mux].Index < 0 THEN
	                "DB2010_V".Mux[#for_mux].Index := 0;
	            END_IF;
	            IF "DB2010_V".Mux[#for_mux].Index > "N_MAX_DISP_V" THEN
	                "DB2010_V".Mux[#for_mux].Index := "N_MAX_DISP_V";
	            END_IF;
	            IF "DB2010_V".Mux[#for_mux].Index >= "N_MAX_DISP_V" THEN
	                "DB2010_V".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2010_V".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2010_V".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2010_V".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2010_V".Mux[#for_mux].oldIndex := #t_Index;
	        
	        
	        IF "DB2010_V".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2010_V".Mux[#for_mux].V := "DB2010_V".V[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	                
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2010_V".Mux[#for_mux].V.Hmi_Estado := "DB2010_V".V[#t_Index].Hmi_Estado;
	                    "DB2010_V".Mux[#for_mux].V.Estado_SeguridadOk := "DB2010_V".V[#t_Index].Estado_SeguridadOk;
	                    IF NOT "DB2010_V".V[#t_Index].Estado_AutoMan THEN
	                        "DB2010_V".Mux[#for_mux].V.Orden_ActivarManual := "DB2010_V".V[#t_Index].Orden_ActivarManual;
	                    ELSE
	                        IF NOT #SeguridadesOK OR NOT "DB2010_V".Mux[#for_mux].V.Estado_SeguridadOk THEN
	                            "DB2010_V".Mux[#for_mux].V.Orden_ActivarManual :=
	                            "DB2010_V".V[#t_Index].Orden_ActivarManual := FALSE;
	                        END_IF;
	                    END_IF;
	                    "DB2010_V".Mux[#for_mux].V.Estado_Activado := "DB2010_V".V[#t_Index].Estado_Activado;
	                    "DB2010_V".Mux[#for_mux].V.Estado_Enclavado := "DB2010_V".V[#t_Index].Estado_Enclavado;
	                    "DB2010_V".Mux[#for_mux].V.Estado_Salida := "DB2010_V".V[#t_Index].Estado_Salida;
	                    "DB2010_V".Mux[#for_mux].V.Estado_EntradaRetornoReposo := "DB2010_V".V[#t_Index].Estado_EntradaRetornoReposo;
	                    "DB2010_V".Mux[#for_mux].V.Estado_EntradaRetornoTrabajo := "DB2010_V".V[#t_Index].Estado_EntradaRetornoTrabajo;
	                    "DB2010_V".Mux[#for_mux].V.Alarmas_Doble := "DB2010_V".V[#t_Index].Alarmas_Doble;
	                    "DB2010_V".Mux[#for_mux].V.Alarmas_General := "DB2010_V".V[#t_Index].Alarmas_General;
	                    "DB2010_V".Mux[#for_mux].V.Alarmas_Mantenimiento := "DB2010_V".V[#t_Index].Alarmas_Mantenimiento;
	                    "DB2010_V".Mux[#for_mux].V.Alarmas_Reposo := "DB2010_V".V[#t_Index].Alarmas_Reposo;
	                    "DB2010_V".Mux[#for_mux].V.Alarmas_Trabajo := "DB2010_V".V[#t_Index].Alarmas_Trabajo;
	                    "DB2010_V".Mux[#for_mux].V.Orden_ActivarAuto := "DB2010_V".V[#t_Index].Orden_ActivarAuto;
	                    "DB2010_V".Mux[#for_mux].V.Tiempos_Alarma := "DB2010_V".V[#t_Index].Tiempos_Alarma;
	                    "DB2010_V".Mux[#for_mux].V.Tiempos_Ciclos := "DB2010_V".V[#t_Index].Tiempos_Ciclos;
	                    "DB2010_V".Mux[#for_mux].V.Aux_oldActivado := "DB2010_V".V[#t_Index].Aux_oldActivado;
	                    "DB2010_V".Mux[#for_mux].V.Aux_oldAlarma := "DB2010_V".V[#t_Index].Aux_oldAlarma;
	                    "DB2010_V".Mux[#for_mux].V.Aux_oldAutoMan := "DB2010_V".V[#t_Index].Aux_oldAutoMan;
	                    "DB2010_V".Mux[#for_mux].V.Config_GrupoAlarma := "DB2010_V".V[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2010_V".Mux[#for_mux].ExisteCambio := false;
	                    
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2010_V".Mux[#for_mux].V.Estado_AutoMan <> "DB2010_V".V[#t_Index].Estado_AutoMan THEN
	                        "DB2010_V".V[#t_Index].Estado_AutoMan := "DB2010_V".Mux[#for_mux].V.Estado_AutoMan;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2010_V".Mux[#for_mux].V.Orden_ActivarManual <> "DB2010_V".V[#t_Index].Orden_ActivarManual THEN
	                        "DB2010_V".V[#t_Index].Orden_ActivarManual := "DB2010_V".Mux[#for_mux].V.Orden_ActivarManual;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Orden_ResetCiclos <> "DB2010_V".V[#t_Index].Orden_ResetCiclos THEN
	                        "DB2010_V".V[#t_Index].Orden_ResetCiclos := "DB2010_V".Mux[#for_mux].V.Orden_ResetCiclos;
	                        "DB2010_V".Mux[#for_mux].V.Orden_ResetCiclos := FALSE;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2010_V".Mux[#for_mux].V.Config_DireccionRetReposoBit <> "DB2010_V".V[#t_Index].Config_DireccionRetReposoBit THEN
	                        "DB2010_V".V[#t_Index].Config_DireccionRetReposoBit := "DB2010_V".Mux[#for_mux].V.Config_DireccionRetReposoBit;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_DireccionRetReposoByte <> "DB2010_V".V[#t_Index].Config_DireccionRetReposoByte THEN
	                        "DB2010_V".V[#t_Index].Config_DireccionRetReposoByte := "DB2010_V".Mux[#for_mux].V.Config_DireccionRetReposoByte;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_DireccionRetTrabajoBit <> "DB2010_V".V[#t_Index].Config_DireccionRetTrabajoBit THEN
	                        "DB2010_V".V[#t_Index].Config_DireccionRetTrabajoBit := "DB2010_V".Mux[#for_mux].V.Config_DireccionRetTrabajoBit;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_DireccionRetTrabajoByte <> "DB2010_V".V[#t_Index].Config_DireccionRetTrabajoByte THEN
	                        "DB2010_V".V[#t_Index].Config_DireccionRetTrabajoByte := "DB2010_V".Mux[#for_mux].V.Config_DireccionRetTrabajoByte;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_DireccionSalidaBit <> "DB2010_V".V[#t_Index].Config_DireccionSalidaBit THEN
	                        "DB2010_V".V[#t_Index].Config_DireccionSalidaBit := "DB2010_V".Mux[#for_mux].V.Config_DireccionSalidaBit;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_DireccionSalidaByte <> "DB2010_V".V[#t_Index].Config_DireccionSalidaByte THEN
	                        "DB2010_V".V[#t_Index].Config_DireccionSalidaByte := "DB2010_V".Mux[#for_mux].V.Config_DireccionSalidaByte;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_Habilitar <> "DB2010_V".V[#t_Index].Config_Habilitar THEN
	                        "DB2010_V".V[#t_Index].Config_Habilitar := "DB2010_V".Mux[#for_mux].V.Config_Habilitar;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_HabilitarInvertirReposo <> "DB2010_V".V[#t_Index].Config_HabilitarInvertirReposo THEN
	                        "DB2010_V".V[#t_Index].Config_HabilitarInvertirReposo := "DB2010_V".Mux[#for_mux].V.Config_HabilitarInvertirReposo;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_HabilitarInvertirTrabajo <> "DB2010_V".V[#t_Index].Config_HabilitarInvertirTrabajo THEN
	                        "DB2010_V".V[#t_Index].Config_HabilitarInvertirTrabajo := "DB2010_V".Mux[#for_mux].V.Config_HabilitarInvertirTrabajo;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_HabilitarMantenimiento <> "DB2010_V".V[#t_Index].Config_HabilitarMantenimiento THEN
	                        "DB2010_V".V[#t_Index].Config_HabilitarMantenimiento := "DB2010_V".Mux[#for_mux].V.Config_HabilitarMantenimiento;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_HabilitarRetornoReposo <> "DB2010_V".V[#t_Index].Config_HabilitarRetornoReposo THEN
	                        "DB2010_V".V[#t_Index].Config_HabilitarRetornoReposo := "DB2010_V".Mux[#for_mux].V.Config_HabilitarRetornoReposo;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_HabilitarRetornoTrabajo <> "DB2010_V".V[#t_Index].Config_HabilitarRetornoTrabajo THEN
	                        "DB2010_V".V[#t_Index].Config_HabilitarRetornoTrabajo := "DB2010_V".Mux[#for_mux].V.Config_HabilitarRetornoTrabajo;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Config_TipoAcceso <> "DB2010_V".V[#t_Index].Config_TipoAcceso THEN
	                        "DB2010_V".V[#t_Index].Config_TipoAcceso := "DB2010_V".Mux[#for_mux].V.Config_TipoAcceso;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Tiempos
	                    IF "DB2010_V".Mux[#for_mux].V.Tiempos_SetPointTiempoAlarma <> "DB2010_V".V[#t_Index].Tiempos_SetPointTiempoAlarma THEN
	                        "DB2010_V".V[#t_Index].Tiempos_SetPointTiempoAlarma := "DB2010_V".Mux[#for_mux].V.Tiempos_SetPointTiempoAlarma;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2010_V".Mux[#for_mux].V.Tiempos_SetPointCiclos <> "DB2010_V".V[#t_Index].Tiempos_SetPointCiclos THEN
	                        "DB2010_V".V[#t_Index].Tiempos_SetPointCiclos := "DB2010_V".Mux[#for_mux].V.Tiempos_SetPointCiclos;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2010_V".Mux[#for_mux].ExisteCambio THEN
	                        
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2010_V".Mux[#for_mux_cambios].Index THEN
	                                    "DB2010_V".Mux[#for_mux_cambios].V := "DB2010_V".V[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2010_V".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la V[0] que no se usa para escribir el index.
	                "DB2010_V".Mux[#for_mux].V := "DB2010_V".V[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            "DB2010_V".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2010_V".Mux[#for_mux].Index :=
	            "DB2010_V".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	        
	    END_FOR;
	    
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2010_V".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2010_V".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_V" DO
	        
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2010_V".V[#for_i].Config_Habilitar THEN
	            
	            REGION LIMITE_GRUPO_ALARMA
	                
	                IF "DB2010_V".V[#for_i].Config_GrupoAlarma < 0 THEN
	                    "DB2010_V".V[#for_i].Config_GrupoAlarma := 0;
	                END_IF;
	                IF "DB2010_V".V[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                    "DB2010_V".V[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	                END_IF;
	                
	            END_REGION LIMITE_GRUPO_ALARMA
	            
	            // =============================================================================
	            //  PUESTA A CERO DE LA SALIDA
	            #t_Activar := FALSE;
	            
	            REGION LECTURA_VALORES
	                
	                CASE "DB2010_V".V[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        (* AREA: Pueden seleccionarse las siguientes áreas: 16#81: Input, 16#82: Output, 16#83: Marcas, 16#84: DB, 16#1: Entrada de periferia (solo S7-1500)
	                        DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                        BYTEOFFSET: Dirección en la que se lee. Solo se utilizan los 16 bits menos significativos.*)
	                        
	                        // =============================================================================
	                        // RETORNO REPOSO
	                        IF "DB2010_V".V[#for_i].Config_DireccionRetReposoByte >= 0 THEN
	                            
	                            "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo := PEEK_BOOL(area := 16#81,
	                                                                                          dbNumber := 0,
	                                                                                          byteOffset := "DB2010_V".V[#for_i].Config_DireccionRetReposoByte,
	                                                                                          bitOffset := "DB2010_V".V[#for_i].Config_DireccionRetReposoBit);
	                            
	                            IF "DB2010_V".V[#for_i].Config_HabilitarInvertirReposo THEN
	                                "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo := NOT (PEEK_BOOL(area := 16#81,
	                                                                                                   dbNumber := 0,
	                                                                                                   byteOffset := "DB2010_V".V[#for_i].Config_DireccionRetReposoByte,
	                                                                                                   bitOffset := "DB2010_V".V[#for_i].Config_DireccionRetReposoBit));
	                            END_IF;
	                            
	                        END_IF;
	                        
	                        // =============================================================================
	                        // RETORNO TRABAJO
	                        IF "DB2010_V".V[#for_i].Config_DireccionRetTrabajoByte >= 0 THEN
	                            "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo := PEEK_BOOL(area := 16#81,
	                                                                                           dbNumber := 0,
	                                                                                           byteOffset := "DB2010_V".V[#for_i].Config_DireccionRetTrabajoByte,
	                                                                                           bitOffset := "DB2010_V".V[#for_i].Config_DireccionRetTrabajoBit);
	                            IF "DB2010_V".V[#for_i].Config_HabilitarInvertirTrabajo THEN
	                                "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo := NOT (PEEK_BOOL(area := 16#81,
	                                                                                                    dbNumber := 0,
	                                                                                                    byteOffset := "DB2010_V".V[#for_i].Config_DireccionRetTrabajoByte,
	                                                                                                    bitOffset := "DB2010_V".V[#for_i].Config_DireccionRetTrabajoBit));
	                            END_IF;
	                            
	                        END_IF;
	                        
	                        
	                    #TIPO_ACCESO_PLC:
	                        ;
	                        
	                END_CASE;
	                
	            END_REGION LECTURA_VALORES
	            
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                //  MODO MANUAL
	                IF "DB2010_V".V[#for_i].Estado_AutoMan THEN
	                    "DB2010_V".Agrup["DB2010_V".V[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    IF "DB2010_V".V[#for_i].Orden_ActivarManual AND #SeguridadesOK AND "DB2010_V".V[#for_i].Estado_SeguridadOk THEN // En caso de enclavar válvula en manual AND NOT "DB2035_TMF1_DISP_V".V[#i].Estado_Enclavado
	                        #t_Activar := TRUE;
	                    ELSE
	                        #t_Activar := FALSE;
	                        "DB2010_V".V[#for_i].Orden_ActivarManual := FALSE;
	                    END_IF;
	                ELSE
	                    "DB2010_V".V[#for_i].Orden_ActivarManual := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  MODO AUTO
	                IF NOT "DB2010_V".V[#for_i].Estado_AutoMan THEN
	                    IF "DB2010_V".V[#for_i].Orden_ActivarAuto AND NOT "DB2010_V".V[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2010_V".V[#for_i].Estado_SeguridadOk THEN
	                        #t_Activar := TRUE;
	                    ELSE
	                        #t_Activar := FALSE;
	                    END_IF;
	                    "DB2010_V".V[#for_i].Orden_ActivarManual := "DB2010_V".V[#for_i].Estado_Activado;
	                END_IF;
	                
	            END_REGION MODOS_DE_TRABAJO
	            
	            
	            REGION ESTADO_DEL_DISPOSITIVO
	                
	                // =============================================================================
	                //  VÁLVULA SIMULADA
	                IF #Simulacion THEN
	                    
	                    IF #t_Activar THEN
	                        "DB2010_V".V[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2010_V".V[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                // VÁLVULA 2 RETORNOS (REPOSO + TRABAJO)
	                IF NOT #Simulacion AND
	                    "DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo
	                THEN
	                    
	                    IF "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo AND NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo AND #t_Activar THEN
	                        "DB2010_V".V[#for_i].Estado_Activado := TRUE;
	                    END_IF;
	                    
	                    IF "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo AND NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo AND NOT #t_Activar THEN
	                        "DB2010_V".V[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                // VÁLVULA SOLO RETORNO REPOSO
	                IF NOT #Simulacion AND
	                    "DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND NOT "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo
	                THEN
	                    
	                    IF NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo THEN
	                        "DB2010_V".V[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2010_V".V[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                // VÁLVULA SOLO RETORNO TRABAJO
	                IF NOT #Simulacion AND
	                    NOT "DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo
	                THEN
	                    
	                    IF "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo THEN
	                        "DB2010_V".V[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2010_V".V[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                // VÁLVULA SIN RETORNOS
	                IF NOT #Simulacion AND
	                    NOT "DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND NOT "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo
	                THEN
	                    
	                    IF #t_Activar THEN
	                        "DB2010_V".V[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2010_V".V[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	            END_REGION ESTADO_DEL_DISPOSITIVO
	            
	            
	            REGION ERRORES
	                
	                // =============================================================================
	                // CHEQUEO RETORNO REPOSO
	                IF NOT #Simulacion AND
	                    "DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND
	                    (
	                    (#t_Activar AND "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo)
	                    OR
	                    (NOT #t_Activar AND NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo)
	                    )
	                THEN
	                    #t_ErrorReposo := TRUE;
	                ELSE
	                    #t_ErrorReposo := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                // CHEQUEO RETORNO TRABAJO
	                IF NOT #Simulacion AND
	                    "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo AND
	                    (
	                    (#t_Activar AND NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo)
	                    OR
	                    (NOT #t_Activar AND "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo)
	                    )
	                THEN
	                    #t_ErrorTrabajo := TRUE;
	                ELSE
	                    #t_ErrorTrabajo := FALSE;
	                END_IF;
	                
	                
	                // =============================================================================
	                // CHEQUEO DOBLE RETORNO EN DOS POSICIONES O EN NINGUNA POSICION
	                IF NOT #Simulacion AND
	                    ("DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo)
	                    AND
	                    (
	                    (NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo AND NOT "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo)
	                    OR
	                    ("DB2010_V".V[#for_i].Estado_EntradaRetornoReposo AND "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo)
	                    )
	                THEN
	                    #t_ErrorDoble := TRUE;
	                ELSE
	                    #t_ErrorDoble := FALSE;
	                END_IF;
	                
	                
	                
	                // =============================================================================
	                // TEMPORIZADO DE ERRORES
	                IF (
	                    ("DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND #t_ErrorReposo AND NOT "DB2010_V".V[#for_i].Alarmas_Reposo)
	                    OR
	                    ("DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo AND #t_ErrorTrabajo AND NOT "DB2010_V".V[#for_i].Alarmas_Trabajo)
	                    OR
	                    ("DB2010_V".V[#for_i].Config_HabilitarRetornoReposo AND "DB2010_V".V[#for_i].Config_HabilitarRetornoTrabajo AND #t_ErrorDoble AND NOT "DB2010_V".V[#for_i].Alarmas_Doble)
	                    )
	                THEN
	                    IF #Pulso1seg AND NOT #Simulacion THEN
	                        "DB2010_V".V[#for_i].Tiempos_Alarma += 1;
	                    END_IF;
	                ELSE
	                    "DB2010_V".V[#for_i].Tiempos_Alarma := 0;
	                END_IF;
	                
	                
	                // =============================================================================
	                // ERROR REPOSO
	                IF "DB2010_V".V[#for_i].Tiempos_Alarma >= "DB2010_V".V[#for_i].Tiempos_SetPointTiempoAlarma AND #t_ErrorReposo THEN
	                    "DB2010_V".V[#for_i].Alarmas_Reposo := TRUE;
	                END_IF;
	                IF NOT #t_ErrorReposo THEN
	                    "DB2010_V".V[#for_i].Alarmas_Reposo := FALSE;
	                END_IF;
	                
	                
	                // =============================================================================
	                // ERROR TRABAJO
	                IF "DB2010_V".V[#for_i].Tiempos_Alarma >= "DB2010_V".V[#for_i].Tiempos_SetPointTiempoAlarma AND #t_ErrorTrabajo THEN
	                    "DB2010_V".V[#for_i].Alarmas_Trabajo := TRUE;
	                END_IF;
	                IF NOT #t_ErrorTrabajo THEN
	                    "DB2010_V".V[#for_i].Alarmas_Trabajo := FALSE;
	                END_IF;
	                
	                
	                // =============================================================================
	                // ERROR DOBLE
	                IF "DB2010_V".V[#for_i].Tiempos_Alarma >= "DB2010_V".V[#for_i].Tiempos_SetPointTiempoAlarma AND #t_ErrorDoble THEN
	                    "DB2010_V".V[#for_i].Alarmas_Doble := TRUE;
	                END_IF;
	                IF NOT #t_ErrorDoble THEN
	                    "DB2010_V".V[#for_i].Alarmas_Doble := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                // ERROR GLOBAL
	                IF "DB2010_V".V[#for_i].Alarmas_Reposo OR
	                    "DB2010_V".V[#for_i].Alarmas_Trabajo OR
	                    "DB2010_V".V[#for_i].Alarmas_Doble
	                THEN
	                    "DB2010_V".V[#for_i].Alarmas_General := TRUE;
	                END_IF;
	                IF #Ack AND
	                    NOT "DB2010_V".V[#for_i].Alarmas_Reposo AND
	                    NOT "DB2010_V".V[#for_i].Alarmas_Trabajo AND
	                    NOT "DB2010_V".V[#for_i].Alarmas_Doble
	                THEN
	                    "DB2010_V".V[#for_i].Alarmas_General := FALSE;
	                END_IF;
	                
	                //"DB2010_V".V[#for_i].Alarmas_General := "DB2010_V".V[#for_i].Alarmas_Reposo OR "DB2010_V".V[#for_i].Alarmas_Trabajo OR "DB2010_V".V[#for_i].Alarmas_Doble;
	                
	                IF "DB2010_V".V[#for_i].Alarmas_General THEN
	                    "DB2010_V".Agrup["DB2010_V".V[#for_i].Config_GrupoAlarma].AlgunaAlarma := TRUE;
	                END_IF;
	                
	            END_REGION ERRORES
	            
	            
	            REGION DIAGNOSIS
	                
	                // =============================================================================
	                // CONTADOR DE CICLOS DE ACTIVACIÓN DE LA VÁLVULA
	                IF ("DB2010_V".V[#for_i].Estado_Activado AND NOT "DB2010_V".V[#for_i].Aux_oldActivado)
	                    OR
	                    (NOT "DB2010_V".V[#for_i].Estado_Activado AND "DB2010_V".V[#for_i].Aux_oldActivado)
	                THEN
	                    "DB2010_V".V[#for_i].Tiempos_Ciclos += 1;
	                END_IF;
	                
	                IF "DB2010_V".V[#for_i].Orden_ResetCiclos THEN
	                    "DB2010_V".V[#for_i].Tiempos_Ciclos := 0;
	                    "DB2010_V".V[#for_i].Orden_ResetCiclos := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ALARMA CICLOS PARA MANTENIMIENTO ALCANZADOS
	                "DB2010_V".V[#for_i].Alarmas_Mantenimiento := FALSE;
	                IF "DB2010_V".V[#for_i].Config_HabilitarMantenimiento AND ("DB2010_V".V[#for_i].Tiempos_Ciclos > "DB2010_V".V[#for_i].Tiempos_SetPointCiclos) THEN
	                    "DB2010_V".V[#for_i].Alarmas_Mantenimiento := TRUE;
	                END_IF;
	                
	                
	                
	            END_REGION DIAGNOSIS
	            
	            
	            REGION ESCRITURA_SALIDA
	                
	                CASE "DB2010_V".V[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        // =============================================================================
	                        // ESCRITURA SALIDA
	                        (* AREA: Pueden seleccionarse las siguientes áreas:16#81: Input, 16#82: Output, 16#83: Marcas, 16#84: DB, 16#2: Salida de periferia (solo S7-1500)      
	                        DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                        BYTEOFFSET: Dirección que se escribe, Solo se utilizan los 16 bits menos significativos. 
	                        BITOFFSET: Bit que se escribe, 
	                        VALUE: Valor que se escribe *)
	                        
	                        IF "DB2010_V".V[#for_i].Config_DireccionSalidaByte >= 0 THEN
	                            
	                            IF #t_Activar AND NOT "DB2010_V".V[#for_i].Alarmas_General THEN
	                                
	                                "DB2010_V".V[#for_i].Estado_Salida := TRUE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2010_V".V[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2010_V".V[#for_i].Config_DireccionSalidaBit,
	                                          value := TRUE);
	                            ELSE
	                                
	                                "DB2010_V".V[#for_i].Estado_Salida := FALSE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2010_V".V[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2010_V".V[#for_i].Config_DireccionSalidaBit,
	                                          value := FALSE);
	                            END_IF;
	                        END_IF;
	                        
	                    #TIPO_ACCESO_PLC:
	                        IF #t_Activar AND NOT "DB2010_V".V[#for_i].Alarmas_General THEN
	                            "DB2010_V".V[#for_i].Estado_Salida := TRUE;
	                        ELSE
	                            "DB2010_V".V[#for_i].Estado_Salida := FALSE;
	                        END_IF;
	                        
	                END_CASE;
	                
	            END_REGION
	            
	            
	            // =============================================================================
	            //  RESET ORDEN ACTIVAR EN AUTO
	            "DB2010_V".V[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2010_V".V[#for_i].Estado_Enclavado := FALSE;
	            
	            
	            REGION TRAZABILIDAD_MANUALIZACION
	                
	                IF "DB2010_V".V[#for_i].Estado_AutoMan AND NOT "DB2010_V".V[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_14_DISP_V",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_V",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2010_V".V[#for_i].Estado_AutoMan AND "DB2010_V".V[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_14_DISP_V",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_V",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2010_V".V[#for_i].Estado_AutoMan AND "DB2010_V".V[#for_i].Estado_Activado AND NOT "DB2010_V".V[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_14_DISP_V",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_V",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_ON",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2010_V".V[#for_i].Estado_AutoMan AND NOT "DB2010_V".V[#for_i].Estado_Activado AND "DB2010_V".V[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_14_DISP_V",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_V",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_OFF",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	            END_REGION TRAZABILIDAD_MANUALIZACION
	            
	            // =============================================================================
	            //  Estado anterior manual/automatico
	            "DB2010_V".V[#for_i].Aux_oldActivado := "DB2010_V".V[#for_i].Estado_Activado;
	            "DB2010_V".V[#for_i].Aux_oldAutoMan := "DB2010_V".V[#for_i].Estado_AutoMan;
	            
	        ELSE
	            
	            // =============================================================================
	            // DISPOSITIVO NO HABILITADO
	            // =============================================================================
	            "DB2010_V".V[#for_i].Alarmas_General := FALSE;
	            "DB2010_V".V[#for_i].Alarmas_Reposo := FALSE;
	            "DB2010_V".V[#for_i].Alarmas_Trabajo := FALSE;
	            "DB2010_V".V[#for_i].Alarmas_Doble := FALSE;
	            "DB2010_V".V[#for_i].Alarmas_Mantenimiento := FALSE;
	            "DB2010_V".V[#for_i].Estado_EntradaRetornoTrabajo := FALSE;
	            "DB2010_V".V[#for_i].Estado_EntradaRetornoReposo := FALSE;
	            "DB2010_V".V[#for_i].Estado_Enclavado := FALSE;
	            "DB2010_V".V[#for_i].Estado_Salida := FALSE;
	            "DB2010_V".V[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2010_V".V[#for_i].Estado_Activado := FALSE;
	            "DB2010_V".V[#for_i].Tiempos_Alarma := 0;
	            "DB2010_V".V[#for_i].Orden_ActivarManual := FALSE;
	            "DB2010_V".V[#for_i].Estado_AutoMan := FALSE;
	            
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
	            "DB2010_V".V[#for_i].Hmi_Estado.%X0 := "DB2010_V".V[#for_i].Config_Habilitar;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X1 := "DB2010_V".V[#for_i].Estado_AutoMan;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X2 := "DB2010_V".V[#for_i].Estado_Enclavado;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X3 := "DB2010_V".V[#for_i].Estado_Activado;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X4 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X8 := "DB2010_V".V[#for_i].Alarmas_General;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X9 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X10 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X13 := "DB2010_V".V[#for_i].Alarmas_Mantenimiento;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2010_V".V[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION GESTION_HMI
	        
	        REGION GESTION_NUEVA_ALARMA
	            
	            // =============================================================================
	            //  DETECCION DE NUEVA ALARMA
	            IF "DB2010_V".V[#for_i].Alarmas_General AND NOT "DB2010_V".V[#for_i].Aux_oldAlarma THEN
	                "DB2010_V".Agrup["DB2010_V".V[#for_i].Config_GrupoAlarma].NuevaAlarma := TRUE;
	            END_IF;
	            
	            //  Estado anterior de las alarmas
	            "DB2010_V".V[#for_i].Aux_oldAlarma := "DB2010_V".V[#for_i].Alarmas_General;
	            
	        END_REGION GESTION_NUEVA_ALARMA
	        
	        
	    END_FOR;
	    
	    
	    // =============================================================================
	    //  ACUSE DE NUEVAS ALARMAS
	    IF #Ack THEN
	        FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	            "DB2010_V".Agrup[#for_i].NuevaAlarma := FALSE;
	        END_FOR;
	    END_IF;
	    
	END_REGION LOGICA_DEL_DISPOSITIVO
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>