print('Libraries')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from time import time
import pandas as pd
import numpy as np

print('Parameters')
path = r'C:\Users\arthu\Desktop\TCC\\'
save_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\\'
chart_path = r'C:\Users\arthu\Desktop\TCC\Analysis\\'
MyFont = {'fontname': 'Century Gothic'}
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Century Gothic']
linewidth = 3
width= 10
fontsize = 10
figsize = (13, 6)

print('DataFrames')
# df = pd.read_excel(save_path + r'HIST_PAINEL_COVIDBR_31ago2020_1.xlsx')
df_micro_final = pd.read_excel(path + r'DataFrame Final.xlsx')


print('Percentis de Renda per capita - Line')
aux = pd.DataFrame(index=range(0,100))
for i in range(0, 100):
    aux.loc[i, 'percentil'] = np.percentile(df_micro_final['log_renda'], i)

aux['percentil'] = aux['percentil']*1000

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Percentis de Renda per capita', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux.index, aux, color='cornflowerblue', zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Percentis de Renda per capita - Line.png', dpi=800)

print('Percentis de Renda per capita - Bar')
aux = pd.Series([np.percentile(df_micro_final['log_renda'], 25),
                 np.percentile(df_micro_final['log_renda'], 25),
                 np.percentile(df_micro_final['log_renda'], 50),
                 np.percentile(df_micro_final['log_renda'], 66),
                 np.percentile(df_micro_final['log_renda'], 75)],
                 index = ["25%", "33%", "50%", "66%", "75%"])
aux = aux*1000

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Percentis de Renda per capita', fontweight="bold", fontsize=fontsize + 5)
ax.bar(aux.index, aux, color=['orangered', 'orangered', 'yellow', 'forestgreen', 'forestgreen'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.axhline(0, color='black', alpha=0.3, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
plt.ylim(top=7000)
fig.tight_layout()
fig.savefig(chart_path + f'Percentis de Renda per capita - Bar.png', dpi=800)

print('Controles - Bar')
aux = df_micro_final
aux1 = df_micro_final[df_micro_final['mediana_log_renda'] == 1]
aux2 = df_micro_final[df_micro_final['mediana_log_renda'] == 0]
aux = pd.Series([aux1['analfabetismo'].mean(),
                 aux2['analfabetismo'].mean(),
                 aux1['em_comp'].mean(),
                 aux2['em_comp'].mean(),
                 aux1['desemprego'].mean(),
                 aux2['desemprego'].mean()],
                 index = ["Analfabetismo ", "Analfabetismo", "E.M. Completo ",
                          "E.M. Completo", "Desemprego ", 'Desemprego'])

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Analfabetismo, Escolaridade e Desemprego', fontweight="bold", fontsize=fontsize + 5)
ax.bar(aux.index, aux, color=['orangered', 'forestgreen', 'orangered', 'forestgreen', 'orangered', 'forestgreen'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.axhline(0, color='black', alpha=0.3, zorder=0)
ax.set_ylabel('%', color='black', fontweight='bold')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Controles.png', dpi=800)

print('Controles Infraestrutura - Bar')
aux = df_micro_final
aux1 = df_micro_final[df_micro_final['1o_tercil_renda'] == 1]
aux2 = df_micro_final[df_micro_final['2o_tercil_renda'] == 1]
aux3 = df_micro_final[df_micro_final['3o_tercil_renda'] == 1]
aux = pd.Series([aux1['esgoto_geral'].mean(),
                 aux2['esgoto_geral'].mean(),
                 aux3['esgoto_geral'].mean(),
                 aux1['agua_geral'].mean(),
                 aux2['agua_geral'].mean(),
                 aux3['agua_geral'].mean(),
                 aux1['limpeza'].mean(),
                 aux2['limpeza'].mean(),
                 aux3['limpeza'].mean()],
                 index = ["Esgoto ", "Esgoto", "Esgoto  ", "Água ",
                          "Água", "Água  ", "Lixo ", 'Lixo', 'Lixo  '])

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Esgoto, Água Encanada e Coleta de Lixo', fontweight="bold", fontsize=fontsize + 5)
ax.bar(aux.index, aux, color=['orangered', 'yellow', 'forestgreen', 'orangered', 'yellow', 'forestgreen', 'orangered', 'yellow', 'forestgreen'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.axhline(0, color='black', alpha=0.3, zorder=0)
ax.set_ylabel('%', color='black', fontweight='bold')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Controles Infraestrutura.png', dpi=800)

print('Diff in Diff - DataSUS 1')
aux = df_micro_final
aux = df_micro_final[df_micro_final['mediana_log_renda'] == 1]
aux1 = df_micro_final[df_micro_final['1o_tercil_renda'] == 1]
aux2 = df_micro_final[df_micro_final['2o_tercil_renda'] == 1]
aux3 = df_micro_final[df_micro_final['abaixo_log_renda'] == 1]
aux = aux.groupby(aux['mes']).sum()
aux1 = aux1.groupby(aux1['mes']).sum()
aux2 = aux2.groupby(aux2['mes']).sum()
aux3 = aux3.groupby(aux3['mes']).sum()

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Óbitos - Brasil (DataSUS)', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux3.index, aux3['SUS_Ób_Int'], color='red', linewidth=linewidth, label='1o Quartil - Renda per capita')
ax.plot(aux1.index, aux1['SUS_Ób_Int'], color='orangered', linewidth=linewidth, label='1o Tercil - Renda per capita')
ax.plot(aux.index, aux['SUS_Ób_Int'], color='darkorange', linewidth=linewidth, label='Abaixo da Mediana - Renda per capita')
ax.plot(aux2.index, aux2['SUS_Ób_Int'], color='mediumseagreen', linewidth=linewidth, label='2o Tercil - Renda per capita')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='upper left', frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.axvspan('2020-04-01', '2020-07-01', color='grey', alpha=0.2, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Diff in Diff - DataSUS 1.png', dpi=800)

print('Diff in Diff - DataSUS')
aux = df_micro_final
aux = df_micro_final[df_micro_final['mediana_log_renda'] == 0]
aux1 = df_micro_final[df_micro_final['mediana_log_renda'] == 1]
aux = aux.groupby(aux['mes']).sum()
aux1 = aux1.groupby(aux1['mes']).sum()

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Óbitos - Brasil (DataSUS)', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux.index, aux['SUS_Ób_Int'], color='forestgreen', linewidth=linewidth, label='Acima da Mediana - Renda per capita')
ax.plot(aux1.index, aux1['SUS_Ób_Int'], color='orangered', linewidth=linewidth, label='Abaixo da Mediana - Renda per capita')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='upper left', frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.axvspan('2020-04-01', '2020-07-01', color='grey', alpha=0.2, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Diff in Diff - DataSUS 2.png', dpi=800)

print('Diff in Diff - Conass 2020 1')
aux = aux[(aux.index > '2019-12-01') & (aux.index < '2020-10-01')]
aux1 = aux1[(aux1.index > '2019-12-01') & (aux1.index < '2020-10-01')]

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Óbitos - Brasil (Conass)', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux.index, aux['CONASS'], color='limegreen', linewidth=linewidth, label='Acima da Mediana - Renda per capita')
ax.plot(aux1.index, aux1['CONASS'], color='orangered', linewidth=linewidth, label='Abaixo da Mediana - Renda per capita')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='upper left', frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.axvspan('2020-04-01', '2020-07-01', color='grey', alpha=0.2, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Diff in Diff - Conass 2020 1.png', dpi=800)

print('Diff in Diff - Conass 2020 2')
aux = df_micro_final
aux = df_micro_final[df_micro_final['mediana_log_renda'] == 1]
aux1 = df_micro_final[df_micro_final['1o_tercil_renda'] == 1]
aux2 = df_micro_final[df_micro_final['2o_tercil_renda'] == 1]
aux3 = df_micro_final[df_micro_final['abaixo_log_renda'] == 1]
aux = aux.groupby(aux['mes']).sum()
aux1 = aux1.groupby(aux1['mes']).sum()
aux2 = aux2.groupby(aux2['mes']).sum()
aux3 = aux3.groupby(aux3['mes']).sum()
aux = aux[(aux.index > '2019-12-01') & (aux.index < '2020-10-01')]
aux1 = aux1[(aux1.index > '2019-12-01') & (aux1.index < '2020-10-01')]
aux2 = aux2[(aux2.index > '2019-12-01') & (aux2.index < '2020-10-01')]
aux3 = aux3[(aux3.index > '2019-12-01') & (aux3.index < '2020-10-01')]

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Óbitos - Brasil (Conass)', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux3.index, aux3['CONASS'], color='red', linewidth=linewidth, label='1o Quartil - Renda per capita')
ax.plot(aux1.index, aux1['CONASS'], color='orangered', linewidth=linewidth, label='1o Tercil - Renda per capita')
ax.plot(aux.index, aux['CONASS'], color='darkorange', linewidth=linewidth, label='Abaixo da Mediana - Renda per capita')
ax.plot(aux2.index, aux2['CONASS'], color='mediumseagreen', linewidth=linewidth, label='2o Tercil - Renda per capita')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='upper left', frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.axvspan('2020-04-01', '2020-07-01', color='grey', alpha=0.2, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Diff in Diff - Conass 2020 2.png', dpi=800)

print('Diff in Diff - Conass 2019 1')
aux = df_micro_final
aux = df_micro_final[df_micro_final['mediana_log_renda'] == 0]
aux1 = df_micro_final[df_micro_final['mediana_log_renda'] == 1]
aux = aux.groupby(aux['mes']).sum()
aux1 = aux1.groupby(aux1['mes']).sum()
aux = aux[(aux.index <= '2019-09-01')]
aux1 = aux1[(aux1.index <= '2019-09-01')]

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Óbitos - Brasil (Conass)', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux.index, aux['CONASS'], color='limegreen', linewidth=linewidth, label='Acima da Mediana - Renda per capita')
ax.plot(aux1.index, aux1['CONASS'], color='orangered', linewidth=linewidth, label='Abaixo da Mediana - Renda per capita')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='upper left', frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Diff in Diff - Conass 2019 1.png', dpi=800)

print('Diff in Diff - Conass 2019 2')
aux = df_micro_final
aux = df_micro_final[df_micro_final['mediana_log_renda'] == 1]
aux1 = df_micro_final[df_micro_final['1o_tercil_renda'] == 1]
aux2 = df_micro_final[df_micro_final['2o_tercil_renda'] == 1]
aux3 = df_micro_final[df_micro_final['abaixo_log_renda'] == 1]
aux = aux.groupby(aux['mes']).sum()
aux1 = aux1.groupby(aux1['mes']).sum()
aux2 = aux2.groupby(aux2['mes']).sum()
aux3 = aux3.groupby(aux3['mes']).sum()
aux = aux[(aux.index <= '2019-09-01')]
aux1 = aux1[(aux1.index <= '2019-09-01')]
aux2 = aux2[(aux2.index <= '2019-09-01')]
aux3 = aux3[(aux3.index <= '2019-09-01')]

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Óbitos - Brasil (Conass)', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux3.index, aux3['CONASS'], color='red', linewidth=linewidth, label='1o Quartil - Renda per capita')
ax.plot(aux1.index, aux1['CONASS'], color='orangered', linewidth=linewidth, label='1o Tercil - Renda per capita')
ax.plot(aux.index, aux['CONASS'], color='darkorange', linewidth=linewidth, label='Abaixo da Mediana - Renda per capita')
ax.plot(aux2.index, aux2['CONASS'], color='mediumseagreen', linewidth=linewidth, label='2o Tercil - Renda per capita')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='upper left', frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Diff in Diff - Conass 2019 2.png', dpi=800)

print('Scatter DataSUS Idosos')
aux = df_micro_final

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'População Acima de 70 Anos e Óbitos (DataSUS)', fontweight="bold", fontsize=fontsize + 5)
scatter = ax.scatter(aux['acima70'], aux['SUS_Ób_Int'], alpha=0.5, c=aux['mediana_log_renda'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
legend1 = ax.legend(*scatter.legend_elements(num=1),
                    loc="upper left", title="Mediana - Renda per capita",frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.add_artist(legend1)
fig.tight_layout()
fig.savefig(chart_path + f'Scatter - DataSUS Idosos.png', dpi=800)

print('Scatter Conass Densidade')
fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'População Acima de 70 Anos e Óbitos (Conass)', fontweight="bold", fontsize=fontsize + 5)
scatter = ax.scatter(aux['densidade'], aux['CONASS'], alpha=0.5, c=aux['mediana_log_renda'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
legend1 = ax.legend(*scatter.legend_elements(num=1),
                    loc="upper left", title="Mediana - Renda per capita",frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.add_artist(legend1)
fig.tight_layout()
fig.savefig(chart_path + f'Scatter - Conass Densidade.png', dpi=800)

print('Scatter DataSUS Idosos')
fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'População Acima de 70 Anos e Óbitos (DataSUS)', fontweight="bold", fontsize=fontsize + 5)
scatter = ax.scatter(aux['acima70'], aux['SUS_Ób_Int'], alpha=0.5, c=aux['mediana_log_renda'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
legend1 = ax.legend(*scatter.legend_elements(num=1),
                    loc="upper left", title="Mediana - Renda per capita",frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.add_artist(legend1)
fig.tight_layout()
fig.savefig(chart_path + f'Scatter - DataSUS Idosos.png', dpi=800)

print('Scatter Conass Idosos')
fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'População Acima de 70 Anos e Óbitos (Conass)', fontweight="bold", fontsize=fontsize + 5)
scatter = ax.scatter(aux['acima70'], aux['CONASS'], alpha=0.5, c=aux['tercis'], zorder=5)
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
legend1 = ax.legend(*scatter.legend_elements(num=2),
                    loc="upper left", title="Tercis - Renda per capita",frameon=False, prop={'size': fontsize, 'weight': 'bold'})
ax.add_artist(legend1)
fig.tight_layout()
fig.savefig(chart_path + f'Scatter - Conass Idosos.png', dpi=800)

print('Casos Brasil')
aux = df_micro_final
aux = aux.groupby(aux['mes']).sum()

fig, ax = plt.subplots(figsize=figsize)
fig.suptitle(f'Casos de SRAG - Brasil', fontweight="bold", fontsize=fontsize + 5)
ax.plot(aux.index, aux['SRAG_Casos'], color='cornflowerblue', linewidth=linewidth)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
ax.grid(True, which='both', linestyle='--', alpha=0.5, zorder=0)
ax.axvspan('2020-04-01', '2020-07-01', color='grey', alpha=0.2, zorder=0)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
plt.yticks(weight='bold')
plt.xticks(weight='bold')
fig.tight_layout()
fig.savefig(chart_path + f'Casos Brasil.png', dpi=800)

