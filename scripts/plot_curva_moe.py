import csv
import matplotlib.pyplot as plt

ns, tgs, pps, status = [], [], [], []
with open(r"C:\llm-hardware-envelope\data\medicoes_curva_moe.csv", encoding="utf-8-sig") as f:
    for linha in csv.DictReader(f):
        ns.append(int(linha["n_cpu_moe"]))
        status.append(linha["status"])
        tgs.append(float(linha["tg128_tps"]) if linha["tg128_tps"] else None)
        pps.append(float(linha["pp512_tps"]) if linha["pp512_tps"] else None)

fig, ax = plt.subplots(figsize=(9, 5))

# Linha de decode (tg128) para os pontos validos
validos = [(n, t) for n, t, s in zip(ns, tgs, status) if t is not None]
if validos:
    xs, ys = zip(*validos)
    ax.plot(xs, ys, marker="o", linewidth=2, markersize=8,
            color="#ff7f0e", label="Decode (tg128)")

# Linha de prefill (pp512), eixo secundario
validos_pp = [(n, p) for n, p, s in zip(ns, pps, status) if p is not None]
if validos_pp:
    xs_p, ys_p = zip(*validos_pp)
    ax2 = ax.twinx()
    ax2.plot(xs_p, ys_p, marker="s", linewidth=2, markersize=7,
             color="#1f77b4", linestyle="--", label="Prefill (pp512)")
    ax2.set_ylabel("Prefill (tokens/s)", color="#1f77b4")
    ax2.tick_params(axis="y", labelcolor="#1f77b4")

# Marcar os pontos que deram OOM
for n, s in zip(ns, status):
    if s == "OOM":
        ax.axvline(n, color="red", linestyle=":", alpha=0.5)
        ax.text(n, 0.5, "OOM", ha="center", va="bottom",
                color="red", fontsize=10, rotation=90)

ax.set_xlabel("--n-cpu-moe (camadas de experts na CPU)")
ax.set_ylabel("Decode (tokens/s)", color="#ff7f0e")
ax.tick_params(axis="y", labelcolor="#ff7f0e")
ax.set_title("Qwen3-30B-A3B (17,28 GB): curva de offload de experts\nVRAM RX 580 = 7,3 GB livres")
ax.set_xticks(ns)
ax.grid(alpha=0.3)

# Legenda combinada
linhas1, labels1 = ax.get_legend_handles_labels()
if validos_pp:
    linhas2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(linhas1 + linhas2, labels1 + labels2, loc="lower right")
else:
    ax.legend(loc="lower right")

plt.tight_layout()
plt.savefig(r"C:\llm-hardware-envelope\data\grafico_curva_moe.png", dpi=150)
print("Grafico salvo em data/grafico_curva_moe.png")