# Analyze and Present A/B Test Results

# Facebook recently introduced a new bidding type, “average bidding”, as an alternative to its
# exisiting bidding type, called “maximum bidding”. One of our clients,bombabomba.com, has
# decided to test this new feature and wants to conduct an A/B test to understand if average
# bidding brings more conversions than maximum bidding.

# In this A/B test, bombabomba.com randomly splits its audience into two equally sized
# groups, e.g. the test and the control group. A Facebook ad campaign with “maximum
# bidding” is served to “control group” and another campaign with “average bidding” is served
# to the “test group”.

# The A/B test has run for 1 month and bombabomba.com now expects
# us to analyze and present the results of this A/B test.

# Facebook Ad: An advertisement created by a business on Facebook that's served up to Facebook users.
# Impressions: The number of times an ad is displayed.
# Reach: The number of unique people who saw an ad.
# Website Clicks: The number of clicks on ad links directed to Advertiser’s website.
# Website Click Through Rate: Number of Website Clicks / Number of Impressions x 100
# Cost per Action: Spend / Number of Actions
# Action: Can be any conversion event, such as Search, View Content, Add to Cart and Purchase.
# Conversion Rate: Number of Actions / Number of Website Clicks x 100

# The ultimate success metric for bombabomba.com is Number of Purchases.Therefore, we should
# focus on Purchase metrics for statistical testing.


# How would we define the hypothesis of this A/B test?
# H0 : There is no statistically significant difference between the Control group that was served
# “maximum bidding” campaign and Test group that was served “average bidding” campaign.
# H1 : There is statistically significant difference between the Control group that was served
# “maximum bidding” campaign and Test group that was served “average bidding” campaign.

import numpy as np
import pandas as pd
from scipy.stats import shapiro
import scipy.stats as stats

pd.pandas.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: '%.4f' % x)

# reading the data
Control_Group = pd.read_excel("Datasets/ab_testing_data.xlsx", sheet_name='Control Group')  # maximum bidding
Test_Group = pd.read_excel("Datasets/ab_testing_data.xlsx", sheet_name='Test Group')        # average bidding

# assinging name for dataframes
Control_Group.name = "Control_Group"
Test_Group.name = "Test_Group"

# Analyze the dataframes
def analyze_df (df):
    print("Dataframe Name : %s" % df.name,"\n") # dataframe name
    print("Shape of dataframe: {0}".format(df.shape), "\n") # shape of dataframe
    print("There are {0} observations and {1} features".format(len(df),len(df.columns)),"\n") # number of observations and features
    print(df.head(),"\n") # first 5 observation
    for col in df.columns:
        print(" Number of null value in the {0} column: {1}".format(col,df[col].isnull().sum())) # is there a null value in any columns
    print("\n","Website Click Through Rate: %.4f" % (df["Click"].sum()/df["Impression"].sum()*100),"%","\n") # rate of website click
    print(df.describe().T) # for observe the outliers

#analyze Control Group
analyze_df(Control_Group)

# analyze Test Group
analyze_df(Test_Group)

# The ultimate success metric for bombabomba.com is Number of Purchases.
# Therefore, we should focus on Purchase metrics for statistical testing.
A = pd.DataFrame(Control_Group["Purchase"])
B = pd.DataFrame(Test_Group["Purchase"])

# Combine the test and control group with group and purchase
AB = pd.concat([A,B],axis=1)
AB.columns=["A","B"]

print(" Mean of purchase of control group: %.3f"%AB.A.mean(),"\n",
      "Mean of purchase of test group: %.3f"%AB.B.mean())

# When we look at the purchase average of the two groups, we can observe that the test group, the average
# bidding campaign, is better. But this observation is not a statistically significant results.

# Can we conclude statistically significant results?

# Indepented Two Sample T-Test
# The Independent Samples t Test compares the means of two independent groups in order to determine whether
# there is statistical evidence that the associated population means are significantly different.

# Requirements
# Normal distribution: Non-normal population distributions, especially those that are thick-tailed or heavily skewed, considerably reduce the power of the test
# Homogeneity of variances : When this assumption is violated and the sample sizes for each group differ, the p value is not trustworthy.
# Hypotheses

# The null hypothesis (H0) and alternative hypothesis
# (H1) of the Independent Samples t Test can be expressed in two different but equivalent ways:

# H0: µ1 = µ2 (the two population means are equal)
# H1: µ1 ≠ µ2 (the two population means are not equal)

# The Shapiro-Wilks Test for Normality
# H0: There is no statistically significant difference between sample distribution and theoretical normal distribution
# H1: There is statistically significant difference between sample distribution and theoretical normal distribution

# The test rejects the hypothesis of normality when the p-value is less than or equal to 0.05. Failing the normality test allows you to state with 95% confidence the data does not fit the normal distribution.

#p-value < 0.05 (H0 rejected)
#p-value > 0.05 (H0 not rejected)

# Shapiro-Wilks Test  for Group A
test_statistic , pvalue = shapiro(AB.A)
print('Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue))

# Shapiro-Wilks Test  for Group B
test_statistic , pvalue = shapiro(AB.B)
print('Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue))

#p-value greater then 0.05 so H0 is not rejected for Group B.
print(pvalue < 0.05)

#There is no statistically significant difference between sample distribution and theoretical normal distribution in groups A and B.

# Levene’s Test for Homogeneity of variances
# Levene’s test is an equal variance test. It can be used to check if our data sets fulfill the homogeneity of variance assumption
# before we perform the t-test or Analysis of Variance

# H0: the compared groups have equal variance.
# H1: the compared groups do not have equal variance.

test_statistic,pvalue = stats.levene(AB.A,AB.B)
print('Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue))

# p-value greater then 0.05 so H0 is not rejected.
pvalue < 0.05

# The compared groups have equal variance.

# The assumptions of normality distribution and variance homogeneity were tested.Two assumptions are provided, we can now test for our main hypothesis.
# H0 : There is no statistically significant difference between the Control group that was served “maximum bidding” campaign and Test group that was served “average bidding” campaign.
# H1 : There is statistically significant difference between the Control group that was served “maximum bidding” campaign and Test group that was served “average bidding” campaign.

tvalue, pvalue = stats.ttest_ind(AB["A"], AB["B"], equal_var=True)
print('tvalue = %.4f, pvalue = %.4f' % (tvalue, pvalue))

# p-value greater then 0.05 so H0 is not rejected.
pvalue < 0.05

# P-value greater then 0.05 so H0 is not rejected.So, There is no statistically significant
# difference between the Control group that was served “maximum bidding” campaign and Test group
# that was served “average bidding” campaign.


# Which statistical test did we use, and why?
# We used independent t-test because we want to determine
# if there is a significant difference between the means of two indepented groups,
# which may be related in certain features.


# What would be our recommendation to client?
# There is no statistically significant difference between the Control group that was served
# “maximum bidding” campaign and Test group that was served “average bidding” campaign. For this reason,
# we can recommend continuing with the maximum bidding campaign currently used.

# Conclusion
# Hypothesis established and interpreted
# The data was analyzed, outliers were observed
# It was checked whether the assumptions were met for the statistical test to be applied
# The assumptions were observed and tested
# Commented based on -p-value
# Suggestion offered to customer