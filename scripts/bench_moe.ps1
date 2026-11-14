# bench_moe.ps1 - roda llama-bench em tres configuracoes para o MoE
param(
    [string]$Model = "C:\models\Qwen3-30B-A3B-Q4_K_M.gguf",
    [string]$LlamaBench = "C:\llama.cpp\build\bin\Release\llama-bench.exe",
    [string]$OutCsv = "C:\llm-hardware-envelope\data\medicoes_moe.csv",
    [int]$NCpuMoe = 40,
    [int]$Repeticoes = 3
)

"config,modelo,n_cpu_moe,ngl,pp512_tps,tg128_tps" | Out-File -FilePath $OutCsv -Encoding utf8

$Configs = @(
    @{ Nome = "gpu_ingenuo"; Args = @("-ngl","99") },
    @{ Nome = "hibrido";     Args = @("-ngl","99","--n-cpu-moe",$NCpuMoe) },
    @{ Nome = "cpu_pura";    Args = @("-ngl","0") }
)

foreach ($cfg in $Configs) {
    Write-Host "Rodando $($cfg.Nome)..."
    $cliArgs = @("-m",$Model) + $cfg.Args + @("-t","28","-p","512","-n","128","-r",$Repeticoes)
    $saida = & $LlamaBench @cliArgs 2>&1 | Out-String
    Write-Host $saida

    $pp = ""; $tg = ""
    foreach ($linha in ($saida -split "`n")) {
        if ($linha -match "pp512") {
            if ($linha -match "\|\s*([\d.]+)\s*±") { $pp = $matches[1] }
        }
        if ($linha -match "tg128") {
            if ($linha -match "\|\s*([\d.]+)\s*±") { $tg = $matches[1] }
        }
    }
    $n = if ($cfg.Args -contains "--n-cpu-moe") { $NCpuMoe } else { 0 }
    $ngl = $cfg.Args[1]
    "$($cfg.Nome),$(Split-Path $Model -Leaf),$n,$ngl,$pp,$tg" | Out-File -FilePath $OutCsv -Append -Encoding utf8
}
Write-Host "Concluido. Resultados em $OutCsv"