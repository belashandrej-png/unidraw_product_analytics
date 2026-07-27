# 1. Загрузка данных A/B теста

df_users_ab = pd.read_csv('unidraw_users_ab.csv')
print(f"AB тест: {len(df_users_ab)} пользователей")
print(df_users_ab['group_name'].value_counts())

# 2. Проверка однородности групп (SRM check)

from scipy.stats import chi2_contingency

# Объединяем данные
df = df_users_ab.merge(df_users[['user_id', 'gender', 'age_segment']], 
                       on='user_id', how='left')

# Проверка по industry
contingency = pd.crosstab(df['group_name'], df['industry'])
chi2, p_value, dof, expected = chi2_contingency(contingency)
print(f"Chi-square p-value: {p_value:.4f}")
print(f"Группы однородны: {'ДА' if p_value > 0.05 else 'НЕТ'}")

# 3. Анализ template_activity

from scipy import stats
import matplotlib.pyplot as plt

control = df[df['group_name']=='control']['template_activity']
test = df[df['group_name']=='test']['template_activity']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Гистограмма
axes[0].hist(control, bins=50, alpha=0.5, label='control', density=True)
axes[0].hist(test, bins=50, alpha=0.5, label='test', density=True)
axes[0].set_title('Распределение template_activity')
axes[0].legend()

# Boxplot
axes[1].boxplot([control, test], labels=['control', 'test'])
axes[1].set_title('Boxplot распределения')

plt.tight_layout()
plt.savefig('images/ab_template_activity_dist.png', dpi=300)
plt.show()

# Статистический тест:

from statsmodels.stats.weightstats import ttest_ind

t_stat, p_value, dof = ttest_ind(test, control, alternative='two-sided')
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4e}")

# Эффект
abs_effect = test.mean() - control.mean()
rel_effect = (abs_effect / control.mean()) * 100
print(f"Абсолютный эффект: {abs_effect:.4f}")
print(f"Относительный эффект: {rel_effect:.2f}%")

4. Анализ templates_per_user

# 4. Анализ templates_per_user. График 6: Распределение templates_per_user

df_templates['event_dttm'] = pd.to_datetime(df_templates['event_dttm'])
df_april = df_templates[(df_templates['event_dttm'] >= '2026-04-01') & 
                        (df_templates['event_dttm'] <= '2026-04-30')]

templates_per_user = df_april.groupby('user_id').size().reset_index(name='cnt')
df_analysis = df_users_ab[['user_id', 'group_name']].merge(
    templates_per_user, on='user_id', how='left'
)
df_analysis['cnt'] = df_analysis['cnt'].fillna(0)

control_cnt = df_analysis[df_analysis['gr#oup_name']=='control']['cnt']
test_cnt = df_analysis[df_analysis['group_name']=='test']['cnt']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Гистограмма (только активные)
axes[0].hist(control_cnt[control_cnt>0], bins=range(1, 21), alpha=0.5, label='control')
axes[0].hist(test_cnt[test_cnt>0], bins=range(1, 21), alpha=0.5, label='test')
axes[0].set_title('templates_per_user (активные пользователи)')
axes[0].legend()

# Доля нулей
zero_rates = [(control_cnt==0).mean(), (test_cnt==0).mean()]
axes[1].bar(['control', 'test'], zero_rates, color=['blue', 'orange'])
axes[1].set_title('Доля пользователей с 0 шаблонов')
axes[1].set_ylabel('Доля')

plt.tight_layout()
plt.savefig('images/ab_templates_per_user_dist.png', dpi=300)
plt.show()

# 5. Расчет MDE График 7: MDE Visualization

from statsmodels.stats.power import TTestIndPower

n_control = len(control_cnt)
n_test = len(test_cnt)
pooled_std = np.sqrt(((n_control-1)*control_cnt.var() + (n_test-1)*test_cnt.var()) / 
                     (n_control + n_test - 2))

analysis = TTestIndPower()
cohen_d_mde = analysis.solve_power(nobs1=n_control, alpha=0.05, power=0.80, 
                                    ratio=n_test/n_control, alternative='two-sided')
absolute_mde = cohen_d_mde * pooled_std

fig, ax = plt.subplots(figsize=(10, 6))
effects = ['Наблюдаемый\nэффект', 'MDE']
values = [abs(abs_effect), absolute_mde]
colors = ['red' if abs(abs_effect) < absolute_mde else 'green', 'gray']

ax.bar(effects, values, color=colors, alpha=0.7)
ax.set_ylabel('Абсолютное значение')
ax.set_title(f'MDE Analysis\nMDE={absolute_mde:.4f}, Наблюдаемый эффект={abs(abs_effect):.4f}')
ax.axhline(y=absolute_mde, color='gray', linestyle='--', alpha=0.5)

plt.savefig('images/ab_mde_visualization.png', dpi=300)
plt.show()

# template_activity: +5% (значимо). templates_per_user: -7.94% (не значимо, p=0.37). MDE = 24.91% → выборки недостаточно. 96% пользователей = 0 шаблонов
