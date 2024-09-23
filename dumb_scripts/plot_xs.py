import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Define the function
def f(k4, kl):
    return (0.0171438267834114 * k4**2 +
            0.0484410770554855 * k4 * kl**2 -
            0.267133807660256 * k4 * kl +
            0.094646032715672 * k4 +
            0.0401689052554822 * kl**4 -
            0.421396525745443 * kl**3 +
            1.85988687200578 * kl**2 -
            3.32655173777117 * kl +
            2.95479535736103)

# Generate the grid
kl_range = np.linspace(-20, 20, 400)
k4_range = np.linspace(-1300, 1300, 400)
KL, K4 = np.meshgrid(kl_range, k4_range)
Z = f(K4, KL)

# Plot the contour plot with log scale
plt.figure(figsize=(10, 8))
norm = mcolors.LogNorm(vmin=Z.min(), vmax=Z.max())
cp = plt.contourf(KL, K4, Z, levels=np.logspace(np.log10(Z.min()), np.log10(Z.max()), 100), norm=norm, cmap='plasma')
plt.colorbar(cp)

# Add contour lines at specified Z values
Z_vals = [1000, 2000]
contours = plt.contour(KL, K4, Z, levels=Z_vals, colors='black')
plt.clabel(contours, inline=True, fontsize=8, fmt='%1.0f')

# Add labels and title
plt.title('2D Contour Plot of f(kl, k4)')
plt.xlabel('$\kappa_3$ (kl)')
plt.ylabel('$\kappa_4$ (k4)')
plt.ylim([-1300, 1300])
plt.xlim([-20, 20])

# Save the figure as a PNG image
plt.savefig('test.pdf')

# Show the plot
plt.show()