import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# read data
data = pd.read_csv('./dataset/MPG_DataSet.csv', sep=';')
USAMpg = data['USA'].values
JapanMpg = data['Japan']
JapanMpg = JapanMpg[JapanMpg != -999].values


print'USA data length %d' % len(USAMpg)
print'Japan data length %d' % len(JapanMpg)

print'USA data mean %f' % USAMpg.mean()
print'Japan data mean %f' % JapanMpg.mean()


# plot the data
showPlots = True
if showPlots:
    fig = plt.figure('T-Test')
    fig.suptitle("Box Plots", fontsize=16)
    ax = plt.subplot("121")
    ax.set_title("USA MPG")
    ax.boxplot(USAMpg)

    ax = plt.subplot("122")
    ax.set_title("Japan MPG")
    ax.boxplot(JapanMpg)
    plt.show(block=True)

# Two tailed
# H1_0(null hypothesis): two means are equal
# Significance Level = 0.05
significance = 0.05
t, p = ttest_ind(USAMpg, JapanMpg, equal_var=False)
print("First hypothesis: MPG means of USA and Japan are equal")
print("t-value = %g  p-value = %g  alpha = %g" % (t, p, significance))

# H1_1: two means are not equal
if p < significance:
    print ('For H1: It is unlikely to except null hypothesis!')
else:
    print ('For H1: Null hypothesis cannot be rejected!')

print(' ------------- ')
'''
Taken from: http://stackoverflow.com/questions/15984221/how-to-perform-two-sample-one-tailed-t-test-with-numpy-scipy

It goes on to say that scipy always gives the test statistic as signed.
This means that given p and t values from a two-tailed test,
you would reject the null hypothesis of a greater-than test when p/2 < alpha and t > 0, and of a less-than test when p/2 < alpha and t < 0.

Another good soruce: http://stattrek.com/hypothesis-test/difference-in-means.aspx?Tutorial=AP
'''

# One Tailed Hypothesis
# H2_0(null hypothesis): USA's mean is greater or equal than Japan's
# data points are inverted in order to make T value > 0
t, p = ttest_ind(JapanMpg, USAMpg, equal_var=False)
print("Second null hypothesis: USA's mean is greater or equal than Japan's")
print("t-value = %g  p-value = %g  alpha = %g" % (t, p, significance))
p_one_tailed = p/2

# H2_1: Japan's mean is greater than USA's
if (p/2) < significance:
    print ('For H_3: It is unlikely to except null hypothesis!')
else:
    print ('For H_3: Null hypothesis cannot be rejected!')

print(' ------------- ')