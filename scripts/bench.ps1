# bench.ps1 - roda 3 execucoes por configuracao e extrai tokens/s
param(
    [string]$Model = "C:\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    [string]$LlamaCli = "C:\llama.cpp\build\bin\Release\llama-cli.exe",
    [string]$OutCsv = "C:\llm-hardware-envelope\data\medicoes.csv"
)

$Prompt = "Explain in one paragraph why local LLM inference matters."
$Repeticoes = 3

$Configs = @(
    @{ Nome = "gpu_vulkan"; Args = @("-ngl","100","--device","Vulkan0") },
    @{ Nome = "cpu_pura";   Args = @("-ngl","0") }
)

"config,modelo,execucao,prompt_tps,geracao_tps,threads,ngl,contexto" | Out-File -FilePath $OutCsv -Encoding utf8

foreach ($cfg in $Configs) {
    for ($i = 1; $i -le $Repeticoes; $i++) {
        Write-Host "Rodando $($cfg.Nome) execucao $i/$Repeticoes..."
        $cliArgs = @("-m",$Model) + $cfg.Args + @("-t","28","-c","2048","-n","128","-p",$Prompt,"--no-warmup","-st")
        $saida = & $LlamaCli @cliArgs 2>&1 | Out-String

        $pt = ""; $gt = ""
        $linhaResumo = ($saida -split "`n" | Where-Object { $_ -match "Prompt:\s*[\d.]+\s*t/s" }) | Select-Object -Last 1
        if ($linhaResumo -match "Prompt:\s*([\d.]+)\s*t/s\s*\|\s*Generation:\s*([\d.]+)\s*t/s") {
            $pt = $matches[1]; $gt = $matches[2]
            Write-Host "  Prompt: $pt t/s | Generation: $gt t/s"
        } else {
            $linhaPerf = ($saida -split "`n" | Where-Object { $_ -match "eval time" }) | Select-Object -Last 1
            if ($linhaPerf -match "eval time.*?([\d.]+)\s*tokens per second") { $gt = $matches[1] }
            Write-Host "  Resumo nao encontrado. Linha perf: $linhaPerf"
        }
        "$($cfg.Nome),$(Split-Path $Model -Leaf),$i,$pt,$gt,28,$($cfg.Args[1]),2048" | Out-File -FilePath $OutCsv -Append -Encoding utf8
    }
}
Write-Host "Concluido. Resultados em $OutCsv"