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
df_micro = pd.read_excel(save_path + r'Analysis & Charts - Microrregioes.xlsx', sheet_name='Full', index_col='mes')

# ===============================================
# ===== Adjusting the DataFrames ================
# ===============================================
print('Ajustando os DataFrames')
print('Municipios')
df['mes'] = df.index

df_final = df[['mes', 'UF', 'cod_mic', 'mic', 'cod_mun', 'mun', # Vari
               'RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', # IBGE (Absoluto)
               'Leitos', # CNES (Absoluto)
               'idosos', # Censo 2010 - Idosos Morando com Parente (%)
               'desemprego', # Censo 2010 - Taxa de Desemprego (%)
               'analfabetismo', # Censo 2010 - Taxa de Analfabetismo (%)
               'acima50', 'acima60', 'acima70', '80a150', # Censo 2010 - População (%)
               'renda_per_capita', 'pop_05_sm', 'pop_025_sm', # Censo 2010 - Renda (%)
               'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', # Censo 2010 - Escolaridade (%)
               'esgoto_geral', 'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio', 'esgoto_outro', 'esgoto_sem',  # Censo 2010 - Esgoto (%)
               'agua_geral', 'poco', 'poco_fora', 'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio', 'poco_aldeia', 'poco_fora_aldeia', 'agua_outra',  # Censo 2010 - Água (%)
               'limpeza', 'cacamba', 'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', # Censo 2010 - Lixo (%)
               'SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', # SIVEP-Gripe (Absoluto)
               'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', # DataSUS (Absoluto)
               'CONASS', # CONASS (Absoluto)
               ]]

df_final['renda_per_capita'] = df_final['renda_per_capita'].replace({np.nan: 1}) # Corrigindo os NAs da Renda per Capita para passar o Logaritmo
df_final['log_renda'] = np.log(df_final['renda_per_capita']) # Logaritmo da Renda per Capita
df_final['log_pib'] = np.log(df_final['pib_per_capita']) # Logaritmo do Produto Interno Bruto per Capita
df_final['abaixo_log_renda'] = np.where(df_final['log_renda'] <= np.percentile(df_final['log_renda'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo da Renda per Capita
df_final['abaixo_log_pib'] = np.where(df_final['log_pib'] <= np.percentile(df_final['log_pib'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo do Produto Interno Bruto per Capita
df_final['acima_log_renda'] = np.where(df_final['log_renda'] >= np.percentile(df_final['log_renda'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 da Logaritmo da Renda per Capita
df_final['acima_log_pib'] = np.where(df_final['log_pib'] >= np.percentile(df_final['log_pib'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 do Logaritmo do Produto Interno Bruto per Capita
df_final['mediana_log_renda'] = np.where((df_final['log_renda'] <= df_final['log_renda'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo da Renda per Capita
df_final['mediana_log_pib'] = np.where((df_final['log_pib'] <= df_final['log_pib'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo do Produto Interno Bruto per Capita
df_final['pandemia'] = 0
df_final.loc[(df_final['mes'] >= '2020-03-01') & (df_final['mes'] <= '2020-06-01'), 'pandemia'] = 1

for col in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']:
    df_final[f'{col}_pop'] = (df_final[col] / df_final['populacao'])*100000 # Y por 100.000 Habitantes

writer = pd.ExcelWriter(save_path + r'Analysis - Stata & R.xlsx')
df_final.to_excel(writer, sheet_name='Full')
writer.close()

print('Microrregioes')
df_micro_final = df_micro
df_micro['mes'] = df_micro.index

df_micro_final['renda'] = df_micro_final['renda'].replace({np.nan: 1}) # Corrigindo os NAs da Renda per Capita para passar o Logaritmo
df_micro_final['log_renda'] = np.log(df_micro_final['renda']) # Logaritmo da Renda per Capita
df_micro_final['log_pib'] = np.log(df_micro_final['pib']) # Logaritmo do Produto Interno Bruto per Capita
df_micro_final['abaixo_log_renda'] = np.where(df_micro_final['log_renda'] <= np.percentile(df_micro_final['log_renda'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo da Renda per Capita
df_micro_final['abaixo_log_pib'] = np.where(df_micro_final['log_pib'] <= np.percentile(df_micro_final['log_pib'], 25), 1, 0) # Dummy - se o município se encontra abaixo do percetil 25 do Logaritmo do Produto Interno Bruto per Capita
df_micro_final['acima_log_renda'] = np.where(df_micro_final['log_renda'] >= np.percentile(df_micro_final['log_renda'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 da Logaritmo da Renda per Capita
df_micro_final['acima_log_pib'] = np.where(df_micro_final['log_pib'] >= np.percentile(df_micro_final['log_pib'], 75), 1, 0) # Dummy - se o município se encontra acima do percetil 75 do Logaritmo do Produto Interno Bruto per Capita
df_micro_final['mediana_log_renda'] = np.where((df_micro_final['log_renda'] <= df_micro_final['log_renda'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo da Renda per Capita
df_micro_final['mediana_log_pib'] = np.where((df_micro_final['log_pib'] <= df_micro_final['log_pib'].median()), 1, 0) # Dummy - se o município se encontra abaixo da mediana do Logaritmo do Produto Interno Bruto per Capita
df_micro_final['pandemia'] = 0
df_micro_final.loc[(df_micro_final['mes'] >= '2020-04-01') & (df_micro_final['mes'] <= '2020-07-01'), 'pandemia'] = 1

for col in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']:
    df_micro_final[f'{col}'] = df_micro_final[col] * 100000 # Y por 100.000 Habitantes

writer = pd.ExcelWriter(save_path + r'Analysis - Microrregioes.xlsx')
df_final.to_excel(writer, sheet_name='Full')
writer.close()

print('Descrição das Variáveis')
writer = pd.ExcelWriter(save_path + r'Descriptive Analysis.xlsx')
print('Full - Pré')
df_descriptive = df_final.loc[: '2020-02-01']
aux = round(df_descriptive[['RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', 'Leitos', 'idosos', 'desemprego',
            'analfabetismo', 'acima50', 'acima60', 'acima70', '80a150', 'renda_per_capita', 'pop_05_sm', 'pop_025_sm',
            'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral',
            'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio',
            'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora',
            'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio',
            'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba',
            'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', 'log_renda', 'log_pib',
            'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
            'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']].describe(), 2)
aux.to_excel(writer, f'Full - Pré')

print('Abaixo de 25% - Pré')
abaixo = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 1]
aux = round(abaixo[['RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', 'Leitos', 'idosos', 'desemprego',
            'analfabetismo', 'acima50', 'acima60', 'acima70', '80a150', 'renda_per_capita', 'pop_05_sm', 'pop_025_sm',
            'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral',
            'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio',
            'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora',
            'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio',
            'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba',
            'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', 'log_renda', 'log_pib',
            'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
            'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']].describe(), 2)
aux.to_excel(writer, f'Abaixo 25% - Pré')

print('Acima de 25% - Pré')
acima = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 0]
aux = round(acima[['RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', 'Leitos', 'idosos', 'desemprego',
            'analfabetismo', 'acima50', 'acima60', 'acima70', '80a150', 'renda_per_capita', 'pop_05_sm', 'pop_025_sm',
            'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral',
            'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio',
            'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora',
            'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio',
            'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba',
            'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', 'log_renda', 'log_pib',
            'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
            'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']].describe(), 2)
aux.to_excel(writer, f'Acima 25% - Pré')

print('Full - Pós')
df_descriptive = df_final.loc['2020-03-01':]
aux = round(df_descriptive[['RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', 'Leitos', 'idosos', 'desemprego',
            'analfabetismo', 'acima50', 'acima60', 'acima70', '80a150', 'renda_per_capita', 'pop_05_sm', 'pop_025_sm',
            'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral',
            'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio',
            'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora',
            'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio',
            'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba',
            'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', 'log_renda', 'log_pib',
            'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
            'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']].describe(), 2)
aux.to_excel(writer, f'Full - Pós')

print('Abaixo de 25% - Pós')
abaixo = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 1]
aux = round(abaixo[['RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', 'Leitos', 'idosos', 'desemprego',
            'analfabetismo', 'acima50', 'acima60', 'acima70', '80a150', 'renda_per_capita', 'pop_05_sm', 'pop_025_sm',
            'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral',
            'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio',
            'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora',
            'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio',
            'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba',
            'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', 'log_renda', 'log_pib',
            'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
            'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']].describe(), 2)
aux.to_excel(writer, f'Abaixo 25% - Pós')

print('Acima de 25% - Pós')
acima = df_descriptive.loc[df_descriptive['abaixo_log_renda'] == 0]
aux = round(acima[['RM', 'pib', 'pib_per_capita', 'populacao', 'densidade_pop', 'Leitos', 'idosos', 'desemprego',
            'analfabetismo', 'acima50', 'acima60', 'acima70', '80a150', 'renda_per_capita', 'pop_05_sm', 'pop_025_sm',
            'fundamental_inc', 'em_inc', 'em_comp', 'escola_na', 'esgoto_geral',
            'fossa_septica', 'fossa_rudimentar', 'vala', 'esgoto_rio',
            'esgoto_outro', 'esgoto_sem', 'agua_geral', 'poco', 'poco_fora',
            'carro_pipa', 'chuva_cisterna', 'chuva_outra', 'agua_rio',
            'poco_aldeia', 'poco_fora_aldeia', 'agua_outra', 'limpeza', 'cacamba',
            'queimado', 'enterrado', 'terreno_baldio', 'lixo_rio', 'lixo_outro', 'log_renda', 'log_pib',
            'abaixo_log_renda', 'abaixo_log_pib', 'acima_log_renda',
            'acima_log_pib', 'mediana_log_renda', 'mediana_log_pib',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']].describe(), 2)
aux.to_excel(writer, f'Acima 25% - Pós')

writer.save()

print('Gráficos - Brasil') # TODO GRAFICOS
df_brasil = df_final.groupby(df_final['mes']).sum()


# ===============================================
# ===== Analysis - Regressions ==================
# ===============================================
print('Municipios')
print('Distribuições das Variáveis Dependentes')
for col in [ # 'SRAG_Casos', 'SRAG_UTI', 'SRAG_Óbitos', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS',
            'SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']:
    bins=[df_final[f'{col}'].std()/2,  df_final[f'{col}'].std(), df_final[f'{col}'].std()*2, df_final[f'{col}'].std()*3, df_final[f'{col}'].std()*4, df_final[f'{col}'].std()*5,
          df_final[f'{col}'].std()*6, df_final[f'{col}'].std()*7, df_final[f'{col}'].std()*8, df_final[f'{col}'].std()*9, df_final[f'{col}'].std()*10, df_final[f'{col}'].std()*11,
          df_final[f'{col}'].std()*12, df_final[f'{col}'].std()*13]
    sns.displot(x=df_final[f'{col}'], bins=bins, kind='hist')
    print(sns)
    plt.savefig(chart_path + r'\Histogramas\\' + f'{col} (Histograma).png')

print('Regressões')
for y in ['SRAG_Casos_pop', 'SRAG_Óbitos_pop', 'SRAG_UTI_pop', 'SUS_Ób_Int_pop', 'SUS_Ób_Res_pop', 'SUS_Int_Int_pop', 'SUS_Int_Res_pop', 'CONASS_pop']: # Y por 10.000 Habitantes
    writer = pd.ExcelWriter(regression_path + f'{y} (OLS).xlsx')

    for x in ['log_renda', 'mediana_log_renda', 'abaixo_log_renda', 'acima_log_renda', # Renda per Capita
              'log_pib', 'mediana_log_pib', 'abaixo_log_pib',  'acima_log_pib', # Produto Interno Bruto per Capita
              'pop_05_sm', 'pop_025_sm', # Censo 2010 - População de Baixa Renda (%)
              ]: # TODO - Leitos Absoluto - colocar em T-1 ???
        ols_reg = ols(formula=f'{y} ~ densidade_pop + populacao + UF + RM +' # IBGE - TODO URBAN POPULATION RATE - Controle de mês?
                              f'idosos + acima70 +' # Censo 2010 - Idosos (%)
                              f'analfabetismo +' # Censo 2010 - Analfabetismo (%)
                              f'desemprego +' # Censo 2010 - Desemprego (%)
                              f'em_comp +' # Censo 2010 - Escolaridade (%) - Ensino Médio Completo
                              f'esgoto_geral +' # Censo 2010 - Esgoto (%) - Rede Geral de Esgoto
                              f'agua_geral +' # Censo 2010 - Água (%) - Rede Geral de Água
                              f'limpeza +' # Censo 2010 - Lixo (%) - Serviço de Limpeza
                              f'{x}*pandemia', # IBGE - Proxy da Renda * Dummy de Pandemia - TODO TROCAR POR DUMMY DE MÊS
                  data=df_final).fit()

        ols_reg = pd.read_html(ols_reg.summary().tables[1].as_html(), header=0, index_col=0)[0]
        ols_reg.to_excel(writer, sheet_name=f'{x}')

    writer.close()

print('Microrregioes')
print('Regressões')
for y in ['SRAG_Casos', 'SRAG_Óbitos', 'SRAG_UTI', 'SUS_Ób_Int', 'SUS_Ób_Res', 'SUS_Int_Int', 'SUS_Int_Res', 'CONASS']: # Y por 100.000 Habitantes
    writer = pd.ExcelWriter(regression_path + f'{y} (OLS) - Microrregioes.xlsx')

    for x in ['log_renda', 'mediana_log_renda', 'abaixo_log_renda', 'acima_log_renda', # Renda per Capita
              'log_pib', 'mediana_log_pib', 'abaixo_log_pib',  'acima_log_pib', # Produto Interno Bruto per Capita
              'pop_05_sm', 'pop_025_sm', # Censo 2010 - População de Baixa Renda (%)
              ]: # TODO - Leitos Absoluto - colocar em T-1 ???
        ols_reg = ols(formula=f'{y} ~ densidade + populacao +' # IBGE - TODO URBAN POPULATION RATE - Controle de mês?
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

# ===============================================
# ===== Saving the DataFrames ===================
# ===============================================
writer = pd.ExcelWriter(save_path + r'Analysis - Stata.xlsx')
df_final.to_excel(writer, sheet_name='Full')
writer.close()

print('Levou ' + str(round((time() - start_time)/60, 1)) + ' minutos para rodar a rotina.')
