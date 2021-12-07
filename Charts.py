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
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from time import time

# =================================
# ===== Parameters ================
# =================================
print('Creating Parameters')
save_path = r'C:\Users\arthu\Desktop\TCC\\'
read_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\\'
chart_path = r'C:\Users\arthu\Desktop\TCC\Chartbooks\\'

start_time = time()

MyFont = {'fontname': 'Century Gothic'}
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Century Gothic']
linewidth = 3
fontsize = 10
figsize = (13, 6)
locators = mdates.MonthLocator(interval=3)

# ===============================================
# ===== Collecting the DataFrames ===============
# ===============================================
print('Opening DataFrames')
df_6 = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='75% - 25%', index_col='mes')
df_5 = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='25% +', index_col='mes')
df_4 = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='75% +', index_col='mes')
df_3 = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='75% - 50%', index_col='mes')
df_2 = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='50% - 25%', index_col='mes')
df_1 = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='25% -', index_col='mes')
df_acima = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='Mediana +', index_col='mes')
df_abaixo= pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='Mediana -', index_col='mes')
df_rm_6 = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='75% - 25%', index_col='mes')
df_rm_5 = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='25% +', index_col='mes')
df_rm_4 = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='75% +', index_col='mes')
df_rm_3 = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='75% - 50%', index_col='mes')
df_rm_2 = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='50% - 25%', index_col='mes')
df_rm_1 = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='25% -', index_col='mes')
df_rm_acima = pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='Mediana +', index_col='mes')
df_rm_abaixo= pd.read_excel(save_path + r'Analysis & Charts - RM.xlsx', sheet_name='Mediana -', index_col='mes')

# ===============================================
# ===== Adjusting the DataFrames ================
# ===============================================
print('Adjusting DataFrames')

cols = {'SRAG Casos': 'Casos de SRAG',
        'SRAG Casos 1mm': 'Casos de SRAG por 1mm de Habitantes',
        'SRAG Óbitos': 'Óbitos de SRAG',
        'SRAG Óbitos 1mm': 'Óbitos de SRAG por 1mm de Habitantes',
        'SRAG UTI': 'UTI de SRAG',
        'SRAG UTI 1mm': 'UTI de SRAG por 1mm de Habitantes',
        'SUS Ób Int': 'Óbitos do SUS por Local de Internação',
        'SUS Ób Int 1mm': 'Óbitos do SUS por Local de Internação por 1mm de Habitantes',
        'SUS Ób Res': 'Óbitos do SUS por Local de Residência',
        'SUS Ób Res 1mm': 'Óbitos do SUS por Local de Residência por 1mm de Habitantes',
        'SUS Int Int': 'Internações do SUS por Local de Internação',
        'SUS Int Int 1mm': 'Internações do SUS por Local de Internação por 1mm de Habitantes',
        'SUS Int Res': 'Internações do SUS por Local de Residência',
        'SUS Int Res 1mm': 'Internações do SUS por Local de Residência por 1mm de Habitantes',
        'CONASS': 'Óbitos do Conass',
        'CONASS 1mm': 'Óbitos do Conass por 1mm de Habitantes'}

print('Excessos - Full')
pp = PdfPages(chart_path + r'Chart Analysis.pdf')

for col in cols:
    # Percentil de Renda per Capita
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - por Percentil de Renda per Capita', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_4.index, df_4[f'{col}'], color='limegreen', linewidth=linewidth, label='75% +')
    ax.plot(df_3.index, df_3[f'{col}'], color='olive', linewidth=linewidth, label='75% - 50%')
    ax.plot(df_2.index, df_2[f'{col}'], color='orange', linewidth=linewidth, label='50% - 25%')
    ax.plot(df_1.index, df_1[f'{col}'], color='red', linewidth=linewidth, label='25% -')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - por Percentil de Renda per Capita.png')

    pp.savefig(fig)

    # Faixa de Renda per Capita
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - por Faixa de Renda per Capita', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_4.index, df_4[f'{col}'], color='limegreen', linewidth=linewidth, label='Alta')
    ax.plot(df_6.index, df_6[f'{col}'], color='olive', linewidth=linewidth, label='Média')
    ax.plot(df_1.index, df_1[f'{col}'], color='red', linewidth=linewidth, label='Baixa')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - por Faixa de Renda per Capita.png')

    pp.savefig(fig)

    # Comparação com o Percentil Mais Baixo
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - em Comparação com o Percentil Mais Baixo', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_5.index, df_5[f'{col}'], color='limegreen', linewidth=linewidth, label='25% +')
    ax.plot(df_1.index, df_1[f'{col}'], color='red', linewidth=linewidth, label='25% -')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - em Comparação com o Percentil Mais Baixo.png')

    pp.savefig(fig)

    # Mediana de Renda per Capita
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - pela Mediana de Renda per Capita', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_acima.index, df_acima[f'{col}'], color='limegreen', linewidth=linewidth, label='Acima')
    ax.plot(df_abaixo.index, df_abaixo[f'{col}'], color='red', linewidth=linewidth, label='Abaixo')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - pela Mediana de Renda per Capita.png')

    pp.savefig(fig)

pp.close()

print('Excessos - RM')
pp = PdfPages(chart_path + r'Chart Analysis - RM.pdf')

for col in cols:
    # Percentil de Renda per Capita
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - por Percentil de Renda per Capita', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_rm_4.index, df_rm_4[f'{col}'], color='limegreen', linewidth=linewidth, label='75% +')
    ax.plot(df_rm_3.index, df_rm_3[f'{col}'], color='olive', linewidth=linewidth, label='75% - 50%')
    ax.plot(df_rm_2.index, df_rm_2[f'{col}'], color='orange', linewidth=linewidth, label='50% - 25%')
    ax.plot(df_rm_1.index, df_rm_1[f'{col}'], color='red', linewidth=linewidth, label='25% -')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - por Percentil de Renda per Capita.png')

    pp.savefig(fig)

    # Faixa de Renda per Capita
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - por Faixa de Renda per Capita', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_rm_4.index, df_rm_4[f'{col}'], color='limegreen', linewidth=linewidth, label='Alta')
    ax.plot(df_rm_6.index, df_rm_6[f'{col}'], color='olive', linewidth=linewidth, label='Média')
    ax.plot(df_rm_1.index, df_rm_1[f'{col}'], color='red', linewidth=linewidth, label='Baixa')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - por Faixa de Renda per Capita.png')

    pp.savefig(fig)

    # Comparação com o Percentil Mais Baixo
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - em Comparação com o Percentil Mais Baixo', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_rm_5.index, df_rm_5[f'{col}'], color='limegreen', linewidth=linewidth, label='25% +')
    ax.plot(df_rm_1.index, df_rm_1[f'{col}'], color='red', linewidth=linewidth, label='25% -')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - em Comparação com o Percentil Mais Baixo.png')

    pp.savefig(fig)

    # Mediana de Renda per Capita
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'{cols[col]} - pela Mediana de Renda per Capita', fontweight="bold", fontsize=fontsize + 5)

    ax.plot(df_rm_acima.index, df_rm_acima[f'{col}'], color='limegreen', linewidth=linewidth, label='Acima')
    ax.plot(df_rm_abaixo.index, df_rm_abaixo[f'{col}'], color='red', linewidth=linewidth, label='Abaixo')
    ax.legend(loc='best', frameon=True, prop={'size': 10})
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)

    fig.tight_layout()

    fig.savefig(chart_path + f'{cols[col]} - pela Mediana de Renda per Capita.png')

    pp.savefig(fig)

pp.close()

# fig, ax = plt.subplots(figsize=figsize)
# ax.scatter(np.log(df['pib_per_capita']), df['CONASS 20'])

# TODO EVENT STUDY GRAPHS

# df = pd.read_stata(r'G:\Arthur Alberti\bacon_example.dta')
#
# df['time_to_treat'] = (df['_nfd'] - (df['year'])).fillna(0).astype(int)
# df = (pd.get_dummies(df, columns=['time_to_treat'], prefix='INX').rename(columns=lambda x: x.replace('-', 'm'))
#       .drop(columns='INX_m1').set_index(['stfips', 'year']))
#
# scalars = ['pcinc', 'asmrh', 'cases']
# factors = df.columns[df.columns.str.contains('INX')]
# exog = factors.union(scalars)
# endog = 'asmrs'
#
# mod = lm.PanelOLS(df[endog], df[exog], entity_effects=True, time_effects=True)
# fit = mod.fit(cov_type='clustered', cluster_entity=True)
# fit.summary
#
# inxnames = df.columns[range(13,df.shape[1])]
# formula = '{} ~ {} + EntityEffects + TimeEffects'.format(endog, '+'.join(exog))
#
# clfe = mod.fit(cov_type = 'clustered',
#     cluster_entity = True)
#
# # Plottinh
# res = pd.concat([clfe.params, clfe.std_errors], axis = 1)
# res['ci'] = res['std_error']*1.96
# res = res.filter(like='INX', axis=0)
# res.index = (res.index.str.replace('INX_', '').str.replace('m', '-').astype(int).rename('time_to_treat'))
# res = res.reindex(range(res.index.min(), res.index.max()+1)).fillna(0)
#
# figsize = (12, 12 * 8 / 18)
#
# fig, ax = plt.subplots(figsize=figsize)
# fig.suptitle(f'Event Study', fontweight="bold", fontsize=fontsize + 5)
#
# ax.scatter(res.index, res['parameter'], color='black', zorder=10)
# ax.errorbar(res.index, res['parameter'], yerr=res['ci'], color='lightskyblue', zorder=5)
#
# ax.grid(True, which='both', linestyle='--', alpha=0.4)
# ax.axhline(0, color='black', zorder=0, alpha=0.5)
# ax.axvline(0, color='black', zorder=0, alpha=0.5)
# ax.tick_params(axis='x', labelsize=fontsize)
# ax.tick_params(axis='y', labelsize=fontsize)
# ax.set_ylabel('Estimated Effect', color='black', fontweight='bold')
# ax.set_xlabel('Time to Treatment', color='black', fontweight='bold')
#
# fig.tight_layout()

print('It took ' + str(round((time() - start_time)/60, 1)) + ' minutes to run the routine.')
