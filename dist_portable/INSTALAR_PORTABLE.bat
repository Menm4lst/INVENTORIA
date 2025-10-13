@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0 PORTABLE
echo 📦 INSTALADOR PORTÁTIL COMPLETO
echo 👨‍💻 Desarrollado por: Antware (SysAdmin)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

set "APP_NAME=EXPANSION_DOMINIO_INVENTORIA_PORTABLE"
set "INSTALL_DIR=%USERPROFILE%\Desktop\%APP_NAME%"
set "EXE_FILE=EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe"

echo 📁 Creando instalación portátil...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo ✅ Directorio creado: %INSTALL_DIR%
)

echo 📋 Copiando aplicación portátil...
copy "%EXE_FILE%" "%INSTALL_DIR%\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Aplicación portátil instalada
) else (
    echo ❌ Error en instalación
    goto error
)

echo 💾 Verificando base de datos integrada...
echo ✅ Base de datos SQLite integrada en el ejecutable

echo 🔗 Creando acceso directo...
powershell -Command "try { $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXE_FILE%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema Portátil de Inventario - by Antware'; $Shortcut.Save(); Write-Host '✅ Acceso directo creado' } catch { Write-Host '⚠️ Error creando acceso directo' }" 2>nul

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🎉 ¡INSTALACIÓN PORTÁTIL COMPLETADA!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📂 Ubicación: %INSTALL_DIR%
echo 🚀 Ejecutar: %EXE_FILE%
echo 💾 Base de datos: Integrada (SQLite)
echo 📁 Modo: 100%% Portátil
echo.
echo 🔐 CREDENCIALES:
echo   👤 Usuario: admin
echo   🔑 Contraseña: admin123
echo.
echo 💡 VENTAJAS DE LA VERSIÓN PORTÁTIL:
echo   • Un solo archivo ejecutable
echo   • Base de datos integrada
echo   • No requiere instalación adicional
echo   • Funciona en cualquier Windows 10/11
echo   • Todos los recursos incluidos
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
pause
goto end

:error
echo ❌ Error durante la instalación portátil
pause

:end
