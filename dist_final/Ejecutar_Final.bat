@echo off
title HomologadorInventoria v1.0.2-final - Windows 11 Compatible
echo.
echo ========================================================
echo   HomologadorInventoria v1.0.2-final
echo   Sistema de Gestion de Homologaciones
echo   *** TODAS LAS DEPENDENCIAS INCLUIDAS ***
echo ========================================================
echo.
echo Iniciando aplicacion final...
echo   - Pandas: INCLUIDO
echo   - Numpy: INCLUIDO  
echo   - PyQt6: INCLUIDO
echo   - SQLite: INCLUIDO
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar Windows
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo Sistema detectado: Windows %VERSION%

REM Ejecutar la aplicacion
echo.
echo Ejecutando HomologadorInventoria...
HomologadorInventoria.exe

REM Verificar resultado
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Aplicacion cerrada correctamente.
) else (
    echo.
    echo ============================================
    echo ERROR: Codigo de salida %ERRORLEVEL%
    echo ============================================
    echo.
    echo Si persisten problemas:
    echo 1. Ejecutar como administrador
    echo 2. Desbloquear archivo (Propiedades)
    echo 3. Verificar antivirus
    echo.
    pause
)
