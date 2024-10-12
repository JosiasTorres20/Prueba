# 🏢 **Sistema de Gestión Empresa**

## 🚀 **Funcionalidades Principales**

### 1. 🔐 **Inicio de Sesión**

Al iniciar el sistema desde la consola, se presentará una pantalla de inicio de sesión que solicitará **usuario** y **contraseña**.

- **Usuario por defecto**: `root`
- **Contraseña por defecto**: `root`

Estas credenciales van a estár **precargadas en la base de datos** y corresponden al **Gerente** de la empresa. Este inicio de sesión sera **necesario para acceder** a las funciones del sistema.

### 2. 👤 **Rol del Gerente**

Una vez autenticado como **Gerente**, este podra realizar lo siguiente:

- **Ver y editar perfil**: El Gerente puede **visualizar su información** de perfil y **cambiar su contraseña**.
- **Generar informes**: Basados en la información proporcionada por los empleados y jefes, los informes mostrarán:
  - **Los departamentos creados**.
  - **Los proyectos asignados** a cada departamento.
  - **El estado de los proyectos** (completados o pendientes).
  
- **Gestión de usuarios (Jefes) CRUD**:
  - **Crear usuarios** para los jefes, asignándolos a un departamento.**(CREATE)**
  - **Ver el listado de jefes** creados en el sistema.**(READ)**
  - **Modificar** la información de los jefes.(UPDATE)
  - **Eliminar** usuarios de jefes cuando sea necesario.**(DELETE)**
    

### 3. 📊 **Proyectos y Departamentos**

Este sistema permitira la **asignación de jefes a departamentos**. Cada jefe es responsable de **gestionar los proyectos** dentro de su departamento. Los informes generados por el Gerente mostrarán:

- **Los departamentos creados**.
- **Los proyectos asignados** a cada uno.
- **El estado de los proyectos** (realizados o no).

### 4. ⏱️ **Registro de Horas Trabajadas**

El sistema registrará **las horas trabajadas** de los empleados según el **tiempo que permanezcan conectados** al sistema.

### 5. 🧑💼 **Funciones del Jefe**

El jefe tiene un conjunto de funciones específicas dentro del sistema:

- **Gestion de usuarios para empleados (CRUD)**: El jefe creará los usuarios para sus empleados y los **asignará al mismo departamento** al que pertenece automaticamente. 
- **Asignación automática de empleados a proyectos**: El jefe creará proyectos y, al ingresar la **cantidad de empleados**, estos se asignarán automáticamente al proyecto.

## 📋 **Requisitos**

- **Python 3.x**
- Base de datos **MYSQl precargada** con las credenciales iniciales del usuario `root`.

use empresa;

CREATE TABLE DEPARTAMENTO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE EMPLEADO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(50),
    APELLIDO VARCHAR(50),
    TELEFONO VARCHAR(15),
    MAIL VARCHAR(100),
    SALARIO DECIMAL(10, 2),
    FECHA_INICIO DATE,
    DEPTO_ID INT,
    ES_JEFE BOOLEAN,
    ES_GERENTE BOOLEAN,
    USUARIO VARCHAR(50) UNIQUE,
    PSW VARCHAR(100),
    FOREIGN KEY (DEPTO_ID) REFERENCES DEPARTAMENTO(ID)
);

CREATE TABLE PROYECTO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(255) NOT NULL,
    DESCRIPCION VARCHAR(1000),
    FECHA_INICIO DATE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ESTADO VARCHAR(50),
    DEPARTAMENTO_ID INT,
    FOREIGN KEY (DEPARTAMENTO_ID) REFERENCES DEPARTAMENTO(ID)
);
select * from empleado;
CREATE TABLE ASIGNACION (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PROYECTO_ID INT,
    EMPLEADO_ID INT,
    FOREIGN KEY (PROYECTO_ID) REFERENCES PROYECTO(ID),
    FOREIGN KEY (EMPLEADO_ID) REFERENCES EMPLEADO(ID)
);

