"""
Author: Arthur Alberti

- Rotina que coleta o DataFrame, filtra as variáveis para construir o DataFrame Final, faz a Análise Descritiva e as Regressões.

- Dados coletados das seguintes fontes: DataSUS, SIVEP-Gripe, CONASS, CNES, IBGE e Censo 2010.
"""
# ==========================================
# ===== Importing Libraries ================
# ==========================================
print('Importando as Bibliotecas')
import pandas as pd
import numpy as np
from time import time
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
import seaborn as sns

# =================================
# ===== Parameters ================
# =================================
print('Criando os Parâmetros')
save_path = r'C:\Users\arthu\Desktop\TCC\\'
read_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\\'
chart_path = r'C:\Users\arthu\Desktop\TCC\Regressions\Graphs\\'
regression_path = r'C:\Users\arthu\Desktop\TCC\Regressions\\'

start_time = time()

# ===============================================
# ===== Collecting the DataFrames ===============
# ===============================================
print('Abrindo o DataFrame')
df_micro = pd.read_excel(save_path + r'Analysis & Charts - Microrregioes.xlsx', sheet_name='Full', index_col='mes')

# ===============================================
# ===== Adjusting the DataFrames ================
# ===============================================
print('Ajustando os DataFrames')
print('Microrregioes')
df_micro_final = df_micro
df_micro['mes'] = df_micro.index

df_micro_final['log_renda'] = np.log(df_micro_final['renda']) # Logaritmo da Renda per Capita
df_micro_final['log_pib'] = np.log(df_micro_final['pib']) # Logaritmo do Produto Interno Bruto per Capita
df_micro_final['abaixo_log_renda'] = np.where(df_micro_final['log_renda'] <= np.percentile(df_micro_final['log_renda'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo da Renda per Capita
df_micro_final['abaixo_log_pib'] = np.where(df_micro_final['log_pib'] <= np.percentile(df_micro_final['log_pib'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo do Produto Interno Bruto per Capita
df_micro_final['acima_log_renda'] = np.where(df_micro_final['log_renda'] >= np.percentile(df_micro_final['log_renda'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 da Logaritmo da Renda per Capita
df_micro_final['acima_log_pib'] = np.where(df_micro_final['log_pib'] >= np.percentile(df_micro_final['log_pib'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 do Logaritmo do Produto Interno Bruto per Capita
df_micro_final['mediana_log_renda'] = np.where((df_micro_final['log_renda'] <= df_micro_final['log_renda'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo da Renda per Capita
df_micro_final['mediana_log_pib'] = np.where((df_micro_final['log_pib'] <= df_micro_final['log_pib'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo do Produto Interno Bruto per Capita
df_micro_final['primeiro_tercil_renda'] = np.where((df_micro_final['log_renda'] <= np.percentile(df_micro_final['log_renda'], 33)), 1, 0)
df_micro_final['segundo_tercil_renda'] = np.where(((df_micro_final['log_renda'] <= np.percentile(df_micro_final['log_renda'], 66)) & (df_micro_final['log_renda'] > np.percentile(df_micro_final['log_renda'], 33))), 1, 0)
df_micro_final['terceiro_tercil_renda'] = np.where((df_micro_final['log_renda'] > np.percentile(df_micro_final['log_renda'], 66)), 1, 0)
df_micro_final['tercis'] = 0
df_micro_final.loc[df_micro_final['primeiro_tercil_renda'] == 1, 'tercis'] = 1
df_micro_final.loc[df_micro_final['segundo_tercil_renda'] == 1, 'tercis'] = 2
df_micro_final.loc[df_micro_final['terceiro_tercil_renda'] == 1, 'tercis'] = 3
df_micro_final['pandemia'] = 0
df_micro_final.loc[(df_micro_final['mes'] >= '2020-04-01') & (df_micro_final['mes'] <= '2020-06-01'), 'pandemia'] = 1

for col in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']:
    df_micro_final[f'{col}'] = df_micro_final[col] * 100000 # Y por 100.000 Habitantes

df_micro_final.to_excel(save_path + r'DataFrame Final.xlsx')

print('Analysis')
aux = df_micro_final[df_micro_final['pandemia'] == 1]
print((2.505/aux['CONASS'].mean())*100)
print((2.018/aux['SUS_Ób_Int'].mean())*100)
aux = df_micro_final[df_micro_final['pandemia'] == 0]
print((2.505/aux['CONASS'].mean())*100)
print((2.018/aux['SUS_Ób_Int'].mean())*100)

print('Descrição das Variáveis')
writer = pd.ExcelWriter(save_path + r'Descriptive Analysis - Microrregioes.xlsx')
print('Full - Pré')
df_descriptive = df_micro_final.loc[: '2020-02-01']
aux = round(df_descriptive[['cod_mic', 'UF', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI',
       'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
       'limpeza', 'acima70', 'idosos', 'analfabetismo', 'desemprego',
       'agua_geral', 'esgoto_geral', 'em_comp', 'pop_025_sm', 'pop_05_sm',
       'pib', 'populacao', 'area', 'renda', 'densidade', 'mes', 'log_renda',
       'log_pib', 'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
       'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib', 'pandemia']].describe(), 2)
aux.to_excel(writer, f'Full - Pré')

print('Abaixo de 25% - Pré')
abaixo = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 1]
aux = round(abaixo[['cod_mic', 'UF', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI',
       'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
       'limpeza', 'acima70', 'idosos', 'analfabetismo', 'desemprego',
       'agua_geral', 'esgoto_geral', 'em_comp', 'pop_025_sm', 'pop_05_sm',
       'pib', 'populacao', 'area', 'renda', 'densidade', 'mes', 'log_renda',
       'log_pib', 'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
       'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib', 'pandemia']].describe(), 2)
aux.to_excel(writer, f'Abaixo 25% - Pré')

print('Acima de 25% - Pré')
acima = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 0]
aux = round(acima[['cod_mic', 'UF', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI',
       'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
       'limpeza', 'acima70', 'idosos', 'analfabetismo', 'desemprego',
       'agua_geral', 'esgoto_geral', 'em_comp', 'pop_025_sm', 'pop_05_sm',
       'pib', 'populacao', 'area', 'renda', 'densidade', 'mes', 'log_renda',
       'log_pib', 'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
       'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib', 'pandemia']].describe(), 2)
aux.to_excel(writer, f'Acima 25% - Pré')

print('Full - Pós')
df_descriptive = df_micro_final.loc['2020-03-01':]
aux = round(df_descriptive[['cod_mic', 'UF', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI',
       'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
       'limpeza', 'acima70', 'idosos', 'analfabetismo', 'desemprego',
       'agua_geral', 'esgoto_geral', 'em_comp', 'pop_025_sm', 'pop_05_sm',
       'pib', 'populacao', 'area', 'renda', 'densidade', 'mes', 'log_renda',
       'log_pib', 'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
       'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib', 'pandemia']].describe(), 2)
aux.to_excel(writer, f'Full - Pós')

print('Abaixo de 25% - Pós')
abaixo = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 1]
aux = round(abaixo[['cod_mic', 'UF', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI',
       'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
       'limpeza', 'acima70', 'idosos', 'analfabetismo', 'desemprego',
       'agua_geral', 'esgoto_geral', 'em_comp', 'pop_025_sm', 'pop_05_sm',
       'pib', 'populacao', 'area', 'renda', 'densidade', 'mes', 'log_renda',
       'log_pib', 'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
       'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib', 'pandemia']].describe(), 2)
aux.to_excel(writer, f'Abaixo 25% - Pós')

print('Acima de 25% - Pós')
acima = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 0]
aux = round(acima[['cod_mic', 'UF', 'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI',
       'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
       'limpeza', 'acima70', 'idosos', 'analfabetismo', 'desemprego',
       'agua_geral', 'esgoto_geral', 'em_comp', 'pop_025_sm', 'pop_05_sm',
       'pib', 'populacao', 'area', 'renda', 'densidade', 'mes', 'log_renda',
       'log_pib', 'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
       'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib', 'pandemia']].describe(), 2)
aux.to_excel(writer, f'Acima 25% - Pós')

writer.save()

# ===============================================
# ===== Analysis - Regressions ==================
# ===============================================
print('Microrregioes')
print('Distribuições das Variáveis Dependentes')
for col in ['SRAG_Casos', 'SRAG_UTI', 'SRAG_Óbitos', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']:
    bins=[df_micro_final[f'{col}'].std()/2,  df_micro_final[f'{col}'].std(), df_micro_final[f'{col}'].std()*2, df_micro_final[f'{col}'].std()*3, df_micro_final[f'{col}'].std()*4, df_micro_final[f'{col}'].std()*5,
          df_micro_final[f'{col}'].std()*6, df_micro_final[f'{col}'].std()*7, df_micro_final[f'{col}'].std()*8, df_micro_final[f'{col}'].std()*9, df_micro_final[f'{col}'].std()*10, df_micro_final[f'{col}'].std()*11,
          df_micro_final[f'{col}'].std()*12, df_micro_final[f'{col}'].std()*13]
    sns.displot(x=df_micro_final[f'{col}'], bins=bins, kind='hist')
    plt.savefig(chart_path + f'{col}.png')

print('Regressões')
print('Principais variáveis resposta: Conass, SRAG_Óbitos e SUS_Ób_Int')
print('Principais variáveis explcativas: mediana_log_renda, abaixo_log_renda e pop_05_sm')
# TODO FAZER REGRESSAO SEM CONTROLES
for y in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']: # Y por 100.000 Habitantes
    writer = pd.ExcelWriter(regression_path + f'{y} (OLS) - Microrregioes.xlsx')

    for x in ['log_renda', 'mediana_log_renda', 'abaixo_log_renda', 'acima_log_renda', # Renda per Capita
              'log_pib', 'mediana_log_pib', 'abaixo_log_pib',  'acima_log_pib', # Produto Interno Bruto per Capita
              'pop_05_sm', 'pop_025_sm', # Censo 2010 - População de Baixa Renda (%)
              ]: # TODO - Leitos Absoluto - colocar em T-1 ???
        ols_reg = ols(formula=f'{y} ~ UF + densidade + populacao +' # IBGE - TODO URBAN POPULATION RATE - Controle de mês?
                              f'idosos + acima70 +' # Censo 2010 - Idosos (%)
                              f'analfabetismo +' # Censo 2010 - Analfabetismo (%)
                              f'desemprego +' # Censo 2010 - Desemprego (%)
                              f'em_comp +' # Censo 2010 - Escolaridade (%) - Ensino Médio Completo
                              f'esgoto_geral +' # Censo 2010 - Esgoto (%) - Rede Geral de Esgoto
                              f'agua_geral +' # Censo 2010 - Água (%) - Rede Geral de Água
                              f'limpeza +' # Censo 2010 - Lixo (%) - Serviço de Limpeza
                              f'{x}*pandemia', # IBGE - Proxy da Renda * Dummy de Pandemia - TODO TROCAR POR DUMMY DE MÊS
                  data=df_micro_final).fit()

        ols_reg = pd.read_html(ols_reg.summary().tables[1].as_html(), header=0, index_col=0)[0]
        ols_reg.to_excel(writer, sheet_name=f'{x}')

    writer.close()


print('Gráficos - Brasil') # TODO GRAFICOS
df_brasil = df_micro_final.groupby(df_micro_final['mes']).sum()

# ===============================================
# ===== Saving the DataFrames ===================
# ===============================================
writer = pd.ExcelWriter(save_path + r'Analysis - Microrregioes.xlsx')
df_micro_final.to_excel(writer, sheet_name='Full')
writer.close()

print('Levou ' + str(round((time() - start_time)/60, 1)) + ' minutos para rodar a rotina.')
