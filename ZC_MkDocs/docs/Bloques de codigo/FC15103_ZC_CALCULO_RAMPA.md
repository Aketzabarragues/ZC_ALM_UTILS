---
title: FC15103_ZC_CALCULO_RAMPA
---
# FC FC15103_ZC_CALCULO_RAMPA

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
| `Pulso100ms` | `Bool` | - | `-` | Pulso 100 ms |
| `HabilitarRampa` | `Bool` | - | `-` | Habilitar Rampa |
| `ValorObjetivo` | `Real` | - | `-` | Valor a alcanzar |
| `IncRespRapida` | `Real` | - | `-` | Incremento rapido en ud. ing. / segundo |
| `DecRespRapida` | `Real` | - | `-` | Decremento Rapido ud. ing. / segundo |
| `IncRespLenta` | `Real` | - | `-` | Incremento lento en ud. ing. / segundo |
| `DecRespLenta` | `Real` | - | `-` | Decremento lento ud. ing. / segundo |
| `HistRapidaLenta` | `Real` | - | `-` | Histeresis respuesta rapida-lenta rampa |

### Entrada/Salida
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `ValorRampa` | `Real` | - | `-` | Valor actual de la rampa |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `t_Diferencia` | `Real` | - | `-` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15103_ZC_CALCULO_RAMPA" : Void
TITLE = FC15103_ZC_CALCULO_RAMPA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para calculo de rampa hasta valor objetivo.
   VAR_INPUT 
      Pulso100ms : Bool;   // Pulso 100 ms
      HabilitarRampa : Bool;   // Habilitar Rampa
      ValorObjetivo : Real;   // Valor a alcanzar
      IncRespRapida : Real;   // Incremento rapido en ud. ing. / segundo
      DecRespRapida : Real;   // Decremento Rapido ud. ing. / segundo
      IncRespLenta : Real;   // Incremento lento en ud. ing. / segundo
      DecRespLenta : Real;   // Decremento lento ud. ing. / segundo
      HistRapidaLenta : Real;   // Histeresis respuesta rapida-lenta rampa
   END_VAR

   VAR_IN_OUT 
      ValorRampa : Real;   // Valor actual de la rampa
   END_VAR

   VAR_TEMP 
      t_Diferencia : Real;
      t_Incremento : Real;
   END_VAR


BEGIN
	(*  
	ZEUS CONTROL, S.A.
	(c)Copyright (2023) All Rights Reserved
	--------------------------------------------------------------------------------------
	
	Software:       TIA Portal 16
	Restricciones:  PLC serie 1200/1500
	
	Nombre:         FC15042_ZC_STD_RAMPA
	Descripcion:    Calculo rampas hasta alcanzar valor objetivo
	
	Dependencias:
	    FC:         -
	    FB:         -
	    UDT:        -
	    DB:         -
	
	Change log:
	
	    Version     Fecha       Tecnico a cargo     Descripcion
	    
	    01.00.00    05.09.2023  (ABH)               Primera version.
	    
	//=====================================================================================
	*)
	
	
	//  ===============================================================================================================
	//  Gestion de la rampa de Set Point al cambiar de valor
	IF #HabilitarRampa THEN
	    
	    
	    REGION CALCULOS
	        
	        // =============================================================================
	        //  Calculo diferencia entre Set Point y valor de la rampa
	        #t_Diferencia := ABS(#ValorObjetivo - #ValorRampa);
	        
	        // =============================================================================
	        //  Calculo de incremento DOWN
	        IF #ValorObjetivo < #ValorRampa THEN
	            IF #t_Diferencia > #HistRapidaLenta THEN
	                #t_Incremento := #DecRespRapida / 10;
	            ELSE
	                #t_Incremento := #DecRespLenta / 10;
	            END_IF;
	        END_IF;
	        
	        
	        // =============================================================================
	        //  Calculo de incremento UP
	        IF #ValorObjetivo > #ValorRampa THEN
	            IF #t_Diferencia > #HistRapidaLenta THEN
	                #t_Incremento := #IncRespRapida / 10;
	            ELSE
	                #t_Incremento := #IncRespLenta / 10;
	            END_IF;
	        END_IF;
	        
	    END_REGION
	    
	    
	    REGION GESTION_INCREMENTOS
	        
	        // =============================================================================
	        //  Gestion incremento UP
	        IF #ValorRampa < #ValorObjetivo
	            AND
	            #t_Diferencia > #t_Incremento
	            AND
	            #Pulso100ms
	        THEN
	            #ValorRampa := #ValorRampa + #t_Incremento;
	        END_IF;
	        
	        
	        // =============================================================================
	        //  Gestion incremento DOWN
	        IF #ValorRampa > #ValorObjetivo
	            AND
	            #t_Diferencia > #t_Incremento
	            AND
	            #Pulso100ms
	        THEN
	            #ValorRampa := #ValorRampa - #t_Incremento;
	        END_IF;
	        
	        
	        // =============================================================================
	        //  Gestion limite alcanzado o sin incremento configurado
	        IF #t_Diferencia <= #t_Incremento
	            OR
	            #t_Incremento = 0
	        THEN
	            #ValorRampa := #ValorObjetivo;
	        END_IF;
	        
	    END_REGION
	    
	    
	ELSE
	    
	    #ValorRampa := #ValorObjetivo;
	    
	END_IF;
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>