---
title: FC15026_ZC_PULSADOR
---
# FC FC15026_ZC_PULSADOR

!!! info "Información del Sistema"
    **Hardware:** PLC serie 1200/1500<br>
    **Ingeniería:** TIA Portal 18<br>
    **Versión:** 1.0<br>
    **Autor:** ABH

!!! note "Restricciones"
    Ninguna restricción operativa detectada.

## Descripción Funcional
Función encargada de la gestión temporizada de los pulsadores virtuales provenientes del sistema HMI, integrando el registro automático de cada acción en el sistema de trazabilidad.
    
    En ella se realizan las siguientes acciones:
        - Evalúa continuamente si existe una orden activa desde el HMI y si el pulsador dispone del permiso de ejecución necesario.
        - Incrementa un temporizador interno auxiliar mediante un pulso de un segundo hasta alcanzar el tiempo de retardo configurado.
        - Una vez superado el tiempo de retardo:
            - Registra el evento en el buffer invocando la función FC8_ZC_TRAZA_REGISTRO, asignando la categoría específica de pulsadores, el identificador, el usuario y la marca de tiempo.
            - Activa la señal de confirmación de orden hacia la lógica del PLC.
            - Resetea automáticamente la marca de activación del HMI.
        - Reinicia a cero el tiempo acumulado del pulsador en caso de perder el permiso de ejecución o si la orden del HMI se cancela antes de finalizar el temporizador.

!!! abstract "Dependencias Requeridas"
    **FC:** [FC8_ZC_TRAZA_REGISTRO](../Bloques de codigo/FC8_ZC_TRAZA_REGISTRO.md)
    **DB:** [UDT_ZC_PULSADOR](../Estructura de datos/UDT_ZC_PULSADOR.md)

## Interfaz de Variables
### Entradas
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulso1Seg` | `Bool` | - | `-` | Pulso 1 segundo |
| `SP_Tiempo` | `Int` | - | `-` | Tiempo retardo pulsador |
| `TrazaCategoria` | `Int` | - | `-` | Categoria de la traza |
| `TrazaIdProceso` | `Int` | - | `-` | ID Proceso para trazabilidad |
| `TrazaIdPulsador` | `Int` | - | `-` | ID Pulsador para trazabilidad |
| `Usuario` | `String` | - | `-` | Usuario actual |
| `FechaHoraActual` | `DTL` | - | `-` | Fecha y hora actual |

### Entrada/Salida
| Nombre | Tipo | Retain | Valor Defecto | Comentario |
|---|---|:---:|---|---|
| `Pulsador` | `UDT_ZC_PULSADOR` | - | `-` | Pulsador |

## Código Fuente
<details class="group rounded-xl border bg-card p-4 shadow-sm">
<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>
<div class="mt-4" markdown>

```pascal
﻿FUNCTION "FC15026_ZC_PULSADOR" : Void
TITLE = FC15026_ZC_PULSADOR
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : ABH
FAMILY : ZeusControl
VERSION : 1.0
//Funcion para gestion de pulsadores
   VAR_INPUT 
      Pulso1Seg : Bool;   // Pulso 1 segundo
      SP_Tiempo : Int;   // Tiempo retardo pulsador
      TrazaCategoria : Int;   // Categoria de la traza
      TrazaIdProceso : Int;   // ID Proceso para trazabilidad
      TrazaIdPulsador : Int;   // ID Pulsador para trazabilidad
      Usuario : String;   // Usuario actual
      FechaHoraActual {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // Fecha y hora actual
   END_VAR

   VAR_IN_OUT 
      Pulsador : "UDT_ZC_PULSADOR";   // Pulsador
   END_VAR


BEGIN
	REGION DESCRIPCION
	(*
	###### (C)Copyright ZeusControl 2025 - 2026
	
	---
	### Información del Sistema
	| Hardware Compatible | Entorno de Ingeniería |
	|---------------------|-----------------------|
	| PLC serie 1200/1500 | TIA Portal 18         |
	
	---
	> **Restricciones:** Ninguna.
	
	---
	### Descripción Funcional
	
	Función encargada de la gestión temporizada de los pulsadores virtuales provenientes del sistema HMI, integrando el registro automático de cada acción en el sistema de trazabilidad.
	
	En ella se realizan las siguientes acciones:
	    - Evalúa continuamente si existe una orden activa desde el HMI y si el pulsador dispone del permiso de ejecución necesario.
	    - Incrementa un temporizador interno auxiliar mediante un pulso de un segundo hasta alcanzar el tiempo de retardo configurado.
	    - Una vez superado el tiempo de retardo:
	        - Registra el evento en el buffer invocando la función FC8_ZC_TRAZA_REGISTRO, asignando la categoría específica de pulsadores, el identificador, el usuario y la marca de tiempo.
	        - Activa la señal de confirmación de orden hacia la lógica del PLC.
	        - Resetea automáticamente la marca de activación del HMI.
	    - Reinicia a cero el tiempo acumulado del pulsador en caso de perder el permiso de ejecución o si la orden del HMI se cancela antes de finalizar el temporizador.
	
	---
	### Dependencias Requeridas
	| Tipo | Elementos |
	|------|-----------|
	| FC   | `FC8_ZC_TRAZA_REGISTRO` |
	| FB   | - |
	| DB   | - |
	| UDT  | `UDT_ZC_PULSADOR` |
	    
	---
	### Historial de Cambios
	| Versión  | Fecha      | Técnico | Cambios |
	|----------|------------|---------|---------|
	| 01.00.00 | 14.03.2025 | (ABH) | Primera version. |
	*)
	END_REGION DESCRIPCION
	
	
	//  ==========================================================================================================
	REGION GESTION_PULSADOR
	    
	    //  Reset orden PLC
	    #Pulsador.Plc := FALSE;
	    
	    //  Con permiso y con la orden desde HMI, contamos el tiempo para activar la orden de PLC
	    IF #Pulsador.Hmi AND #Pulsador.Permiso THEN
	        
	        IF #Pulso1Seg AND #Pulsador.AuxTiempo < #SP_Tiempo THEN
	            #Pulsador.AuxTiempo += 1;
	        END_IF;
	        
	        IF #Pulsador.AuxTiempo >= #SP_Tiempo THEN
	            
	            //  Registramos la trazabilidad de la pulsacion del boton
	            "FC8_ZC_TRAZA_REGISTRO"(FechaHora := #FechaHoraActual,
	                                    Registrar := 1,
	                                    Categoria := #TrazaCategoria,
	                                    User := #Usuario,
	                                    CodInt_1 := #TrazaIdProceso,
	                                    CodInt_2 := #TrazaIdPulsador,
	                                    CodInt_3 := 0,
	                                    CodInt_4:= 0,
	                                    CodInt_5:= 0,
	                                    CodReal_1 := 0.0,
	                                    CodReal_2 := 0.0);
	            
	            //  Activacion de orden PLC y reset orden HMI
	            #Pulsador.Plc := TRUE;
	            #Pulsador.Hmi := FALSE;
	            
	        END_IF;
	        
	    END_IF;
	    
	END_REGION GESTION_PULSADOR
	
	
	//  ==========================================================================================================
	REGION RESET_DATOS
	    
	    //  Sin orden desde HMI o si no tenemos permiso, reseteamos el tiempo del pulsador
	    IF NOT #Pulsador.Hmi OR NOT #Pulsador.Permiso THEN
	        #Pulsador.AuxTiempo := 0;
	    END_IF;
	    
	END_REGION RESET_DATOS
	
	
END_FUNCTION

```

</div>
</details>
<div class="h-24"></div>