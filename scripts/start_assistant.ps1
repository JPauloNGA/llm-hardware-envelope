# start_assistant.ps1 - sobe o servidor e espera ficar pronto
param(
    [string]$Model = "C:\models\voice\qwen2.5-0.5b-instruct-q4_k_m.gguf",
    [string]$Port = "8080"
)

$server = Start-Process -FilePath "C:\llama.cpp\build\bin\Release\llama-server.exe" `
    -ArgumentList @("-m", $Model, "-ngl", "0", "-t", "28", "-c", "2048", "-np", "1", "--port", $Port) `
    -PassThru -WindowStyle Hidden

Write-Host "Servidor iniciado (PID $($server.Id)). Aguardando..."
for ($i = 1; $i -le 60; $i++) {
    Start-Sleep -Seconds 2
    try {
        $r = Invoke-RestMethod -Uri "http://localhost:$Port/health" -TimeoutSec 2
        if ($r.status -eq "ok") { Write-Host "Pronto."; break }
    } catch {}
}