@echo off
title HomologadorInventoria - Sistema de Gestión
echo.
echo ======================================
echo   HomologadorInventoria v1.0.0
echo   Sistema de Gestión de Homologaciones
echo ======================================
echo.
echo Iniciando aplicación...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar la aplicación
HomologadorInventoria.exe

REM Pausa si hay error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error al ejecutar la aplicación. Código: %ERRORLEVEL%
    pause
)
