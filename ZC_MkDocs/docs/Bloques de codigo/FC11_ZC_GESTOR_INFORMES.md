---
title: FC11_ZC_GESTOR_INFORMES
---
# FC FC11_ZC_GESTOR_INFORMES

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función para la gestión e interfaz de escritura de informes hacia el sistema SCADA/HMI mediante una máquina de estados y la lectura de un buffer.
    
    Las tareas que realiza son las siguientes:
    
    - Extracción de datos del buffer: Búsqueda inversa del registro más antiguo pendiente de envío evaluando la condición `Registrar` = 1 mediante un bucle `FOR`.
    - Transferencia del registro a la estructura estática `Gestion.Datos` y generación de un `Id` único basado en la fecha y hora actual.
    - Limpieza inmediata de todas las variables (Booleanos, Reales, Enteros, Fechas y Strings) en la posición original del buffer.
    - Ejecución de la etapa **REPOSO**: Activación de la secuencia ante la orden `OrdenIniciar`, siempre que se detecte conexión con el SCADA y la habilitación general esté activa.
    - Ejecución de la etapa **ESPERA_ENTRE_AVISOS**: Temporización basada en pulsos de 1 segundo (`Pulso1Seg`) antes de un reintento. Deriva a fallo si se supera el máximo de intentos.
    - Ejecución de la etapa **LANZAR_AVISO**: Activación de la señal `Aviso.Registrar` hacia el SCADA y paso a espera tras cumplirse el tiempo parametrizado.
    - Ejecución de la etapa **ESPERA_CONFIRMACION**: Monitoreo de la respuesta del sistema superior. Si `Aviso.Estado` es igual a 4, el envío es exitoso. Si hay error (estado 12) o agotamiento de tiempo, se incrementa el contador de intentos y se repite el ciclo.
    - Ejecución de la etapa **FALLO**: Generación de una traza de sistema (`TRZ_CAT_1_SYS`) registrando el código de error `TRZ_SYS_INF_ERR` ante la imposibilidad de entrega del informe.
    - Ejecución de la etapa **BORRAR_DATOS**: Reseteo íntegro de la estructura `Gestion.Datos` para preparar el sistema para el próximo ciclo de comunicación y retorno al estado de reposo.

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1Seg` | `Bool` | - | `-` | Pulso de 1 segundo |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | Variable para bucles FOR |
| `t_PosicionRegistro` | `Int` | - | `-` | Posicion del registro encontrado en el buffer |
| `t_RegistroEncontrado` | `Bool` | - | `-` | Indicador de registro encontrado |
| `t_RetVal` | `Int` | - | `-` | Variable para su uso en programa |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `REPOSO` | `Int` | - | `0` | Etapa reposo |
| `ESPERA_ENTRE_AVISOS` | `Int` | - | `10` | Etapa espera entre avisos |
| `LANZAR_AVISO` | `Int` | - | `20` | Etapa lanzar aviso |
| `ESPERA_CONFIRMACION` | `Int` | - | `30` | Etapa espera confirmacion |
| `FALLO` | `Int` | - | `40` | Etapa fallo |
| `BORRAR_DATOS` | `Int` | - | `50` | Etapa borrar datos |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC11_ZC_GESTOR_INFORMES" : Void
TITLE = FC11_ZC_GESTOR_INFORMES
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para gestion de informes
   VAR_INPUT 
      Pulso1Seg : Bool;   // Pulso de 1 segundo
   END_VAR

   VAR_TEMP 
      for_i : Int;   // Variable para bucles FOR
      t_PosicionRegistro : Int;   // Posicion del registro encontrado en el buffer
      t_RegistroEncontrado : Bool;   // Indicador de registro encontrado
      t_RetVal : Int;   // Variable para su uso en programa
   END_VAR

   VAR CONSTANT 
      REPOSO : Int := 0;   // Etapa reposo
      ESPERA_ENTRE_AVISOS : Int := 10;   // Etapa espera entre avisos
      LANZAR_AVISO : Int := 20;   // Etapa lanzar aviso
      ESPERA_CONFIRMACION : Int := 30;   // Etapa espera confirmacion
      FALLO : Int := 40;   // Etapa fallo
      BORRAR_DATOS : Int := 50;   // Etapa borrar datos
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2024 - 2024
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función para la gestión e interfaz de escritura de informes hacia el sistema SCADA/HMI mediante una máquina de estados y la lectura de un buffer.
	
	Las tareas que realiza son las siguientes:
	
	- Extracción de datos del buffer: Búsqueda inversa del registro más antiguo pendiente de envío evaluando la condición `Registrar` = 1 mediante un bucle `FOR`.
	- Transferencia del registro a la estructura estática `Gestion.Datos` y generación de un `Id` único basado en la fecha y hora actual.
	- Limpieza inmediata de todas las variables (Booleanos, Reales, Enteros, Fechas y Strings) en la posición original del buffer.
	- Ejecución de la etapa **REPOSO**: Activación de la secuencia ante la orden `OrdenIniciar`, siempre que se detecte conexión con el SCADA y la habilitación general esté activa.
	- Ejecución de la etapa **ESPERA_ENTRE_AVISOS**: Temporización basada en pulsos de 1 segundo (`Pulso1Seg`) antes de un reintento. Deriva a fallo si se supera el máximo de intentos.
	- Ejecución de la etapa **LANZAR_AVISO**: Activación de la señal `Aviso.Registrar` hacia el SCADA y paso a espera tras cumplirse el tiempo parametrizado.
	- Ejecución de la etapa **ESPERA_CONFIRMACION**: Monitoreo de la respuesta del sistema superior. Si `Aviso.Estado` es igual a 4, el envío es exitoso. Si hay error (estado 12) o agotamiento de tiempo, se incrementa el contador de intentos y se repite el ciclo.
	- Ejecución de la etapa **FALLO**: Generación de una traza de sistema (`TRZ_CAT_1_SYS`) registrando el código de error `TRZ_SYS_INF_ERR` ante la imposibilidad de entrega del informe.
	- Ejecución de la etapa **BORRAR_DATOS**: Reseteo íntegro de la estructura `Gestion.Datos` para preparar el sistema para el próximo ciclo de comunicación y retorno al estado de reposo.
	
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
	| 01.00.00 | 30.07.2024 | (ABH)   | Primera version. |
	| 01.00.01 | 11.09.2024 | (ABH)   | Se añade la generacion de ID con fecha y hora en el momento del guardar en SQL. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION GESTION_INFORMES
	    
	    // =============================================================================
	    //  COPIAMOS EL ULTIMO REGISTRO (El mas antiguo) A LA VARIABLE REGISTRO QUE ES LA 
	    //  ENCARGADA DE COMUNICARLA CON EL SCADA/HMI
	    IF "DB11_INFORMES".Gestion.HabilitacionGeneral AND "DB11_INFORMES".Gestion.Datos.Registrar = 0 AND #Pulso1Seg THEN
	        
	        // =============================================================================
	        // Buscamos el ultimo registro
	        FOR #for_i := "N_MAX_INF_BUFFER" TO 0 BY -1 DO
	            
	            // =============================================================================
	            // Registro encontrado
	            IF "DB11_INFORMES".Buffer[#for_i].Registrar = 1 THEN
	                #t_PosicionRegistro := #for_i;
	                #t_RegistroEncontrado := TRUE;
	                EXIT;
	            END_IF;
	            
	        END_FOR;
	        
	        // =============================================================================
	        // Si hemos encontrado el registro, copiamos a variable estatica
	        IF #t_RegistroEncontrado THEN
	            
	            // =============================================================================
	            //  Copiamos el los datos de la traza a variable estatica para tratarla
	            "DB11_INFORMES".Gestion.Datos := "DB11_INFORMES".Buffer[#t_PosicionRegistro];
	            "DB11_INFORMES".Gestion.Datos.Id := "FC15006_ZC_DTL_TO_STRING"(FechaDTL := "DB1_SYS".FechaHoraActual, Formato := 3);
	            
	            // =============================================================================
	            //  Quitamos el registro del buffer
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Registrar := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Id := '';
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Tipo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Codigo := '';
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.Ano := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.Mes := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.Dia := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.DiaSemana := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.Hora := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.Minuto := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.Segundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_1.NanoSegundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.Ano := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.Mes := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.Dia := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.DiaSemana := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.Hora := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.Minuto := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.Segundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_2.NanoSegundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.Ano := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.Mes := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.Dia := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.DiaSemana := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.Hora := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.Minuto := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.Segundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Fecha_3.NanoSegundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_1 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_2 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_3 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_4 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_5 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_6 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_7 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_8 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_9 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_10 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_11 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_12 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_13 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_14 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_15 := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_1 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_2 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_3 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_4 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_5 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_6 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_7 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_8 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_9 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_10 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_11 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_12 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_13 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_14 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_15 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_16 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_17 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_18 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_19 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_20 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_21 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_22 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_23 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_24 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_25 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_26 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_27 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_28 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_29 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_30 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_31 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Bool_32 := FALSE;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_1 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_2 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_3 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_4 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_5 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_6 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_7 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_8 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_9 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_10 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_11 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_12 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_13 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_14 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_15 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_16 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_17 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_18 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_19 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Real_20 := 0.0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_1 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_2 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_3 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_4 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_5 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_6 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_7 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_8 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_9 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_10 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_11 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_12 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_13 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_14 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_15 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_16 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_17 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_18 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_19 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].Int_20 := 0;
	            
	        END_IF;
	        
	    END_IF;
	    
	    
	    // =============================================================================
	    //  Si existe registro a trazar, lanzamos la orden de iniciar la secuencia
	    IF "DB11_INFORMES".Gestion.Datos.Registrar = 1 AND "DB11_INFORMES".Gestion.Etapa = #REPOSO AND "DB11_INFORMES".Gestion.EstadoConexion THEN
	        
	        //  Lanzamos la orden de iniciar la secuencia de registro
	        "DB11_INFORMES".Gestion.OrdenIniciar := TRUE;
	        
	    END_IF;
	    
	    
	END_REGION
	
	
	//  ==========================================================================================================
	REGION SECUENCIA_INFORME    
	    
	    
	    IF NOT "DB11_INFORMES".Gestion.HabilitacionGeneral AND "DB11_INFORMES".Gestion.Etapa <> #REPOSO THEN
	        "DB11_INFORMES".Gestion.Etapa := #BORRAR_DATOS;
	    END_IF;
	    
	    
	    CASE "DB11_INFORMES".Gestion.Etapa OF
	            
	            
	            // =============================================================================
	        #REPOSO:
	            IF "DB11_INFORMES".Gestion.OrdenIniciar THEN
	                "DB11_INFORMES".Gestion.Etapa := #LANZAR_AVISO;
	                "DB11_INFORMES".Gestion.OrdenIniciar := FALSE;
	                "DB11_INFORMES".Gestion.Aviso.Registrar := 0;
	                "DB11_INFORMES".Gestion.TiempoActual := 0;
	                "DB11_INFORMES".Gestion.Aviso.NumeroIntentosActual := 0;
	            END_IF;
	            
	            
	            
	            // =============================================================================
	        #ESPERA_ENTRE_AVISOS:
	            //  Contador de tiempo de etapa
	            IF #Pulso1Seg THEN
	                "DB11_INFORMES".Gestion.TiempoActual += 1;
	            END_IF;
	            //  Tiempo maximo de espera
	            IF ("DB11_INFORMES".Gestion.TiempoActual >= "DB11_INFORMES".Gestion.SP_Tiempo) THEN
	                "DB11_INFORMES".Gestion.TiempoActual := 0;
	                "DB11_INFORMES".Gestion.Etapa := #LANZAR_AVISO;
	            END_IF;
	            
	            //  Si ya se ha alcanzado el numero maximo de intentos, generamos la traza
	            IF "DB11_INFORMES".Gestion.Aviso.NumeroIntentosActual >= "DB11_INFORMES".Gestion.NumeroMaxIntentos THEN
	                "DB11_INFORMES".Gestion.Etapa := #FALLO;
	                "DB11_INFORMES".Gestion.Aviso.Registrar := 0;
	            END_IF;
	            
	            
	            
	            // =============================================================================
	        #LANZAR_AVISO:
	            
	            IF #Pulso1Seg THEN
	                "DB11_INFORMES".Gestion.TiempoActual += 1;
	            END_IF;
	            "DB11_INFORMES".Gestion.Aviso.Registrar := TRUE;
	            
	            
	            
	            IF ("DB11_INFORMES".Gestion.TiempoActual >= "DB11_INFORMES".Gestion.SP_Tiempo) THEN
	                "DB11_INFORMES".Gestion.Etapa := #ESPERA_CONFIRMACION;
	            END_IF;
	            
	            
	            // =============================================================================
	        #ESPERA_CONFIRMACION:
	            
	            IF #Pulso1Seg THEN
	                "DB11_INFORMES".Gestion.TiempoActual += 1;
	            END_IF;
	            
	            //  Confirmacion desde SCADA OK
	            IF "DB11_INFORMES".Gestion.Aviso.Estado = 4 THEN
	                "DB11_INFORMES".Gestion.TiempoActual := 0;
	                "DB11_INFORMES".Gestion.Aviso.Estado := 0;
	                "DB11_INFORMES".Gestion.Aviso.Registrar := FALSE;
	                "DB11_INFORMES".Gestion.Etapa := #BORRAR_DATOS;
	            END_IF;
	            
	            //  Tiempo maximo de espera
	            IF ("DB11_INFORMES".Gestion.TiempoActual >= "DB11_INFORMES".Gestion.SP_Tiempo)
	                OR
	                ("DB11_INFORMES".Gestion.Aviso.Estado = 12)
	            THEN
	                "DB11_INFORMES".Gestion.TiempoActual := 0;
	                "DB11_INFORMES".Gestion.Aviso.Estado := 0;
	                "DB11_INFORMES".Gestion.Aviso.Registrar := FALSE;
	                "DB11_INFORMES".Gestion.Etapa := #ESPERA_ENTRE_AVISOS;
	                "DB11_INFORMES".Gestion.Aviso.NumeroIntentosActual += 1;
	            END_IF;
	            
	            
	            // =============================================================================
	        #BORRAR_DATOS:
	            
	            "DB11_INFORMES".Gestion.Datos.Registrar := 0;
	            "DB11_INFORMES".Gestion.Datos.Id := '';
	            "DB11_INFORMES".Gestion.Datos.Tipo := 0;
	            "DB11_INFORMES".Gestion.Datos.Codigo := '';
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.Ano := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.Mes := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.Dia := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.DiaSemana := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.Hora := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.Minuto := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.Segundo := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_1.NanoSegundo := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.Ano := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.Mes := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.Dia := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.DiaSemana := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.Hora := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.Minuto := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.Segundo := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_2.NanoSegundo := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.Ano := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.Mes := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.Dia := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.DiaSemana := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.Hora := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.Minuto := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.Segundo := 0;
	            "DB11_INFORMES".Gestion.Datos.Fecha_3.NanoSegundo := 0;
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_1 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_2 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_3 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_4 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_5 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_6 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_7 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_8 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_9 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_10 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_11 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_12 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_13 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_14 :=
	            "DB11_INFORMES".Buffer[#t_PosicionRegistro].CodString_15 := 0;
	            "DB11_INFORMES".Gestion.Datos.Bool_1 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_2 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_3 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_4 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_5 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_6 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_7 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_8 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_9 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_10 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_11 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_12 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_13 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_14 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_15 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_16 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_17 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_18 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_19 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_20 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_21 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_22 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_23 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_24 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_25 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_26 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_27 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_28 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_29 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_30 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_31 :=
	            "DB11_INFORMES".Gestion.Datos.Bool_32 := FALSE;
	            "DB11_INFORMES".Gestion.Datos.Real_1 :=
	            "DB11_INFORMES".Gestion.Datos.Real_2 :=
	            "DB11_INFORMES".Gestion.Datos.Real_3 :=
	            "DB11_INFORMES".Gestion.Datos.Real_4 :=
	            "DB11_INFORMES".Gestion.Datos.Real_5 :=
	            "DB11_INFORMES".Gestion.Datos.Real_6 :=
	            "DB11_INFORMES".Gestion.Datos.Real_7 :=
	            "DB11_INFORMES".Gestion.Datos.Real_8 :=
	            "DB11_INFORMES".Gestion.Datos.Real_9 :=
	            "DB11_INFORMES".Gestion.Datos.Real_10 :=
	            "DB11_INFORMES".Gestion.Datos.Real_11 :=
	            "DB11_INFORMES".Gestion.Datos.Real_12 :=
	            "DB11_INFORMES".Gestion.Datos.Real_13 :=
	            "DB11_INFORMES".Gestion.Datos.Real_14 :=
	            "DB11_INFORMES".Gestion.Datos.Real_15 :=
	            "DB11_INFORMES".Gestion.Datos.Real_16 :=
	            "DB11_INFORMES".Gestion.Datos.Real_17 :=
	            "DB11_INFORMES".Gestion.Datos.Real_18 :=
	            "DB11_INFORMES".Gestion.Datos.Real_19 :=
	            "DB11_INFORMES".Gestion.Datos.Real_20 := 0.0;
	            "DB11_INFORMES".Gestion.Datos.Int_1 :=
	            "DB11_INFORMES".Gestion.Datos.Int_2 :=
	            "DB11_INFORMES".Gestion.Datos.Int_3 :=
	            "DB11_INFORMES".Gestion.Datos.Int_4 :=
	            "DB11_INFORMES".Gestion.Datos.Int_5 :=
	            "DB11_INFORMES".Gestion.Datos.Int_6 :=
	            "DB11_INFORMES".Gestion.Datos.Int_7 :=
	            "DB11_INFORMES".Gestion.Datos.Int_8 :=
	            "DB11_INFORMES".Gestion.Datos.Int_9 :=
	            "DB11_INFORMES".Gestion.Datos.Int_10 :=
	            "DB11_INFORMES".Gestion.Datos.Int_11 :=
	            "DB11_INFORMES".Gestion.Datos.Int_12 :=
	            "DB11_INFORMES".Gestion.Datos.Int_13 :=
	            "DB11_INFORMES".Gestion.Datos.Int_14 :=
	            "DB11_INFORMES".Gestion.Datos.Int_15 :=
	            "DB11_INFORMES".Gestion.Datos.Int_16 :=
	            "DB11_INFORMES".Gestion.Datos.Int_17 :=
	            "DB11_INFORMES".Gestion.Datos.Int_18 :=
	            "DB11_INFORMES".Gestion.Datos.Int_19 :=
	            "DB11_INFORMES".Gestion.Datos.Int_20 := 0;
	            "DB11_INFORMES".Gestion.Aviso.Registrar := 0;
	            "DB11_INFORMES".Gestion.Etapa := #REPOSO;
	            
	            // =============================================================================
	        #FALLO:
	            
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := "DB1_SYS".FechaHoraActual,
	                                    Registrar := 1,
	                                    Categoria := "TRZ_CAT_1_SYS",
	                                    User := '',
	                                    CodInt_1 := "TRZ_CAT_1_SYS",
	                                    CodInt_2 := "TRZ_SYS_INF_ERR",
	                                    CodInt_3 := 0,
	                                    CodInt_4 := 0,
	                                    CodInt_5 := 0,
	                                    CodReal_1 := 0.0,
	                                    CodReal_2 := 0.0);
	            "DB11_INFORMES".Gestion.Datos.Registrar := 0;
	            "DB11_INFORMES".Gestion.Etapa := #REPOSO;
	            
	    END_CASE;
	    
	END_REGION
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>