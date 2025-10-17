@echo off
title HomologadorInventoria v1.0.3-x64 - Arquitectura 64 bits
echo.
echo ================================================================
echo   HomologadorInventoria v1.0.3-x64
echo   Sistema de Gestion de Homologaciones
echo   *** COMPILACION NATIVA 64 BITS ***
echo ================================================================
echo.
echo Verificando sistema...

REM Verificar arquitectura del sistema
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo ✅ Sistema x64 detectado: %PROCESSOR_ARCHITECTURE%
) else (
    echo ❌ ERROR: Sistema no es x64
    echo    Arquitectura detectada: %PROCESSOR_ARCHITECTURE%
    echo    Se requiere sistema de 64 bits
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion x64...
echo   - Pandas: INCLUIDO
echo   - Numpy: INCLUIDO
echo   - PyQt6: INCLUIDO  
echo   - SQLite: INCLUIDO
echo   - Arquitectura: 64 bits nativa
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar aplicacion
echo Ejecutando HomologadorInventoria_x64.exe...
HomologadorInventoria_x64.exe

REM Verificar resultado
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Aplicacion ejecutada correctamente
) else (
    echo.
    echo ================================================================
    echo ❌ ERROR: Codigo de salida %ERRORLEVEL%
    echo ================================================================
    echo.
    echo Posibles soluciones:
    echo 1. Ejecutar como administrador
    echo 2. Desbloquear archivo (Propiedades ^> Desbloquear)
    echo 3. Verificar antivirus no esta bloqueando
    echo 4. Instalar Visual C++ Redistributable x64
    echo.
    pause
)
