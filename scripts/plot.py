import csv
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

# Dados do llama-cli (prompt curto, ~19 tokens)
cli = defaultdict(lambda: {"prompt": [], "geracao": []})
with open(r"C:\llm-hardware-envelope\data\medicoes.csv", encoding="utf-8-sig") as f:
    for linha in csv.DictReader(f):
        cfg = linha["config"]
        if linha["prompt_tps"]:
            cli[cfg]["prompt"].append(float(linha["prompt_tps"]))
        if linha["geracao_tps"]:
            cli[cfg]["geracao"].append(float(linha["geracao_tps"]))

# Dados do llama-bench (pp512 / tg128)
bench = {
    "gpu_vulkan": {"prompt": 115.12, "geracao": 20.60},
    "cpu_pura":   {"prompt": 91.12,  "geracao": 9.74},
}

configs = ["gpu_vulkan", "cpu_pura"]
rotulos = {"gpu_vulkan": "RX 580 (Vulkan)", "cpu_pura": "Xeon (CPU pura)"}

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Painel esquerdo: llama-cli (prompt curto)
prefill_cli = [statistics.median(cli[c]["prompt"]) for c in configs]
decode_cli  = [statistics.median(cli[c]["geracao"]) for c in configs]
x = range(len(configs)); w = 0.35
b1 = axes[0].bar([i - w/2 for i in x], prefill_cli, w, label="Prefill")
b2 = axes[0].bar([i + w/2 for i in x], decode_cli,  w, label="Decode")
axes[0].set_xticks(list(x)); axes[0].set_xticklabels([rotulos[c] for c in configs])
axes[0].set_ylabel("tokens/s"); axes[0].set_title("llama-cli (prompt curto, ~19 tokens)")
axes[0].bar_label(b1, fmt="%.1f"); axes[0].bar_label(b2, fmt="%.1f")
axes[0].legend(); axes[0].grid(axis="y", alpha=0.3)

# Painel direito: llama-bench (pp512 / tg128)
prefill_b = [bench[c]["prompt"] for c in configs]
decode_b  = [bench[c]["geracao"] for c in configs]
b3 = axes[1].bar([i - w/2 for i in x], prefill_b, w, label="pp512 (prefill)")
b4 = axes[1].bar([i + w/2 for i in x], decode_b,  w, label="tg128 (decode)")
axes[1].set_xticks(list(x)); axes[1].set_xticklabels([rotulos[c] for c in configs])
axes[1].set_ylabel("tokens/s"); axes[1].set_title("llama-bench (prompt de 512 tokens)")
axes[1].bar_label(b3, fmt="%.1f"); axes[1].bar_label(b4, fmt="%.1f")
axes[1].legend(); axes[1].grid(axis="y", alpha=0.3)

plt.suptitle("Mistral 7B Q4_K_M: GPU antiga vs CPU — dois instrumentos, dois regimes", fontsize=13)
plt.tight_layout()
plt.savefig(r"C:\llm-hardware-envelope\data\grafico_mistral.png", dpi=150)
print("Grafico salvo em data/grafico_mistral.png")