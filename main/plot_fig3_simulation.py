import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

groups = ['Qd-tree', 'Z-Order']
algorithms = ['Static', 'OREO', 'Greedy', 'Regret']

totals_qdtree = [36.0, 24.5, 22.0, 28.5]

totals_zorder = [45.0, 32.0, 30.5, 38.0]

q_costs = {
    'Qd-tree': np.array([36.0, 14.5, 18.0, 27.0]),
    'Z-Order': np.array([45.0, 22.0, 25.5, 36.5])
}

r_costs = {
    'Qd-tree': np.array([0.0, 10.0, 4.0, 1.5]),
    'Z-Order': np.array([0.0, 10.0, 5.0, 1.5])
}

colors = ['#C8D4D8', '#FBC05E', '#83CCD2', '#007CA3'] 
hatch_pattern = '////'

fig, ax = plt.subplots(figsize=(10, 7))

n_groups = len(groups)
n_algos = len(algorithms)
bar_width = 0.18  
index = np.arange(n_groups)

# Loop membuat bar
for i in range(n_algos):

    x_pos = index + (i * bar_width) - (bar_width * n_algos / 2) + (bar_width / 2)
    
    q_data = np.array([q_costs[g][i] for g in groups])
    r_data = np.array([r_costs[g][i] for g in groups])
    
    ax.bar(x_pos, q_data, bar_width, color=colors[i], edgecolor='black', 
           linewidth=1, label=algorithms[i])
    
    ax.bar(x_pos, r_data, bar_width, bottom=q_data, color=colors[i], 
           edgecolor='black', linewidth=1, hatch=hatch_pattern)

ax.set_ylabel('Total Time (hour)', fontsize=14, fontweight='bold')
ax.set_title('Impact of Data Structure (Simulated)', fontsize=16, fontweight='bold', y=1.12)
ax.set_xticks(index)
ax.set_xticklabels(groups, fontsize=14, fontweight='bold')
ax.tick_params(axis='x', which='both', length=0) 

ax.set_ylim(0, 55)
ax.yaxis.grid(True, linestyle='--', color='grey', alpha=0.5)
ax.set_axisbelow(True)

for i, g_name in enumerate(groups):
    group_totals = totals_qdtree if g_name == 'Qd-tree' else totals_zorder
    for j in range(n_algos):
        x_pos = i + (j * bar_width) - (bar_width * n_algos / 2) + (bar_width / 2)
        val = group_totals[j]
        ax.text(x_pos, val + 0.8, f"{val:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

legend_elements = [Patch(facecolor=colors[i], edgecolor='black', label=algorithms[i]) for i in range(n_algos)]
legend_elements.append(Patch(facecolor='white', edgecolor='white', label=' '))
legend_elements.append(Patch(facecolor='white', edgecolor='black', hatch=hatch_pattern, label='Reorg Overhead'))

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.10), 
          ncol=6, frameon=False, fontsize=11)

plt.tight_layout()
plt.subplots_adjust(top=0.85) 

output_file = 'figure3_simulation_fixed.png'
print(f"✅ Done!")
print(f"📁 Saved to: {output_file}")
plt.savefig(output_file, dpi=300, bbox_inches='tight')