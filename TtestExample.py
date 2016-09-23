import pandas as pd
import matplotlib.pyplot as plt
from scipy.special._ufuncs import stdtr
from scipy.stats import ttest_ind, ttest_ind_from_stats
from numpy import sqrt

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
showPlots = False
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


''' Another good soruce: http://stattrek.com/hypothesis-test/difference-in-means.aspx?Tutorial=AP '''
# Problem 2: One-Tailed Test
#
#  The Acme Company has developed a new battery. The engineer in charge claims that the new battery will operate continuously for at least 7 minutes longer than the old battery.
# To test the claim, the company selects a simple random sample of 100 new batteries and 100 old batteries. The old batteries run continuously for 190 minutes with a standard deviation of 20 minutes; the new batteries, 200 minutes with a standard deviation of 40 minutes.
# Test the engineer's claim that the new batteries run at least 7 minutes longer than the old. Use a 0.05 level of significance. (Assume that there are no outliers in either sample.)
# Solution: The solution to this problem takes four steps: (1) state the hypotheses, (2) formulate an analysis plan, (3) analyze sample data, and (4) interpret results. We work through those steps below:

#Null hypothesis: Mu1 - Mu2 >= 7
#Alternative hypothesis: Mu1 - Mu2 < 7


na = float(100)
adof = na - 1
abar = float(200)
avar = float(40)**2 * (na / adof)


nb = float(100)
bdof = nb - 1
bbar = float(190)
bvar = float(20)**2 * (nb / bdof)

# Use scipy.stats.ttest_ind_from_stats.
t2, p2 = ttest_ind_from_stats(abar, sqrt(avar), na,
                              bbar, sqrt(bvar), nb,
                              equal_var=False)
print("ttest_ind_from_stats: t = %g  p = %g" % (t2, p2))

# Use the formulas directly.
tf = (abar - bbar - 7) / sqrt(avar/na + bvar/nb)
dof = (avar/na + bvar/nb)**2 / (avar**2/(na**2*adof) + bvar**2/(nb**2*bdof))

#calculating p value of P(T > tf)
pval = stdtr(dof, abs(tf))

print 't = %f p = %f dof = %f' % (tf,pval,dof)
if pval < significance:
    print ('It is unlikely to except null hypothesis!')
else:
    print ('Null hypothesis cannot be rejected!')
