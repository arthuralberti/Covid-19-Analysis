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
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns

# =================================
# ===== Parameters ================
# =================================
print('Criando os Parâmetros')
save_path = r'C:\Users\arthu\Desktop\TCC\\'
read_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\\'
chart_path = r'C:\Users\arthu\Desktop\TCC\Chartbooks\\'
regression_path = r'C:\Users\arthu\Desktop\TCC\Regressions\\'

start_time = time()

# ===============================================
# ===== Collecting the DataFrames ===============
# ===============================================
print('Abrindo o DataFrame')
df = pd.read_excel(save_path + r'Analysis & Charts.xlsx', sheet_name='Full', index_col='mes')

# ===============================================
# ===== Adjusting the DataFrames ================
# ===============================================
print('Ajustando o DataFrame Final')
df['mes'] = df.index

df_final = df[['mes', 'UF', 'cod_mic', 'mic', 'cod_mun', 'mun', 'RM', 'pib', 'pib_per_capita', 'area_mun', 'populacao', # IBGE (Absoluto)
               'Leitos', # CNES (Absoluto)
               'renda_per_capita', 'pop_05_sm', 'pop_025_sm', 'idosos', # Censo 2010 - Lixo (%)
               'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral', 'fossa_septica', # Censo 2010 - Escolaridade (%)
               'fossa_rudimentar', 'vala', 'esgoto_rio', 'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora', 'carro_pipa', # Censo 2010 - Esgoto (%)
               'chuva_cisterna', 'chuva_outra', 'agua_rio', 'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba', 'queimado', # Censo 2010 - Água (%)
               'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', # Censo 2010 - Lixo (%)
               'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', # SIVEP-Gripe (Absoluto)
               'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', # DataSUS (Absoluto)
               'CONASS', # CONASS (Absoluto)
               ]]

df_final['renda_per_capita'] = df_final['renda_per_capita'].replace({0: 1}) # Corrigindo os NAs da Renda per Capita para passar o Logaritmo
df_final['log_renda'] = np.log(df_final['renda_per_capita']) # Logaritmo da Renda per Capita
df_final['log_pib'] = np.log(df_final['pib_per_capita']) # Logaritmo do Produto Interno Bruto per Capita
df_final['abaixo_log_renda'] = np.where(df_final['log_renda'] <= np.percentile(df_final['log_renda'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo da Renda per Capita
df_final['abaixo_log_pib'] = np.where(df_final['log_pib'] <= np.percentile(df_final['log_pib'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo do Produto Interno Bruto per Capita
df_final['acima_log_renda'] = np.where(df_final['log_renda'] >= np.percentile(df_final['log_renda'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 da Logaritmo da Renda per Capita
df_final['acima_log_pib'] = np.where(df_final['log_pib'] >= np.percentile(df_final['log_pib'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 do Logaritmo do Produto Interno Bruto per Capita
df_final['mediana_log_renda'] = np.where((df_final['log_renda'] <= df_final['log_renda'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo da Renda per Capita
df_final['mediana_log_pib'] = np.where((df_final['log_pib'] <= df_final['log_pib'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo do Produto Interno Bruto per Capita

for col in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']:
    df_final[f'{col}_pop'] = (df_final[col] / df_final['populacao'])*10000 # Y por 10.000 Habitantes

print('Descrição das Variáveis') # TODO ESCOLHER VARIÁVEIS PARA ANALISAR - OLHAR RM
for col in df_final.columns:
    try:
        print(round(df_final[col].describe(), 2))
    except TypeError:
        continue

# ===============================================
# ===== Analysis - Regressions ==================
# ===============================================
print('Distribuições das Variáveis Dependentes')
for col in ['SRAG_Casos', 'SRAG_UTI', 'SRAG_Óbitos', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']:
    bins=[df_final[f'{col}'].std()/2,  df_final[f'{col}'].std(), df_final[f'{col}'].std()*2, df_final[f'{col}'].std()*3, df_final[f'{col}'].std()*4, df_final[f'{col}'].std()*5,
          df_final[f'{col}'].std()*6, df_final[f'{col}'].std()*7, df_final[f'{col}'].std()*8, df_final[f'{col}'].std()*9, df_final[f'{col}'].std()*10, df_final[f'{col}'].std()*11,
          df_final[f'{col}'].std()*12, df_final[f'{col}'].std()*13]
    sns.displot(x=df_final[f'{col}'], bins=bins, kind='hist')
    print(sns)
    plt.savefig(chart_path + r'\Histogramas\\' + f'{col} (Histograma).png')

print('Regressões')
for y in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS', # Y em Absoluto
          'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']: # Y por 10.000 Habitantes
    writer = pd.ExcelWriter(regression_path + f'{y} (OLS).xlsx')

    for x in ['log_renda', 'abaixo_log_renda', 'acima_log_renda', 'mediana_log_renda', # Renda per Capita
              'log_pib', 'abaixo_log_pib',  'acima_log_pib', 'mediana_log_pib', # Produto Interno Bruto per Capita
              'pop_05_sm', 'pop_025_sm', # Censo 2010 - População de Baixa Renda (%)
              'Leitos']: # Leitos Absoluto - colocar em T-1 ???
        ols_reg = ols(formula=f'{y} ~ area_mun + populacao + UF + RM + log_pib +' # IBGE
                              f'idosos +' # Censo 2010 - Idosos (%)
                              f'fundamental_inc + em_inc + em_comp + escola_na +' # Censo 2010 - Escolaridade (%)
                              f'esgoto_geral + fossa_septica + fossa_rudimentar + vala + esgoto_rio + esgoto_outro + esgoto_sem +' # Censo 2010 - Esgoto (%)
                              f'agua_geral + poco + poco_fora + carro_pipa + chuva_cisterna + chuva_outra + agua_rio + poco_aldeia + poco_fora_aldeia + agua_outra +' # Censo 2010 - Água (%)
                              f'limpeza + cacamba + queimado + enterrado + terreno_baldio + lixo_rio + lixo_outro +' # Censo 2010 - Lixo (%)
                              f'{x}*mes', # IBGE - Proxy da Renda vs Mês
                  data=df_final).fit()

        ols_reg = pd.read_html(ols_reg.summary().tables[1].as_html(), header=0, index_col=0)[0]
        ols_reg.to_excel(writer, sheet_name=f'{x}')

    writer.close()

# ===============================================
# ===== Saving the DataFrames ===================
# ===============================================
writer = pd.ExcelWriter(save_path + r'Analysis - Stata.xlsx')
df_final.to_excel(writer, sheet_name='Full')
writer.close()

print('Levou ' + str(round((time() - start_time)/60, 1)) + ' minutos para rodar a rotina.')

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