---
title: FC21_GESTION_SCADA
---
# FC FC21_GESTION_SCADA

!!! info "Información del Sistema"
    **Hardware:** -<br>
    **Ingeniería:** -<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Interfaz de Variables
### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC21_GESTION_SCADA" : Void
TITLE = FC21_GESTION_SCADA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Gestor de conexiones con SCADA, para determinar quien es el maestro en un sistema de dos equipos monopuesto
   VAR_TEMP 
      for_i : Int;
   END_VAR


BEGIN
	(* (*
	ZEUS CONTROL, S.A.
	(c)Copyright (2023) All Rights Reserved
	--------------------------------------------------------------------------------------
	
	Software:       TIA Portal 18
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC10_GESTION_SCADA
	Descripcion:    Gestor de conexiones con SCADA, para determinar quien es el maestro en un sistema de 
	                dos equipos monopuesto
	
	Dependencias:
	    FC:         FC2928_ZC_TON_INDV
	                FC2929_ZC_TOF_INDV
	    FB:         -
	    DB:         -
	    UDT:        -
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    30.08.2024  (ABH)                Primera version.
	    
	//=====================================================================================
	*)
	
	
	REGION GESTION_CONEXION_OK
	    
	    //  ====================================================================================
	    //  Gestion bit de vida
	    FOR #for_i := 0 TO 1 DO
	        
	        "DB16_GESTION_SCADA".ConexionOk[#for_i] := FALSE;
	        "DB16_GESTION_SCADA".TON_ON[#for_i].SP := 3;
	        "DB16_GESTION_SCADA".TON_OFF[#for_i].SP := 3;
	        
	        "DB16_GESTION_SCADA".TON_ON[#for_i].IN := "DB16_GESTION_SCADA".BitDevida[#for_i];
	        "DB16_GESTION_SCADA".TON_OFF[#for_i].IN := NOT "DB16_GESTION_SCADA".BitDevida[#for_i];
	        IF "DB16_GESTION_SCADA".TON_ON[#for_i].Q OR "DB16_GESTION_SCADA".TON_OFF[#for_i].Q THEN
	            "DB16_GESTION_SCADA".ConexionOk[#for_i] := FALSE;
	        ELSE
	            "DB16_GESTION_SCADA".ConexionOk[#for_i] := TRUE;
	        END_IF;
	        
	    END_FOR;
	
	    
	END_REGION
	
	
	REGION DEFINICION_MAESTRO
	    
	    //  Si no estan las conexion OK con ninguno de los dos SCADAS, ponemos el maestro a -1
	    IF NOT "DB16_GESTION_SCADA".ConexionOk[0] AND NOT "DB16_GESTION_SCADA".ConexionOk[1] THEN
	        "DB16_GESTION_SCADA".Maestro := -1;
	    END_IF;
	    
	    //  Si todavia no se ha seleccionado ningun maestro, comprobamos el estado de la conexion con los dos Scadas.
	    IF "DB16_GESTION_SCADA".Maestro = -1 THEN
	        
	        //  Si esta OK la conexion con SCADA01, lo marcamos como el maestro actual
	        IF "DB16_GESTION_SCADA".ConexionOk[0] THEN
	            "DB16_GESTION_SCADA".Maestro := 10;
	        END_IF;
	        
	        //  Si esta OK la conexion con SCADA02 y el SCADA01 esta NO OK, lo marcamos como el maestro actual
	        IF NOT "DB16_GESTION_SCADA".ConexionOk[0] AND "DB16_GESTION_SCADA".ConexionOk[1] THEN
	            "DB16_GESTION_SCADA".Maestro := 11;
	        END_IF;
	        
	    END_IF;
	    
	    //  Reset seleccion maestro si pierde la conexion
	    CASE "DB16_GESTION_SCADA".Maestro OF
	        10:  
	            IF NOT "DB16_GESTION_SCADA".ConexionOk[0] THEN
	                "DB16_GESTION_SCADA".Maestro := -1;
	            END_IF;
	        11:
	            IF NOT "DB16_GESTION_SCADA".ConexionOk[1] THEN
	                "DB16_GESTION_SCADA".Maestro := -1;
	            END_IF;
	    END_CASE;
	    
	    //  Gestion marcas para ejecucion de scripts
	    "DB16_GESTION_SCADA".PermisoInformes[0] := "DB16_GESTION_SCADA".Maestro = 10;
	    "DB16_GESTION_SCADA".PermisoInformes[1] := "DB16_GESTION_SCADA".Maestro = 11;
	    
	END_REGION
	
	
	REGION DEFICION_SINCRONIZACION
	    
	    
	    //  ====================================================================================
	    //  Comprobamos que estan ambos Scadas conectados
	    "DB16_GESTION_SCADA".Sincronizacion.AmbosConectados := "DB16_GESTION_SCADA".ConexionOk[0] AND "DB16_GESTION_SCADA".ConexionOk[1];
	    
	    
	    //  ====================================================================================
	    //  Reseteamos ordenes de sincronizacion.
	    //  Si estan ambos conectados, quitamos las ordenes de sincronizacion
	    IF NOT "DB16_GESTION_SCADA".Sincronizacion.AmbosConectados THEN
	        
	        "DB16_GESTION_SCADA".Sincronizacion.Informes[0] :=
	        "DB16_GESTION_SCADA".Sincronizacion.CIP[0] :=
	        "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[0] :=
	        "DB16_GESTION_SCADA".Sincronizacion.Cocina1[0] := 0;
	        "DB16_GESTION_SCADA".Sincronizacion.Informes[1] :=
	        "DB16_GESTION_SCADA".Sincronizacion.CIP[1] :=
	        "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[1] :=
	        "DB16_GESTION_SCADA".Sincronizacion.Cocina1[1] := 0;
	        
	    END_IF;
	    
	    
	    
	    //  ====================================================================================
	    //  Cuando se conecten los dos SCADAs, lanzamos orden para que se sincronicen
	    IF "DB16_GESTION_SCADA".Sincronizacion.AmbosConectados AND NOT "DB16_GESTION_SCADA".Aux.OldAmbosConectados THEN
	        IF "DB16_GESTION_SCADA".Maestro = 10 THEN
	            "DB16_GESTION_SCADA".Sincronizacion.Informes[1] :=
	            "DB16_GESTION_SCADA".Sincronizacion.CIP[1] :=
	            "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[1] :=
	            "DB16_GESTION_SCADA".Sincronizacion.Cocina1[1] := 2;
	        END_IF;
	        IF "DB16_GESTION_SCADA".Maestro = 11 THEN
	            "DB16_GESTION_SCADA".Sincronizacion.Informes[0] :=
	            "DB16_GESTION_SCADA".Sincronizacion.CIP[0] :=
	            "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[0] :=
	            "DB16_GESTION_SCADA".Sincronizacion.Cocina1[0] := 2;
	        END_IF;
	        
	    END_IF;
	    
	    "DB16_GESTION_SCADA".Aux.OldAmbosConectados := "DB16_GESTION_SCADA".Sincronizacion.AmbosConectados;
	    
	END_REGION
	
	
	REGION GESTION_ESTADO_OK
	    
	    //  ====================================================================================
	    //  Gestion estado sinronizacion OK
	    FOR #for_i := 0 TO 1 DO
	        
	        "DB16_GESTION_SCADA".TON_CIP_ESTADO[#for_i].SP := 
	        "DB16_GESTION_SCADA".TON_INFORME_ESTADO[#for_i].SP := 
	        "DB16_GESTION_SCADA".TON_COCINA1_ESTADO[#for_i].SP := 
	        "DB16_GESTION_SCADA".TON_FERM_ESTADO[#for_i].SP := 2;
	        
	        
	        
	        "DB16_GESTION_SCADA".TON_CIP_ESTADO[#for_i].IN := "DB16_GESTION_SCADA".Sincronizacion.CIP[#for_i] = 4 OR "DB16_GESTION_SCADA".Sincronizacion.CIP[#for_i] = 12;
	        IF "DB16_GESTION_SCADA".TON_CIP_ESTADO[#for_i].Q THEN
	            IF "DB16_GESTION_SCADA".Sincronizacion.CIP[#for_i] = 12 THEN
	                "FC8_ZC_TRAZA_REGISTRO"(FechaHora:="DB1_SYS".FechaHoraActual,
	                                        Registrar:=1,
	                                        Categoria:="TRAZA_CAT_1_SISTEMA",
	                                        User:='',
	                                        Codigo1:=0,
	                                        Codigo2:=0,
	                                        Codigo3:=0,
	                                        Texto:='Fallo al sincronizar registros CIP',
	                                        CodInt_1:=_int_in_,
	                                        CodInt_2:=_int_in_,
	                                        CodInt_3:=_int_in_,
	                                        CodInt_4:=_int_in_,
	                                        CodInt_5:=_int_in_,
	                                        CodReal_1:=_real_in_,
	                                        CodReal_2:=_real_in_);
	            END_IF;
	            "DB16_GESTION_SCADA".Sincronizacion.CIP[#for_i] := 0;
	        END_IF;
	        
	        "DB16_GESTION_SCADA".TON_INFORME_ESTADO[#for_i].IN := "DB16_GESTION_SCADA".Sincronizacion.Informes[#for_i] = 4 OR "DB16_GESTION_SCADA".Sincronizacion.Informes[#for_i] = 12;
	        IF "DB16_GESTION_SCADA".TON_INFORME_ESTADO[#for_i].Q THEN
	            IF "DB16_GESTION_SCADA".Sincronizacion.Informes[#for_i] = 12 THEN
	                "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                        Registrar := 1,
	                                        Categoria := "TRAZA_CAT_1_SISTEMA",
	                                        User := '',
	                                        Codigo1 := 0,
	                                        Codigo2 := 0,
	                                        Codigo3 := 0,
	                                        Texto := 'Fallo al sincronizar registros CIP',
	                                        CodInt_1:=_int_in_,
	                                        CodInt_2:=_int_in_,
	                                        CodInt_3:=_int_in_,
	                                        CodInt_4:=_int_in_,
	                                        CodInt_5:=_int_in_,
	                                        CodReal_1:=_real_in_,
	                                        CodReal_2:=_real_in_);
	            END_IF;
	            "DB16_GESTION_SCADA".Sincronizacion.Informes[#for_i] := 0;
	        END_IF;
	        
	        "DB16_GESTION_SCADA".TON_COCINA1_ESTADO[#for_i].IN := "DB16_GESTION_SCADA".Sincronizacion.Cocina1[#for_i] = 4 OR "DB16_GESTION_SCADA".Sincronizacion.Cocina1[#for_i] = 12;
	        IF "DB16_GESTION_SCADA".TON_COCINA1_ESTADO[#for_i].Q THEN
	            IF "DB16_GESTION_SCADA".Sincronizacion.Cocina1[#for_i] = 12 THEN
	                IF "DB16_GESTION_SCADA".Sincronizacion.Informes[#for_i] = 12 THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRAZA_CAT_1_SISTEMA",
	                                            User := '',
	                                            Codigo1 := 0,
	                                            Codigo2 := 0,
	                                            Codigo3 := 0,
	                                            Texto := 'Fallo al sincronizar registros CIP',
	                                            CodInt_1:=_int_in_,
	                                            CodInt_2:=_int_in_,
	                                            CodInt_3:=_int_in_,
	                                            CodInt_4:=_int_in_,
	                                            CodInt_5:=_int_in_,
	                                            CodReal_1:=_real_in_,
	                                            CodReal_2:=_real_in_);
	                END_IF;
	                "DB16_GESTION_SCADA".Sincronizacion.Cocina1[#for_i] := 0;
	            END_IF;
	        END_IF;
	        "DB16_GESTION_SCADA".TON_FERM_ESTADO[#for_i].IN := "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[#for_i] = 4 OR "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[#for_i] = 12;
	        IF "DB16_GESTION_SCADA".TON_FERM_ESTADO[#for_i].Q THEN
	            IF "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[#for_i] = 12 THEN
	                IF "DB16_GESTION_SCADA".Sincronizacion.Informes[#for_i] = 12 THEN
	                    "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                            Registrar := 1,
	                                            Categoria := "TRAZA_CAT_1_SISTEMA",
	                                            User := '',
	                                            Codigo1 := 0,
	                                            Codigo2 := 0,
	                                            Codigo3 := 0,
	                                            Texto := 'Fallo al sincronizar registros CIP',
	                                            CodInt_1:=_int_in_,
	                                            CodInt_2:=_int_in_,
	                                            CodInt_3:=_int_in_,
	                                            CodInt_4:=_int_in_,
	                                            CodInt_5:=_int_in_,
	                                            CodReal_1:=_real_in_,
	                                            CodReal_2:=_real_in_);
	                END_IF;
	                "DB16_GESTION_SCADA".Sincronizacion.Fermentadores[#for_i] := 0;
	            END_IF;
	        END_IF;
	        
	    END_FOR;
	    
	END_REGION
	
	
	REGION GESTION_TEMPORIZADORES
	    
	    //  ====================================================================================
	    //  Gestion de marcas de bit de vida, reinicializamos los valores
	    FOR #for_i := 0 TO 1 DO
	        "FC2928_ZC_TON_INDV"(Pulso1seg := "DB1_SYS".Pulso1seg,
	                             TON := "DB16_GESTION_SCADA".TON_ON[#for_i]);
	        "FC2928_ZC_TON_INDV"(Pulso1seg := "DB1_SYS".Pulso1seg,
	                             TON := "DB16_GESTION_SCADA".TON_OFF[#for_i]);
	        "FC2928_ZC_TON_INDV"(Pulso1seg := "DB1_SYS".Pulso1seg,
	                             TON := "DB16_GESTION_SCADA".TON_CIP_ESTADO[#for_i]);
	        "FC2928_ZC_TON_INDV"(Pulso1seg := "DB1_SYS".Pulso1seg,
	                             TON := "DB16_GESTION_SCADA".TON_INFORME_ESTADO[#for_i]);
	        "FC2928_ZC_TON_INDV"(Pulso1seg := "DB1_SYS".Pulso1seg,
	                             TON := "DB16_GESTION_SCADA".TON_COCINA1_ESTADO[#for_i]);
	        "FC2928_ZC_TON_INDV"(Pulso1seg := "DB1_SYS".Pulso1seg,
	                             TON := "DB16_GESTION_SCADA".TON_FERM_ESTADO[#for_i]);
	    END_FOR;
	    
	END_REGION
	
	*)
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>