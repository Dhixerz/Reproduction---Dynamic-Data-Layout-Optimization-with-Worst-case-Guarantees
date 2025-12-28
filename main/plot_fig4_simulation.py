import matplotlib.pyplot as plt
import numpy as np


n_queries = 30000
x = np.linspace(0, n_queries, n_queries)


final_static = 14000

final_mts = 9000

final_oreo = 7500

final_optimal = 5000

def generate_curve(final_value, noise_level=50):

    base = np.linspace(0, final_value, n_queries)
    
    # Add random walk noise (cumulative sum)
    np.random.seed(42)
    noise = np.random.normal(0, 1, n_queries).cumsum() * noise_level

    noise = noise - np.linspace(0, noise[-1], n_queries)
    
    return base + noise

# Generate the data arrays
y_static = generate_curve(final_static, 1)
y_mts = generate_curve(final_mts, 2)
y_oreo = generate_curve(final_oreo, 1.5)
y_optimal = generate_curve(final_optimal, 1)

fig, ax = plt.subplots(figsize=(8, 5))


ax.plot(x, y_static, label='Static', color='#90C3C9', linewidth=2)      
ax.plot(x, y_mts, label='MTS Optimal', color='#C67828', linewidth=2)     
ax.plot(x, y_oreo, label='OREO', color='#FBC05E', linewidth=2.5)  
ax.plot(x, y_optimal, label='Offline Optimal', color='#007CA3', linewidth=2)

ax.set_xlim(0, n_queries)
ax.set_ylim(0, 15000)

ax.set_xlabel('Query Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Cost', fontsize=12, fontweight='bold')


ax.text(1500, 14000, 'TPC-H', fontsize=14, fontweight='bold')

for i in range(2000, 30000, 2000):
    ax.axvline(x=i, color='grey', linestyle='-', alpha=0.3, linewidth=1)

# Legend (Placed horizontally at the top)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), 
          ncol=4, frameon=False, fontsize=11)

# Grid
ax.grid(True, linestyle='--', alpha=0.5)

# Save output
output_file = 'figure4_cumulative_simulated.png'
plt.tight_layout()
print(f"✅ Cumulative Cost Figure generated successfully!")
print(f"📁 Saved to: {output_file}")
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# plt.show()