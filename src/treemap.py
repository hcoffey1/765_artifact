import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import seaborn as sns
import squarify

# read in the dataset
df = pd.read_csv("atussum_0321-reduced.csv", index_col=False)
means = df.mean().to_frame().reset_index() # obtain mean values
means.columns = ['Category', 'Mean']
means = means[means['Category'].str.contains('t')] # drop everything except the category information
df_std_devs = df.std().to_frame().reset_index() # obtain std values
df_std_devs.columns = ['Category', 'std']
df_std_devs = df_std_devs[df_std_devs['Category'].str.contains('t')] # drop everything except the category information
means['StdDev'] = df_std_devs['std']
# Normalize the standard deviation by dividing by mean
means['NormStdDev'] = means['StdDev'].div(means['Mean'])
means = means.sort_values(by=['Mean'], ascending = False) # sort in descending order of mean values, so that the greatest values are at the head of the data frame
means = means.reset_index().drop('index', axis = 1)
means['Cumulative'] = [sum(means['Mean'].to_list()[0:i+1]) for i in range(len(means))] # Create a new column for cumulative time spent
#print(means)

cmap = plt.cm.Greens # Use shades of green for color mapping

# In case we want information and color encodings based on normalized standard deviation
mini = min(means['NormStdDev'])
maxi = max(means['NormStdDev'])

# In case we want information and color encodings based on standard deviation
#mini = min(means['StdDev'])
#maxi = max(means['StdDev'])

# Encode colors on a linear scale
#norm = colors.Normalize(vmin = mini, vmax = maxi)
# Encode colors on a logarithmic scale
norm = colors.LogNorm(vmin = mini, vmax = maxi)

# Derive color mappings based on normalized standard deviation
std_colors = [cmap(norm(value)) for value in means['NormStdDev']]
# Derive color mappings based on standard deviation
#std_colors = [cmap(norm(value)) for value in means['StdDev']]

#treemap block sizes
block_sizes = means['Mean']

# Hacks to prevent text from overlapping in final visualization
label = means['Category'].str.upper() + '\nMean:' + means['Mean'].round(2).astype(str) + '\nNorm. Std..:' + means['NormStdDev'].round(2).astype(str)
#label = means['Category'].str.upper() + '\nMean:' + means['Mean'].round(2).astype(str) + '\nStd. Dev.:' + means['StdDev'].round(2).astype(str)
label[16] = label[16] + '\n' + '\n'
label[17] = '.                         ' + means['Category'][17].upper() + '\n.                         Mean:' + means['Mean'][17].round(2).astype(str) + '\n.                         Norm. Std.:' + means['NormStdDev'][17].round(2).astype(str) + '\n' + '\n'

# plot the treemap
treemap_plot = squarify.plot(sizes=block_sizes, label=label, alpha=0.6,color=std_colors, text_kwargs={'fontsize':12})
plt.axis('off')
plt.title('Category part-whole breakdown with distribution information', pad = 20, fontsize = 12)
# enable a color scale
plt.colorbar(cm.ScalarMappable(norm = norm, cmap = cmap))
plt.tight_layout()
plt.show()
