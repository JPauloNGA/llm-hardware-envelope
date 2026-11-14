import csv
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

# --- Dados do Mistral (CSV existente) ---
cli = defaultdict(lambda: {"prompt": [], "geracao": []})
with open(r"C:\llm-hardware-envelope\data\medicoes.csv", encoding="utf-8-sig") as f:
    for linha in csv.DictReader(f):
        cfg = linha["config"]
        if linha["prompt_tps"]:
            cli[cfg]["prompt"].append(float(linha["prompt_tps"]))
        if linha["geracao_tps"]:
            cli[cfg]["geracao"].append(float(linha["geracao_tps"]))

mistral_gpu_p = statistics.median(cli["gpu_vulkan"]["prompt"])
mistral_gpu_g = statistics.median(cli["gpu_vulkan"]["geracao"])
mistral_cpu_p = statistics.median(cli["cpu_pura"]["prompt"])
mistral_cpu_g = statistics.median(cli["cpu_pura"]["geracao"])

# --- Dados do MoE (CSV novo) ---
moe = {}
with open(r"C:\llm-hardware-envelope\data\medicoes_moe.csv", encoding="utf-8-sig") as f:
    for linha in csv.DictReader(f):
        if linha["pp512_tps"] and linha["tg128_tps"]:
            moe[linha["config"]] = {
                "pp": float(linha["pp512_tps"]),
                "tg": float(linha["tg128_tps"]),
            }

moe_hib_p = moe["hibrido"]["pp"]
moe_hib_g = moe["hibrido"]["tg"]
moe_cpu_p = moe["cpu_pura"]["pp"]
moe_cpu_g = moe["cpu_pura"]["tg"]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

w = 0.35

# Painel 1: Mistral 7B (GPU vs CPU)
x = range(2)
b1 = axes[0].bar([i - w/2 for i in x], [mistral_gpu_p, mistral_cpu_p], w, label="Prefill")
b2 = axes[0].bar([i + w/2 for i in x], [mistral_gpu_g, mistral_cpu_g], w, label="Decode")
axes[0].set_xticks(list(x)); axes[0].set_xticklabels(["RX 580", "CPU pura"])
axes[0].set_ylabel("tokens/s"); axes[0].set_title("Mistral 7B (denso, 4 GB)")
axes[0].bar_label(b1, fmt="%.1f"); axes[0].bar_label(b2, fmt="%.1f")
axes[0].legend(); axes[0].grid(axis="y", alpha=0.3)

# Painel 2: Qwen3-30B-A3B (híbrido vs CPU)
x = range(2)
b3 = axes[1].bar([i - w/2 for i in x], [moe_hib_p, moe_cpu_p], w, label="Prefill")
b4 = axes[1].bar([i + w/2 for i in x], [moe_hib_g, moe_cpu_g], w, label="Decode")
axes[1].set_xticks(list(x)); axes[1].set_xticklabels(["Híbrido", "CPU pura"])
axes[1].set_ylabel("tokens/s"); axes[1].set_title("Qwen3-30B-A3B (MoE, 17 GB)")
axes[1].bar_label(b3, fmt="%.1f"); axes[1].bar_label(b4, fmt="%.1f")
axes[1].legend(); axes[1].grid(axis="y", alpha=0.3)

# Painel 3: comparação direta no decode
modelos = ["Mistral 7B\nGPU", "Mistral 7B\nCPU", "MoE 30B\nhíbrido", "MoE 30B\nCPU"]
valores = [mistral_gpu_g, mistral_cpu_g, moe_hib_g, moe_cpu_g]
cores = ["#1f77b4", "#1f77b4", "#ff7f0e", "#ff7f0e"]
b5 = axes[2].bar(range(4), valores, color=cores)
axes[2].set_xticks(range(4)); axes[2].set_xticklabels(modelos, fontsize=9)
axes[2].set_ylabel("tokens/s (decode)"); axes[2].set_title("Decode: denso vs MoE")
axes[2].bar_label(b5, fmt="%.1f")
axes[2].grid(axis="y", alpha=0.3)

plt.suptitle("Hardware obsoleto: quando a GPU ajuda e quando a CPU vence", fontsize=13)
plt.tight_layout()
plt.savefig(r"C:\llm-hardware-envelope\data\grafico_moe.png", dpi=150)
print("Grafico salvo em data/grafico_moe.png")