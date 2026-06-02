---
title: FC2016_ZC_M_VF
---
# FC FC2016_ZC_M_VF

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Funcion para la gestion de dispositivo de tipo Motor con variador de frecuencia.
    
    En ella se realizan las siguientes acciones:
    
    - Se gestiona el multiplexado de los dispositivos para su uso en sistemas HMI/SCADA.
    - Se gestiona el estado del dispositivo
    - Se gestiona el tiempo en marcha
    - Se gestiona la orden de escritura
    - Se gestiona la trazabilidad de las manualizaciones del dispositivo

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **FC:** [FC15025_ZC_CONTADOR_TIEMPO](../Bloques de codigo/FC15025_ZC_CONTADOR_TIEMPO.md)
    **DB:** [DB2016_DISP_M_VF](../Estructura de datos/DB2016_DISP_M_VF.md)
    **DB:** [ZC_DISP_M_VF](../Estructura de datos/ZC_DISP_M_VF.md)
    **DB:** [ZC_DISP_MUX_M_VF](../Estructura de datos/ZC_DISP_MUX_M_VF.md)
    **DB:** [ZC_CONTADOR_TIEMPO](../Estructura de datos/ZC_CONTADOR_TIEMPO.md)

## Interfaz de Variables
### Estáticas
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
| `t_ErrorTermico` | `Bool` | - | `-` | - |
| `t_Frecuencia` | `Real` | - | `-` | - |
| `t_x0` | `Real` | - | `-` | - |
| `t_y0` | `Real` | - | `-` | - |
| `t_ValorSalida` | `Real` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TIPO_ACCESO_INDIRECTO` | `SInt` | - | `0` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2016_ZC_M_VF" : Void
TITLE = FC2016_M_VF
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Modelo de dispositivo motor variador
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
      t_ErrorTermico : Bool;
      t_ErrorConfirmacionMarcha : Bool;
      t_Frecuencia : Real;
      t_x : Real;
      t_x0 : Real;
      t_x1 : Real;
      t_y0 : Real;
      t_y1 : Real;
      t_ValorSalida : Real;
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
	
	Funcion para la gestion de dispositivo de tipo Motor con variador de frecuencia.
	
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
	| DB   | DB2016_DISP_M_VF |
	| UDT  | ZC_DISP_M_VF, ZC_DISP_MUX_M_VF, `ZC_CONTADOR_TIEMPO` |
	
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.01 | 15.10.2020 | (ABH)   | Primera version. |
	| 00.00.02 | 28.11.2020 | (ABH)   | Añadidas alarmas mantenimiento |
	| 00.00.03 | 26.10.2021 | (ABH)   | Se integra la gestion de directo/inverso |
	| 00.00.04 | 26.04.2022 | (HCR)   | Cambio en la organizacion del UDT. Se organiza en estructuras en base al tipo de funcion que realizan los datos. Se quita el enclavamiento para orden manual. |
	| 00.00.05 | 27.04.2022 | (ABH)   | Se añaden auxiliares de estado anterior del modo manual y automatico para poder registrar las trazas.   |
	| 00.00.06 | 27.04.2022 | (HCR)   | Si no esta habilitado se quita orden manual y se quita el estado manual. Se agrega Ack para alarmas de confirmación de marcha. Se mantiene el estado cuando se pasa a manual. Cambio en lógica de errores. Cambio en la escritura de la salida. Cambio en laógica de modos |
	| 00.00.07 | 08.11.2022 | (ABH)   | Se añade trazabilidad manualizaciones |
	| 00.00.08 | 08.11.2022 | (HCR)   | Se añade trazabilidad de activación manual |
	| 00.00.09 | 08.11.2022 | (HCR)   | Cambio lógica enclavamiento |
	| 00.00.10 | 18.09.2023 | (ABH)   | Cambio en tipo de dato de horas de alarma. Se utiliza el tipo de dato ZC_CONTADOR_TIEMPO y el FC15025_ZC_CONTADOR_TIEMPO |
	| 00.00.11 | 22.02.2024 | (ABH)   | Se añade gestion multiplexado para Scada (no indexado) |
	| 00.00.12 | 08.01.2025 | (ABH)   | Se añade entrada de primer arranque del PLC para resetear indices de multiplexado Se añade movimiento de M[0] a multiplexado en caso de que el indice sea 0.  |
	| 00.00.13 | 24.01.2025 | (ABH)   | Se modifica la logica del multiplexado, la asignacion de oldindex se cambia de sitio ya que de vez en cuando (dependiendo de cuando el HMI realiza la comunicacion asincrona con el PLC) no detectaba el cambio y se machacaban valores. |
	| 00.00.14 | 26.03.2025 | (ABH)   | Se añade variable grupo de alarma para separar los nuevos avisos por cuadro. |
	| 00.00.15 | 24.04.2025 | (HCR)   | Se añade gestion de idioma  |
	| 00.00.16 | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	| 00.00.17 | 17.12.2025 | (ABH)   | Se eliminan los idiomas. Se utiliza codigos para trazabilidad. Se elimina entrada "Idioma". Se elimina nombre de UDT. Se elimina nombre de UDT. Se añade indexHMI para lista de texto en sistemas de supervision. |
	| 01.00.00 | 18.05.2026 | (ABH)   | Se añade variable `Config_TipoAcceso` para uso de direccionamiento indirecto o uso directo en PLC. |
	*)
	END_REGION DESCRIPCION
	
	
	REGION MULTIPLEXADO
	    
	    //  ===========================================================================================================
	    //  Al arranque del PLC, ponemos a 0 todos los indices de los multiplexados y salimos del bloque sin gestionarlo
	    IF #Arranque THEN
	        FOR #for_mux := 0 TO "N_MAX_MUX_DISP" DO
	            "DB2016_M_VF".Mux[#for_mux].Index :=
	            "DB2016_M_VF".Mux[#for_mux].oldIndex := 0;
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
	            IF "DB2016_M_VF".Mux[#for_mux].Index < 0 THEN
	                "DB2016_M_VF".Mux[#for_mux].Index := 0;
	            END_IF;
	            IF "DB2016_M_VF".Mux[#for_mux].Index > "N_MAX_DISP_M_VF" THEN
	                "DB2016_M_VF".Mux[#for_mux].Index := "N_MAX_DISP_M_VF";
	            END_IF;
	            IF "DB2016_M_VF".Mux[#for_mux].Index >= "N_MAX_DISP_M_VF" THEN
	                "DB2016_M_VF".Mux[#for_mux].MaxVisible := TRUE;
	            ELSE
	                "DB2016_M_VF".Mux[#for_mux].MaxVisible := FALSE;
	            END_IF;
	            
	        END_REGION LIMITES
	        
	        //  Pasamos el indice a variable temporal para evisar cambios no deseados
	        #t_Index := "DB2016_M_VF".Mux[#for_mux].Index;
	        #t_oldIndex := "DB2016_M_VF".Mux[#for_mux].oldIndex;
	        
	        //  ===========================================================================================================
	        //  Valor anterior del indice
	        "DB2016_M_VF".Mux[#for_mux].oldIndex := #t_Index;
	        
	        IF "DB2016_M_VF".Mux[#for_mux].Habilitar THEN
	            
	            //  ===========================================================================================================
	            //  Gestionamos solo los tipos 
	            IF #t_Index > 0 THEN
	                
	                REGION CARGA_INICIAL
	                    
	                    //  ===========================================================================================================
	                    //  Al detectar un cambio en el indice del dispositivo, cargamos los valores del dispositivo que tenga el indice.
	                    IF #t_Index <> #t_oldIndex THEN
	                        "DB2016_M_VF".Mux[#for_mux].M_VF := "DB2016_M_VF".M_VF[#t_Index];
	                    END_IF;
	                    
	                END_REGION CARGA_INICIAL
	                
	                
	                REGION DATOS_LECTURA
	                    
	                    //  ===========================================================================================================
	                    //  Movimiento de datos gestionados en FC
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Hmi_Estado := "DB2016_M_VF".M_VF[#t_Index].Hmi_Estado;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_SeguridadOk := "DB2016_M_VF".M_VF[#for_i].Estado_SeguridadOk;
	                    IF NOT "DB2016_M_VF".M_VF[#t_Index].Estado_AutoMan AND #SeguridadesOK AND "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_SeguridadOk AND NOT "DB2016_M_VF".M_VF[#t_Index].Alarmas_Termico THEN
	                        "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ActivarManual := "DB2016_M_VF".M_VF[#t_Index].Orden_ActivarManual;
	                        "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ConsignaManual := "DB2016_M_VF".M_VF[#t_Index].Orden_ConsignaManual;
	                    ELSE
	                        IF NOT #SeguridadesOK OR NOT "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_SeguridadOk OR "DB2016_M_VF".M_VF[#t_Index].Alarmas_Termico THEN
	                            "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ActivarManual :=
	                            "DB2016_M_VF".M_VF[#t_Index].Orden_ActivarManual := FALSE;
	                        END_IF;
	                    END_IF;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_Activado := "DB2016_M_VF".M_VF[#t_Index].Estado_Activado;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_Enclavado := "DB2016_M_VF".M_VF[#t_Index].Estado_Enclavado;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_Salida := "DB2016_M_VF".M_VF[#t_Index].Estado_Salida;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_EntradaTermico := "DB2016_M_VF".M_VF[#t_Index].Estado_EntradaTermico;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_EntradaConfMarcha := "DB2016_M_VF".M_VF[#t_Index].Estado_EntradaConfMarcha;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_ValorActual := "DB2016_M_VF".M_VF[#t_Index].Estado_ValorActual;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_ValorTarjeta := "DB2016_M_VF".M_VF[#t_Index].Estado_ValorTarjeta;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_Escritura := "DB2016_M_VF".M_VF[#t_Index].Estado_Escritura;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Alarmas_ConfirmacionMarcha := "DB2016_M_VF".M_VF[#t_Index].Alarmas_ConfirmacionMarcha;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Alarmas_Escritura := "DB2016_M_VF".M_VF[#t_Index].Alarmas_Escritura;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Alarmas_General := "DB2016_M_VF".M_VF[#t_Index].Alarmas_General;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Alarmas_Mantenimiento := "DB2016_M_VF".M_VF[#t_Index].Alarmas_Mantenimiento;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Alarmas_Parametros := "DB2016_M_VF".M_VF[#t_Index].Alarmas_Parametros;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Alarmas_Termico := "DB2016_M_VF".M_VF[#t_Index].Alarmas_Termico;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ActivarAuto := "DB2016_M_VF".M_VF[#t_Index].Orden_ActivarAuto;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ConsignaAuto := "DB2016_M_VF".M_VF[#t_Index].Orden_ConsignaAuto;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Tiempos_Alarma := "DB2016_M_VF".M_VF[#t_Index].Tiempos_Alarma;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Tiempos_Mantenimiento := "DB2016_M_VF".M_VF[#t_Index].Tiempos_Mantenimiento;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Aux_oldActivado := "DB2016_M_VF".M_VF[#t_Index].Aux_oldActivado;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Aux_oldAlarma := "DB2016_M_VF".M_VF[#t_Index].Aux_oldAlarma;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Aux_oldAutoMan := "DB2016_M_VF".M_VF[#t_Index].Aux_oldAutoMan;
	                    "DB2016_M_VF".Mux[#for_mux].M_VF.Config_GrupoAlarma := "DB2016_M_VF".M_VF[#t_Index].Config_GrupoAlarma;
	                    
	                END_REGION DATOS_LECTURA
	                
	                
	                REGION DATOS_ESCRITURA
	                    
	                    //  ===========================================================================================================
	                    //  Reinicializamos valor existe cambio
	                    "DB2016_M_VF".Mux[#for_mux].ExisteCambio := false;
	
	                    //  ===========================================================================================================
	                    //  Estado auto/manual
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_AutoMan <> "DB2016_M_VF".M_VF[#t_Index].Estado_AutoMan THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Estado_AutoMan := "DB2016_M_VF".Mux[#for_mux].M_VF.Estado_AutoMan;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Ordenes
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ActivarManual <> "DB2016_M_VF".M_VF[#t_Index].Orden_ActivarManual THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Orden_ActivarManual := "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ActivarManual;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ResetHoras <> "DB2016_M_VF".M_VF[#t_Index].Orden_ResetHoras THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Orden_ResetHoras := "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ResetHoras;
	                        "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ResetHoras := FALSE;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ConsignaManual <> "DB2016_M_VF".M_VF[#t_Index].Orden_ConsignaManual THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Orden_ConsignaManual := "DB2016_M_VF".Mux[#for_mux].M_VF.Orden_ConsignaManual;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Configuracion
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetConfMarchaBit <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetConfMarchaBit THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetConfMarchaBit := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetConfMarchaBit;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetConfMarchaByte <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetConfMarchaByte THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetConfMarchaByte := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetConfMarchaByte;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetTermicoBit <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetTermicoBit THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetTermicoBit := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetTermicoBit;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetTermicoByte <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetTermicoByte THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionRetTermicoByte := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionRetTermicoByte;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionSalidaAnalogicaByte <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionSalidaAnalogicaByte THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionSalidaAnalogicaByte := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionSalidaAnalogicaByte;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionSalidaBit <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionSalidaBit THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionSalidaBit := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionSalidaBit;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionSalidaByte <> "DB2016_M_VF".M_VF[#t_Index].Config_DireccionSalidaByte THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_DireccionSalidaByte := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_DireccionSalidaByte;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_EscaladoMaxIngenieria <> "DB2016_M_VF".M_VF[#t_Index].Config_EscaladoMaxIngenieria THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_EscaladoMaxIngenieria := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_EscaladoMaxIngenieria;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_EscaladoMinIngenieria <> "DB2016_M_VF".M_VF[#t_Index].Config_EscaladoMinIngenieria THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_EscaladoMinIngenieria := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_EscaladoMinIngenieria;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_Habilitar <> "DB2016_M_VF".M_VF[#t_Index].Config_Habilitar THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_Habilitar := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_Habilitar;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarAlarmaEscrituraSalida <> "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarAlarmaEscrituraSalida THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarAlarmaEscrituraSalida := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarAlarmaEscrituraSalida;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarInvertirConfMarcha <> "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarInvertirConfMarcha THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarInvertirConfMarcha := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarInvertirConfMarcha;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarInvertirTermico <> "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarInvertirTermico THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarInvertirTermico := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarInvertirTermico;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarMantenimiento <> "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarMantenimiento THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarMantenimiento := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarMantenimiento;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarRetornoConfMarcha <> "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarRetornoConfMarcha THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarRetornoConfMarcha := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarRetornoConfMarcha;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarRetornoTermico <> "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarRetornoTermico THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_HabilitarRetornoTermico := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_HabilitarRetornoTermico;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Config_TipoAcceso <> "DB2016_M_VF".M_VF[#t_Index].Config_TipoAcceso THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Config_TipoAcceso := "DB2016_M_VF".Mux[#for_mux].M_VF.Config_TipoAcceso;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                    //  ===========================================================================================================
	                    //  Tiempos
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Tiempos_SetPointAlarma <> "DB2016_M_VF".M_VF[#t_Index].Tiempos_SetPointAlarma THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Tiempos_SetPointAlarma := "DB2016_M_VF".Mux[#for_mux].M_VF.Tiempos_SetPointAlarma;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    IF "DB2016_M_VF".Mux[#for_mux].M_VF.Tiempos_SetPointMantenimiento <> "DB2016_M_VF".M_VF[#t_Index].Tiempos_SetPointMantenimiento THEN
	                        "DB2016_M_VF".M_VF[#t_Index].Tiempos_SetPointMantenimiento := "DB2016_M_VF".Mux[#for_mux].M_VF.Tiempos_SetPointMantenimiento;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := true;
	                    END_IF;
	                    
	                END_REGION DATOS_ESCRITURA
	                
	                
	                REGION GESTION_CAMBIOS
	                    
	                    //  ===========================================================================================================
	                    //  Si existe cambios en el dispositivo generados por SCADA, actualizamos los datos en el resto de multiplexados,
	                    //  en caso de que este abierto el mismo dispositivo.
	                    IF "DB2016_M_VF".Mux[#for_mux].ExisteCambio THEN
	                        //  Recorremos todos los multiplexados
	                        FOR #for_mux_cambios := 0 TO "N_MAX_MUX_DISP" DO
	                            
	                            //  No miramos el multiplexado actual
	                            IF #for_mux_cambios <> #for_mux THEN
	                                
	                                //  En caso de que este seleccionado el mismo indice, movemos el dispositivo al multiplexado
	                                //  correspondiente
	                                IF #t_Index = "DB2016_M_VF".Mux[#for_mux_cambios].Index THEN
	                                    "DB2016_M_VF".Mux[#for_mux_cambios].M_VF := "DB2016_M_VF".M_VF[#t_Index];
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_FOR;
	                        "DB2016_M_VF".Mux[#for_mux].ExisteCambio := FALSE;
	                    END_IF;
	                    
	                END_REGION GESTION_CAMBIOS
	                
	            ELSE
	                
	                //  ===========================================================================================================
	                //  En caso de que el indice sea 0, movemos el valor de la M_VF[0] que no se usa para escribir el index.
	                "DB2016_M_VF".Mux[#for_mux].M_VF := "DB2016_M_VF".M_VF[0];
	                
	            END_IF;
	            
	        ELSE
	            
	            "DB2016_M_VF".Mux[#for_mux].ExisteCambio := FALSE;
	            "DB2016_M_VF".Mux[#for_mux].Index :=
	            "DB2016_M_VF".Mux[#for_mux].oldIndex := 0;
	            
	        END_IF;
	
	    END_FOR;
	    
	END_REGION MULTIPLEXADO
	
	
	REGION LOGICA_DEL_DISPOSITIVO
	    
	    // =============================================================================
	    // Resetear todas las alarmas para que se vuelvan a generar
	    FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	        "DB2016_M_VF".Agrup[#for_i].AlgunaAlarma := FALSE;
	        "DB2016_M_VF".Agrup[#for_i].AlgunaEnManual := FALSE;
	    END_FOR;
	    
	    FOR #for_i := 1 TO "N_MAX_DISP_M_VF" DO
	        
	        
	        // =============================================================================
	        // DISPOSITIVO HABILITADO
	        // =============================================================================
	        IF "DB2016_M_VF".M_VF[#for_i].Config_Habilitar THEN
	            
	            REGION LIMITE_GRUPO_ALARMA
	                
	                IF "DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma < 0 THEN
	                    "DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma := 0;
	                END_IF;
	                IF "DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma > "N_MAX_DISP_AGRUP" THEN
	                    "DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma := "N_MAX_DISP_AGRUP";
	                END_IF;
	                
	            END_REGION LIMITE_GRUPO_ALARMA
	            
	            // =============================================================================
	            //  PUESTA A CERO DE LA SALIDA
	            #t_Activar := FALSE;
	            #t_Frecuencia := 0.0;
	            
	            REGION LECTURA_VALORES
	                
	                CASE "DB2016_M_VF".M_VF[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        (* AREA: Pueden seleccionarse las siguientes áreas: 16#81: Input, 16#82: Output, 16#83: Marcas, 16#84: DB, 16#1: Entrada de periferia (solo S7-1500)
	                        DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                        BYTEOFFSET: Dirección en la que se lee. Solo se utilizan los 16 bits menos significativos.*)
	                        
	                        IF "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetTermicoByte >= 0 THEN
	                            
	                            "DB2016_M_VF".M_VF[#for_i].Estado_EntradaTermico := PEEK_BOOL(area := 16#81,
	                                                                                          dbNumber := 0,
	                                                                                          byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetTermicoByte,
	                                                                                          bitOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetTermicoBit);
	                            IF "DB2016_M_VF".M_VF[#for_i].Config_HabilitarInvertirTermico THEN
	                                
	                                "DB2016_M_VF".M_VF[#for_i].Estado_EntradaTermico := NOT (PEEK_BOOL(area := 16#81,
	                                                                                                   dbNumber := 0,
	                                                                                                   byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetTermicoByte,
	                                                                                                   bitOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetTermicoBit));
	                            END_IF;
	                        END_IF;
	                        
	                        // =============================================================================
	                        // RETORNO CONFIRMACION DE MARCHA
	                        IF "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetConfMarchaByte >= 0 THEN
	                            
	                            "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha := PEEK_BOOL(area := 16#81,
	                                                                                             dbNumber := 0,
	                                                                                             byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetConfMarchaByte,
	                                                                                             bitOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetConfMarchaBit);
	                            IF "DB2016_M_VF".M_VF[#for_i].Config_HabilitarInvertirConfMarcha THEN
	                                
	                                "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha := NOT (PEEK_BOOL(area := 16#81,
	                                                                                                      dbNumber := 0,
	                                                                                                      byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetConfMarchaByte,
	                                                                                                      bitOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionRetConfMarchaBit));
	                            END_IF;
	                        END_IF;
	                        
	                        
	                    #TIPO_ACCESO_PLC:
	                        ;
	                        
	                END_CASE;
	                
	            END_REGION LECTURA_VALORES
	            
	            
	            REGION MODOS_DE_TRABAJO
	                
	                // =============================================================================
	                //  MODO MANUAL
	                IF "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan THEN
	                    "DB2016_M_VF".Agrup["DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma].AlgunaEnManual := TRUE;
	                    IF "DB2016_M_VF".M_VF[#for_i].Orden_ActivarManual = TRUE AND #SeguridadesOK AND "DB2016_M_VF".M_VF[#for_i].Estado_SeguridadOk AND NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico THEN //En caso de enclavar manual NOT "DB2037_TMF1_DISP_M_VF".M_VF[#i].Estado_Enclavado
	                        #t_Activar := TRUE;
	                        #t_Frecuencia := "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaManual;
	                    ELSE
	                        #t_Activar := FALSE;
	                        #t_Frecuencia := 0.0;
	                        "DB2016_M_VF".M_VF[#for_i].Orden_ActivarManual := FALSE;
	                        
	                    END_IF;
	                ELSE
	                    "DB2016_M_VF".M_VF[#for_i].Orden_ActivarManual := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  MODO AUTO
	                IF NOT "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan THEN
	                    IF "DB2016_M_VF".M_VF[#for_i].Orden_ActivarAuto = TRUE AND NOT "DB2016_M_VF".M_VF[#for_i].Estado_Enclavado AND #SeguridadesOK AND "DB2016_M_VF".M_VF[#for_i].Estado_SeguridadOk AND NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico THEN
	                        #t_Activar := TRUE;
	                        #t_Frecuencia := "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaAuto;
	                        "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaManual := "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaAuto;
	                    ELSE
	                        #t_Activar := FALSE;
	                        #t_Frecuencia := 0.0;
	                    END_IF;
	                    
	                    "DB2016_M_VF".M_VF[#for_i].Orden_ActivarManual := "DB2016_M_VF".M_VF[#for_i].Estado_Activado;
	                    
	                END_IF;
	                
	            END_REGION MODOS_DE_TRABAJO
	            
	            
	            REGION ESTADO_DEL_DISPOSITIVO
	                
	                // =============================================================================
	                //  MOTOR SIMULADO
	                IF #Simulacion THEN
	                    
	                    IF #t_Activar THEN
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR RETORNO TERMICO Y CONFIRMACION DE MARCHA
	                IF NOT #Simulacion AND "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoTermico
	                    AND "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoConfMarcha
	                THEN
	                    
	                    IF NOT "DB2016_M_VF".M_VF[#for_i].Estado_EntradaTermico AND "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha THEN
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR RETORNO SOLO TERMICO
	                IF NOT #Simulacion AND "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoTermico
	                    AND NOT "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoConfMarcha THEN
	                    
	                    IF NOT "DB2016_M_VF".M_VF[#for_i].Estado_EntradaTermico AND #t_Activar THEN
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR RETORNO SOLO CONFIRMACION DE MARCHA
	                IF NOT #Simulacion AND NOT "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoTermico
	                    AND "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoConfMarcha THEN
	                    
	                    IF "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha THEN
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	                // =============================================================================
	                //  MOTOR SIN RETORNOS
	                IF NOT #Simulacion AND NOT "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoTermico
	                    AND NOT "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoConfMarcha THEN
	                    
	                    IF #t_Activar THEN
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := TRUE;
	                    ELSE
	                        "DB2016_M_VF".M_VF[#for_i].Estado_Activado := FALSE;
	                    END_IF;
	                    
	                END_IF;
	                
	            END_REGION ESTADO_DEL_DISPOSITIVO
	            
	            
	            REGION ERRORES
	                
	                // =============================================================================
	                //  CHEQUEO RETORNO TERMICO
	                IF NOT #Simulacion AND "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoTermico
	                    AND "DB2016_M_VF".M_VF[#for_i].Estado_EntradaTermico THEN
	                    #t_ErrorTermico := TRUE;
	                ELSE
	                    #t_ErrorTermico := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  CHEQUEO RETORNO CONFIRMACION DE MARCHA
	                IF NOT #Simulacion AND "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoConfMarcha AND
	                    (
	                    (#t_Activar AND NOT "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha)
	                    OR
	                    (NOT #t_Activar AND "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha)
	                    ) THEN
	                    #t_ErrorConfirmacionMarcha := TRUE;
	                ELSE
	                    #t_ErrorConfirmacionMarcha := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  TEMPORIZADO DE ERRORES
	                IF "DB2016_M_VF".M_VF[#for_i].Config_HabilitarRetornoConfMarcha
	                    AND #t_ErrorConfirmacionMarcha
	                    AND NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha
	                    AND NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico
	                THEN
	                    IF NOT #Simulacion AND #Pulso1seg THEN
	                        "DB2016_M_VF".M_VF[#for_i].Tiempos_Alarma += 1;
	                    END_IF;
	                ELSE
	                    "DB2016_M_VF".M_VF[#for_i].Tiempos_Alarma := 0;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR TERMICO
	                IF #t_ErrorTermico THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico := TRUE;
	                END_IF;
	                IF NOT #t_ErrorTermico THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR CONFIRMACION DE MARCHA
	                IF "DB2016_M_VF".M_VF[#for_i].Tiempos_Alarma >= "DB2016_M_VF".M_VF[#for_i].Tiempos_SetPointAlarma AND #t_ErrorConfirmacionMarcha THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha := TRUE;
	                END_IF;
	                IF NOT #t_ErrorConfirmacionMarcha THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha := FALSE;
	                END_IF;
	                
	                // =============================================================================
	                //  ERROR GLOBAL
	                IF "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico OR
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha
	                THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_General := TRUE;
	                END_IF;
	                IF #Ack AND
	                    NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico AND
	                    NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha
	                THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_General := FALSE;
	                END_IF;
	                //"DB2016_M_VF".M_VF[#for_i].Alarmas_General := "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico OR "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha OR "DB2016_M_VF".M_VF[#for_i].Alarmas_Escritura;
	                
	                IF "DB2016_M_VF".M_VF[#for_i].Alarmas_General THEN
	                    "DB2016_M_VF".Agrup["DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma].AlgunaAlarma := TRUE;
	                    // =============================================================================
	                    //  SI TENEMOS UN ERROR DESACTIVAMOS LA SALIDA
	                    #t_Frecuencia := 0.0;
	                END_IF;
	                
	            END_REGION ERRORES
	            
	            
	            REGION DIAGNOSIS
	                
	                //  =============================================================================
	                //  CONTADOR DE HORAS DE FUNCIONAMIENTO
	                IF "DB2016_M_VF".M_VF[#for_i].Orden_ResetHoras THEN
	                    "DB2016_M_VF".M_VF[#for_i].Orden_ResetHoras := FALSE;
	                END_IF;
	                IF NOT #Simulacion AND #Pulso1seg AND "DB2016_M_VF".M_VF[#for_i].Estado_Activado THEN
	                    "DB2016_M_VF".M_VF[#for_i].Tiempos_Mantenimiento += 0.00027778;
	                END_IF;
	                //  =============================================================================
	                //  ALARMA HORAS PARA MANTENIMIENTO ALCANZADOS
	                "DB2016_M_VF".M_VF[#for_i].Alarmas_Mantenimiento := FALSE;
	                IF "DB2016_M_VF".M_VF[#for_i].Config_HabilitarMantenimiento
	                    AND
	                    "DB2016_M_VF".M_VF[#for_i].Tiempos_Mantenimiento > "DB2016_M_VF".M_VF[#for_i].Tiempos_SetPointMantenimiento
	                THEN
	                    "DB2016_M_VF".M_VF[#for_i].Alarmas_Mantenimiento := TRUE;
	                END_IF;
	                
	                
	            END_REGION DIAGNOSIS
	            
	            
	            REGION ESCRITURA_SALIDA
	                
	                CASE "DB2016_M_VF".M_VF[#for_i].Config_TipoAcceso OF
	                        
	                    #TIPO_ACCESO_INDIRECTO:
	                        // =============================================================================
	                        // ESCRITURA SALIDA
	                        (* AREA: Pueden seleccionarse las siguientes áreas:16#81: Input, 16#82: Output, 16#83: Marcas, 16#84: DB, 16#2: Salida de periferia (solo S7-1500)      
	                        DBNUMBER: Número del bloque de datos si AREA = DB, de lo contrario "0"
	                        BYTEOFFSET: Dirección que se escribe, Solo se utilizan los 16 bits menos significativos. 
	                        BITOFFSET: Bit que se escribe, 
	                        VALUE: Valor que se escribe *)
	                        
	                        IF "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaByte >= 0 THEN
	                            
	                            IF #t_Activar AND NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_General THEN
	                                "DB2016_M_VF".M_VF[#for_i].Estado_Salida := TRUE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaBit,
	                                          value := TRUE);
	                            ELSE
	                                "DB2016_M_VF".M_VF[#for_i].Estado_Salida := FALSE;
	                                POKE_BOOL(area := 16#82,
	                                          dbNumber := 0,
	                                          byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaByte,
	                                          bitOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaBit,
	                                          value := FALSE);
	                            END_IF;
	                        END_IF;
	                        
	                    #TIPO_ACCESO_PLC:
	                        IF #t_Activar AND NOT "DB2016_M_VF".M_VF[#for_i].Alarmas_General THEN
	                            "DB2016_M_VF".M_VF[#for_i].Estado_Salida := TRUE;
	                        ELSE
	                            "DB2016_M_VF".M_VF[#for_i].Estado_Salida := FALSE;
	                        END_IF;
	                        
	                END_CASE;
	                
	            END_REGION ESCRITURA_SALIDA
	            
	            
	            REGION SALIDA
	                
	                //  =============================================================================
	                //  TRASPASO DE PARAMETROS
	                "DB2016_M_VF".M_VF[#for_i].Estado_ValorActual := #t_Frecuencia;
	                
	                //  =============================================================================
	                //  CONVERSIÓN DE VALORES
	                #t_y0 := INT_TO_REAL(0);
	                #t_y1 :=  INT_TO_REAL(27648);
	                #t_x := "DB2016_M_VF".M_VF[#for_i].Estado_ValorActual;
	                #t_x0 := "DB2016_M_VF".M_VF[#for_i].Config_EscaladoMinIngenieria;
	                #t_x1 := "DB2016_M_VF".M_VF[#for_i].Config_EscaladoMaxIngenieria;
	                
	                //  SI TENEMOS ORDEN DE ACTIVAR
	                IF #t_Activar THEN
	                    
	                    // =============================================================================
	                    //  ESCALADO Y = (X-x0)*((y1-y0)/(x1-x0)) + y0
	                    IF "DB2016_M_VF".M_VF[#for_i].Config_EscaladoMaxIngenieria > "DB2016_M_VF".M_VF[#for_i].Config_EscaladoMinIngenieria THEN
	                        #t_ValorSalida := ((#t_x - #t_x0) * ((#t_y1 - #t_y0) / (#t_x1 - #t_x0))) + #t_y0;
	                        "DB2016_M_VF".M_VF[#for_i].Alarmas_Parametros := FALSE;
	                    ELSE
	                        #t_ValorSalida := 0.0;
	                        "DB2016_M_VF".M_VF[#for_i].Alarmas_Parametros := TRUE;
	                    END_IF;
	                    
	                ELSE
	                    #t_ValorSalida := 0.0;
	                END_IF;
	                
	                
	                REGION ESCRITURA_SALIDA
	                    
	                    CASE "DB2016_M_VF".M_VF[#for_i].Config_TipoAcceso OF
	                            
	                        #TIPO_ACCESO_INDIRECTO:
	                            // =============================================================================
	                            //  ESCRITURA DEL CANAL - POKE (area) 16#2 para CPU 1500 ; 16#82 para CPU 1200
	                            IF "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaAnalogicaByte > 0 THEN
	                                
	                                "DB2016_M_VF".M_VF[#for_i].Estado_ValorTarjeta := REAL_TO_INT(#t_ValorSalida);
	                                
	                                POKE(area := 16#82,
	                                     dbNumber := 0,
	                                     byteOffset := "DB2016_M_VF".M_VF[#for_i].Config_DireccionSalidaByte,
	                                     value := INT_TO_WORD("DB2016_M_VF".M_VF[#for_i].Estado_ValorTarjeta));
	                                
	                                "DB2016_M_VF".M_VF[#for_i].Estado_Escritura := GET_ERR_ID();
	                                IF "DB2016_M_VF".M_VF[#for_i].Estado_Escritura <> 0 THEN
	                                    "DB2016_M_VF".M_VF[#for_i].Alarmas_Escritura := TRUE;
	                                ELSE
	                                    "DB2016_M_VF".M_VF[#for_i].Alarmas_Escritura := FALSE;
	                                END_IF;
	                                
	                            ELSE
	                                
	                                "DB2016_M_VF".M_VF[#for_i].Estado_ValorTarjeta := 0;
	                                
	                            END_IF;
	                            
	                        #TIPO_ACCESO_PLC:
	                            // =============================================================================
	                            //  ESCRITURA VALORES DE LA TARJETA
	                            "DB2016_M_VF".M_VF[#for_i].Estado_ValorTarjeta := REAL_TO_INT(#t_ValorSalida);
	                            
	                    END_CASE;
	                    
	                END_REGION ESCRITURA_SALIDA
	                
	                
	            END_REGION SALIDA
	            
	            
	            
	            // =============================================================================
	            //  RESET ORDEN ACTIVAR EN AUTO
	            "DB2016_M_VF".M_VF[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Estado_Enclavado := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaAuto := 0.0;
	            
	            
	            REGION TRAZABILIDAD_MANUALIZACION
	                
	                IF "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan AND NOT "DB2016_M_VF".M_VF[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_16_DISP_M_VF",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M_VF",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF NOT "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan AND "DB2016_M_VF".M_VF[#for_i].Aux_oldAutoMan THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_16_DISP_M_VF",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M_VF",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan AND "DB2016_M_VF".M_VF[#for_i].Estado_Activado AND NOT "DB2016_M_VF".M_VF[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_16_DISP_M_VF",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M_VF",
	                                            CodInt_2 := #for_i,
	                                            CodInt_3 := "TRZ_SYS_DISP_ACC_MAN_ON",
	                                            CodInt_4 := 0,
	                                            CodInt_5 := 0,
	                                            CodReal_1 := 0.0,
	                                            CodReal_2 := 0.0);
	                END_IF;
	                
	                IF "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan AND NOT "DB2016_M_VF".M_VF[#for_i].Estado_Activado AND "DB2016_M_VF".M_VF[#for_i].Aux_oldActivado THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRZ_CAT_16_DISP_M_VF",
	                                            User := #UsuarioActual,
	                                            CodInt_1 := "TRZ_SYS_DISP_TIPO_M_VF",
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
	            "DB2016_M_VF".M_VF[#for_i].Aux_oldAutoMan := "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan;
	            "DB2016_M_VF".M_VF[#for_i].Aux_oldActivado := "DB2016_M_VF".M_VF[#for_i].Estado_Activado;
	        ELSE
	            
	            // =============================================================================
	            // DISPOSITIVO NO HABILITADO
	            // =============================================================================
	            "DB2016_M_VF".M_VF[#for_i].Alarmas_General := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Alarmas_Termico := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Alarmas_ConfirmacionMarcha := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Alarmas_Mantenimiento := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Alarmas_Escritura := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Estado_EntradaTermico := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Estado_EntradaConfMarcha := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Estado_Enclavado := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Estado_ValorTarjeta := 0;
	            "DB2016_M_VF".M_VF[#for_i].Orden_ActivarAuto := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Estado_Activado := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Tiempos_Alarma := 0;
	            "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaAuto := 0.0;
	            "DB2016_M_VF".M_VF[#for_i].Orden_ConsignaManual := 0.0;
	            "DB2016_M_VF".M_VF[#for_i].Estado_ValorActual := 0.0;
	            "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Orden_ActivarManual := FALSE;
	            
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
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X0 := "DB2016_M_VF".M_VF[#for_i].Config_Habilitar;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X1 := "DB2016_M_VF".M_VF[#for_i].Estado_AutoMan;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X2 := "DB2016_M_VF".M_VF[#for_i].Estado_Enclavado;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X3 := "DB2016_M_VF".M_VF[#for_i].Estado_Activado;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X3 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X4 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X5 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X6 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X7 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X8 := "DB2016_M_VF".M_VF[#for_i].Alarmas_General;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X9 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X10 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X11 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X12 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X13 := "DB2016_M_VF".M_VF[#for_i].Alarmas_Mantenimiento;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X14 := FALSE;
	            "DB2016_M_VF".M_VF[#for_i].Hmi_Estado.%X15 := FALSE;
	            
	        END_REGION GESTION_HMI
	        
	        REGION GESTION_NUEVA_ALARMA
	            
	            // =============================================================================
	            //  DETECCION DE NUEVA ALARMA
	            IF "DB2016_M_VF".M_VF[#for_i].Alarmas_General AND NOT "DB2016_M_VF".M_VF[#for_i].Aux_oldAlarma THEN
	                "DB2016_M_VF".Agrup["DB2016_M_VF".M_VF[#for_i].Config_GrupoAlarma].NuevaAlarma := TRUE;
	            END_IF;
	            
	            //  Estado anterior de las alarmas
	            "DB2016_M_VF".M_VF[#for_i].Aux_oldAlarma := "DB2016_M_VF".M_VF[#for_i].Alarmas_General;
	            
	        END_REGION GESTION_NUEVA_ALARMA
	        
	        
	    END_FOR;
	    
	    // =============================================================================
	    //  ACUSE DE NUEVAS ALARMAS
	    IF #Ack THEN
	        FOR #for_i := 0 TO "N_MAX_DISP_AGRUP" DO
	            "DB2016_M_VF".Agrup[#for_i].NuevaAlarma := FALSE;
	        END_FOR;
	    END_IF;
	    
	END_REGION LOGICA_DEL_DISPOSITIVO
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>