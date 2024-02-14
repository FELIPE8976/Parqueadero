# Sistema de Parqueadero Universidad Javeriana

Este proyecto consiste en un sistema de parqueadero para la Universidad Javeriana. El sistema está diseñado para gestionar la entrada y salida de vehículos, asignar espacios de estacionamiento, y generar informes sobre la ocupación del parqueadero.

## Funcionalidades

### 1. Cargar archivo de tipos de parqueadero
Permite cargar un archivo JSON que contiene la información sobre la disposición de los espacios en el parqueadero, organizados por pisos y tipos de vehículos.

### 2. Cargar archivo de usuarios
Permite cargar un archivo JSON que contiene la información de los usuarios registrados en el sistema, incluyendo nombre, identificación, tipo de usuario, placa del vehículo, tipo de vehículo y plan de pago.

### 3. Realizar registro de usuario
Permite registrar un nuevo usuario en el sistema proporcionando su nombre, identificación, tipo de usuario, placa del vehículo, tipo de vehículo y plan de pago.

### 4. Ingresar vehículo al parqueadero
Permite ingresar un vehículo al parqueadero verificando la disponibilidad de espacios según el tipo de vehículo. Además, asigna automáticamente un espacio libre y actualiza la información del usuario.

### 5. Retirar vehículo
Permite retirar un vehículo del parqueadero, liberando el espacio ocupado y calculando el costo del estacionamiento según el tipo de usuario y plan de pago.

### 6. Generar reportes
Genera informes sobre la cantidad de vehículos según el tipo de usuario, la cantidad de vehículos según el tipo de vehículo y el porcentaje de ocupación del parqueadero.

### 7. Salir
Permite salir del sistema.

## Cómo usar el sistema

1. Ejecutar el programa e ingresar a la opción correspondiente según la operación que se desee realizar.
2. Seguir las instrucciones en la consola para ingresar la información necesaria.
3. Explorar los reportes generados para obtener información detallada sobre la ocupación del parqueadero.

## Requisitos

- Python 3.x
- Archivos JSON con la estructura adecuada para cargar información.

## Notas adicionales

- Este proyecto ha sido desarrollado como parte de un curso de programación en la Universidad Javeriana.
- La estructura de clases y funciones está diseñada para simular un sistema de parqueadero, y puede ser ampliada o mejorada según los requerimientos específicos del usuario.
