import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from operator import add

plt.rc('xtick', labelsize=14)    # fontsize of the tick labels
plt.rc('ytick', labelsize=14)    # fontsize of the tick labels
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

df = pd.read_csv("atussum_0321-reduced.csv", index_col=False)
means = df.mean().to_frame().reset_index() # obtain mean values
means.columns = ['Category', 'Mean']
means = means[means['Category'].str.contains('t')] # drop everything except the category information
means = means.sort_values(by=['Mean'], ascending = False) # sort in descending order of mean values, so that the greatest values are at the head of the data frame
means = means.reset_index().drop('index', axis = 1)
means['Cumulative'] = [sum(means['Mean'].to_list()[0:i+1]) for i in range(len(means))] # Create a new column for cumulative time spent

fig = plt.figure()

# Left subplot
ax1 = fig.add_subplot(121)
ax1.set_facecolor('black')
# set limits - both can range to 1440, the total value for part-whole, and the max possible amount for a category (even if it is very difficult to spend 1440 minutes doing one thing)
ax1.set_xlim(0, 1440)
ax1.set_ylim(0, 1440)
# twin the axis to plot mean values on the upper bar
ax2 = ax1.twiny()

cumulatives = [0] +  means['Cumulative'].to_list() # add a zero at the start to make calculating mid-points of bands easier
categories = means['Category'].to_list()
mean_vals = means['Mean'].to_list()
num_cat = len(means)
len_df_cats = [len(df[categories[i]]) for i in range(num_cat)]
y_locs = []
for i in range(num_cat):
        if i != 0:
            # Plot horizontal lines demarcating the different categories
            ax1.hlines(y=cumulatives[i], xmin=0, xmax=1440, color = 'grey', linestyle = '--', linewidth=2, colors='w')
        # violin plot for category i
        violin_parts = ax1.violinplot(dataset = df[categories[i]], positions = [(cumulatives[i] + cumulatives[i + 1])/2], vert = False, widths = mean_vals[i], showmeans=False, showmedians=False, showextrema=False)
        # set the edge and face color for the violin plot
        for pc in violin_parts['bodies']:
            # dark blue
            pc.set_facecolor('#030764')
            # dark red - discarded keeping in mind red-green colorblindness
            #pc.set_facecolor('#D43F3A')
            pc.set_edgecolor('white')
            pc.set_alpha(1)
        ax1.scatter(df[categories[i]], [(cumulatives[i] + cumulatives[i + 1])/2 for j in range(len_df_cats[i])], marker = '|', linewidths = 0.01, color = 'w') # Plot marks for each data point in that category
        y_locs.append((cumulatives[i] + cumulatives[i + 1])/2) # Create a list of plot marker locations along the y-axis
        # Since this is the left/high level subplot, we only plot a few categories and arrows to keep things from becoming messy
        # We plot the rest of them in the code for the right subplot, which is below
        if i < 6:
            # Create a double headed arrow spanning a category's height
            ax1.annotate('', xy = (1300, cumulatives[i]), xytext = (1300, cumulatives[i+1]), arrowprops=dict(arrowstyle='<->', color = 'w'))
            # place text next to the arrow to indicate which category is it
            if i < 5:
                ax1.text(1320, (cumulatives[i] + cumulatives[i + 1])/2 + 4, categories[i], fontsize = 16, color = 'w')
            else: 
                ax1.text(1320, (cumulatives[i] + cumulatives[i + 1])/2, categories[i], fontsize = 16, color = 'w')
# Plot stem charts from the means to the top axis
stem_markers, stem_lines, stem_base  = ax1.stem(mean_vals[:6], y_locs[:6], linefmt = 'w:', markerfmt = 'x', bottom = 1440)
plt.setp(stem_markers, markersize = 8)
plt.setp(stem_markers, 'linewidth', 3)
plt.setp(stem_lines, 'linewidth', 3)
ax1.set_xlabel('Range of category values (distribution)', fontsize=24)
ax1.set_ylabel('Cumulative of mean category values (part-whole relationship)', fontsize=24)
ax1.set_yticks(np.arange(0, 1600, 200), np.arange(0, 1600, 200))

ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(mean_vals[:6])
ax2_locs = [round(item, 1) for item in mean_vals[:6]]
# hacks to keep the mean values from overlapping
ax2_tick_labels = [str(round(item, 1)) for item in mean_vals[:6]]
ax2_tick_labels[4] = '\n' + ax2_tick_labels[4]
ax2_tick_labels[5] = ax2_tick_labels[5] + '\n'
ax2.set_xticklabels(ax2_tick_labels, rotation = 90)

# Right subplot - very similar to what was done with the left subplot
ax3 = fig.add_subplot(122)
ax3.set_facecolor('black')
# set limits to zoom into the top left
ax3.set_xlim(0, 50)
ax3.set_ylim(cumulatives[6], 1440)
ax4 = ax3.twiny()
ax4.set_xlim(ax3.get_xlim())
ax4.set_xticks(mean_vals[6:num_cat])
ax4_tick_labels = [str(round(item, 1)) for item in mean_vals[6:num_cat]]
ax4_tick_labels[4] = '\n' + ax4_tick_labels[4]
ax4_tick_labels[5] = ax4_tick_labels[5] + '\n'
ax4_tick_labels[6] = '\n' + ax4_tick_labels[6]
ax4_tick_labels[7] = ax4_tick_labels[7] + '\n'
ax4.set_xticklabels(ax4_tick_labels, rotation = 90)

# range is for the categories which could not be represented clearly in the first subplot
for i in range(6, num_cat):
        ax3.hlines(y=cumulatives[i], xmin=0, xmax=50, color = 'grey', linestyle = '--', linewidth=2, colors='w')
        violin_parts = ax3.violinplot(dataset = df[categories[i]], positions = [(cumulatives[i] + cumulatives[i + 1])/2], vert = False, widths = mean_vals[i], showmeans=False, showmedians=False, showextrema=False) # Plot marks for each data point in that category
        for pc in violin_parts['bodies']:
            pc.set_facecolor('#030764')
            #pc.set_facecolor('#D43F3A')
            pc.set_edgecolor('white')
            pc.set_alpha(1)
        ax3.scatter(df[categories[i]], [(cumulatives[i] + cumulatives[i + 1])/2 for j in range(len_df_cats[i])], marker = '|', linewidths = 0.01, color = 'w') # Plot marks for each data point in that category
        y_locs.append((cumulatives[i] + cumulatives[i + 1])/2) # Create a list of plot marker locations along the y-axis
        ax3.annotate('', xy = (45, cumulatives[i]), xytext = (45, cumulatives[i+1]), arrowprops=dict(arrowstyle='<->', color = 'w'))
        ax3.text(46, (cumulatives[i] + cumulatives[i + 1])/2, categories[i], fontsize = 16, color = 'w')
stem_markers, stem_lines, stem_base  = ax3.stem(mean_vals[6:num_cat], y_locs[6:num_cat], linefmt = 'w:', markerfmt = 'x', bottom = 1440)
plt.setp(stem_markers, markersize = 8)
plt.setp(stem_markers, 'linewidth', 3)
plt.setp(stem_lines, 'linewidth', 3)
ax3.set_xlabel('Range of category values (distribution)', fontsize=24)
ax3.set_ylabel('Cumulative of mean category values (part-whole relationship)', fontsize=24)

plt.show()
