---
title: FC5_ZC_GESTOR_PROCESO
---
# FC FC5_ZC_GESTOR_PROCESO

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ZeusControl

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función principal para la gestión integral del ciclo de vida, la máquina de estados y los recursos asociados a un proceso individual.
    
    Las tareas que realiza son las siguientes:
    
    - Generación de pulsos de transición (flancos) y evaluación continua de los enclavamientos externos y la entrada de seguridad general.
    - Gestión centralizada de las órdenes de mando procedentes del HMI mediante pulsadores temporizados (`Marcha`, `Paro`, `Pausa`, `Reanudar`, `Salto de etapa` y `Reset de errores`).
    - Ejecución cíclica de la máquina de estados (Grafcet) del proceso, gestionando las etapas de Reposo/Finalizado, Arrancando, En Marcha, Pausando/Pausado/Reanudando, Finalizando y En Error.
    - Administración dinámica de las entidades operativas (equipos, válvulas, motores): validación de disponibilidad, captura/liberación, y asignación de sus estados físicos y lógicos (Producción, CIP, SIP, Standby, Con Producto, Con Agua, Vacía).
    - Monitoreo consolidado de alarmas, agrupando fallos de dispositivos o de usuario para abortar el proceso si la configuración lo requiere.
    - Gestión de transiciones y recursos internos de la etapa actual: salto de etapa (forzado o automático), temporizaciones (`TON`, `TONR`, `Tiempo de Etapa`) y volumetría (`Litros de Etapa`).
    - Registro de datos de informe operativo, capturando marcas de tiempo de inicio/fin y contabilizando el tiempo en marcha y total.
    - Generación y envío estructurado de registros de trazabilidad al sistema para auditar los cambios de estado principales (Inicio, Pausa, Reanudar, Fin), saltos de etapa y errores.

!!! abstract "Dependencias Requeridas"
    **FC:** [FC15001_ZC_INT_TO_STRING](../Bloques de codigo/FC15001_ZC_INT_TO_STRING.md)
    **FC:** [FC15025_ZC_CONTADOR_TIEMPO](../Bloques de codigo/FC15025_ZC_CONTADOR_TIEMPO.md)
    **FC:** [FC15026_ZC_PULSADOR](../Bloques de codigo/FC15026_ZC_PULSADOR.md)
    **FC:** [FC15151_ZC_MARCHA_PARO_SEC](../Bloques de codigo/FC15151_ZC_MARCHA_PARO_SEC.md)
    **FC:** [FC2928_ZC_TON_INDV](../Bloques de codigo/FC2928_ZC_TON_INDV.md)
    **FC:** [FC2930_ZC_TONR_INDV](../Bloques de codigo/FC2930_ZC_TONR_INDV.md)
    **FC:** [FC4_ZC_DISPONIBILIDAD_ENTIDAD](../Bloques de codigo/FC4_ZC_DISPONIBILIDAD_ENTIDAD.md)
    **FC:** [FC6_ZC_ESTADO_ENTIDAD](../Bloques de codigo/FC6_ZC_ESTADO_ENTIDAD.md)
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **DB:** [DB6_ENTIDAD](../Estructura de datos/DB6_ENTIDAD.md)
    **DB:** [UDT_ZC_CONTADOR_TIEMPO](../Estructura de datos/UDT_ZC_CONTADOR_TIEMPO.md)
    **DB:** [UDT_ZC_DISP_TON](../Estructura de datos/UDT_ZC_DISP_TON.md)
    **DB:** [UDT_ZC_DISP_TONR](../Estructura de datos/UDT_ZC_DISP_TONR.md)
    **DB:** [UDT_ZC_FECHA](../Estructura de datos/UDT_ZC_FECHA.md)
    **DB:** [UDT_ZC_MARCHA_PARO_SEC](../Estructura de datos/UDT_ZC_MARCHA_PARO_SEC.md)
    **DB:** [UDT_ZC_PRO_LITROS_ETAPA](../Estructura de datos/UDT_ZC_PRO_LITROS_ETAPA.md)
    **DB:** [UDT_ZC_PRO_PROCESO](../Estructura de datos/UDT_ZC_PRO_PROCESO.md)
    **DB:** [UDT_ZC_PRO_TIEMPO_ETAPA](../Estructura de datos/UDT_ZC_PRO_TIEMPO_ETAPA.md)
    **DB:** [UDT_ZC_PULSADOR](../Estructura de datos/UDT_ZC_PULSADOR.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1Seg` | `Bool` | - | `-` | - |
| `FechaHoraActual` | `DTL` | - | `-` | - |
| `SeguridadOk` | `Bool` | - | `-` | Seguridad OK |
| `HabilitacionErrores` | `Bool` | - | `-` | Habilita el chequeo de todos los errores de los procesos |
| `HabilitacionErroresEntidades` | `Bool` | - | `-` | Habilita el chequeo de compatibilidad de entidades en uso |
| `HabilitacionErroresDispositivos` | `Bool` | - | `-` | Habilita el chequeo de los errores/manualizaciones de válvula/motores |
| `HabilitacionAbortarErrores` | `Bool` | - | `-` | Habilita abortar el proceso con errores |
| `TiempoPulsadores` | `Int` | - | `-` | - |

### Entrada/Salida
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `PRO` | `UDT_ZC_PRO_PROCESO` | - | `-` | - |

### Temporales
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `for_i` | `Int` | - | `-` | - |
| `t_DispNumero` | `Int` | - | `-` | - |
| `t_ErrorYaRegistrado` | `Bool` | - | `-` | - |

### Constantes
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `REANUDANDO` | `USInt` | - | `3` | - |
| `EN_MARCHA` | `USInt` | - | `5` | - |
| `PAUSADO` | `USInt` | - | `7` | - |
| `FINALIZADO` | `USInt` | - | `0` | - |
| `COMPROBACION_ERRORES` | `USInt` | - | `0` | - |
| `ARRANQUE_OK` | `USInt` | - | `2` | - |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC5_ZC_GESTOR_PROCESO" : Void
TITLE = FC5_ZC_GESTOR_PROCESO
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ZeusControl
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para gestion de procesos
   VAR_INPUT 
      Pulso1Seg : Bool;
      Usuario : String;
      FechaHoraActual {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;
      PrimerArranque : Bool;
      SeguridadOk : Bool;   // Seguridad OK
      HabilitacionErrores : Bool;   // Habilita el chequeo de todos los errores de los procesos
      HabilitacionErroresEntidades : Bool;   // Habilita el chequeo de compatibilidad de entidades en uso
      HabilitacionErroresDispositivos : Bool;   // Habilita el chequeo de los errores/manualizaciones de válvula/motores
      HabilitacionAbortarErrores : Bool;   // Habilita abortar el proceso con errores
      TiempoPulsadores : Int;
   END_VAR

   VAR_IN_OUT 
      PRO : "UDT_ZC_PRO_PROCESO";
   END_VAR

   VAR_TEMP 
      for_i : Int;
      t_TipoError : Int;
      t_DispNumero : Int;
      t_EntidadesCargadas : Bool;
      t_ErrorYaRegistrado : Bool;
   END_VAR

   VAR CONSTANT 
      REANUDANDO : USInt := 3;
      ARRANCANDO : USInt := 4;
      EN_MARCHA : USInt := 5;
      PAUSANDO : USInt := 6;
      PAUSADO : USInt := 7;
      FINALIZANDO : USInt := 8;
      FINALIZADO : USInt := 0;
      EN_ERROR : USInt := 10;
      COMPROBACION_ERRORES : USInt := 0;
      COMPROBACION_ENTIDADES : USInt := 1;
      ARRANQUE_OK : USInt := 2;
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2018 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función principal para la gestión integral del ciclo de vida, la máquina de estados y los recursos asociados a un proceso individual.
	
	Las tareas que realiza son las siguientes:
	
	- Generación de pulsos de transición (flancos) y evaluación continua de los enclavamientos externos y la entrada de seguridad general.
	- Gestión centralizada de las órdenes de mando procedentes del HMI mediante pulsadores temporizados (`Marcha`, `Paro`, `Pausa`, `Reanudar`, `Salto de etapa` y `Reset de errores`).
	- Ejecución cíclica de la máquina de estados (Grafcet) del proceso, gestionando las etapas de Reposo/Finalizado, Arrancando, En Marcha, Pausando/Pausado/Reanudando, Finalizando y En Error.
	- Administración dinámica de las entidades operativas (equipos, válvulas, motores): validación de disponibilidad, captura/liberación, y asignación de sus estados físicos y lógicos (Producción, CIP, SIP, Standby, Con Producto, Con Agua, Vacía).
	- Monitoreo consolidado de alarmas, agrupando fallos de dispositivos o de usuario para abortar el proceso si la configuración lo requiere.
	- Gestión de transiciones y recursos internos de la etapa actual: salto de etapa (forzado o automático), temporizaciones (`TON`, `TONR`, `Tiempo de Etapa`) y volumetría (`Litros de Etapa`).
	- Registro de datos de informe operativo, capturando marcas de tiempo de inicio/fin y contabilizando el tiempo en marcha y total.
	- Generación y envío estructurado de registros de trazabilidad al sistema para auditar los cambios de estado principales (Inicio, Pausa, Reanudar, Fin), saltos de etapa y errores.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC15001_ZC_INT_TO_STRING`, `FC15025_ZC_CONTADOR_TIEMPO`, `FC15026_ZC_PULSADOR`, `FC15151_ZC_MARCHA_PARO_SEC`, `FC2928_ZC_TON_INDV`, `FC2930_ZC_TONR_INDV`, `FC4_ZC_DISPONIBILIDAD_ENTIDAD`, `FC6_ZC_ESTADO_ENTIDAD`, `FC8_ZC_TRAZA_REGISTRO` |
	| FB   | - |
	| DB   | `DB6_ENTIDAD` |
	| UDT  | `UDT_ZC_CONTADOR_TIEMPO`, `UDT_ZC_DISP_TON`, `UDT_ZC_DISP_TONR`, `UDT_ZC_FECHA`, `UDT_ZC_MARCHA_PARO_SEC`, `UDT_ZC_PRO_LITROS_ETAPA`, `UDT_ZC_PRO_PROCESO`, `UDT_ZC_PRO_TIEMPO_ETAPA`, `UDT_ZC_PULSADOR` |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico   | Cambios |
	|----------|------------|-----------|---------|
	| 01.00.00 | 01.01.2018 | (ZC)      | Primera version. Antiguo `FC20` y `DB20` (Ver 21029 Gullon). |
	| 01.00.01 | 15.10.2020 | (ABH)     | Segunda version. (Ver 21115 Da Veiga). |
	| 01.00.02 | 27.07.2021 | (ABH)     | Cambio en reset error para mostrar texto en HMI/SCADA. |
	| 01.00.03 | 15.10.2020 | (HCR)     | Cambio en logica gestor para uso de proceso individual en vez de array de procesos. Cambio en logica pulsadores. |
	| 01.00.04 | 08.11.2022 | (ABH)     | Fix marca de tiempo cumplido al cambio de etapa. |
	| 01.00.05 | 12.12.2022 | (ABH)     | Reorganizacion UDT proceso para estandarizacion. Se añade trazabilidad. Integracion marcha paro secuencial a traves de FC. |
	| 01.00.06 | 18.09.2023 | (ABH)     | Se añade ID de asignacion de la entidad al texto de error al capturar la entidad. |
	| 01.00.07 | 23.10.2023 | (ABH/HCR) | Fix secuencia arranque, problema con entidades con numero 0. |
	| 01.00.08 | 29.08.2024 | (ABH)     | Fix texto error en captura entidades, se acorta. |
	| 01.00.09 | 13.01.2025 | (ABH)     | Modificacion reset estado entidades. |
	| 01.00.10 | 15.01.2025 | (ABH)     | Reorganizacion UDT para añadir ordenes ConProducto, ConAgua y Vacia en las entidades. Se añade logica de asignacion con entidades capturadas. |
	| 01.00.11 | 27.01.2025 | (ABH)     | Fix en grafcet proceso. En reanudando, con algun error, sin tener la secuencia de arranque OK, vamos a estado EnError. |
	| 01.00.12 | 07.03.2025 | (ABH)     | Se añade litros etapa, al estilo de tiempo etapa. |
	| 01.00.13 | 10.03.2025 | (ABH)     | Se añade gestion de codigo de producto a las entidades. |
	| 01.00.14 | 12.03.2025 | (ABH)     | Reorganizacion UDT para añadir temporizadores. Se añade entidad STANDBY. Cambio en gestion entidades para ver si esta disponible. |
	| 01.00.15 | 24.04.2025 | (HCR)     | Se añade gestion de idioma. |
	| 01.00.16 | 11.09.2025 | (ABH)     | Se eliminan las constantes de idioma dentro del FC. Se utilizan constantes globales para facilitar su traduccion. |
	| 01.00.17 | 05.11.2025 | (ABH)     | Se integra la gestion de salto de etapa directamente en el `FC` de proceso. |
	| 01.00.18 | 04.12.2025 | (ABH)     | Se eliminan los string del proceso. Solo se mantiene un string auxiliar para poder generar dinamicamente los textos de entidades, o para su uso en programa (No recomendado). |
	| 01.00.19 | 05.12.2025 | (ABH)     | Se refactoriza gestion entidades para realizarla de forma eficiente. Se fusionan bucles FOR para optimizacion de tiempo de ciclo. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION COMPROBACION_PROCESO_HABILITADO
	    
	    //  Si el proceso no esta habilitado, salimos de la funcion
	    IF #PRO.TipoProceso = 0 THEN
	        RETURN;
	    END_IF;
	    
	END_REGION COMPROBACION_PROCESO_HABILITADO
	
	
	//  ==========================================================================================================
	REGION GESTION_PULSOS_ESTADOS
	    
	    //  Flancos de estado de procesos
	    #PRO.Flanco.F_Arrancando := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND ((#PRO.EtapaActual <> 0) AND (#PRO.Aux.oldEtapa = 0)) AND (#PRO.Estado.CodEstado = #ARRANCANDO);
	    #PRO.Flanco.F_EnMarcha := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #EN_MARCHA);
	    #PRO.Flanco.F_Finalizado := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #FINALIZADO);
	    #PRO.Flanco.F_Finalizando := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #FINALIZANDO);
	    #PRO.Flanco.F_Pausado := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #PAUSADO);
	    #PRO.Flanco.F_Pausando := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #PAUSANDO);
	    #PRO.Flanco.F_Reanudando := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #REANUDANDO);
	    #PRO.Flanco.F_EnError := (#PRO.Estado.CodEstado <> #PRO.Aux.oldCodigoEstado) AND (#PRO.Estado.CodEstado = #EN_ERROR);
	    #PRO.Flanco.F_InformeInicio := #PRO.Informe.OrdenIncio AND NOT #PRO.Aux.oldInformeInicio;
	    #PRO.Flanco.F_InformeFin := #PRO.Informe.OrdenFin AND NOT #PRO.Aux.oldInformeFin;
	    #PRO.Flanco.F_CambioEtapa := #PRO.EtapaActual <> #PRO.Aux.oldEtapa;
	    
	    //  Actualizar Estado y Etapa Anterior
	    #PRO.Aux.oldEtapa := #PRO.EtapaActual;
	    #PRO.Aux.oldCodigoEstado := #PRO.Estado.CodEstado;
	    #PRO.Aux.oldInformeInicio := #PRO.Informe.OrdenIncio;
	    #PRO.Aux.oldInformeFin := #PRO.Informe.OrdenFin;
	    
	END_REGION GESTION_PULSOS_ESTADOS
	
	
	//  ==========================================================================================================
	REGION PULSADORES
	    
	    //  Pulsador marcha
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_MAR",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.Pulsadores.Marcha,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador paro
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_PAR",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.Pulsadores.Paro,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador pausa
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_PAU",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.Pulsadores.Pausa,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador reanudar
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_REA",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.Pulsadores.Reanudar,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador reset errores
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_RST_ERR",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.Pulsadores.ResetErrores,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador salto etapa
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_SALTO_ETA",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.Pulsadores.SaltoEtapa,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador aceptar ventana de avisos
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_VEN_ACE",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.VentanaAviso.Aceptar,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	    //  Pulsador cancelar ventana de avisos
	    "FC15026_ZC_PULSADOR"(Pulso1Seg := #Pulso1Seg,
	                          TrazaCategoria := "TRZ_CAT_4_PRO_PUL",
	                          TrazaIdProceso := #PRO.ID,
	                          TrazaIdPulsador := "TRZ_SYS_PRO_PUL_VEN_CAN",
	                          Usuario := #Usuario,
	                          FechaHoraActual := #FechaHoraActual,
	                          Pulsador := #PRO.VentanaAviso.Cancelar,
	                          SP_Tiempo := #TiempoPulsadores);
	    
	END_REGION PULSADORES
	
	
	//  ==========================================================================================================
	REGION RESET_ORDENES_PREVIAS
	    
	    //  Si no tenemos habilitado el paro con errores, reseteamos la orden de paro.
	    IF NOT #HabilitacionAbortarErrores AND #PRO.Estado.AlgunError AND (#PRO.Ordenes.Paro OR #PRO.Pulsadores.Paro.Plc) THEN
	        #PRO.Ordenes.Paro := FALSE;
	    END_IF;
	    
	    //  Reset Orden Salto Etapa
	    IF NOT #PRO.Estado.EnMarcha THEN
	        #PRO.Ordenes.SaltarEtapa := FALSE;
	    END_IF;
	    
	END_REGION RESET_ORDENES_PREVIAS
	
	
	//  ==========================================================================================================
	REGION ENCLAVAMIENTO
	    
	    //  Gestion marca proceso enclavado
	    #PRO.Estado.Enclavado := FALSE;
	    FOR #for_i := 1 TO 15 DO
	        
	        IF #PRO.Enclavamiento[#for_i] THEN
	            #PRO.Estado.Enclavado := TRUE;
	            EXIT;
	        END_IF;
	    END_FOR;
	    
	END_REGION ENCLAVAMIENTO
	
	
	//  ==========================================================================================================
	REGION PRIMER_ARRANQUE
	    
	    //  En el arranque del PLC, ponemos el proceso en error.
	    IF #PRO.EtapaActual > 0 AND #PrimerArranque THEN
	        #PRO.Error.Codigo := -1;
	        #PRO.Error.Sistema[5] := TRUE;
	    END_IF;
	    
	END_REGION PRIMER_ARRANQUE
	
	
	//  ==========================================================================================================
	REGION ENTRADA_SEGURIDAD
	    
	    //  Gestion entrada de seguridad.
	    IF NOT #SeguridadOk THEN
	        #PRO.Error.Codigo := -2;
	        #PRO.Error.Sistema[4] := TRUE;
	    END_IF;
	    
	END_REGION ENTRADA_SEGURIDAD
	
	
	//  ==========================================================================================================
	REGION BITS_ESTADO
	    
	    //  Activación de bits de estado
	    #PRO.Estado.Finalizado := (#PRO.Estado.CodEstado = #FINALIZADO OR #PRO.Estado.CodEstado = 0);
	    #PRO.Estado.Arrancando := (#PRO.Estado.CodEstado = #ARRANCANDO);
	    #PRO.Estado.EnMarcha := (#PRO.Estado.CodEstado = #EN_MARCHA);
	    #PRO.Estado.Pausando := (#PRO.Estado.CodEstado = #PAUSANDO);
	    #PRO.Estado.Pausado := (#PRO.Estado.CodEstado = #PAUSADO);
	    #PRO.Estado.Reanudando := (#PRO.Estado.CodEstado = #REANUDANDO);
	    #PRO.Estado.Finalizando := (#PRO.Estado.CodEstado = #FINALIZANDO);
	    #PRO.Estado.EnError := (#PRO.Estado.CodEstado = #EN_ERROR);
	    
	END_REGION BITS_ESTADO
	
	
	//  ==========================================================================================================
	REGION MAQUINA_DE_ESTADOS
	    
	    CASE #PRO.Estado.CodEstado OF
	            
	        #FINALIZADO:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado finalizado del proceso.
	            //  En el, se resetean los estados y marcas auxiliares del proceso. Ademas, en caso de paro por operador, esperamos 10 segungos
	            //  para quitar el aviso de "Paro operador".
	            //  Tambien se gestiona el estado de cambio de estado de FINALIZADO ---> ARRANCANDO
	            REGION FINALIZADO
	                
	                //  =============================================================================
	                REGION RESET_VARIABLES
	                    
	                    #PRO.Error.Codigo := 0;
	                    #PRO.Estado.CodEstado := 0;
	                    #PRO.EtapaActual := 0;
	                    #PRO.TiempoEtapa.Actual := 0;
	                    #PRO.Informe.OrdenIncio := FALSE;
	                    #PRO.Aux.oldInformeInicio := FALSE;
	                    #PRO.Informe.OrdenFin := FALSE;
	                    #PRO.Aux.oldInformeFin := FALSE;
	                    #PRO.Informe.OrdenMarcha := FALSE;
	                    #PRO.Aux.ProArrancadoOK := FALSE;
	                    #PRO.Aux.ProParadoOK := FALSE;
	                    #PRO.Aux.ProFinalizadoOK := FALSE;
	                    #PRO.Aux.ErroresComprobados := FALSE;
	                    #PRO.Aux.EntidadesCargadas := FALSE;
	                    #PRO.Aux.EntidadesDisponibles := FALSE;
	                    #PRO.Aux.SecuenciaArranque := 0;
	                    #PRO.TiempoEtapa.SP := 0;
	                    
	                    //  Reset aviso paro operador pasados 10 segundos
	                    IF #PRO.Aviso.Sistema[2] THEN
	                        
	                        IF #Pulso1Seg THEN
	                            
	                            #PRO.Aux.TiempoResetParoOp += 1;
	                            
	                            IF #PRO.Aux.TiempoResetParoOp >= 10 THEN
	                                #PRO.Aviso.Sistema[2] := FALSE;
	                                #PRO.Aux.TiempoResetParoOp := 0;
	                            END_IF;
	                            
	                        END_IF;
	                        
	                    END_IF;
	                    
	                END_REGION RESET_VARIABLES
	                
	                
	                //  =============================================================================
	                REGION FINALIZADO_TO_ARRANCANDO
	                    
	                    //  Si el proceso no está enclavado no tiene alarma, con pulsador u orden de marcha arrancamos el proceso
	                    IF NOT #PRO.#Estado.Enclavado
	                        AND
	                        (#PRO.Ordenes.Marcha OR #PRO.Pulsadores.Marcha.Plc)
	                        AND
	                        NOT #PRO.Estado.AlgunError
	                    THEN
	                        
	                        #PRO.Ordenes.Marcha := FALSE;
	                        #PRO.Aux.ParoOperador := FALSE;
	                        #PRO.Estado.CodEstado := #ARRANCANDO;
	                        #PRO.EtapaSiguiente := 1;
	                        GOTO FIN_ESTADOS;
	                        
	                    END_IF;
	                    
	                END_REGION FINALIZADO_TO_ARRANCANDO
	                
	            END_REGION FINALIZADO
	            
	        #ARRANCANDO:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado arrancando del proceso.
	            //  En el, se realiza una subsecuencia de comprobacion de arranque:
	            //      1- Se comprueban errores
	            //      2- Se comprueban disponibilidad de entidades
	            //      3- Si errores y entidades esta correcto, vamos a estado en marcha, de lo contrario, nos vamos a estado pausando
	            REGION ARRANCANDO
	                
	                //  Reset aviso paro operador
	                #PRO.Aviso.Sistema[2] := FALSE;
	                #PRO.Aux.TiempoResetParoOp := 0;
	                
	                //  Con orden de finalizar, vamos a etapa FINALIZANDO
	                IF #PRO.Ordenes.Paro OR #PRO.Pulsadores.Paro.Plc THEN
	                    #PRO.Aux.ParoOperador := TRUE;
	                    #PRO.Estado.CodEstado := #FINALIZANDO;
	                    GOTO FIN_ESTADOS;
	                END_IF;
	                
	                //  Con orden de pausar, vamos a etapa PAUSANDO
	                IF #PRO.Ordenes.Pausa OR #PRO.Pulsadores.Pausa.Plc THEN
	                    #PRO.Estado.CodEstado := #PAUSANDO;
	                    GOTO FIN_ESTADOS;
	                END_IF;
	                
	                //  ==========================================================================================================
	                REGION SECUENCIA_ARRANQUE
	                    
	                    CASE #PRO.Aux.SecuenciaArranque OF
	                            
	                        #COMPROBACION_ERRORES:
	                            //  ==========================================================================================================
	                            REGION COMPROBACION_ERRORES
	                                
	                                //  En el arranque, primero esperamos un ciclo de SCAN del plc para comprobar los errores
	                                IF NOT #PRO.Aux.ErroresComprobados THEN
	                                    
	                                    IF #HabilitacionErrores AND #PRO.Estado.AlgunError THEN
	                                        #PRO.Estado.CodEstado := #PAUSANDO;
	                                        GOTO FIN_ESTADOS;
	                                    END_IF;
	                                    
	                                ELSE
	                                    #PRO.Aux.SecuenciaArranque := #COMPROBACION_ENTIDADES;
	                                END_IF;
	                                
	                                #PRO.Aux.ErroresComprobados := TRUE;
	                                
	                            END_REGION COMPROBACION_ERRORES
	                            
	                        #COMPROBACION_ENTIDADES:
	                            //  ==========================================================================================================
	                            REGION COMPROBACION_ENTIDADES
	                                
	                                IF NOT #PRO.Estado.AlgunError THEN
	                                    
	                                    //  Revisamos si las entidades estan disponibles, si es asi,
	                                    //  las capturamos y ponemos a TRUE el bit EntidadesCapturadas, de lo contrario ponemos
	                                    //  a FALSE el bit EntidadesDisponibles y vamos a etapa PAUSANDO.
	                                    IF NOT #PRO.Aux.EntidadesCargadas THEN
	                                        
	                                        //  Inicializamos el bit entidades Disponibles
	                                        #PRO.Aux.EntidadesDisponibles := TRUE;
	                                        
	                                        FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	                                            
	                                            //  Comprobamos que está declarada la entidad y que esta configurada como captura al arranque
	                                            IF #PRO.Entidad[#for_i].ID <> 0 AND NOT #PRO.Entidad[#for_i].Tipo THEN
	                                                
	                                                //  Revisamos el estado de las entidades en el arranque
	                                                "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                                        TipoProceso := #PRO.TipoProceso,
	                                                                        CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                                        TipoError => #t_TipoError,
	                                                                        DispNumero => #t_DispNumero);
	                                                
	                                                //  Si hay alguna entidad que no esta disponible, ponemos a FALSE el bit EntidadesDisponibles para irnos al etapa PAUSANDO
	                                                IF NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Disponible THEN
	                                                    #PRO.Aux.EntidadesDisponibles := FALSE;
	                                                    EXIT;
	                                                END_IF;
	                                                
	                                            END_IF;
	                                        END_FOR;
	                                    END_IF;
	                                    
	                                ELSE
	                                    
	                                    //  En caso de algun error, vamos a pausando directamente.
	                                    #PRO.Estado.CodEstado := #PAUSANDO;
	                                    GOTO FIN_ESTADOS;
	                                    
	                                END_IF;
	                                
	                                //  CAPTURA DE ENTIDADES
	                                //  Si no estan disponibles pausamos la secuencia
	                                IF NOT #PRO.Aux.EntidadesDisponibles THEN
	                                    
	                                    //  Lla entidad esta en error o no esta disponible
	                                    IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Alarma.Dispositivo THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_ERR";
	                                    ELSIF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Alarma.Manual THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_MAN";
	                                    ELSIF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_PRD";
	                                    ELSIF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_CIP";
	                                    ELSIF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_SIP";
	                                    ELSIF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_SBY";
	                                    ELSIF NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Disponible THEN
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_OCU";
	                                    END_IF;
	                                    
	                                    #PRO.Error.Sistema[1] := TRUE;
	                                    #PRO.Estado.CodEstado := #PAUSANDO;
	                                    GOTO FIN_ESTADOS;
	                                    
	                                ELSE
	                                    
	                                    //  Si estan disponible las capturamos
	                                    #t_EntidadesCargadas := TRUE;
	                                    
	                                    //  Captura de las entidades
	                                    FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	                                        
	                                        IF #PRO.Entidad[#for_i].ID <> 0 AND NOT #PRO.Entidad[#for_i].Tipo THEN
	                                            // =============================================================================
	                                            //  Asignamos entidad al proceso
	                                            "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion := #PRO.ID;
	                                            "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                                    TipoProceso := #PRO.TipoProceso,
	                                                                    CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                                    TipoError => #t_TipoError,
	                                                                    DispNumero => #t_DispNumero);
	                                            
	                                            //  Marcar como capturada
	                                            IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion = #PRO.ID
	                                                AND
	                                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Capturada
	                                            THEN
	                                                #PRO.Entidad[#for_i].EstadoCapturada := TRUE;
	                                            ELSE
	                                                #PRO.Entidad[#for_i].EstadoCapturada := FALSE;
	                                                #t_EntidadesCargadas := FALSE;
	                                                EXIT;
	                                            END_IF;
	                                            
	                                        END_IF;
	                                        
	                                    END_FOR;
	                                    
	                                    
	                                    //  Comprobacion de entidades capturadas en el arranque
	                                    //  Si no estan todas capturadas ponemos error [2] y pausamos
	                                    IF #t_EntidadesCargadas THEN
	                                        #PRO.Aux.EntidadesCargadas := TRUE;
	                                        #PRO.Aux.SecuenciaArranque := #ARRANQUE_OK;
	                                    ELSE
	                                        
	                                        FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	                                            
	                                            //  Si esta decladara la entidad
	                                            IF #PRO.Entidad[#for_i].ID <> 0 AND NOT #PRO.Entidad[#for_i].Tipo THEN
	                                                
	                                                //  Asignamos entidad al proceso
	                                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion := 0;
	                                                "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                                        TipoProceso := #PRO.TipoProceso,
	                                                                        CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                                        TipoError => #t_TipoError,
	                                                                        DispNumero => #t_DispNumero);
	                                            END_IF;
	                                            
	                                        END_FOR;
	                                        
	                                        #PRO.Aux.EntidadesDisponibles := FALSE;
	                                        #PRO.Error.Codigo := "TRZ_SYS_PRO_ERR_ENT_ARRANQUE";
	                                        #PRO.Error.Sistema[2] := TRUE;
	                                        #PRO.Estado.CodEstado := #PAUSANDO;
	                                        GOTO FIN_ESTADOS;
	                                        
	                                    END_IF;
	                                    
	                                END_IF;
	                                
	                            END_REGION COMPROBACION_ENTIDADES
	                            
	                        #ARRANQUE_OK:
	                            //  ==========================================================================================================
	                            REGION ARRANQUE_OK
	                                
	                                //  Con arranque Ok, vamos a estado en marcha
	                                #PRO.Estado.CodEstado := #EN_MARCHA;
	                                #PRO.Aux.ProArrancadoOK := TRUE;
	                                GOTO FIN_ESTADOS;
	                                
	                            END_REGION ARRANQUE_OK
	                            
	                        ELSE
	                            
	                            #PRO.Estado.CodEstado := #FINALIZANDO;
	                            
	                    END_CASE;
	                    
	                END_REGION SECUENCIA_ARRANQUE
	                
	            END_REGION ARRANCANDO
	            
	        #EN_MARCHA:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado en marcha del proceso.
	            //  En el, se gestiona los saltos de estado de:
	            //      EN MARCHA ---> #PAUSANDO (por orden de operador o por orden de PLC)
	            //      EN MARCHA ---> PAUSANDO POR ERROR (en caso de error)
	            //      EN MARCHA ---> #FINALIZANDO (por orden de siguiente etapa a FIN PROCESO)
	            REGION EN_MARCHA
	                
	                //  ==========================================================================================================
	                REGION EN_MARCHA_A_PAUSANDO
	                    
	                    //  Con orden de pausa o boton pausar nos vamos a estado pausando
	                    IF #PRO.Ordenes.Pausa OR #PRO.Pulsadores.Pausa.Plc THEN
	                        #PRO.Estado.CodEstado := #PAUSANDO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION EN_MARCHA_A_PAUSANDO
	                
	                
	                //  ==========================================================================================================
	                REGION EN_MARCHA_A_PAUSANDO_POR_ERROR
	                    
	                    //  Con algun error y si tenemos la habilitacion nos vamos a pausando
	                    IF #HabilitacionErrores AND #PRO.Estado.AlgunError THEN
	                        #PRO.Estado.CodEstado := #PAUSANDO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION EN_MARCHA_A_PAUSANDO_POR_ERROR
	                
	                
	                //  ==========================================================================================================
	                REGION EN_MARCHA_A_FINALIZANDO
	                    
	                    IF #PRO.EtapaActual = "FIN_PROCESO" THEN
	                        #PRO.Estado.CodEstado := #FINALIZANDO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION EN_MARCHA_A_FINALIZANDO
	                
	            END_REGION EN_MARCHA
	            
	            
	        #PAUSANDO:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado pausando del proceso.
	            //  En el, se gestiona los saltos de estado de PAUSANDO ---> #PAUSADO.
	            REGION PAUSANDO
	                
	                //  ==========================================================================================================
	                REGION PAUSANDO_A_PAUSADO
	                    
	                    //  Con proceso arrancado OK
	                    IF #PRO.Aux.ProArrancadoOK THEN
	                        
	                        //  Esperamos a que el tiempo de pausa se cumpla
	                        IF #PRO.BitMarcha.SecParoCompletada THEN
	                            #PRO.Estado.CodEstado := #PAUSADO;
	                            GOTO FIN_ESTADOS;
	                        END_IF;
	                        
	                    ELSE
	                        #PRO.Estado.CodEstado := #PAUSADO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION PAUSANDO_A_PAUSADO
	                
	            END_REGION PAUSANDO
	            
	            
	        #PAUSADO:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado pausado del proceso.
	            //  En el, se gestiona los saltos de estado de:
	            //      PAUSADO ---> EN ERROR (en caso de error)
	            //      PAUSADO ---> #REANUDANDO (en caso de no haber error y con orden de operador o PLC) PAUSADO ---> #FINALIZANDO (por orden de operador o PLC)
	            REGION PAUSADO
	                
	                //  ==========================================================================================================
	                REGION PAUSADO_A_EN_ERROR
	                    
	                    // Si hay algun error, vamos a etapa EN ERROR
	                    IF #PRO.Estado.AlgunError THEN
	                        #PRO.Estado.CodEstado := #EN_ERROR;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION PAUSADO_A_EN_ERROR
	                
	                
	                //  ==========================================================================================================
	                REGION PAUSADO_A_REANUDANDO
	                    
	                    // Con orden de reanudar o pulsador reanudar nos vamos a estado reanudando
	                    IF NOT #PRO.Estado.AlgunError
	                        AND
	                        (#PRO.Ordenes.Reanudar OR #PRO.Pulsadores.Reanudar.Plc)
	                    THEN
	                        #PRO.Estado.CodEstado := #REANUDANDO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION PAUSADO_A_REANUDANDO
	                
	                
	                //  ==========================================================================================================
	                REGION PAUSADO_A_FINALIZANDO
	                    
	                    // Orden finalizar
	                    IF #PRO.Ordenes.Paro OR #PRO.Pulsadores.Paro.Plc
	                    THEN
	                        #PRO.Aux.ParoOperador := TRUE;
	                        #PRO.Estado.CodEstado := #FINALIZANDO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                END_REGION PAUSADO_A_FINALIZANDO
	                
	            END_REGION PAUSADO            
	            
	            
	        #REANUDANDO:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado reanudando del proceso.
	            //  En el, se gestiona los saltos de estado de:
	            //      En caso de arranque OK:
	            //          REANUDANDO ---> EN MARCHA
	            //          REANUDANDO ---> EN ERROR
	            //      En caso de arranque NO OK:
	            //          REANUDANDO ---> ARRANCANDO (sin errores y con secuencia de marha completada)
	            //          REANUDANDO ---> EN ERROR (en caso de error y con secuencia de marha completada)
	            REGION REANUDANDO
	                
	                IF #PRO.Aux.ProArrancadoOK THEN
	                    
	                    //  Esperamos a que el tiempo de reanudar se cumpla
	                    IF #PRO.BitMarcha.SecMarchaCompletada THEN
	                        
	                        //  ==========================================================================================================
	                        REGION REANUDANDO_A_EN_MARCHA
	                            
	                            IF NOT #PRO.Estado.AlgunError AND #PRO.Aux.ProArrancadoOK THEN
	                                #PRO.Estado.CodEstado := #EN_MARCHA;
	                                GOTO FIN_ESTADOS;
	                            END_IF;
	                            
	                        END_REGION REANUDANDO_A_EN_MARCHA
	                        
	                    ELSE
	                        //  ==========================================================================================================
	                        //  Si no se ha cumplido el tiempo de reanudar, miramos si salta algun error para ir a pausando
	                        REGION REANUDANDO_A_EN_ERROR
	                            
	                            IF #PRO.Estado.AlgunError THEN
	                                #PRO.Estado.CodEstado := #EN_ERROR;
	                                GOTO FIN_ESTADOS;
	                            END_IF;
	                            
	                        END_REGION REANUDANDO_A_EN_ERROR
	                        
	                    END_IF;
	                    
	                ELSE
	                    
	                    //  ==========================================================================================================
	                    REGION REANUDANDO_A_ARRANCANDO
	                        
	                        IF NOT #PRO.Estado.AlgunError AND NOT #PRO.Aux.ProArrancadoOK THEN
	                            #PRO.Estado.CodEstado := #ARRANCANDO;
	                            GOTO FIN_ESTADOS;
	                        END_IF;
	                        
	                    END_REGION REANUDANDO_A_ARRANCANDO
	                    
	                    
	                    //  ==========================================================================================================
	                    REGION REANUDANDO_A_EN_ERROR
	                        
	                        IF #PRO.Estado.AlgunError THEN
	                            #PRO.Estado.CodEstado := #EN_ERROR;
	                            GOTO FIN_ESTADOS;
	                        END_IF;
	                        
	                    END_REGION REANUDANDO_A_EN_ERROR
	                    
	                END_IF;
	                
	            END_REGION REANUDANDO
	            
	            
	        #FINALIZANDO:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado finalizando del proceso.
	            //  En el, se gestiona la liberacion de las entidades capturadas por el proceso.
	            //  Tambien se gestiona los saltos de estado de FINALIZANDO ---> #FINALIZADO.
	            REGION FINALIZANDO
	                
	                #PRO.Aux.ProFinalizadoOK := TRUE;
	                
	                //  ==========================================================================================================
	                REGION LIBERAR_ENTIDADES
	                    
	                    FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	                        
	                        //  Si tenemos entidad declara en proceso
	                        IF #PRO.Entidad[#for_i].ID <> 0 THEN
	                            
	                            IF #PRO.Entidad[#for_i].EstadoCapturada OR "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion = #PRO.ID THEN
	                                
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion := 0;
	                                
	                                IF #PRO.TipoProceso = 1 THEN    // Produccion
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := FALSE;
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := FALSE;
	                                ELSIF #PRO.TipoProceso = 2 THEN     // CIP 
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := NOT #PRO.Aux.ParoOperador;
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := FALSE;
	                                ELSIF #PRO.TipoProceso = 3 THEN     // SIP 
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := NOT #PRO.Aux.ParoOperador;
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                    "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := NOT #PRO.Aux.ParoOperador;
	                                ELSIF #PRO.TipoProceso = 4 THEN     // STANDBY
	                                    ;   //  No se gestiona en modo standby. Se gestiona libremente.
	                                END_IF;
	                                
	                                //  Reset estados produccion, CIP, SIP.
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby := FALSE;
	                                "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                        TipoProceso := #PRO.TipoProceso,
	                                                        CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                        TipoError => #t_TipoError,
	                                                        DispNumero => #t_DispNumero);
	                                
	                                #PRO.Entidad[#for_i].EstadoCapturada := FALSE;
	                                
	                            END_IF;
	                            
	                        END_IF;
	                        
	                        IF #PRO.Entidad[#for_i].EstadoCapturada THEN
	                            #PRO.Aux.ProFinalizadoOK := FALSE;
	                        END_IF;
	                        
	                    END_FOR;
	                    
	                END_REGION LIBERAR_ENTIDADES
	                
	                
	                //  ==========================================================================================================
	                REGION FINALIZANDO_A_FINALIZADO
	                    
	                    IF #PRO.Aux.ProFinalizadoOK THEN
	                        #PRO.Estado.CodEstado := #FINALIZADO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION FINALIZANDO_A_FINALIZADO
	                
	            END_REGION FINALIZANDO
	            
	            
	            
	        #EN_ERROR:
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado en error
	            //  En el, se gestiona los saltos de estado de:
	            //      EN ERROR ---> PAUSADO
	            //      EN ERROR ---> FINALIZADO
	            REGION EN_ERROR
	                
	                //  ==========================================================================================================
	                REGION EN_ERROR_A_PAUSADO
	                    
	                    // Con orden de marcha y no hay error, Vamos a etapa REANUDANDO
	                    IF NOT #PRO.Estado.AlgunError THEN
	                        #PRO.Error.Codigo := 0;
	                        #PRO.Estado.CodEstado := #PAUSADO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION EN_ERROR_A_PAUSADO
	                
	                
	                //  ==========================================================================================================
	                REGION EN_ERROR_A_FINALIZANDO
	                    
	                    IF #PRO.Ordenes.Paro OR #PRO.Pulsadores.Paro.Plc THEN
	                        #PRO.Estado.CodEstado := #FINALIZANDO;
	                        GOTO FIN_ESTADOS;
	                    END_IF;
	                    
	                END_REGION EN_ERROR_A_FINALIZANDO
	                
	            END_REGION EN_ERROR
	            
	        ELSE
	            //  ==========================================================================================================
	            //  Este bloque se encarga de gestionar el estado desconocido
	            //  En el, se gestiona los saltos de estado de:
	            //      DESCONOCIDO ---> PAUSADO
	            REGION ESTADO_DESCONOCIDO
	                
	                #PRO.Estado.CodEstado := #PAUSADO;
	                GOTO FIN_ESTADOS;
	                
	            END_REGION ESTADO_DESCONOCIDO
	            
	    END_CASE;
	    
	END_REGION MAQUINA_DE_ESTADOS
	FIN_ESTADOS:
	
	
	//  ==========================================================================================================
	REGION ENTIDADES
	    
	    // Inicializamos bandera de error para este ciclo
	    #t_ErrorYaRegistrado := FALSE;
	    
	    //  ==========================================================================================================
	    REGION GESTION_DISPONIBILIDAD_Y_ESTADOS
	        
	        IF NOT #PRO.Estado.Finalizado THEN
	            
	            //  Comprobacion de entidades declaradas en el proceso
	            FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	                IF #PRO.Entidad[#for_i].ID <> 0 THEN
	                    
	                    //  Actualizamos el estado de las entidades declaradas en el proceso
	                    #PRO.Entidad[#for_i].EstadoDisponible := "FC4_ZC_DISPONIBILIDAD_ENTIDAD"(#PRO.Entidad[#for_i].ID);
	                    
	                    //  Estados y errores
	                    IF NOT #PRO.Estado.Arrancando THEN
	                        
	                        //  La entidad la tiene capturada el proceso actual
	                        IF #PRO.Entidad[#for_i].EstadoCapturada THEN
	                            
	                            //  Actualizamos el estado de la entidad
	                            "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                    TipoProceso := #PRO.TipoProceso,
	                                                    CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                    TipoError => #t_TipoError,
	                                                    DispNumero => #t_DispNumero);
	                            
	                            
	                            IF #PRO.TipoProceso = 1 THEN    // Produccion
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion := NOT #PRO.Aux.ProFinalizadoOK;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := FALSE;
	                                
	                            ELSIF #PRO.TipoProceso = 2 THEN     // CIP
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP := NOT #PRO.Aux.ProFinalizadoOK;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := NOT #PRO.Aux.ParoOperador;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := FALSE;
	                                
	                            ELSIF #PRO.TipoProceso = 3 THEN     // SIP
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP := TRUE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia AND NOT #PRO.Aux.ParoOperador;
	                                
	                            ELSIF #PRO.TipoProceso = 4 THEN     // STANDBY
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby := TRUE;
	                                
	                                // No se gestionan los estados en standby, se mantienen con su ultimo estado
	                                
	                            END_IF;
	                            
	                            //  Asignacion de producto, agua, vacia
	                            IF #PRO.Entidad[#for_i].OrdenConProducto THEN
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.ConProducto := TRUE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.ConAgua := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Vacia := FALSE;
	                            END_IF;
	                            IF #PRO.Entidad[#for_i].OrdenConAgua THEN
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.ConProducto := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.ConAgua := TRUE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Vacia := FALSE;
	                            END_IF;
	                            IF #PRO.Entidad[#for_i].OrdenVacia THEN
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.ConProducto := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.ConAgua := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Vacia := TRUE;
	                            END_IF;
	                            
	                            
	                            // Comprobacion de errores, solo revisamos el primer error que encontremos.
	                            IF #HabilitacionErroresDispositivos AND NOT #t_ErrorYaRegistrado THEN
	                                
	                                IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Alarma.Dispositivo THEN
	                                    
	                                    #PRO.Error.Sistema[3] := TRUE;
	                                    #PRO.Error.Codigo := -3;
	                                    #t_ErrorYaRegistrado := TRUE; // Bloqueamos futuros errores en este ciclo
	                                    
	                                END_IF;
	                                
	                                IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Alarma.Manual THEN
	                                    
	                                    #PRO.Error.Sistema[3] := TRUE;
	                                    #PRO.Error.Codigo := -4;
	                                    #t_ErrorYaRegistrado := TRUE; // Bloqueamos futuros errores en este ciclo
	                                    
	                                END_IF;
	                                
	                            END_IF;
	                            
	                        END_IF;
	                        
	                    END_IF;
	                    
	                END_IF;
	                
	            END_FOR;
	            
	        END_IF;
	        
	    END_REGION GESTION_DISPONIBILIDAD_Y_ESTADOS
	    
	    
	    //  ==========================================================================================================
	    REGION CAPTURAR_LIBERAR_ENTIDADES
	        
	        IF (NOT #PRO.Estado.Finalizado
	            AND
	            NOT #PRO.Estado.Pausando
	            AND
	            NOT #PRO.Estado.Reanudando
	            AND
	            NOT #PRO.Estado.Arrancando)
	            OR #PRO.Flanco.F_Finalizado
	        THEN
	            
	            FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	                
	                //  Comprobar si esta declarada en el proceso
	                IF #PRO.Entidad[#for_i].ID <> 0 THEN
	                    
	                    //  ==========================================================================================================
	                    REGION LIBERAR_ENTIDAD
	                        
	                        //  Liberar Entidad
	                        IF #PRO.Entidad[#for_i].EstadoCapturada
	                            AND
	                            (#PRO.Entidad[#for_i].OrdenLiberar OR #PRO.Flanco.F_Finalizado)
	                        THEN
	                            
	                            "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion := 0;
	                            
	                            IF #PRO.TipoProceso = 1 THEN    // Produccion
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := FALSE;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := FALSE;
	                            ELSIF #PRO.TipoProceso = 2 THEN     // CIP 
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia := NOT #PRO.Aux.ParoOperador;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Sucia := NOT "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia;
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := FALSE;
	                            ELSIF #PRO.TipoProceso = 3 THEN     // SIP 
	                                // Los estados de limpia y sucio no se gestionan en esterilizacion, se mantienen con su ultimo estado.
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Esterilizada := "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Limpia AND NOT #PRO.Aux.ParoOperador;
	                            ELSIF #PRO.TipoProceso = 4 THEN     // STANDBY 
	                                // No se gestionan los estados en standby, se mantienen con su ultimo estado
	                                ;
	                            END_IF;
	                            
	                            //  Reset estados produccion, CIP, SIP, Standby
	                            "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnProduccion := FALSE;
	                            "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnCIP := FALSE;
	                            "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnSIP := FALSE;
	                            "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.EnStandby := FALSE;
	                            
	                            "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                    TipoProceso := #PRO.TipoProceso,
	                                                    CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                    TipoError => #t_TipoError,
	                                                    DispNumero => #t_DispNumero);
	                            
	                            IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Disponible THEN
	                                #PRO.Entidad[#for_i].EstadoCapturada := FALSE;
	                                #PRO.Entidad[#for_i].ID := 0;
	                            END_IF;
	                            
	                        END_IF;
	                        
	                    END_REGION LIBERAR_ENTIDAD
	                    
	                    
	                    //  ==========================================================================================================
	                    REGION CAPTURAR_ENTIDAD
	                        
	                        // Capturar Entidad
	                        IF NOT #PRO.Entidad[#for_i].EstadoCapturada AND #PRO.Entidad[#for_i].OrdenCapturar THEN
	                            "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                    TipoProceso := #PRO.TipoProceso,
	                                                    CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                    TipoError => #t_TipoError,
	                                                    DispNumero => #t_DispNumero);
	                            
	                            IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Disponible THEN
	                                
	                                //  Asignamos la entidad al proceso
	                                "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion := #PRO.ID;
	                                
	                            END_IF;
	                            
	                            "FC6_ZC_ESTADO_ENTIDAD"(Entidad := #PRO.Entidad[#for_i].ID,
	                                                    TipoProceso := #PRO.TipoProceso,
	                                                    CodigoProducto := #PRO.Entidad[#for_i].Producto,
	                                                    TipoError => #t_TipoError,
	                                                    DispNumero => #t_DispNumero);
	                            
	                            //  Si la entidad ha sido capturada correctamente por el proceso, la marcamos como capturada
	                            IF "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Asignacion = #PRO.ID AND "DB6_ENTIDAD".ENT[#PRO.Entidad[#for_i].ID].Estado.Capturada THEN
	                                #PRO.Entidad[#for_i].EstadoCapturada := TRUE;
	                            END_IF;
	                            
	                        END_IF;
	                        
	                    END_REGION CAPTURAR_ENTIDAD
	                    
	                END_IF;
	                
	            END_FOR;
	            
	        END_IF;
	        
	    END_REGION CAPTURAR_LIBERAR_ENTIDADES    
	    
	    
	END_REGION
	
	
	//  ==========================================================================================================
	REGION ERRORES
	    
	    //  ==========================================================================================================
	    REGION ALGUN_ERROR
	        
	        //  Algun ERROR de proceso
	        IF #HabilitacionErrores AND NOT #PRO.Estado.Finalizado THEN
	            FOR #for_i := 1 TO 8 DO
	                IF #PRO.Error.Sistema[#for_i] OR #PRO.Error.Usuario[#for_i] THEN
	                    #PRO.Estado.AlgunError := TRUE;
	                END_IF;
	            END_FOR;
	        END_IF;
	        
	    END_REGION ALGUN_ERROR
	    
	    //  ==========================================================================================================
	    REGION RECONOCER_ERRORES
	        
	        //  Reconocer errores
	        IF (#PRO.Estado.EnError AND (#PRO.Pulsadores.ResetErrores.Plc OR #PRO.Ordenes.ResetErrores))
	            OR
	            #PRO.Estado.Finalizado
	        THEN
	            FOR #for_i := 1 TO 8 DO
	                #PRO.Error.Usuario[#for_i] := #PRO.Error.Sistema[#for_i] := #PRO.Estado.AlgunError := FALSE;
	            END_FOR;
	        END_IF;
	        
	    END_REGION RECONOCER_ERRORES
	    
	END_REGION ERRORES
	
	
	//  ==========================================================================================================
	REGION AVISOS
	    
	    //  Proceso enclavado
	    #PRO.Aviso.Sistema[1] := FALSE;
	    
	    IF #PRO.Estado.Finalizado THEN
	        
	        IF #PRO.Estado.Enclavado THEN
	            #PRO.Aviso.Sistema[1] := TRUE;
	            #PRO.Aviso.Codigo := -2;
	        END_IF;
	        
	    END_IF;
	    
	    //  Paro por operador
	    IF #PRO.Aviso.Sistema[2] THEN
	        #PRO.Aviso.Codigo := -1;
	    END_IF;
	    
	    //  Algun aviso
	    #PRO.Estado.AlgunAviso := FALSE;
	    
	    IF #PRO.VentanaAviso.Mostrar THEN
	        #PRO.Estado.AlgunAviso := TRUE;
	    END_IF;
	    
	    FOR #for_i := 1 TO 8 DO
	        
	        IF #PRO.Aviso.Sistema[#for_i] OR #PRO.Aviso.Usuario[#for_i] THEN
	            #PRO.Estado.AlgunAviso := TRUE;
	        END_IF;
	        
	    END_FOR;
	    
	    //  Limpiamos los textos de avisos cuando no los hay
	    IF NOT #PRO.Estado.AlgunAviso THEN
	        #PRO.Aviso.Codigo := 0;
	    END_IF;
	    
	END_REGION AVISOS
	
	
	//  ==========================================================================================================
	REGION VENTANA_DE_AVISOS
	    
	    IF NOT #PRO.Estado.EnMarcha THEN
	        #PRO.VentanaAviso.Mostrar := FALSE;
	    END_IF;
	    
	    //  Gestion de ventana de avisos
	    IF NOT #PRO.VentanaAviso.Mostrar THEN
	        #PRO.VentanaAviso.Tipo := 0;
	        #PRO.VentanaAviso.CodigoTexto1 := 0;
	        #PRO.VentanaAviso.CodigoTexto2 := 0;
	        #PRO.VentanaAviso.CodigoTextoAceptar := 0;
	        #PRO.VentanaAviso.CodigoTextoCancelar := 0;
	    ELSE
	        
	        CASE #PRO.VentanaAviso.Tipo OF
	            0:  //  0 = Aceptar/Cancelar
	                #PRO.VentanaAviso.Aceptar.Permiso := TRUE;
	                #PRO.VentanaAviso.Cancelar.Permiso := TRUE;
	            1:  //  1 = Solo Aceptar
	                #PRO.VentanaAviso.Aceptar.Permiso := TRUE;
	                #PRO.VentanaAviso.Cancelar.Permiso := FALSE;
	            2:  // 2 = Solo Cancelar    
	                #PRO.VentanaAviso.Aceptar.Permiso := FALSE;
	                #PRO.VentanaAviso.Cancelar.Permiso := TRUE;
	        END_CASE;
	        
	    END_IF;
	    
	END_REGION VENTANA_DE_AVISOS
	
	
	//  ==========================================================================================================
	REGION CAMBIO_ETAPA
	    
	    //  Permiso boton salto de etapa
	    #PRO.Pulsadores.SaltoEtapa.Permiso := #PRO.SaltoEtapa.CambioPosible AND #PRO.SaltoEtapa.NuevaEtapa <> 0;
	    
	    //  Cambio de etapa desde HMI
	    IF #PRO.SaltoEtapa.NuevaEtapa <> 0 THEN
	        
	        //  Forzamos campo de etapa
	        IF #PRO.SaltoEtapa.CambioPosible AND
	            #PRO.Pulsadores.SaltoEtapa.Plc
	        THEN
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                    Registrar := 1,
	                                    Categoria := "TRZ_CAT_6_PRO_SAL_ETA",
	                                    User := 'Sistema',
	                                    CodInt_1 := #PRO.ID,
	                                    CodInt_2 := "TRZ_SYS_PRO_SAL_ETA_ACT",
	                                    CodInt_3 := "TRZ_SYS_PRO_SAL_ETA_NUE",
	                                    CodInt_4 := #PRO.EtapaActual,
	                                    CodInt_5 := #PRO.SaltoEtapa.NuevaEtapa,
	                                    CodReal_1 := 0.0,
	                                    CodReal_2 := 0.0);
	            #PRO.EtapaSiguiente := #PRO.SaltoEtapa.NuevaEtapa;
	            #PRO.SaltoEtapa.NuevaEtapa := 0;
	        END_IF;
	        
	    END_IF;
	    
	    //  Cambio de etapa
	    IF #PRO.EtapaSiguiente <> 0 THEN
	        
	        #PRO.EtapaActual := #PRO.EtapaSiguiente;
	        #PRO.EtapaSiguiente := 0;
	        #PRO.Ordenes.SaltarEtapa := FALSE;
	        #PRO.TiempoEtapa.Actual := 0;
	        #PRO.TiempoEtapa.Cumplido := FALSE;
	        #PRO.TiempoEtapa.Activar := FALSE;
	        #PRO.LitrosEtapa.Actual := 0;
	        #PRO.LitrosEtapa.Cumplido := FALSE;
	        #PRO.LitrosEtapa.Activar := FALSE;
	        #PRO.TON[1].IN :=
	        #PRO.TON[2].IN :=
	        #PRO.TON[1].Q :=
	        #PRO.TON[2].Q := FALSE;
	        
	    END_IF;
	    
	    //  Activamos marca de cambio posible para su gestion en el proceso
	    #PRO.SaltoEtapa.CambioPosible := TRUE;
	    
	END_REGION CAMBIO_ETAPA
	
	
	//  ==========================================================================================================
	REGION TIEMPO_ETAPA
	    
	    //  Proceso en estado parado
	    IF #PRO.Estado.Finalizado THEN
	        #PRO.TiempoEtapa.Actual := 0;
	        #PRO.TiempoEtapa.Activar := FALSE;
	        #PRO.TiempoEtapa.Cumplido := FALSE;
	    END_IF;
	    
	    //  Salto de etapa
	    IF #PRO.Flanco.F_CambioEtapa THEN
	        #PRO.TiempoEtapa.Activar := FALSE;
	        #PRO.TiempoEtapa.Cumplido := FALSE;
	        #PRO.TiempoEtapa.Actual := 0;
	    END_IF;
	    
	    //  Temporizador activo
	    IF #PRO.Estado.EnMarcha
	        AND
	        #PRO.TiempoEtapa.Activar
	    THEN
	        
	        IF #Pulso1Seg
	            AND
	            (#PRO.TiempoEtapa.Actual < #PRO.TiempoEtapa.SP)
	        THEN
	            #PRO.TiempoEtapa.Actual += 1;
	        END_IF;
	        
	        //  Reiniciar tiempo etapa cumplido para esperar condicion
	        #PRO.TiempoEtapa.Cumplido := FALSE;
	        
	        //  Tiempo etapa cumplido 
	        IF #PRO.TiempoEtapa.Actual >= #PRO.TiempoEtapa.SP AND #PRO.TiempoEtapa.Activar THEN
	            #PRO.TiempoEtapa.Cumplido := TRUE;
	        END_IF;
	        
	        //  Tiempo restante
	        #PRO.TiempoEtapa.Restante := #PRO.TiempoEtapa.SP - #PRO.TiempoEtapa.Actual;
	        
	    END_IF;
	    
	    //  Reiniciar tiempo etapa
	    IF #PRO.TiempoEtapa.Reset THEN
	        #PRO.TiempoEtapa.Actual := 0;
	        #PRO.TiempoEtapa.Cumplido := FALSE;
	        #PRO.TiempoEtapa.Reset := FALSE;
	    END_IF;
	    
	    //  Tiempo restante
	    #PRO.TiempoEtapa.Restante := #PRO.TiempoEtapa.SP - #PRO.TiempoEtapa.Actual;
	    
	    //  Reset orden para poder usar como SET en proceso
	    #PRO.TiempoEtapa.Activar := FALSE;
	    
	END_REGION TIEMPO_ETAPA
	
	
	//  ==========================================================================================================
	REGION LITROS_ETAPA
	    
	    //  Proceso en estado parado
	    IF #PRO.Estado.Finalizado THEN
	        #PRO.LitrosEtapa.Actual := 0.0;
	        #PRO.LitrosEtapa.Activar := FALSE;
	        #PRO.LitrosEtapa.Cumplido := FALSE;
	    END_IF;
	    
	    //  Salto de etapa
	    IF #PRO.Flanco.F_CambioEtapa THEN
	        #PRO.LitrosEtapa.Activar := FALSE;
	        #PRO.LitrosEtapa.Cumplido := FALSE;
	        #PRO.LitrosEtapa.Actual := 0.0;
	    END_IF;
	    
	    //  Contaje de litros activo
	    IF NOT #PRO.Estado.Finalizado
	        AND
	        #PRO.LitrosEtapa.Activar
	    THEN
	        
	        //  Reiniciar litros etapa cumplido para esperar condicion
	        #PRO.LitrosEtapa.Cumplido := FALSE;
	        
	        //  Litros etapa cumplido 
	        IF #PRO.LitrosEtapa.Actual >= #PRO.LitrosEtapa.SP THEN
	            #PRO.LitrosEtapa.Cumplido := TRUE;
	        END_IF;
	        
	    END_IF;
	    
	    //  Reiniciar tiempo etapa
	    IF #PRO.LitrosEtapa.Reset THEN
	        #PRO.LitrosEtapa.Actual := 0.0;
	        #PRO.LitrosEtapa.Cumplido := FALSE;
	        #PRO.LitrosEtapa.Reset := FALSE;
	    END_IF;
	    
	    //  Tiempo restante
	    #PRO.LitrosEtapa.Restante := #PRO.LitrosEtapa.SP - #PRO.LitrosEtapa.Actual;
	    IF #PRO.LitrosEtapa.Restante < 0.0 THEN
	        #PRO.LitrosEtapa.Restante := 0.0;
	    END_IF;
	    
	    //  Reset orden para poder usar como SET en proceso
	    #PRO.LitrosEtapa.Activar := FALSE;
	    
	END_REGION LITROS_ETAPA
	
	
	//  ==========================================================================================================
	REGION TEMPORIZADORES
	    
	    //  Gestion de reset temporizadores al cambio de etapa.
	    IF #PRO.Flanco.F_CambioEtapa THEN
	        #PRO.TON[1].IN :=
	        #PRO.TON[2].IN :=
	        #PRO.TONR.IN := FALSE;
	        #PRO.TONR.RESET := TRUE;
	    END_IF;
	    
	    //  Gestion temporizadores
	    "FC2928_ZC_TON_INDV"(Pulso1seg := #Pulso1Seg,
	                         TON := #PRO.TON[1]);
	    "FC2928_ZC_TON_INDV"(Pulso1seg := #Pulso1Seg,
	                         TON := #PRO.TON[2]);
	    "FC2930_ZC_TONR_INDV"(Pulso1seg := #Pulso1Seg,
	                          TONR := #PRO.TONR);
	    
	    //  Reset ordenes para poder usar como SET en proceso
	    #PRO.TON[1].IN :=
	    #PRO.TON[2].IN :=
	    #PRO.TONR.IN := FALSE;
	    
	    //  Gestion reset TONR. En caso de que este finalizado, se pone a 1 para que se reseteen.
	    IF #PRO.Estado.Finalizado THEN
	        #PRO.TONR.RESET := TRUE;
	    ELSE
	        #PRO.TONR.RESET := FALSE;
	    END_IF;
	    
	END_REGION TEMPORIZADORES
	
	
	//  ==========================================================================================================
	REGION INFORME
	    
	    //  INFORME (Hora de inicio)
	    IF #PRO.Flanco.F_InformeInicio THEN
	        
	        //  Datos informe inicio
	        #PRO.Informe.HoraInicio.Ano := #FechaHoraActual.YEAR;
	        #PRO.Informe.HoraInicio.Mes := #FechaHoraActual.MONTH;
	        #PRO.Informe.HoraInicio.Dia := #FechaHoraActual.DAY;
	        #PRO.Informe.HoraInicio.Hora := #FechaHoraActual.HOUR;
	        #PRO.Informe.HoraInicio.Minuto := #FechaHoraActual.MINUTE;
	        #PRO.Informe.HoraInicio.Segundo := #FechaHoraActual.SECOND;
	        
	        //  Reset informe fin
	        #PRO.Informe.HoraFin.Ano := 0;
	        #PRO.Informe.HoraFin.Mes := 0;
	        #PRO.Informe.HoraFin.Dia := 0;
	        #PRO.Informe.HoraFin.Hora := 0;
	        #PRO.Informe.HoraFin.Minuto := 0;
	        #PRO.Informe.HoraFin.Segundo := 0;
	        
	    END_IF;
	    
	    //  INFORME (Hora de fin)
	    IF #PRO.Flanco.F_InformeFin THEN
	        
	        //  Datos informe fin
	        #PRO.Informe.HoraFin.Ano := #FechaHoraActual.YEAR;
	        #PRO.Informe.HoraFin.Mes := #FechaHoraActual.MONTH;
	        #PRO.Informe.HoraFin.Dia := #FechaHoraActual.DAY;
	        #PRO.Informe.HoraFin.Hora := #FechaHoraActual.HOUR;
	        #PRO.Informe.HoraFin.Minuto := #FechaHoraActual.MINUTE;
	        #PRO.Informe.HoraFin.Segundo := #FechaHoraActual.SECOND;
	        
	    END_IF;
	    
	    //  INFORME (Tiempo en marcha)
	    "FC15025_ZC_CONTADOR_TIEMPO"(Pulso1seg := #Pulso1Seg,
	                                 Iniciar := #PRO.Estado.EnMarcha AND #PRO.Informe.OrdenMarcha,
	                                 Reset := #PRO.Informe.ResetMarcha OR #PRO.Flanco.F_InformeInicio,
	                                 Contador := #PRO.Informe.TiempoMarcha);
	    
	    //  INFORME (Tiempo Total)
	    "FC15025_ZC_CONTADOR_TIEMPO"(Pulso1seg := #Pulso1Seg,
	                                 Iniciar := NOT #PRO.Estado.Arrancando AND NOT #PRO.Estado.Finalizando AND NOT #PRO.Estado.Finalizado,
	                                 Reset := #PRO.Informe.ResetTotal OR #PRO.Flanco.F_InformeInicio,
	                                 Contador := #PRO.Informe.TiempoTotal);
	    
	END_REGION INFORME
	
	
	//  ==========================================================================================================
	REGION BIT_M
	    
	    //  Gestion de bits de marcha/paro secuencial
	    "FC15151_ZC_MARCHA_PARO_SEC"(Pulso1Seg := #Pulso1Seg,
	                                 Seguridad := #SeguridadOk,
	                                 Marcha := #PRO.Estado.Arrancando OR #PRO.Estado.EnMarcha OR #PRO.Estado.Reanudando,
	                                 MP_SEC := #PRO.BitMarcha);
	    
	END_REGION BIT_M
	
	
	//  ==========================================================================================================
	REGION RESET_ORDENES_INCONDICIONALES
	    
	    #PRO.Ordenes.Marcha :=
	    #PRO.Ordenes.Pausa :=
	    #PRO.Ordenes.Paro :=
	    #PRO.Ordenes.Reanudar :=
	    #PRO.Ordenes.ResetErrores :=
	    #PRO.Ordenes.SaltarEtapa :=
	    #PRO.Informe.OrdenIncio :=
	    #PRO.Informe.OrdenFin :=
	    #PRO.Informe.OrdenMarcha :=
	    #PRO.Informe.ResetMarcha :=
	    #PRO.Informe.ResetTotal := FALSE;
	    
	    FOR #for_i := 1 TO "N_MAX_ENTIDAD_PROCESO" DO
	        #PRO.Entidad[#for_i].OrdenCapturar :=
	        #PRO.Entidad[#for_i].OrdenLiberar :=
	        #PRO.Entidad[#for_i].OrdenVacia :=
	        #PRO.Entidad[#for_i].OrdenConAgua :=
	        #PRO.Entidad[#for_i].OrdenConProducto := FALSE;
	        #PRO.Entidad[#for_i].Producto := 0;
	    END_FOR;
	    
	    //  Reset de todos los errores de usuario para que se puedan volver a generar
	    FOR #for_i := 1 TO 8 DO
	        #PRO.Error.Usuario[#for_i] := FALSE;
	    END_FOR;
	    
	END_REGION RESET_ORDENES_INCONDICIONALES
	
	
	//  ==========================================================================================================
	REGION TRAZABILIDAD
	    
	    //  ==========================================================================================================
	    REGION TRAZA_INICIO
	        
	        IF #PRO.Flanco.F_Arrancando THEN
	            
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                    Registrar := 1,
	                                    Categoria := "TRZ_CAT_2_PRO_SYS",
	                                    User := 'Sistema',
	                                    CodInt_1 := #PRO.ID,
	                                    CodInt_2 := "TRZ_SYS_PRO_INI",
	                                    CodInt_3 := 0,
	                                    CodInt_4 := 0,
	                                    CodInt_5 := 0,
	                                    CodReal_1 := 0.0,
	                                    CodReal_2 := 0.0);
	        END_IF;
	        
	    END_REGION
	    
	    
	    //  ==========================================================================================================
	    REGION TRAZA_PAUSA
	        
	        IF #PRO.Flanco.F_Pausado THEN
	            
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                    Registrar := 1,
	                                    Categoria := "TRZ_CAT_2_PRO_SYS",
	                                    User := 'Sistema',
	                                    CodInt_1 := #PRO.ID,
	                                    CodInt_2 := "TRZ_SYS_PRO_PAU",
	                                    CodInt_3 := 0,
	                                    CodInt_4 := 0,
	                                    CodInt_5 := 0,
	                                    CodReal_1 := 0.0,
	                                    CodReal_2 := 0.0);
	            
	        END_IF;
	        
	    END_REGION
	    
	    
	    //  ==========================================================================================================
	    REGION TRAZA_REANUDAR
	        
	        IF #PRO.Flanco.F_Reanudando THEN
	            
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                    Registrar := 1,
	                                    Categoria := "TRZ_CAT_2_PRO_SYS",
	                                    User := 'Sistema',
	                                    CodInt_1 := #PRO.ID,
	                                    CodInt_2 := "TRZ_SYS_PRO_RES",
	                                    CodInt_3 := 0,
	                                    CodInt_4 := 0,
	                                    CodInt_5 := 0,
	                                    CodReal_1 := 0.0,
	                                    CodReal_2 := 0.0);
	            
	        END_IF;
	        
	    END_REGION
	    
	    
	    //  ==========================================================================================================
	    REGION TRAZA_ERROR
	        
	        IF #PRO.Flanco.F_EnError THEN
	
	                "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                        Registrar := 1,
	                                        Categoria := "TRZ_CAT_3_PRO_ERR",
	                                        User := 'Sistema',
	                                        CodInt_1 := #PRO.ID,
	                                        CodInt_2 := "TRZ_SYS_PRO_ERR",
	                                        CodInt_3 := #PRO.Error.Codigo,
	                                        CodInt_4 := 0,
	                                        CodInt_5 := 0,
	                                        CodReal_1 := 0.0,
	                                        CodReal_2 := 0.0);
	        END_IF;
	        
	    END_REGION
	    
	    
	    //  ==========================================================================================================
	    REGION TRAZA_FIN
	        
	        IF #PRO.Flanco.F_Finalizado THEN
	            IF #PRO.Aux.ParoOperador THEN
	                "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                        Registrar := 1,
	                                        Categoria := "TRZ_CAT_2_PRO_SYS",
	                                        User := 'Sistema',
	                                        CodInt_1 := #PRO.ID,
	                                        CodInt_2 := "TRZ_SYS_PRO_FIN_OPE",
	                                        CodInt_3 := 0,
	                                        CodInt_4 := 0,
	                                        CodInt_5 := 0,
	                                        CodReal_1 := 0.0,
	                                        CodReal_2 := 0.0);
	                //  Aviso paro operador
	                #PRO.Aviso.Sistema[2] := TRUE;
	            ELSE
	                "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                        Registrar := 1,
	                                        Categoria := "TRZ_CAT_2_PRO_SYS",
	                                        User := 'Sistema',
	                                        CodInt_1 := #PRO.ID,
	                                        CodInt_2 := "TRZ_SYS_PRO_FIN",
	                                        CodInt_3 := 0,
	                                        CodInt_4 := 0,
	                                        CodInt_5 := 0,
	                                        CodReal_1 := 0.0,
	                                        CodReal_2 := 0.0);
	            END_IF;
	        END_IF;
	        
	    END_REGION
	    
	END_REGION
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>