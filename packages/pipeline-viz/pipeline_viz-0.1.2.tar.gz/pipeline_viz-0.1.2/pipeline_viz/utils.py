import matplotlib
from matplotlib import cm

# Add docstring to function
def get_color_map(n):
    """
    Function to get a colormap with n different colors

    Parameters:
    n: int

    Returns:
    colors: list of colors in hex format
    """
    color_norm = matplotlib.colors.Normalize(vmin=0, vmax=n-1)
    scalar_map = cm.ScalarMappable(norm=color_norm, cmap='hsv')
    return [matplotlib.colors.to_hex(scalar_map.to_rgba(i)) for i in range(n)]