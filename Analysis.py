"""
Author: Arthur Alberti

- Routine that collects the DataFrames, cleans them and leave them ready for thge Charts and Analysis.

- Data collected from: DataSUS, SIVEP-Gripe, IBGE and CONASS.
"""
# ==========================================
# ===== Importing Libraries ================
# ==========================================
print('Importing Libraries')
import pandas as pd
import numpy as np
from time import time
from statsmodels.formula.api import ols, poisson

# =================================
# ===== Parameters ================
# =================================
print('Creating Parameters')
save_path = r'C:\Users\arthu\Desktop\TCC\\'
read_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\\'
chart_path = r'C:\Users\arthu\Desktop\TCC\Chartbooks\\'

start_time = time()

# ===============================================
# ===== Collecting the DataFrames ===============
# ===============================================
print('Opening DataFrames')
df = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='Full', index_col='mes')
# df_rm = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='Full', index_col='mes')

# ===============================================
# ===== Adjusting the DataFrames ================
# ===============================================
print('Adjusting DataFrames')
df['mes'] = df.index

print(df.columns)

print('Final DataFrame')
df_final = df[['mes', 'UF', 'cod_mic', 'mic', 'cod_mun', 'mun', 'RM', 'amazonia_legal', 'pib', 'pib_per_capita', 'renda_per_capita', 'area_mun',
               'Leitos', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int','SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res',  'CONASS',
               'idosos_p', 'pop_0.5_sm', 'pop_0.25_sm', 'fundamental_inc', 'fundamental_comp/em_inc', 'em_comp', 'nao_determinado', 'total', 'populacao']]

df_final['mediana_pib'] = np.where((df_final['pib_per_capita'] < df_final['pib_per_capita'].median()), 1, 0)
df_final['mediana_renda'] = np.where((df_final['renda_per_capita'] < df_final['renda_per_capita'].median()), 1, 0)

df_final['em_inc'] = df_final['fundamental_comp/em_inc']
df_final['pop_05_sm'] = df_final['pop_0.5_sm']
df_final['pop_025_sm'] = df_final['pop_0.25_sm']

print('Regressões')
print('% Populacao domiciliar recebendo menos do que 1/4 de um salario minimo')
# CONASS
fit = ols('CONASS ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()
print(fit.summary())

# SUS Ób Int
fit = ols('SUS_Ób_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

# SUS Ób Res
fit = ols('SUS_Ób_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

# SUS Int Int
fit = ols('SUS_Int_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

# SUS Int Res
fit = ols('SUS_Int_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

# SRAG Casos
fit = ols('SRAG_Casos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

# SRAG Óbitos
fit = ols('SRAG_Óbitos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

# SRAG UTI
fit = ols('SRAG_UTI ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_025_sm*mes', data=df_final).fit()

print('% Populacao domiciliar recebendo menos do que 1/2 de um salario minimo')
# CONASS
fit = ols('CONASS ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SUS Ób Int
fit = ols('SUS_Ób_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SUS Ób Res
fit = ols('SUS_Ób_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SUS Int Int
fit = ols('SUS_Int_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SUS Int Res
fit = ols('SUS_Int_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SRAG Casos
fit = ols('SRAG_Casos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SRAG Óbitos
fit = ols('SRAG_Óbitos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

# SRAG UTI
fit = ols('SRAG_UTI ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + pop_05_sm*mes', data=df_final).fit()

print('Mediana da Renda per Capita media domiciliar')
# CONASS
fit = ols('CONASS ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SUS Ób Int
fit = ols('SUS_Ób_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SUS Ób Res
fit = ols('SUS_Ób_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SUS Int Int
fit = ols('SUS_Int_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SUS Int Res
fit = ols('SUS_Int_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SRAG Casos
fit = ols('SRAG_Casos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SRAG Óbitos
fit = ols('SRAG_Óbitos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

# SRAG UTI
fit = ols('SRAG_UTI ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_renda*mes', data=df_final).fit()

print('Mediana do PIB per Capita')
# CONASS
fit = ols('CONASS ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

# SUS Ób Int
fit = ols('SUS_Ób_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

# SUS Ób Res
fit = ols('SUS_Ób_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

# SUS Int Int
fit = ols('SUS_Int_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

# SUS Int Res
fit = ols('SUS_Int_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

# SRAG Casos
fit = ols('SRAG_Casos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

# SRAG Óbitos
fit = ols('SRAG_Óbitos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + mediana_pib*mes', data=df_final).fit()

############################################################# REGRESSAO COMPLETA
# SRAG UTI
fit = ols('SRAG_UTI ~ area_mun + populacao + UF + RM + mediana_pib*fundamental_inc + mediana_pib*em_inc + mediana_pib*em_comp + mediana_pib*nao_determinado + mediana_pib*mes', data=df_final).fit()

print('Leitos de internacao disponiveis')
# CONASS
fit = ols('CONASS ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SUS Ób Int
fit = ols('SUS_Ób_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SUS Ób Res
fit = ols('SUS_Ób_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SUS Int Int
fit = ols('SUS_Int_Int ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SUS Int Res
fit = ols('SUS_Int_Res ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SRAG Casos
fit = ols('SRAG_Casos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SRAG Óbitos
fit = ols('SRAG_Óbitos ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()

# SRAG UTI
fit = ols('SRAG_UTI ~ area_mun + populacao + UF + fundamental_inc + em_inc + em_comp + nao_determinado + RM + Leitos*mes', data=df_final).fit()


# print('Atualmente existem 5570 municípios')
#
# print('A base de 2018 possui ' + str(int(df_2018.groupby(['UF'])['mun'].nunique().sum())) +
#       ' municípios diferentes')
#
# print('A base de 2019 possui ' + str(int(df_2019.groupby(['UF'])['mun'].nunique().sum())) +
#       ' municípios diferentes')
#
# print('A base de 2020 possui ' + str(int(df_2020.groupby(['UF'])['mun'].nunique().sum())) + ' municípios diferentes')
#
# print('A base do IBGE contém ' + str(int(df_ibge['Código Município Completo'].nunique())) + ' códigos únicos de '
#       'municípios')
#
# print('A base do IBGE contém ' + str(int(df_ibge['Nome_Município'].nunique())) + ' nomes únicos de municípios')
#
# print('Há ' + str(int(df_ibge['Código Município Completo'].nunique() - df_ibge['Nome_Município'].nunique())) +
#       ' municípios com o mesmo nome')
#
# print('Logo, para construir a base final, será necessário dar "match" com a sigla do Estado e o nome do município')
#
# print('O número exato de municípios por estado que há na base do IBGE está listado abaixo: ' +
#       str(df_pib.groupby(['UF'])['cod_mun'].nunique()))
#
# print('O número exato de municípios por estado que há na base do CONASS de 2018 está listado abaixo: ' +
#       str(df_2018.groupby(['UF'])['mun'].nunique()))
#
# print('O número exato de municípios por estado que há na base do CONASS de 2019 está listado abaixo: ' +
#       str(df_2019.groupby(['UF'])['mun'].nunique()))
#
# print('O número exato de municípios por estado que há na base do CONASS de 2020 está listado abaixo: ' +
#       str(df_2020.groupby(['UF'])['mun'].nunique()))
#
# df_2019.groupby(['UF', 'mes'])['mun'].nunique()
#
# df_pib.groupby(['UF'])['cod_mun'].nunique().sum() - df_2018.groupby(['UF'])['mun'].nunique().sum()
#
# df_pib.groupby(['UF'])['cod_mun'].nunique().sum() - df_2019.groupby(['UF'])['mun'].nunique().sum()
#
# df_pib.groupby(['UF'])['cod_mun'].nunique().sum() - df_2020.groupby(['UF'])['mun'].nunique().sum()
#
# df.groupby(['UF'])['mun'].nunique().sum()
#
# ################################################ PIB
#
# # ===== Describing the DataFrame ===== #
# print('Describing DataFrames')
#
# print('Atualmente existem 5570 municípios')
#
# print('A base possui ' + str(int(len(df))) + ' municípios')
#
# print('Utilizando dados do IBGE de 2018, e considerando preços correntes, ')
#
# print('Há ' + str(int(df['atividade'].nunique())) + ' tipos de atividades diferentes, e elas são: ' +
#       str(df['atividade'].unique()))
#
# print('A média anual do PIB municipal é de ' + str(int(df['pib'].mean(axis=0))))
#
# print('A mediana anual do PIB municipal é de ' + str(int(df['pib'].median(axis=0))))
#
# print('A média anual do PIB per capita municipal é de ' + str(int(df['pib_per_capita'].mean(axis=0))))
#
# print('A mediana anual do PIB per capita municipal é de ' + str(int(df['pib_per_capita'].median(axis=0))))
#
# print('A média mensal do PIB municipal é de ' + str(int(df['pib'].mean(axis=0)/12)))
#
# print('A mediana mensal do PIB municipal é de ' + str(int(df['pib'].median(axis=0)/12)))
#
# print('A média mensal do PIB per capita municipal é de ' + str(int(df['pib_per_capita'].mean(axis=0)/12)))
#
# print('A mediana mensal do PIB per capita municipal é de ' + str(int(df['pib_per_capita'].median(axis=0)/12)))
#
# print('A tabela abaixo descreve a quantidade de municípios que fazem parte da amazônia legal:' +
#       str(df.groupby(['amazonia_legal'])['cod_mun'].nunique()))
#
# print('A tabela abaixo descreve a quantidade de municípios de acordo com as diferentes atividades que são mais '
#       'relevantes para o PIB de cada um: ' +
#       str(df.groupby(['atividade'])['cod_mun'].nunique()))
#
# print('A tabela abaixo descreve a quantidade de municípios que fazem parte de Regiões Metropolitanas: ' +
#       str(df.groupby(['RM'])['cod_mun'].nunique()))
#
#