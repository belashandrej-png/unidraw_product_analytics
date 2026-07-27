from scipy.stats import chi2_contingency, ttest_ind
from statsmodels.stats.proportion import proportions_ztest

def check_homogeneity(df, group_col, feature_col):
    """Проверка однородности групп (Chi-square)"""
    contingency = pd.crosstab(df[group_col], df[feature_col])
    chi2, p_value, dof, _ = chi2_contingency(contingency)
    return p_value > 0.05, p_value
