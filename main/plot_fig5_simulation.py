import matplotlib.pyplot as plt
import numpy as np

alphas = np.array([10, 25, 50, 75, 80, 100, 125, 150, 175, 200, 225, 250, 275, 300])

decay_rate = 0.015
max_switches = 35  
n_switches = max_switches * np.exp(-decay_rate * (alphas - 10))
n_switches = np.round(n_switches).astype(int) # Bulatkan ke integer

reorg_costs = n_switches * alphas

min_query_cost = 4963  
max_query_cost = 14003 

switch_efficiency = n_switches / max(n_switches) 
query_costs = max_query_cost - (switch_efficiency * (max_query_cost - min_query_cost))

np.random.seed(42)
noise = np.random.normal(0, 100, len(alphas))
query_costs = query_costs + noise

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8),
                               gridspec_kw={'height_ratios': [2, 1]})

color_query = '#007CA3'   
color_reorg = '#FBC05E'  
color_switch = 'grey'

x = np.arange(len(alphas))
width = 0.65

p1 = ax1.bar(x, query_costs, width, label='Query Cost', 
             color=color_query, edgecolor='black', linewidth=0.8)
p2 = ax1.bar(x, reorg_costs, width, bottom=query_costs, label='Reorg Cost', 
             color=color_reorg, edgecolor='black', linewidth=0.8)

ax1.set_yscale('log')
ax1.set_ylabel('Total Cost (Log Scale)', fontsize=12, fontweight='bold')
ax1.set_title('Sensitivity Analysis: Impact of Reorg Cost ($\\alpha$)', fontsize=14, fontweight='bold')
ax1.set_ylim(bottom=1000, top=100000) # Atur batas biar rapi
ax1.grid(True, axis='y', which='major', linestyle='--', alpha=0.5)
ax1.legend(loc='upper left', ncol=2, frameon=False, fontsize=11)

ax2.bar(x, n_switches, width, color=color_switch, edgecolor='black', linewidth=0.8)

ax2.set_ylabel('# Switches', fontsize=12, fontweight='bold')
ax2.set_xlabel(r'Relative Cost of Reorganization ($\alpha$)', fontsize=14, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(alphas)
ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
ax2.set_ylim(0, max(n_switches) * 1.2)

plt.tight_layout()
plt.subplots_adjust(hspace=0.05)

output_filename = 'figure5_sensitivity_simulated.png'
print(f"✅ Done!")
print(f"📁 Saved to: {output_filename}")
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.show()