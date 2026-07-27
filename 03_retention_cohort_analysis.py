# Расчет Retention

df_visits['event_dttm'] = pd.to_datetime(df_visits['event_dttm'])
df_users['registration_dttm'] = pd.to_datetime(df_users['registration_dttm'])

df_visits_full = df_visits.merge(df_users_ab[['user_id', 'group_name']], 
                                  on='user_id', how='left')
df_visits_full = df_visits_full.merge(df_users[['user_id', 'registration_dttm']], 
                                       on='user_id', how='left')

df_visits_full['days_since_reg'] = (df_visits_full['event_dttm'] - 
                                     df_visits_full['registration_dttm']).dt.days
df_visits_full['week_number'] = df_visits_full['days_since_reg'].apply(
    lambda x: min(4, max(1, (x // 7) + 1)) if x >= 0 else 0
)

df_april = df_visits_full[df_visits_full['week_number'].isin([1,2,3,4])].copy()

# Расчет retention по неделям

retention_data = []
for group in ['control', 'test']:
    users_in_group = df_users_ab[df_users_ab['group_name'] == group]['user_id'].unique()
    n_users = len(users_in_group)
    
    for week in [1, 2, 3, 4]:
        week_users = df_april[(df_april['group_name'] == group) & 
                              (df_april['week_number'] == week)]['user_id'].nunique()
        retention_rate = week_users / n_users if n_users > 0 else 0
        
        retention_data.append({
            'group': group,
            'week': f'W{week}',
            'n_users': n_users,
            'n_retained': week_users,
            'retention_rate': retention_rate
        })

retention_df = pd.DataFrame(retention_data)

# График Retention Plot

fig = px.line(retention_df, x='week', y='retention_rate', color='group',
              markers=True, title='Retention W1-W4: Control vs Test',
              labels={'week': 'Неделя', 'retention_rate': 'Доля активных'})
fig.update_traces(marker=dict(size=8))
fig.write_image('images/ab_retention_plot.png', width=800, height=600)
fig.show()

# Статистический тест (Z-test)

from statsmodels.stats.proportion import proportions_ztest

results = []
for week in [1, 2, 3, 4]:
    week_data = retention_df[retention_df['week'] == f'W{week}']
    test_ret = week_data[week_data['group']=='test']['n_retained'].values[0]
    test_tot = week_data[week_data['group']=='test']['n_users'].values[0]
    ctrl_ret = week_data[week_data['group']=='control']['n_retained'].values[0]
    ctrl_tot = week_data[week_data['group']=='control']['n_users'].values[0]
    
    z_stat, p_value = proportions_ztest([test_ret, ctrl_ret], [test_tot, ctrl_tot])
    
    results.append({
        'week': f'W{week}',
        'p_value': p_value,
        'significant': p_value < 0.05
    })

results_df = pd.DataFrame(results)
print(results_df)

# Поправка Бонферрони

alpha_bonf = 0.05 / 4
print(f"Скорректированный уровень значимости: {alpha_bonf:.4f}")
for _, row in results_df.iterrows():
    sig = row['p_value'] < alpha_bonf
    print(f"{row['week']}: p={row['p_value']:.4f} → {'значимо' if sig else 'не значимо'}")


# W1: 37.45% vs 37.57% (p=0.80) W2: 15.64% vs 15.50% (p=0.61) W3: 13.36% vs 13.57% (p=0.79) W4: 18.15% vs 17.88% (p=0.73) Ни одна неделя не значима после поправки Бонферрони
