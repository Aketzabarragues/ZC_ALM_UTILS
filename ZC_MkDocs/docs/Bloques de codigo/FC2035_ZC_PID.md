---
title: FC2035_ZC_PID
---
# FC FC2035_ZC_PID

!!! info "Información del Sistema"
    **Hardware:** -<br>
    **Ingeniería:** -<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `PV` | `Real` | - | `-` | Valor de proceso |
| `DispManAuto` | `Bool` | - | `-` | Dispositivo Manual - Auto |
| `DispValorActual` | `Real` | - | `-` | Dispositivo valor actual |
| `Ack` | `Bool` | - | `-` | Acuse general |
| `Fecha` | `DTL` | - | `-` | Fecha y hora actual |
| `Usuario` | `String` | - | `-` | Usuario actual |
| `NumeroPID` | `Int` | - | `-` | Numero de PID |
| `RangoSuperiorEscalado` | `Real` | - | `-` | Rango superior de valor de proceso para escalado 0-100% |
| `RangoInferiorEscalado` | `Real` | - | `-` | Rango inferior de valor de proceso para escalado 0-100% |

### Entrada/Salida
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `PID_CompactConfig` | `PID_CompactConfig` | - | `-` | - |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `t_Norm_X` | `LReal` | - | `-` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC2035_ZC_PID" : Void
TITLE = FC2035_PID
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion de gestion dispositivo PID
   VAR_INPUT 
      PV : Real;   // Valor de proceso
      DispManAuto : Bool;   // Dispositivo Manual - Auto
      DispValorActual : Real;   // Dispositivo valor actual
      Ack : Bool;   // Acuse general
      Fecha {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
      Usuario : String;   // Usuario actual
      NumeroPID : Int;   // Numero de PID
      RangoSuperiorEscalado : Real;   // Rango superior de valor de proceso para escalado 0-100%
      RangoInferiorEscalado : Real;   // Rango inferior de valor de proceso para escalado 0-100%
   END_VAR

   VAR_IN_OUT 
      PID_CompactConfig {InstructionName := 'PID_CompactConfig'; LibVersion := '1.2'} : PID_CompactConfig;
      PID_CompactControlParams {InstructionName := 'PID_CompactControlParams'; LibVersion := '1.2'} : PID_CompactControlParams;
   END_VAR

   VAR_TEMP 
      t_Norm_X : LReal;
   END_VAR


BEGIN
	(*  
	ZEUS CONTROL, S.A.
	(c)Copyright (2025) All Rights Reserved
	--------------------------------------------------------------------------------------
	
	Software:       TIA Portal 18
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC2030_ZC_DISP_PID
	Descripcion:    Bloque de gestion de dispositivos PID
	
	Dependencias:
	    FC:         -
	    FB:         -
	    UDT:        ZC_DISP_PID
	    DB:         DB2035_PID
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    12.05.2023  (ABH)               Primera version 
	    01.00.01    18.07.2023  (ABH)               Cambio en interfaz bloque. Se pasa IN/OUT solo el PID_COMPACT.
	                                                Se añade a UDT el nombre del PID.
	                                                Se añade como Input el numero de PID en el array de dispositivo PID.
	    01.00.02    05.09.2023  (ABH)               Cambio en UDT PID para añadir rampa para gestion de Set Point.
	                                                Se añade gestion de rampa SP PID.
	    01.00.03    18.09.2023  (ABH)               Reset de consigna auto al final de la gestion del dispositivo.
	                                                Se añade trazabilidad de forzado.
	    01.00.04    16.02.2024  (ABH)               Se elimina el PID compact y la gestion de la rampa en este FC. Se separa en FC2036_PID_COMPACT
	                                                para ser llamado en OB de interrupcion.
	    01.00.05    13.06.2024  (ABH)               Se añade gestion multiplexado para Scada (no indexado)
	    01.00.06    08.01.2025  (ABH)               Se eñlimina multiplexado PID. Se realiza en FC aparte.    
	    01.00.07    24.04.2025  (HCR)               Se añade gestion de idioma
	    01.00.08    11.09.2025  (ABH)               Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para
	                                                facilitar su traduccion. Se añade indexHMI para lista de 
	                                                texto en sistemas de supervision.
	                                                
	//=====================================================================================
	*)
	
	
	REGION TRASPASO_DE_PARAMETROS
	    
	    //  ===============================================================================================================
	    //  TRASPASO DE PARAMETROS A PID COMPACT
	    //  Valores regulacion
	    #PID_CompactControlParams.Gain := "DB2035_PID".PID[#NumeroPID].Config_Gain;
	    #PID_CompactControlParams.Ti := "DB2035_PID".PID[#NumeroPID].Config_Ti;
	    #PID_CompactControlParams.Td := "DB2035_PID".PID[#NumeroPID].Config_Td;
	    //  Tipo Entrada
	    #PID_CompactConfig.InputPerOn := "DB2035_PID".PID[#NumeroPID].Config_TipoEntrada;
	    //  Tipo de control (Directo/Inverso)
	    #PID_CompactConfig.InvertControl := "DB2035_PID".PID[#NumeroPID].Config_InvertirControl;
	    //  Limites y avisos
	    #PID_CompactConfig.InputUpperLimit := 99999.0;
	    #PID_CompactConfig.InputLowerLimit := -99999.0;
	    #PID_CompactConfig.InputUpperWarning := 99999.0;
	    #PID_CompactConfig.InputLowerWarning := -99999.0;
	    //  Valor proceso
	    "DB2035_PID".PID[#NumeroPID].Estado_PV := #PV;
	    
	    "DB2035_PID".PID[#NumeroPID].Config_LimiteSuperiorEntrada := #RangoSuperiorEscalado;
	    "DB2035_PID".PID[#NumeroPID].Config_LimiteInferiorEntrada := #RangoInferiorEscalado;
	    
	    "DB2035_PID".PID[#NumeroPID].Orden_Ack := #Ack;
	    
	END_REGION
	
	
	REGION MODOS_DE_TRABAJO
	    
	    //  ===============================================================================================================
	    // Selector: (0) Automatico / (1) Manual
	    "DB2035_PID".PID[#NumeroPID].Estado_AutoMan :=
	    (#DispManAuto) OR
	    ("DB2035_PID".PID[#NumeroPID].Orden_ActivarAuto AND "DB2035_PID".PID[#NumeroPID].Orden_Forzar) OR
	    (NOT "DB2035_PID".PID[#NumeroPID].Orden_ActivarAuto);
	    
	    //  Reset señal forzado
	    IF NOT "DB2035_PID".PID[#NumeroPID].Orden_ActivarAuto THEN
	        "DB2035_PID".PID[#NumeroPID].Orden_Forzar := FALSE;
	    END_IF;
	    
	END_REGION
	
	
	REGION LIMITES_SALIDA
	    
	    //  ===============================================================================================================
	    //  Configuracion del limite de la salida del PID en funcion del estado Manual/Automatico
	    IF "DB2035_PID".PID[#NumeroPID].Estado_AutoMan THEN
	        //  En modo manual, configuramos el limite de la salida de 0-100%, para que al manualizar el PID se pueda poner el valor que se quiera
	        #PID_CompactConfig.OutputUpperLimit := 100.0;
	        #PID_CompactConfig.OutputLowerLimit := 0.0;
	    ELSE
	        #PID_CompactConfig.OutputUpperLimit := "DB2035_PID".PID[#NumeroPID].Config_LimiteSuperiorSalida;
	        #PID_CompactConfig.OutputLowerLimit := "DB2035_PID".PID[#NumeroPID].Config_LimiteInferiorSalida;
	    END_IF;
	    
	END_REGION
	
	
	REGION ESTADOS
	    
	    //  ===============================================================================================================
	    //  REALIMENTACION DE LAS ENTRADAS/SALIDAS DEL PID
	    //  Estado automatico
	    IF NOT "DB2035_PID".PID[#NumeroPID].Estado_AutoMan THEN
	        "DB2035_PID".PID[#NumeroPID].Aux_SP_Manual := "DB2035_PID".PID[#NumeroPID].Estado_ValorSalida;
	        "DB2035_PID".PID[#NumeroPID].Orden_ConsignaForzado := "DB2035_PID".PID[#NumeroPID].Estado_ValorSalida;
	    ELSE
	        
	        //  Estado manual - Consigna forzar PID
	        IF NOT #DispManAuto AND "DB2035_PID".PID[#NumeroPID].Orden_Forzar THEN
	            "DB2035_PID".PID[#NumeroPID].Aux_SP_Manual := "DB2035_PID".PID[#NumeroPID].Orden_ConsignaForzado;
	            //  Estado manual - Dispositivo forzado
	        ELSIF #DispManAuto AND NOT "DB2035_PID".PID[#NumeroPID].Orden_Forzar THEN
	            "DB2035_PID".PID[#NumeroPID].Aux_SP_Manual := "DB2035_PID".PID[#NumeroPID].Orden_ConsignaForzado := #DispValorActual;
	        ELSIF #DispManAuto AND "DB2035_PID".PID[#NumeroPID].Orden_Forzar THEN
	            "DB2035_PID".PID[#NumeroPID].Aux_SP_Manual := "DB2035_PID".PID[#NumeroPID].Orden_ConsignaForzado := #DispValorActual;
	        ELSE
	            "DB2035_PID".PID[#NumeroPID].Aux_SP_Manual := "DB2035_PID".PID[#NumeroPID].Orden_ConsignaForzado := #DispValorActual;
	        END_IF;
	        
	    END_IF;
	    
	    
	    //  ===============================================================================================================
	    //  CALCULO DE VALORES EN 0-100%
	    //  SP
	    #t_Norm_X := NORM_X(MIN := #RangoInferiorEscalado, VALUE := "DB2035_PID".PID[#NumeroPID].Orden_ConsignaAuto, MAX := #RangoSuperiorEscalado);
	    "DB2035_PID".PID[#NumeroPID].Estado_SP_0_100 := LREAL_TO_REAL(SCALE_X(MIN := 0.0, VALUE := #t_Norm_X, MAX := 100.0));
	    
	    //  PV
	    #t_Norm_X := NORM_X(MIN := #RangoInferiorEscalado, VALUE := "DB2035_PID".PID[#NumeroPID].Estado_PV, MAX := #RangoSuperiorEscalado);
	    "DB2035_PID".PID[#NumeroPID].Estado_PV_0_100 := LREAL_TO_REAL(SCALE_X(MIN := 0.0, VALUE := #t_Norm_X, MAX := 100.0));
	    
	    //  Error SP - PV
	    "DB2035_PID".PID[#NumeroPID].Estado_Error_SP_PV_0_100 := ABS("DB2035_PID".PID[#NumeroPID].Estado_SP_0_100 - "DB2035_PID".PID[#NumeroPID].Estado_PV_0_100);
	    
	END_REGION
	
	
	REGION CAMBIO_MODO
	    
	    //  ===============================================================================================================
	    //  Gestion modo de trabajo del PID (Manual/Automatico)
	    IF "DB2035_PID".PID[#NumeroPID].Estado_AutoMan THEN
	        "DB2035_PID".PID[#NumeroPID].Estado_Mode := 4;
	    ELSE
	        "DB2035_PID".PID[#NumeroPID].Estado_Mode := 3;
	    END_IF;
	    
	    //  Flanco para cambio de modo
	    "DB2035_PID".PID[#NumeroPID].Estado_ModeActivate := "DB2035_PID".PID[#NumeroPID].Estado_Mode <> "DB2035_PID".PID[#NumeroPID].Aux_oldMode;
	    //  Valor anterior de modo para flancos
	    "DB2035_PID".PID[#NumeroPID].Aux_oldMode := "DB2035_PID".PID[#NumeroPID].Estado_Mode;
	    
	END_REGION
	
	
	REGION TRAZABILIDAD
	    
	     //  =============================================================================================
	     //  TRAZA CAMBIOS EN VALOR P
	    IF "DB2035_PID".PID[#NumeroPID].Aux_oldGain <> "DB2035_PID".PID[#NumeroPID].Config_Gain THEN
	        "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                Registrar := 1,
	                                Categoria := "TRZ_CAT_18_DISP_PID_VAL",
	                                User := "DB1_SYS".Usuario.Actual,
	                                CodInt_1 := "TRZ_SYS_DISP_TIPO_PID",
	                                CodInt_2 := #NumeroPID,
	                                CodInt_3 := "TRZ_SYS_DISP_ACC_CAM_P",
	                                CodInt_4 := "TRZ_SYS_COM_FLECHA",
	                                CodInt_5 := 0,
	                                CodReal_1 := "DB2035_PID".PID[#NumeroPID].Aux_oldGain,
	                                CodReal_2 := "DB2035_PID".PID[#NumeroPID].Config_Gain);
	     END_IF;
	     
	     
	     //  =============================================================================================
	     //  TRAZA CAMBIOS EN VALOR P
	     IF "DB2035_PID".PID[#NumeroPID].Aux_oldTi <> "DB2035_PID".PID[#NumeroPID].Config_Ti THEN
	         "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                 Registrar := 1,
	                                 Categoria := "TRZ_CAT_18_DISP_PID_VAL",
	                                 User := "DB1_SYS".Usuario.Actual,
	                                 CodInt_1 := "TRZ_SYS_DISP_TIPO_PID",
	                                 CodInt_2 := #NumeroPID,
	                                 CodInt_3 := "TRZ_SYS_DISP_ACC_CAM_I",
	                                 CodInt_4 := "TRZ_SYS_COM_FLECHA",
	                                 CodInt_5 := 0,
	                                 CodReal_1 := "DB2035_PID".PID[#NumeroPID].Aux_oldTi,
	                                 CodReal_2 := "DB2035_PID".PID[#NumeroPID].Config_Ti);
	     END_IF;
	    
	     
	     //  =============================================================================================
	     //  TRAZA CAMBIOS EN VALOR P
	     IF "DB2035_PID".PID[#NumeroPID].Aux_oldTd <> "DB2035_PID".PID[#NumeroPID].Config_Td THEN
	         "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                 Registrar := 1,
	                                 Categoria := "TRZ_CAT_18_DISP_PID_VAL",
	                                 User := "DB1_SYS".Usuario.Actual,
	                                 CodInt_1 := "TRZ_SYS_DISP_TIPO_PID",
	                                 CodInt_2 := #NumeroPID,
	                                 CodInt_3 := "TRZ_SYS_DISP_ACC_CAM_D",
	                                 CodInt_4 := "TRZ_SYS_COM_FLECHA",
	                                 CodInt_5 := 0,
	                                 CodReal_1 := "DB2035_PID".PID[#NumeroPID].Aux_oldTd,
	                                 CodReal_2 := "DB2035_PID".PID[#NumeroPID].Config_Td);
	     END_IF; 
	    
	    
	    //  =============================================================================================
	    //  TRAZA FORZADO PID
	     IF "DB2035_PID".PID[#NumeroPID].Orden_Forzar AND NOT "DB2035_PID".PID[#NumeroPID].Aux_oldForzar THEN
	         "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                 Registrar := 1,
	                                 Categoria := "TRZ_CAT_19_DISP_PID_ORD",
	                                 User := "DB1_SYS".Usuario.Actual,
	                                 CodInt_1 := "TRZ_SYS_DISP_TIPO_PID",
	                                 CodInt_2 := #NumeroPID,
	                                 CodInt_3 := "TRZ_SYS_DISP_ACC_MAN",
	                                 CodInt_4 := 0,
	                                 CodInt_5 := 0,
	                                 CodReal_1 := 0.0,
	                                 CodReal_2 := 0.0);
	    END_IF;
	    IF NOT "DB2035_PID".PID[#NumeroPID].Orden_Forzar AND "DB2035_PID".PID[#NumeroPID].Aux_oldForzar THEN
	        "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                Registrar := 1,
	                                Categoria := "TRZ_CAT_19_DISP_PID_ORD",
	                                User := "DB1_SYS".Usuario.Actual,
	                                CodInt_1 := "TRZ_SYS_DISP_TIPO_PID",
	                                CodInt_2 := #NumeroPID,
	                                CodInt_3 := "TRZ_SYS_DISP_ACC_AUTO",
	                                CodInt_4 := 0,
	                                CodInt_5 := 0,
	                                CodReal_1 := 0.0,
	                                CodReal_2 := 0.0);
	    END_IF; 
	    
	    
	    //  =============================================================================================
	    //  Guardamos valores anteriores
	    "DB2035_PID".PID[#NumeroPID].Aux_oldGain := "DB2035_PID".PID[#NumeroPID].Config_Gain;
	    "DB2035_PID".PID[#NumeroPID].Aux_oldTi := "DB2035_PID".PID[#NumeroPID].Config_Ti;
	    "DB2035_PID".PID[#NumeroPID].Aux_oldTd := "DB2035_PID".PID[#NumeroPID].Config_Td;
	    "DB2035_PID".PID[#NumeroPID].Aux_oldForzar := "DB2035_PID".PID[#NumeroPID].Orden_Forzar;
	    
	END_REGION
	
	
	"DB2035_PID".PID[#NumeroPID].Aux_SP_Auto := "DB2035_PID".PID[#NumeroPID].Orden_ConsignaAuto;
	
	// =============================================================================
	//  Reset de orden automatica
	"DB2035_PID".PID[#NumeroPID].Orden_ActivarAuto := FALSE;
	"DB2035_PID".PID[#NumeroPID].Orden_ConsignaAuto := 0.0;
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>