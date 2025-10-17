# 🔐 SCRIPT DE FIRMADO DE SOFTWARE - HomologadorInventoria
# Crea un certificado autofirmado y firma el ejecutable

param(
    [Parameter(Mandatory=$true)]
    [string]$ExecutablePath,
    
    [string]$CertificateName = "HomologadorInventoria Code Signing",
    [string]$CompanyName = "Tu Empresa",
    [int]$ValidDays = 365
)

Write-Host "🔐 FIRMADO DIGITAL DE SOFTWARE" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si el ejecutable existe
if (-not (Test-Path $ExecutablePath)) {
    Write-Host "❌ Error: No se encontró el ejecutable en: $ExecutablePath" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Configuración:" -ForegroundColor Yellow
Write-Host "   Ejecutable: $ExecutablePath" -ForegroundColor White
Write-Host "   Certificado: $CertificateName" -ForegroundColor White
Write-Host "   Empresa: $CompanyName" -ForegroundColor White
Write-Host "   Validez: $ValidDays días" -ForegroundColor White
Write-Host ""

try {
    # 1. Crear certificado autofirmado
    Write-Host "🔑 Creando certificado autofirmado..." -ForegroundColor Green
    
    $cert = New-SelfSignedCertificate `
        -Type CodeSigningCert `
        -Subject "CN=$CertificateName, O=$CompanyName" `
        -KeyUsage DigitalSignature `
        -FriendlyName "$CertificateName" `
        -CertStoreLocation "Cert:\CurrentUser\My" `
        -KeyLength 2048 `
        -KeyAlgorithm RSA `
        -HashAlgorithm SHA256 `
        -NotAfter (Get-Date).AddDays($ValidDays)

    Write-Host "✅ Certificado creado: $($cert.Thumbprint)" -ForegroundColor Green

    # 2. Mover certificado a store de confianza (solo para pruebas locales)
    Write-Host "📋 Moviendo certificado a store de confianza..." -ForegroundColor Yellow
    
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store(
        [System.Security.Cryptography.X509Certificates.StoreName]::TrustedPublisher,
        [System.Security.Cryptography.X509Certificates.StoreLocation]::CurrentUser
    )
    $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
    $store.Add($cert)
    $store.Close()

    # 3. Firmar el ejecutable
    Write-Host "✍️ Firmando ejecutable..." -ForegroundColor Green
    
    $signResult = Set-AuthenticodeSignature -FilePath $ExecutablePath -Certificate $cert -TimestampServer "http://timestamp.sectigo.com"
    
    if ($signResult.Status -eq "Valid") {
        Write-Host "✅ Ejecutable firmado exitosamente!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Detalles de la firma:" -ForegroundColor Cyan
        Write-Host "   Estado: $($signResult.Status)" -ForegroundColor White
        Write-Host "   Algoritmo: $($signResult.SignatureType)" -ForegroundColor White
        Write-Host "   Timestamp: $($signResult.TimeStamperCertificate.Subject)" -ForegroundColor White
        
        # Verificar la firma
        Write-Host ""
        Write-Host "🔍 Verificando firma..." -ForegroundColor Yellow
        $verify = Get-AuthenticodeSignature -FilePath $ExecutablePath
        Write-Host "   Verificación: $($verify.Status)" -ForegroundColor White
        
    } else {
        Write-Host "❌ Error al firmar: $($signResult.Status)" -ForegroundColor Red
        Write-Host "   Mensaje: $($signResult.StatusMessage)" -ForegroundColor Red
    }

} catch {
    Write-Host "❌ Error durante el proceso de firmado:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📝 NOTAS IMPORTANTES:" -ForegroundColor Yellow
Write-Host "   • Este es un certificado AUTOFIRMADO (solo para pruebas)" -ForegroundColor White
Write-Host "   • Para distribución, usa un certificado comercial" -ForegroundColor White
Write-Host "   • Los usuarios deben confiar manualmente en este certificado" -ForegroundColor White
Write-Host "   • Para producción, compra un certificado de autoridad reconocida" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Proceso completado!" -ForegroundColor Green