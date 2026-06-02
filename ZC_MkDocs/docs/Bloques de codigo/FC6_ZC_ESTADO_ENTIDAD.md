---
title: FC6_ZC_ESTADO_ENTIDAD
---
# FC FC6_ZC_ESTADO_ENTIDAD

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** AketzaBarragues

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función para la gestión integral de estados, disponibilidad y supervisión de los dispositivos asociados a una entidad.
    
    Las tareas que realiza son las siguientes:
    
    - **Supervisión de dispositivos:** Escaneo cíclico de los dispositivos vinculados a la entidad (Válvulas, Motores, Variadores y Sinamics) mediante un bucle `FOR`.
    - Verificación de alarmas generales (`Alarmas_General`) y estados de mando manual (`Estado_AutoMan`) en cada equipo.
    - Identificación del tipo de incidencia en las salidas `TipoError` (1 para Error, 2 para Manual) y reporte del índice del dispositivo afectado en `DispNumero`.
    - **Cálculo de disponibilidad:** Determinación del estado `Disponible` basándose en la ausencia de alarmas, mandos manuales, capturas activas y estados de proceso (Producción, CIP, SIP, Standby).
    - Actualización del estado `Capturada` si la entidad tiene una asignación distinta de cero.
    - **Gestión de códigos de estado:** Asignación dinámica del código numérico `CodEstado` según la fase de operación actual (Producción: 1000, CIP: 2000, SIP: 3000, Standby: 4000).
    - Refinamiento del código según el contenido detectado (Producto: +10, Agua: +20, Vacío: +30).
    - Registro de estados de limpieza (Sucia: 10000, Limpia: 11000, Esterilizada: 12000).
    - **Sincronización de producto:** Actualización de la variable `Producto` con el valor de entrada `CodigoProducto` siempre que la entidad tenga un estado activo.

!!! abstract "Dependencias Requeridas"
    **DB:** [DB2010_V](../Estructura de datos/DB2010_V.md)
    **DB:** [DB2015_M](../Estructura de datos/DB2015_M.md)
    **DB:** [DB2016_M_VF](../Estructura de datos/DB2016_M_VF.md)
    **DB:** [DB2017_M_SINA](../Estructura de datos/DB2017_M_SINA.md)
    **DB:** [DB6_ENTIDAD](../Estructura de datos/DB6_ENTIDAD.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Entidad` | `Int` | - | `-` | Numero de entidad a gestionar |
| `TipoProceso` | `Int` | - | `-` | Tipo de proceso |
| `CodigoProducto` | `Int` | - | `-` | Codigo de producto |

### Salidas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `TipoError` | `Int` | - | `-` | 1= Error / 2= Manual |
| `DispNumero` | `Int` | - | `-` | Numero de dispositivo HMI |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |
| `t_DispManual` | `Bool` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `DISP_V` | `Int` | - | `10` | - |
| `DISP_M_VF` | `Int` | - | `16` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC6_ZC_ESTADO_ENTIDAD" : Void
TITLE = FC6_ZC_ESTADO_ENTIDAD
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : AketzaBarragues
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para gestion de estados de entidades.
   VAR_INPUT 
      Entidad : Int;   // Numero de entidad a gestionar
      TipoProceso : Int;   // Tipo de proceso
      CodigoProducto : Int;   // Codigo de producto
   END_VAR

   VAR_OUTPUT 
      TipoError : Int;   // 1= Error / 2= Manual
      DispNumero : Int;   // Numero de dispositivo HMI
   END_VAR

   VAR_TEMP 
      for_i : Int;
      t_DispError : Bool;
      t_DispManual : Bool;
      t_DispNumero : Int;
   END_VAR

   VAR CONSTANT 
      DISP_V : Int := 10;
      DISP_M : Int := 15;
      DISP_M_VF : Int := 16;
      DISP_M_SINA : Int := 17;
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
	
	Función para la gestión integral de estados, disponibilidad y supervisión de los dispositivos asociados a una entidad.
	
	Las tareas que realiza son las siguientes:
	
	- **Supervisión de dispositivos:** Escaneo cíclico de los dispositivos vinculados a la entidad (Válvulas, Motores, Variadores y Sinamics) mediante un bucle `FOR`.
	- Verificación de alarmas generales (`Alarmas_General`) y estados de mando manual (`Estado_AutoMan`) en cada equipo.
	- Identificación del tipo de incidencia en las salidas `TipoError` (1 para Error, 2 para Manual) y reporte del índice del dispositivo afectado en `DispNumero`.
	- **Cálculo de disponibilidad:** Determinación del estado `Disponible` basándose en la ausencia de alarmas, mandos manuales, capturas activas y estados de proceso (Producción, CIP, SIP, Standby).
	- Actualización del estado `Capturada` si la entidad tiene una asignación distinta de cero.
	- **Gestión de códigos de estado:** Asignación dinámica del código numérico `CodEstado` según la fase de operación actual (Producción: 1000, CIP: 2000, SIP: 3000, Standby: 4000).
	- Refinamiento del código según el contenido detectado (Producto: +10, Agua: +20, Vacío: +30).
	- Registro de estados de limpieza (Sucia: 10000, Limpia: 11000, Esterilizada: 12000).
	- **Sincronización de producto:** Actualización de la variable `Producto` con el valor de entrada `CodigoProducto` siempre que la entidad tenga un estado activo.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | - |
	| FB   | - |
	| DB   | `DB2010_V`, `DB2015_M`, `DB2016_M_VF`, `DB2017_M_SINA`, `DB6_ENTIDAD` |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.01 | 15.10.2020 | (ABH)   | Primera version. |
	| 00.00.02 | 02.02.2021 | (ABH)   | Modificado para uso como funcion. Se elimina bucle `FOR` para revisar solamente la entidad que se pasa como entrada. |
	| 00.00.03 | 02.12.2022 | (ABH)   | Se modifica el UDT para estandarizacion. |
	| 00.00.01 | 15.10.2025 | (ABH)   | Se añade gestion de codigo de estado. |
	| 00.00.05 | 10.03.2025 | (ABH)   | Se añade gestion de codigo de producto a las entidades. |
	| 00.00.06 | 24.04.2025 | (HCR)   | Se añade gestion de idioma. |
	| 00.00.07 | 11.09.2025 | (ABH)   | Se eliminan las constantes de idioma dentro del `FC`. Se utilizan constantes globales. |
	| 01.00.00 | 26.03.2026 | (ABH)   | Se elimina idioma. Se añaden constantes de tipo de dispositivo. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION GESTION_ENTIDADES
	    
	    IF "DB6_ENTIDAD".ENT[#Entidad].Habilitar THEN
	        
	        //  Asignacion de estado entidad capturada
	        "DB6_ENTIDAD".ENT[#Entidad].Estado.Capturada := "DB6_ENTIDAD".ENT[#Entidad].Asignacion <> 0;
	        
	        //  ==========================================================================================================
	        REGION COMPROBACION_DISPOSITIVOS
	            
	            //  Reset de estados
	            "DB6_ENTIDAD".ENT[#Entidad].Alarma.Dispositivo := "DB6_ENTIDAD".ENT[#Entidad].Alarma.Manual := #t_DispError := #t_DispManual := FALSE;
	            
	            //  Comprobacion de estado de dispositivo declarados dentro de la entidad
	            FOR #for_i := 1 TO "N_MAX_ENTIDAD_DISPOSITIVOS" DO
	                
	                //  Se revisan solamente las entidades declaradas
	                IF "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Tipo <> 0 AND "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num <> 0 THEN
	                    
	                    CASE "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Tipo OF
	                            
	                        #DISP_V:
	                            //  ==========================================================================================================
	                            REGION VALVULA
	                                
	                                IF "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num <= "N_MAX_DISP_V" THEN
	                                    
	                                    //  Comprobacion de errores o dispositivo en manual
	                                    #t_DispError := "DB2010_V".V["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Alarmas_General;
	                                    #t_DispManual := "DB2010_V".V["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Estado_AutoMan;
	                                    
	                                    IF #t_DispError OR #t_DispManual THEN
	                                        #t_DispNumero := "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num;
	                                    END_IF;
	                                    
	                                END_IF;
	                                
	                            END_REGION VALVULA
	                            
	                            
	                        #DISP_M:
	                            //  ==========================================================================================================
	                            REGION MOTOR
	                                
	                                IF "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num <= "N_MAX_DISP_M" THEN
	                                    
	                                    //  Comprobacion de errores o dispositivo en manual
	                                    #t_DispError := "DB2015_M".M["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Alarmas_General;
	                                    #t_DispManual := "DB2015_M".M["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Estado_AutoMan;
	                                    
	                                    IF #t_DispError OR #t_DispManual THEN
	                                        #t_DispNumero := "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num;
	                                    END_IF;
	                                    
	                                END_IF;
	                                
	                            END_REGION MOTOR
	                            
	                            
	                        #DISP_M_SINA:
	                            //  ==========================================================================================================
	                            REGION MOTOR_SINAMICS
	                                
	                                IF "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num <= "N_MAX_DISP_M_SINA" THEN
	                                    
	                                    //  Comprobacion de errores o dispositivo en manual
	                                    #t_DispError := "DB2017_M_SINA".M_SINA["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Alarmas_General;
	                                    #t_DispManual := "DB2017_M_SINA".M_SINA["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Estado_AutoMan;
	                                    
	                                    IF #t_DispError OR #t_DispManual THEN
	                                        #t_DispNumero := "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num;
	                                    END_IF;
	                                    
	                                END_IF;
	                                
	                            END_REGION MOTOR_SINAMICS
	                            
	                            
	                        #DISP_M_VF:
	                            //  ==========================================================================================================
	                            REGION MOTOR_VARIADOR
	                                
	                                IF "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num <= "N_MAX_DISP_M_VF" THEN
	                                    
	                                    //  Comprobacion de errores o dispositivo en manual
	                                    #t_DispError := "DB2016_M_VF".M_VF["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Alarmas_General;
	                                    #t_DispManual := "DB2016_M_VF".M_VF["DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num].Estado_AutoMan;
	                                    
	                                    IF #t_DispError OR #t_DispManual THEN
	                                        #t_DispNumero := "DB6_ENTIDAD".ENT[#Entidad].Dispositivo[#for_i].Num;
	                                    END_IF;
	                                    
	                                END_IF;
	                            END_REGION MOTOR_VARIADOR
	                            
	                            
	                        ELSE
	                            #t_DispError := #t_DispManual := FALSE;
	                    END_CASE;
	                    
	                END_IF;
	                
	                
	                
	                IF #t_DispError THEN
	                    
	                    //  Activacion de estado en error
	                    "DB6_ENTIDAD".ENT[#Entidad].Alarma.Dispositivo := TRUE;
	                    #TipoError := 1;
	                    #DispNumero := #t_DispNumero;
	                    EXIT;
	                    
	                ELSIF #t_DispManual THEN
	                    
	                    //  Activacion de estado en manual
	                    "DB6_ENTIDAD".ENT[#Entidad].Alarma.Manual := TRUE;
	                    #TipoError := 2;
	                    #DispNumero := #t_DispNumero;
	                    EXIT;
	                    
	                END_IF;
	                
	            END_FOR;
	            
	        END_REGION COMPROBACION_DISPOSITIVOS
	        
	        
	        //  ==========================================================================================================
	        REGION ASIGNACION_ESTADOS
	            
	            //  Asignacion de estado disponible
	            "DB6_ENTIDAD".ENT[#Entidad].Estado.Disponible :=
	            ("DB6_ENTIDAD".ENT[#Entidad].Asignacion = 0)
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Alarma.Dispositivo
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Alarma.Manual
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Estado.EnProduccion
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Estado.EnCIP
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Estado.EnSIP
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Estado.EnStandby
	            AND NOT "DB6_ENTIDAD".ENT[#Entidad].Estado.Capturada;
	            
	            //  Asignacion de codigo de estado
	            "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 0;
	            IF "DB6_ENTIDAD".ENT[#Entidad].Estado.EnProduccion THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 1000;
	            ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.EnCIP THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 2000;
	            ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.EnSIP THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 3000;
	            ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.EnStandby THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 4000;
	            ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.Sucia THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 10000;
	            ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.Limpia THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 11000;
	            ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.Esterilizada THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 12000;
	            END_IF;
	            
	            IF (*ENT[#Entidad].Estado.CodEstado >= 1000 AND *)"DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado <= 4999 THEN
	                IF "DB6_ENTIDAD".ENT[#Entidad].Estado.ConProducto THEN
	                    "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado + 10;
	                ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.ConAgua THEN
	                    "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado + 20;
	                ELSIF "DB6_ENTIDAD".ENT[#Entidad].Estado.Vacia THEN
	                    "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado + 30;
	                END_IF;
	            END_IF;
	            
	            //  Asignacion de codigo de producto
	            IF "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado <> 0 THEN
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.Producto := #CodigoProducto;
	            ELSE
	                "DB6_ENTIDAD".ENT[#Entidad].Estado.CodEstado := 0;
	            END_IF;
	            
	        END_REGION ASIGNACION_ESTADOS
	        
	    ELSE
	        "DB6_ENTIDAD".ENT[#Entidad].Estado.Disponible := FALSE;
	        "DB6_ENTIDAD".ENT[#Entidad].Asignacion := 0;
	        
	    END_IF;
	    
	    
	END_REGION GESTION_ENTIDADES
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>