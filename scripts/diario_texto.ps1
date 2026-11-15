param(
    [string]$Url = "http://localhost:8080/v1/chat/completions"
)

$perguntas = @(
    @{ id = "factual";   q = "What is the capital of Australia?" },
    @{ id = "raciocinio"; q = "If I have three apples and give away one, how many do I have?" },
    @{ id = "longa";     q = "Explain in two sentences why the sky is blue." },
    @{ id = "ambigua";   q = "Tell me something interesting." },
    @{ id = "codigo";    q = "Write a Python function that reverses a string." }
)

foreach ($p in $perguntas) {
    Write-Host "`n=== $($p.id) ==="
    Write-Host "P: $($p.q)"
    $body = @{
        model = "local"
        messages = @(
            @{ role = "system"; content = "You are a helpful assistant. Answer concisely." },
            @{ role = "user"; content = $p.q }
        )
        max_tokens = 120
        temperature = 0
        cache_prompt = $true
    } | ConvertTo-Json -Depth 5
    $inicio = Get-Date
    $r = Invoke-RestMethod -Uri $Url -Method Post -Body $body -ContentType "application/json"
    $ms = ((Get-Date) - $inicio).TotalMilliseconds
    Write-Host "R: $($r.choices[0].message.content.Trim())"
    Write-Host "($([math]::Round($ms)) ms)"
}