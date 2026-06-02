---
title: FC7_ZC_GESTOR_TRAZA
---
# FC FC7_ZC_GESTOR_TRAZA

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 2.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función principal para la gestión de mensajes de trazabilidad y su envío estructurado a los sistemas de supervisión.
    
    Las tareas que realiza son las siguientes:
    
    - Búsqueda en orden inverso dentro del buffer para localizar y extraer el último registro con orden de registrar.
    - Transferencia del registro a variables de gestión estáticas, formateo de cadenas de tiempo y usuario, y liberación de la posición ocupada en el buffer.
    - Ejecución de la **Etapa Reposo**: Con un registro habilitado y conexión activa, lanza la orden de inicio de secuencia.
    - Ejecución de la **Etapa Comprobaciones Iniciales**: Valida que la categoría del evento se encuentre en los límites permitidos (forzando una categoría de usuario si excede el índice), limpia las confirmaciones previas y espera la actualización temporal.
    - Ejecución de la **Etapa Generar Texto**: Envía la orden de generación de textos a los SCADAs habilitados, transitando al recibir la confirmación de todos o al superar un tiempo de espera de seguridad.
    - Ejecución de la **Etapa Lanzar Aviso**: Activa la señal de aviso correspondiente a la categoría de la trazabilidad procesada.
    - Ejecución de la **Etapa Espera**: Retiene el aviso activo durante el tiempo configurado para garantizar su captura en los sistemas de supervisión.
    - Ejecución de la **Etapa Borrar Texto**: Lanza la orden de limpieza de textos en pantalla a todos los SCADAs.
    - Ejecución de la **Etapa Quitar Aviso**: Desactiva la señal de aviso y verifica mediante un tiempo corto que el evento ha caído.
    - Ejecución de la **Etapa Borrar Datos**: Inicializa por completo los valores, códigos y textos del aviso actual, regresando a la etapa de reposo.
    - Mapeo final de las activaciones de alarma a nivel de bit, agrupándolas en dos variables tipo `Word` para las 32 categorías y aplicando sus respectivas máscaras de habilitación individual.

!!! abstract "Dependencias Requeridas"
    **DB:** [DB7_TRAZA](../Estructura de datos/DB7_TRAZA.md)

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
| `t_TextoGenerado` | `Bool` | - | `-` | Indicador de texto generado en todos los Scadas |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `REPOSO` | `Int` | - | `0` | ETAPA EN REPOSO |
| `COMPROBACION_INICIAL` | `Int` | - | `10` | ETAPA COMPROBACIONES INICIALES |
| `GENERAR_TEXTO` | `Int` | - | `20` | ETAPA GENERAR TEXTO |
| `LANZAR_AVISO` | `Int` | - | `30` | ETAPA LANZAR AVISO |
| `ESPERA` | `Int` | - | `40` | ETAPA ESPERA |
| `BORRAR_TEXTO` | `Int` | - | `50` | ETAPA BORRAR TEXTO |
| `QUITAR_AVISO` | `Int` | - | `60` | ETAPA QUITAR AVISO |
| `BORRAR_DATOS` | `Int` | - | `70` | ETAPA BORRAR DATOS |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC7_ZC_GESTOR_TRAZA" : Void
TITLE = FC7_GESTOR_TRAZA
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 2.0
//Funcion para gestion de trazabilidad
   VAR_INPUT 
      Pulso1Seg : Bool;   // Pulso de 1 segundo
   END_VAR

   VAR_TEMP 
      for_i : Int;   // Variable para bucles FOR
      t_PosicionRegistro : Int;   // Posicion del registro encontrado en el buffer
      t_RegistroEncontrado : Bool;   // Indicador de registro encontrado
      t_TextoGenerado : Bool;   // Indicador de texto generado en todos los Scadas
   END_VAR

   VAR CONSTANT 
      REPOSO : Int := 0;   // ETAPA EN REPOSO
      COMPROBACION_INICIAL : Int := 10;   // ETAPA COMPROBACIONES INICIALES
      GENERAR_TEXTO : Int := 20;   // ETAPA GENERAR TEXTO
      LANZAR_AVISO : Int := 30;   // ETAPA LANZAR AVISO
      ESPERA : Int := 40;   // ETAPA ESPERA
      BORRAR_TEXTO : Int := 50;   // ETAPA BORRAR TEXTO
      QUITAR_AVISO : Int := 60;   // ETAPA QUITAR AVISO
      BORRAR_DATOS : Int := 70;   // ETAPA BORRAR DATOS
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2022 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función principal para la gestión de mensajes de trazabilidad y su envío estructurado a los sistemas de supervisión.
	
	Las tareas que realiza son las siguientes:
	
	- Búsqueda en orden inverso dentro del buffer para localizar y extraer el último registro con orden de registrar.
	- Transferencia del registro a variables de gestión estáticas, formateo de cadenas de tiempo y usuario, y liberación de la posición ocupada en el buffer.
	- Ejecución de la **Etapa Reposo**: Con un registro habilitado y conexión activa, lanza la orden de inicio de secuencia.
	- Ejecución de la **Etapa Comprobaciones Iniciales**: Valida que la categoría del evento se encuentre en los límites permitidos (forzando una categoría de usuario si excede el índice), limpia las confirmaciones previas y espera la actualización temporal.
	- Ejecución de la **Etapa Generar Texto**: Envía la orden de generación de textos a los SCADAs habilitados, transitando al recibir la confirmación de todos o al superar un tiempo de espera de seguridad.
	- Ejecución de la **Etapa Lanzar Aviso**: Activa la señal de aviso correspondiente a la categoría de la trazabilidad procesada.
	- Ejecución de la **Etapa Espera**: Retiene el aviso activo durante el tiempo configurado para garantizar su captura en los sistemas de supervisión.
	- Ejecución de la **Etapa Borrar Texto**: Lanza la orden de limpieza de textos en pantalla a todos los SCADAs.
	- Ejecución de la **Etapa Quitar Aviso**: Desactiva la señal de aviso y verifica mediante un tiempo corto que el evento ha caído.
	- Ejecución de la **Etapa Borrar Datos**: Inicializa por completo los valores, códigos y textos del aviso actual, regresando a la etapa de reposo.
	- Mapeo final de las activaciones de alarma a nivel de bit, agrupándolas en dos variables tipo `Word` para las 32 categorías y aplicando sus respectivas máscaras de habilitación individual.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | - |
	| FB   | - |
	| DB   | `DB7_TRAZA` |
	| UDT  | - |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 00.00.01 | 31.08.2022 | (ABH)   | Primera version. |
	| 01.00.00 | 18.09.2023 | (ABH)   | Se añade gestion de bits para 16 categorias. |
	| 02.00.00 | 25.03.2026 | (ABH)   | Se eliminan `String`. Se añaden 32 categorias. Se añade gestion de generacion de textos para Scada. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION GESTION_TRAZA
	    
	    //  ==========================================================================================================
	    REGION GESTION_ULTIMO_REGISTRO
	        
	        //  Si la gestion esta habilitada, se busca el ultimo registro y se mueve a la variable de gestion de avisos para
	        //  los sistemas de supervision
	        IF "DB7_TRAZA".Gestion.HabilitacionGeneral AND #Pulso1Seg AND "DB7_TRAZA".Gestion.Etapa = #REPOSO THEN
	            
	            // Buscamos el ultimo registro
	            FOR #for_i := "N_MAX_TRAZA_BUFFER" TO 0 BY -1 DO
	                
	                // Registro encontrado
	                IF "DB7_TRAZA".Buffer[#for_i].Registrar = 1 THEN
	                    #t_PosicionRegistro := #for_i;
	                    #t_RegistroEncontrado := TRUE;
	                    EXIT;
	                END_IF;
	                
	            END_FOR;
	            
	            
	            // Si hemos encontrado el registro, copiamos a variable estatica
	            IF #t_RegistroEncontrado THEN
	                
	                //  Copiamos el los datos de la traza a variable estatica para tratarla
	                "DB7_TRAZA".Gestion.Aviso.Datos := "DB7_TRAZA".Buffer[#t_PosicionRegistro];
	                
	                "DB7_TRAZA".Gestion.Aviso.Datos.TimeStamp := CONCAT_STRING(IN1 := "DB7_TRAZA".Gestion.Aviso.Datos.TimeStamp, IN2 := '.');
	                "DB7_TRAZA".Gestion.Aviso.Datos.User := CONCAT_STRING(IN1 := 'USER: ',
	                                                                      IN2 := "DB7_TRAZA".Gestion.Aviso.Datos.User,
	                                                                      IN3 := '.');
	                
	                //  Quitamos el registro del buffer
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].Registrar := 0;
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].Categoria :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodInt_1 :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodInt_2 :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodInt_3 :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodInt_4 :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodInt_5 := 0;
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodReal_1 :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].CodReal_2 := 0.0;
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].TimeStamp :=
	                "DB7_TRAZA".Buffer[#t_PosicionRegistro].User := '';
	                
	            END_IF;
	            
	        END_IF;
	        
	    END_REGION GESTION_ULTIMO_REGISTRO
	    
	    
	    //  ==========================================================================================================
	    REGION GESTION_ORDEN_INICIAR
	        
	        // =============================================================================
	        //  Si existe registro a trazar, lanzamos la orden de iniciar la secuencia
	        IF "DB7_TRAZA".Gestion.Aviso.Datos.Registrar = 1 AND "DB7_TRAZA".Gestion.Etapa = #REPOSO AND "DB7_TRAZA".Gestion.EstadoConexion THEN
	            
	            //  Lanzamos la orden de iniciar la secuencia de registro
	            "DB7_TRAZA".Gestion.OrdenIniciar := TRUE;
	            
	        END_IF;
	        
	    END_REGION GESTION_ORDEN_INICIAR
	    
	END_REGION GESTION_TRAZA
	
	
	//  ==========================================================================================================
	REGION SECUENCIA_TRAZA
	    
	    //  En caso de deshabilitar la trazabilidad, ponemos el estado en borrar datos.
	    IF NOT "DB7_TRAZA".Gestion.HabilitacionGeneral AND "DB7_TRAZA".Gestion.Etapa <> #REPOSO THEN
	        "DB7_TRAZA".Gestion.Etapa := #BORRAR_DATOS;
	    END_IF;
	    
	    //  Gestion trazabilidad
	    CASE "DB7_TRAZA".Gestion.Etapa OF
	            
	            //  =============================================================================
	            //  Etapa reposo
	        #REPOSO:
	            REGION #REPOSO
	                
	                //  Con orden de iniciar, vamos a etapa comprobaciones iniciales
	                IF "DB7_TRAZA".Gestion.OrdenIniciar THEN
	                    "DB7_TRAZA".Gestion.Etapa := #COMPROBACION_INICIAL;
	                    "DB7_TRAZA".Gestion.OrdenIniciar := FALSE;
	                END_IF;
	                
	            END_REGION
	            
	            //  =============================================================================
	            //  Etapa comprobaciones iniciales
	        #COMPROBACION_INICIAL:
	            REGION #COMPROBACION_INICIAL
	                
	                //  Si el registro actual no tiene orden de registrar, lo borramos yendo a etapa borrar datos
	                IF "DB7_TRAZA".Gestion.Aviso.Datos.Registrar = 0 THEN
	                    "DB7_TRAZA".Gestion.Etapa := #BORRAR_DATOS;
	                ELSE
	                    //  Esperamos a que tenga los datos actualizados en scada/hmi
	                    IF #Pulso1Seg THEN
	                        "DB7_TRAZA".Gestion.TiempoActual += 1;
	                        IF "DB7_TRAZA".Gestion.TiempoActual >= "DB7_TRAZA".Gestion.SP_Tiempo THEN
	                            "DB7_TRAZA".Gestion.TiempoActual := 0;
	                            
	                            //  En caso de tener una categoria fuera de indices, formazos a categoria usuario
	                            IF "DB7_TRAZA".Gestion.Aviso.Datos.Categoria < "TRZ_CAT_1_SYS" OR "DB7_TRAZA".Gestion.Aviso.Datos.Categoria > "TRZ_CAT_32_USER" THEN
	                                "DB7_TRAZA".Gestion.Aviso.Datos.Categoria := "TRZ_CAT_32_USER";
	                            END_IF;
	                            
	                            // Limpiamos las confirmaciones de texto generado por seguridad antes de esperar
	                            "DB7_TRAZA".Gestion.Aviso.TextoGenerado[0] := FALSE;
	                            "DB7_TRAZA".Gestion.Aviso.TextoGenerado[1] := FALSE;
	                            "DB7_TRAZA".Gestion.Aviso.TextoGenerado[2] := FALSE;
	                            "DB7_TRAZA".Gestion.Aviso.TextoGenerado[3] := FALSE;
	                            
	                            "DB7_TRAZA".Gestion.Etapa := #GENERAR_TEXTO;
	                        END_IF;
	                    END_IF;
	                END_IF;
	                
	            END_REGION
	            
	            //  =============================================================================
	            //  Etapa generar texto
	        #GENERAR_TEXTO:
	            REGION #GENERAR_TEXTO
	                
	                //  Lanzamos la orden de generar textos a sistemas scada que esten habilitados
	                "DB7_TRAZA".Gestion.Aviso.GenerarTexto[0] := "DB7_TRAZA".Gestion.Aviso.HabilitarScada[0];
	                "DB7_TRAZA".Gestion.Aviso.GenerarTexto[1] := "DB7_TRAZA".Gestion.Aviso.HabilitarScada[1];
	                "DB7_TRAZA".Gestion.Aviso.GenerarTexto[2] := "DB7_TRAZA".Gestion.Aviso.HabilitarScada[2];
	                "DB7_TRAZA".Gestion.Aviso.GenerarTexto[3] := "DB7_TRAZA".Gestion.Aviso.HabilitarScada[3];
	                
	                //  Activamos marca de texto generado OK desde Scada, antes de realizar las comprobaciones.
	                #t_TextoGenerado := TRUE;
	                
	                //  Comprobamos si los Scadas estan habilitados y tenemos confirmacion de que el texto se ha generado correctamente
	                IF "DB7_TRAZA".Gestion.Aviso.HabilitarScada[0] AND NOT "DB7_TRAZA".Gestion.Aviso.TextoGenerado[0] THEN
	                    #t_RegistroEncontrado := FALSE;
	                END_IF;
	                IF "DB7_TRAZA".Gestion.Aviso.HabilitarScada[1] AND NOT "DB7_TRAZA".Gestion.Aviso.TextoGenerado[1] THEN
	                    #t_RegistroEncontrado := FALSE;
	                END_IF;
	                IF "DB7_TRAZA".Gestion.Aviso.HabilitarScada[2] AND NOT "DB7_TRAZA".Gestion.Aviso.TextoGenerado[2] THEN
	                    #t_RegistroEncontrado := FALSE;
	                END_IF;
	                IF "DB7_TRAZA".Gestion.Aviso.HabilitarScada[3] AND NOT "DB7_TRAZA".Gestion.Aviso.TextoGenerado[3] THEN
	                    #t_RegistroEncontrado := FALSE;
	                END_IF;
	                
	                
	                //  Comprobacion de fin etapa
	                IF #t_RegistroEncontrado THEN
	                    
	                    //  Tenemos confirmacion de todos los Scadas que han generado el texto correctamente
	                    "DB7_TRAZA".Gestion.TiempoActual := 0;
	                    "DB7_TRAZA".Gestion.Etapa := #LANZAR_AVISO;
	                    
	                    //  Reseteamos las ordenes de generar texto
	                    "DB7_TRAZA".Gestion.Aviso.GenerarTexto[0] := FALSE;
	                    "DB7_TRAZA".Gestion.Aviso.GenerarTexto[1] := FALSE;
	                    "DB7_TRAZA".Gestion.Aviso.GenerarTexto[2] := FALSE;
	                    "DB7_TRAZA".Gestion.Aviso.GenerarTexto[3] := FALSE;
	                    
	                ELSE
	                    
	                    //  Esperamos un tiempo de seguridad si no tenemos respuesta desde Scadas
	                    IF #Pulso1Seg THEN
	                        "DB7_TRAZA".Gestion.TiempoActual += 1;
	                        
	                        IF "DB7_TRAZA".Gestion.TiempoActual >= "DB7_TRAZA".Gestion.SP_TiempoTexto THEN
	                            
	                            "DB7_TRAZA".Gestion.TiempoActual := 0;
	                            
	                            //  Reseteamos las ordenes de generar texto
	                            "DB7_TRAZA".Gestion.Aviso.GenerarTexto[0] := FALSE;
	                            "DB7_TRAZA".Gestion.Aviso.GenerarTexto[1] := FALSE;
	                            "DB7_TRAZA".Gestion.Aviso.GenerarTexto[2] := FALSE;
	                            "DB7_TRAZA".Gestion.Aviso.GenerarTexto[3] := FALSE;
	                            
	                            "DB7_TRAZA".Gestion.Etapa := #LANZAR_AVISO;
	                        END_IF;
	                        
	                    END_IF;
	                    
	                END_IF;
	                
	            END_REGION
	            
	            //  =============================================================================
	            //  Etapa lanzar aviso
	        #LANZAR_AVISO:
	            REGION #LANZAR_AVISO
	                
	                //  Activamos orden de lanzar el aviso
	                "DB7_TRAZA".Gestion.Aviso.Aviso["DB7_TRAZA".Gestion.Aviso.Datos.Categoria] := TRUE;
	                "DB7_TRAZA".Gestion.Etapa := #ESPERA;
	                
	            END_REGION
	            
	            //  =============================================================================
	            //  Etapa espera
	        #ESPERA:
	            REGION #ESPERA
	                
	                //  Esperamos un tiempo para que el aviso se haya registrado en todos los sistemas de supervision
	                IF #Pulso1Seg THEN
	                    "DB7_TRAZA".Gestion.TiempoActual += 1;
	                    IF "DB7_TRAZA".Gestion.TiempoActual >= "DB7_TRAZA".Gestion.SP_Tiempo THEN
	                        "DB7_TRAZA".Gestion.TiempoActual := 0;
	                        "DB7_TRAZA".Gestion.Etapa := #BORRAR_TEXTO;
	                    END_IF;
	                END_IF;
	                
	            END_REGION
	            
	            
	            //  =============================================================================
	            //  Etapa borrar texto
	        #BORRAR_TEXTO:
	            REGION #BORRAR_TEXTO
	                
	                //  Lanzamos orden de borrar texto a todos los Scadas
	                "DB7_TRAZA".Gestion.Aviso.BorrarTexto := TRUE;
	                
	                //  Reseteamos los valores del aviso actual
	                "DB7_TRAZA".Gestion.Aviso.Datos.Registrar := 0;
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_1 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_2 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_3 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_4 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_5 := 0;
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodReal_1 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodReal_1 := 0.0;
	                "DB7_TRAZA".Gestion.Aviso.Datos.User :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.TimeStamp := '';
	                
	                //  Saltamos de etapa tras un tiempo
	                IF #Pulso1Seg THEN
	                    "DB7_TRAZA".Gestion.TiempoActual += 1;
	                    IF "DB7_TRAZA".Gestion.TiempoActual >= "DB7_TRAZA".Gestion.SP_Tiempo THEN
	                        "DB7_TRAZA".Gestion.TiempoActual := 0;
	                        "DB7_TRAZA".Gestion.Aviso.BorrarTexto := FALSE;
	                        "DB7_TRAZA".Gestion.Etapa := #QUITAR_AVISO;
	                    END_IF;
	                END_IF;
	                
	            END_REGION
	            
	            //  =============================================================================
	            //  Etapa quitar aviso
	        #QUITAR_AVISO:
	            REGION #QUITAR_AVISO
	                
	                //  Desactivamos el aviso
	                "DB7_TRAZA".Gestion.Aviso.Aviso["DB7_TRAZA".Gestion.Aviso.Datos.Categoria] := FALSE;
	                
	                //  Saltamos de etapa tras un tiempo
	                IF #Pulso1Seg THEN
	                    "DB7_TRAZA".Gestion.TiempoActual += 1;
	                    IF "DB7_TRAZA".Gestion.TiempoActual >= 2 AND NOT "DB7_TRAZA".Gestion.Aviso.Aviso["DB7_TRAZA".Gestion.Aviso.Datos.Categoria] THEN
	                        "DB7_TRAZA".Gestion.TiempoActual := 0;
	                        "DB7_TRAZA".Gestion.Etapa := #BORRAR_DATOS;
	                    END_IF;
	                END_IF;
	                
	            END_REGION
	            
	            
	            //  =============================================================================
	            //  Etapa borrar datos
	        #BORRAR_DATOS:
	            REGION #BORRAR_DATOS
	                
	                //  Reseteamos los valores del aviso actual
	                "DB7_TRAZA".Gestion.Aviso.Datos.Registrar := 0;
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_1 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_2 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_3 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_4 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodInt_5 := 0;
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodReal_1 :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.CodReal_1 := 0.0;
	                "DB7_TRAZA".Gestion.Aviso.Datos.User :=
	                "DB7_TRAZA".Gestion.Aviso.Datos.TimeStamp := '';
	                
	                "DB7_TRAZA".Gestion.Etapa := #REPOSO;
	                
	            END_REGION
	            
	    END_CASE;
	    
	END_REGION SECUENCIA_TRAZA    
	
	
	//  ==========================================================================================================
	REGION ACTIVACION_ALARMAS
	    
	    //  Activamos los avisos en WORD segun la categoria y su habilitacion
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X0 := "DB7_TRAZA".Gestion.HabilitarCategoria[1] AND "DB7_TRAZA".Gestion.Aviso.Aviso[0];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X1 := "DB7_TRAZA".Gestion.HabilitarCategoria[1] AND "DB7_TRAZA".Gestion.Aviso.Aviso[1];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X2 := "DB7_TRAZA".Gestion.HabilitarCategoria[2] AND "DB7_TRAZA".Gestion.Aviso.Aviso[2];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X3 := "DB7_TRAZA".Gestion.HabilitarCategoria[3] AND "DB7_TRAZA".Gestion.Aviso.Aviso[3];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X4 := "DB7_TRAZA".Gestion.HabilitarCategoria[4] AND "DB7_TRAZA".Gestion.Aviso.Aviso[4];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X5 := "DB7_TRAZA".Gestion.HabilitarCategoria[5] AND "DB7_TRAZA".Gestion.Aviso.Aviso[5];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X6 := "DB7_TRAZA".Gestion.HabilitarCategoria[6] AND "DB7_TRAZA".Gestion.Aviso.Aviso[6];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X7 := "DB7_TRAZA".Gestion.HabilitarCategoria[7] AND "DB7_TRAZA".Gestion.Aviso.Aviso[7];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X8 := "DB7_TRAZA".Gestion.HabilitarCategoria[8] AND "DB7_TRAZA".Gestion.Aviso.Aviso[8];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X9 := "DB7_TRAZA".Gestion.HabilitarCategoria[9] AND "DB7_TRAZA".Gestion.Aviso.Aviso[9];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X10 := "DB7_TRAZA".Gestion.HabilitarCategoria[10] AND "DB7_TRAZA".Gestion.Aviso.Aviso[10];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X11 := "DB7_TRAZA".Gestion.HabilitarCategoria[11] AND "DB7_TRAZA".Gestion.Aviso.Aviso[11];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X12 := "DB7_TRAZA".Gestion.HabilitarCategoria[12] AND "DB7_TRAZA".Gestion.Aviso.Aviso[12];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X13 := "DB7_TRAZA".Gestion.HabilitarCategoria[13] AND "DB7_TRAZA".Gestion.Aviso.Aviso[13];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X14 := "DB7_TRAZA".Gestion.HabilitarCategoria[14] AND "DB7_TRAZA".Gestion.Aviso.Aviso[14];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[0].%X15 := "DB7_TRAZA".Gestion.HabilitarCategoria[15] AND "DB7_TRAZA".Gestion.Aviso.Aviso[15];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X0 := "DB7_TRAZA".Gestion.HabilitarCategoria[16] AND "DB7_TRAZA".Gestion.Aviso.Aviso[16];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X1 := "DB7_TRAZA".Gestion.HabilitarCategoria[17] AND "DB7_TRAZA".Gestion.Aviso.Aviso[17];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X2 := "DB7_TRAZA".Gestion.HabilitarCategoria[18] AND "DB7_TRAZA".Gestion.Aviso.Aviso[18];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X3 := "DB7_TRAZA".Gestion.HabilitarCategoria[19] AND "DB7_TRAZA".Gestion.Aviso.Aviso[19];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X4 := "DB7_TRAZA".Gestion.HabilitarCategoria[20] AND "DB7_TRAZA".Gestion.Aviso.Aviso[20];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X5 := "DB7_TRAZA".Gestion.HabilitarCategoria[21] AND "DB7_TRAZA".Gestion.Aviso.Aviso[21];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X6 := "DB7_TRAZA".Gestion.HabilitarCategoria[22] AND "DB7_TRAZA".Gestion.Aviso.Aviso[22];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X7 := "DB7_TRAZA".Gestion.HabilitarCategoria[23] AND "DB7_TRAZA".Gestion.Aviso.Aviso[23];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X8 := "DB7_TRAZA".Gestion.HabilitarCategoria[24] AND "DB7_TRAZA".Gestion.Aviso.Aviso[24];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X9 := "DB7_TRAZA".Gestion.HabilitarCategoria[25] AND "DB7_TRAZA".Gestion.Aviso.Aviso[25];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X10 := "DB7_TRAZA".Gestion.HabilitarCategoria[26] AND "DB7_TRAZA".Gestion.Aviso.Aviso[26];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X11 := "DB7_TRAZA".Gestion.HabilitarCategoria[27] AND "DB7_TRAZA".Gestion.Aviso.Aviso[27];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X12 := "DB7_TRAZA".Gestion.HabilitarCategoria[28] AND "DB7_TRAZA".Gestion.Aviso.Aviso[28];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X13 := "DB7_TRAZA".Gestion.HabilitarCategoria[29] AND "DB7_TRAZA".Gestion.Aviso.Aviso[29];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X14 := "DB7_TRAZA".Gestion.HabilitarCategoria[30] AND "DB7_TRAZA".Gestion.Aviso.Aviso[30];
	    "DB7_TRAZA".Gestion.Aviso.AvisoWord[1].%X15 := "DB7_TRAZA".Gestion.HabilitarCategoria[31] AND "DB7_TRAZA".Gestion.Aviso.Aviso[31];
	    
	END_REGION ACTIVACION_ALARMAS
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>