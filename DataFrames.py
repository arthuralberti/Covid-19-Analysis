"""
Author: Arthur Alberti

- Routine that collects the DataFrames, cleans them and leave them ready for the Charts and Analysis.

- Data collected from: DataSUS, SIVEP-Gripe, IBGE and CONASS.
"""
# ==========================================
# ===== Importing Libraries ================
# ==========================================
print('Importing Libraries')
import pandas as pd
import numpy as np
from time import time
from unidecode import unidecode

# =================================
# ===== Parameters ================
# =================================
print('Creating Parameters')
save_path = r'C:\Users\arthu\Desktop\TCC\\'
read_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\\'
chart_path = r'C:\Users\arthu\Desktop\TCC\Chartbooks\\'
data_sus_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\DataSUS\\'
cnes_path = r'C:\Users\arthu\Desktop\TCC\DataFrames\CNES\\'

start_time = time()

# ===============================================
# ===== Collecting the DataFrames ===============
# ===============================================
print('Opening DataFrames')
df_srag_20_21 = pd.read_csv(read_path + r'SRAG - Final.csv', low_memory=False)
df_srag_19 = pd.read_csv(read_path + r'INFLUD19-29-03-2021.csv', sep=';', low_memory=False, encoding='ISO-8859–1')

df_conass_19 = pd.read_excel(read_path + r'CONASS_2019.xlsx')
df_conass_20 = pd.read_excel(read_path + r'CONASS_2020.xlsx', sheet_name='TOTAL')

df_pib = pd.read_excel(read_path + r'PIB_2010_2018.xlsx')
df_area = pd.read_excel(read_path + r'Area_2020.xls')

toc = time()
print(str(round((toc - start_time) / 60, 1)) + ' minutes.')

# ==============================================
# ===== Adjusting the DataFrame ================
# ==============================================
print('Adjusting the DataFrames')

print('Área')
df_area = df_area.drop(columns={'ID', 'CD_GCUF', 'NM_UF', 'NM_MUN_2020'}).rename(columns={'NM_UF_SIGLA': 'UF', 'CD_GCMUN': 'cod_mun', 'AR_MUN_2020': 'area_mun'})
df_area['cod_mun'] = df_area['cod_mun'].dropna().astype(int).astype(str).str[:-1]

tic = time()
print(str(round((tic - toc) / 60, 1)) + ' minutes.')

print('PIB')
cols = {'Sigla da Unidade da Federação': 'UF',
        'Código do Município': 'cod_mun',
        'Nome do Município': 'mun',
        'Região Metropolitana': 'RM',
        'Código da Microrregião': 'cod_mic',
        'Nome da Microrregião': 'mic',
        'Amazônia Legal': 'amazonia_legal',
        'Produto Interno Bruto, \na preços correntes\n(R$ 1.000)': 'pib',
        'Produto Interno Bruto per capita, \na preços correntes\n(R$ 1,00)': 'pib_per_capita',
        'Atividade com maior valor adicionado bruto': 'atividade'}

df_pib = df_pib[df_pib['Ano'] >= 2018]
df_pib = df_pib.drop(df_pib.columns.difference(cols), axis=1)
df_pib = df_pib.rename(columns=cols)

df_pib['75% - 50%'] = np.where((df_pib['pib_per_capita'] < np.percentile(df_pib['pib_per_capita'], 75)) & (df_pib['pib_per_capita'] >= np.percentile(df_pib['pib_per_capita'], 50)), 1, 0)
df_pib['50% - 25%'] = np.where((df_pib['pib_per_capita'] < np.percentile(df_pib['pib_per_capita'], 50)) & (df_pib['pib_per_capita'] >= np.percentile(df_pib['pib_per_capita'], 25)), 1, 0)
df_pib['75% - 25%'] = np.where((df_pib['pib_per_capita'] < np.percentile(df_pib['pib_per_capita'], 75)) & (df_pib['pib_per_capita'] >= np.percentile(df_pib['pib_per_capita'], 25)), 1, 0)
df_pib['75% +'] = np.where((df_pib['pib_per_capita'] >= np.percentile(df_pib['pib_per_capita'], 75)), 1, 0)
df_pib['25% -'] = np.where((df_pib['pib_per_capita'] < np.percentile(df_pib['pib_per_capita'], 25)), 1, 0)
df_pib['mediana +'] = np.where((df_pib['pib_per_capita'] >= df_pib['pib_per_capita'].median()), 1, 0)
df_pib['mediana -'] = np.where((df_pib['pib_per_capita'] < df_pib['pib_per_capita'].median()), 1, 0)
df_pib['25% +'] = np.where((df_pib['25% -'] == 0), 1, 0)

df_pib['RM'] = df_pib['RM'].str[:2]
df_pib['Ag'] = np.where((df_pib['RM'] == 'Ag'), 1, 0)
df_pib['RI'] = np.where((df_pib['RM'] == 'RI'), 1, 0)
df_pib['RM'] = np.where((df_pib['RM'] == 'RM'), 1, 0)
df_pib['RM'] = df_pib['RM'] + df_pib['Ag'] + df_pib['RI']
df_pib['cod_mun'] = df_pib['cod_mun'].astype(str).str[:-1]
df_pib['populacao'] = ((df_pib['pib'] * 1000) / df_pib['pib_per_capita']).astype(int)
df_pib = df_pib.drop(columns=['Ag', 'RI'])

toc = time()
print(str(round((toc - tic) / 60, 1)) + ' minutes.')

print('SRAG')
cols = {'DT_NOTIFIC': 'date', 'SEM_NOT': 'semana_epid', 'SG_UF_NOT': 'uf_notificacao', 'ID_MUNICIP': 'mun_notificacao',
        'CS_SEXO': 'sexo', 'DT_NASC': 'aniversario', 'NU_IDADE_N': 'idade', 'CS_GESTATNT': 'gestante', 'CS_RACA': 'cor',
        'CS_ETINIA': 'etinia', 'CS_ESCOL_N': 'escolaridade', 'CO_MUN_NOT': 'cod_mun_notificacao',
        'SG_UF': 'uf_residencia',
        'ID_MN_RESI': 'mun_residencia', 'CO_MUN_RES': 'cod_mun_residencia', 'CS_ZONA': 'zona_residencia',
        'ID_PAIS': 'pais_residencia',
        'FEBRE': 'febre', 'TOSSE': 'tosse', 'GARGANTA': 'dor_garganta', 'DISPNEIA': 'dispneia',
        'DESC_RESP': 'desconforto_resp',
        'SATURACAO': 'saturacao', 'DIARREIA': 'diarreia', 'VOMITO': 'vomito', 'DOR_ABD': 'dor_abdominal',
        'FADIGA': 'fadiga',
        'PERD_OLFT': 'perda_olf', 'PERD_PALA': 'perda_pala', 'FATOR_RISC': 'fatores_de_risco', 'VACINA': 'vacina_gripe',
        'HOSPITAL': 'internacao', 'DT_INTERNA': 'data_internacao', 'SG_UF_INTE': 'uf_internacao',
        'ID_MN_INTE': 'mun_internacao',
        'CO_MU_INTE': 'cod_mun_internacao', 'UTI': 'uti', 'SUPORT_VEN': 'sup_ventilador',
        'RES_AN': 'resultado_antigeno',
        'PCR_RESUL': 'resultado_pcr', 'EVOLUCAO': 'cura_obito', 'CLASSI_FIN': 'tipos_SRAG', 'TP_IDADE': 'tipo_idade',
        'VACINA_COV': 'vacina', 'DOSE_1_COV': 'data_1a_dose', 'DOSE_2_COV': 'data_2a_dose',
        'LAB_PR_COV': 'produtor_vacina',
        'FNT_IN_COV': 'fonte_vacina'}

df_srag_20 = df_srag_20_21.loc[(df_srag_20_21['data'] >= '2020-01-01') & (df_srag_20_21['data'] <= '2020-12-31')]
df_srag_19 = df_srag_19.drop(df_srag_19.columns.difference(cols), axis=1)
df_srag_19 = df_srag_19.rename(columns=cols)

df_srag_19['data'] = df_srag_19['date'].str[6:] + '-' + df_srag_19['date'].str[3:5] + '-' + df_srag_19['date'].str[0:2]
df_srag_19['cura_obito'] = df_srag_19['cura_obito'].replace({1: 'Cura', 2: 'Óbito'})

df_srag_19['data'] = pd.to_datetime(df_srag_19['data'])
df_srag_20['data'] = pd.to_datetime(df_srag_20['data'])

df_srag_19['mes'] = df_srag_19['date'].str[3:5]
df_srag_20['mes'] = df_srag_20['date'].str[3:5]

df_srag_19 = df_srag_19.dropna(subset=['cod_mun_internacao'])
df_srag_20 = df_srag_20.dropna(subset=['cod_mun_internacao'])

df_srag_19 = df_srag_19.rename(columns={'cod_mun_internacao': 'cod_mun'})
df_srag_20 = df_srag_20.rename(columns={'cod_mun_internacao': 'cod_mun'})

df_srag_19['cod_mun'] = df_srag_19['cod_mun'].astype(str).str[:-2]
df_srag_20['cod_mun'] = df_srag_20['cod_mun'].astype(str).str[:-2]

df_srag_obito_19 = df_srag_19[df_srag_19['cura_obito'] == 'Óbito']
df_srag_uti_19 = df_srag_19[df_srag_19['uti'] == 1]

df_srag_obito_20 = df_srag_20[df_srag_20['cura_obito'] == 'Óbito']
df_srag_uti_20 = df_srag_20[df_srag_20['uti'] == 1]

df_srag_casos_19 = df_srag_19.groupby(['mes', 'cod_mun'])['data'].count()
df_srag_casos_20 = df_srag_20.groupby(['mes', 'cod_mun'])['sexo'].count()

df_srag_obito_19 = df_srag_obito_19.groupby(['mes', 'cod_mun'])['data'].count()
df_srag_obito_20 = df_srag_obito_20.groupby(['mes', 'cod_mun'])['sexo'].count()

df_srag_uti_19 = df_srag_uti_19.groupby(['mes', 'cod_mun'])['data'].count()
df_srag_uti_20 = df_srag_uti_20.groupby(['mes', 'cod_mun'])['sexo'].count()

df_srag_casos_19 = df_srag_casos_19.reset_index()
df_srag_casos_20 = df_srag_casos_20.reset_index()
df_srag_casos_19['mes'] = df_srag_casos_19['mes'].astype(str)
df_srag_casos_20['mes'] = df_srag_casos_20['mes'].astype(str)
df_srag_casos_19['mes'] = df_srag_casos_19['mes'] + '-01-2019'
df_srag_casos_20['mes'] = df_srag_casos_20['mes'] + '-01-2020'

df_srag_obito_19 = df_srag_obito_19.reset_index()
df_srag_obito_20 = df_srag_obito_20.reset_index()
df_srag_obito_19['mes'] = df_srag_obito_19['mes'].astype(str)
df_srag_obito_20['mes'] = df_srag_obito_20['mes'].astype(str)
df_srag_obito_19['mes'] = df_srag_obito_19['mes'] + '-01-2019'
df_srag_obito_20['mes'] = df_srag_obito_20['mes'] + '-01-2020'

df_srag_uti_19 = df_srag_uti_19.reset_index()
df_srag_uti_20 = df_srag_uti_20.reset_index()
df_srag_uti_19['mes'] = df_srag_uti_19['mes'].astype(str)
df_srag_uti_20['mes'] = df_srag_uti_20['mes'].astype(str)
df_srag_uti_19['mes'] = df_srag_uti_19['mes'] + '-01-2019'
df_srag_uti_20['mes'] = df_srag_uti_20['mes'] + '-01-2020'

df_srag_casos_19 = df_srag_casos_19.rename(columns={'data': 'SRAG Casos 19'})
df_srag_casos_20 = df_srag_casos_20.rename(columns={'sexo': 'SRAG Casos 20'})
df_srag_obito_19 = df_srag_obito_19.rename(columns={'data': 'SRAG Óbitos 19'})
df_srag_obito_20 = df_srag_obito_20.rename(columns={'sexo': 'SRAG Óbitos 20'})
df_srag_uti_19 = df_srag_uti_19.rename(columns={'data': 'SRAG UTI 19'})
df_srag_uti_20 = df_srag_uti_20.rename(columns={'sexo': 'SRAG UTI 20'})

df_srag = df_srag_casos_19.merge(df_srag_casos_20, on=['mes', 'cod_mun'], how='outer')
df_srag = df_srag.merge(df_srag_obito_19, on=['mes', 'cod_mun'], how='outer')
df_srag = df_srag.merge(df_srag_obito_20, on=['mes', 'cod_mun'], how='outer')
df_srag = df_srag.merge(df_srag_uti_19, on=['mes', 'cod_mun'], how='outer')
df_srag = df_srag.merge(df_srag_uti_20, on=['mes', 'cod_mun'], how='outer')
df_srag = df_srag.fillna(0)

df_srag['SRAG Casos'] = df_srag['SRAG Casos 19'] + df_srag['SRAG Casos 20']
df_srag['SRAG Óbitos'] = df_srag['SRAG Óbitos 19'] + df_srag['SRAG Óbitos 20']
df_srag['SRAG UTI'] = df_srag['SRAG UTI 19'] + df_srag['SRAG UTI 20']

df_srag = df_srag.drop(columns={'SRAG Casos 19', 'SRAG Casos 20', 'SRAG Óbitos 19', 'SRAG Óbitos 20', 'SRAG UTI 19', 'SRAG UTI 20'})

tic = time()
print(str(round((tic - toc) / 60, 1)) + ' minutes.')

print('Conass')
mun = {'couto de magalhaes': 'couto magalhaes',
       'sao valerio da natividade': 'sao valerio',
       'florinia': 'florinea',
       'biritiba-mirim': 'biritiba mirim',
       'graccho cardoso': 'gracho cardoso',
       'santana do livramento': "sant'ana do livramento",
       'espigao do oeste': "espigao d'oeste",
       'arez': 'ares',
       'parati': 'paraty',
       "lagoa do itaenga": "lagoa de itaenga",
       'iguaraci': 'iguaracy',
       'serido': 'junco do serido',
       "santa isabel do para": "santa izabel do para",
       "eldorado dos carajas": "eldorado do carajas",
       "poxoreo": "poxoreu",
       "sem peixe": "sem-peixe",
       "olhos d'agua": "olhos-d'agua",
       'brasopolis': 'brazopolis',
       'amparo da serra': 'amparo do serra',
       'senador la roque': 'senador la rocque',
       'governador edson lobao': 'governador edison lobao',
       'gama': 'brasilia',
       'nucleo bandeirantes': 'brasilia',
       'paranoa': 'brasilia',
       'ceilandia': 'brasilia',
       'brazlandia': 'brasilia',
       'jequirica': 'jiquirica',
       'samambaia': 'brasilia',
       'aracai': 'aracuai',
       'parana': 'parauna',
       'dona euzebia': 'dona eusebia',
       'campo de santana': 'cachoeira dos indios'}
estado = {'Acre': 'AC',
          'Alagoas': 'AL',
          'Amapá': 'AP',
          'Amapa': 'AP',
          'Amazonas': 'AM',
          'Bahia': 'BA',
          'Ceará': 'CE',
          'Ceara': 'CE',
          'Distrito Federal': 'DF',
          'Espírito Santo': 'ES',
          'Espirito Santo': 'ES',
          'Goiás': 'GO',
          'Goias': 'GO',
          'Maranhão': 'MA',
          'Maranhao': 'MA',
          'Mato Grosso': 'MT',
          'Mato Grosso do Sul': 'MS',
          'Minas Gerais': 'MG',
          'Pará': 'PA',
          'Para': 'PA',
          'Paraíba': 'PB',
          'Paraiba': 'PB',
          'Paraná': 'PR',
          'Parana': 'PR',
          'Pernambuco': 'PE',
          'Piauí': 'PI',
          'Piaui': 'PI',
          'Roraima': 'RR',
          'Rondônia': 'RO',
          'Rondonia': 'RO',
          'Rio de Janeiro': 'RJ',
          'Rio Grande do Norte': 'RN',
          'Rio Grande do Sul': 'RS',
          'Santa Catarina': 'SC',
          'São Paulo': 'SP',
          'Sao Paulo': 'SP',
          'Sergipe': 'SE',
          'Tocantins': 'TO'}

df_conass_19 = df_conass_19.rename(columns={'obitos': 'CONASS 19', 'municipio': 'mun'})
df_conass_20 = df_conass_20.rename(columns={'obitos': 'CONASS 20', 'municipio': 'mun'})

df_conass_19['mun'] = df_conass_19['mun'].astype(str).str.lower()
df_conass_20['mun'] = df_conass_20['mun'].astype(str).str.lower()
df_conass_19['mun'] = df_conass_19['mun'].apply(unidecode)
df_conass_20['mun'] = df_conass_20['mun'].apply(unidecode)
df_conass_19['mun'] = df_conass_19['mun'].replace(mun)
df_conass_20['mun'] = df_conass_20['mun'].replace(mun)

df_conass_19['UF'] = df_conass_19['UF'].replace(estado)

df_conass_19['mes'] = df_conass_19['mes'].astype(str).str[:1]
df_conass_20['mes'] = df_conass_20['mes'].astype(str)

df_conass_19['mes'] = df_conass_19['mes'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9'], ['01-01-2019', '02-01-2019', '03-01-2019', '04-01-2019', '05-01-2019', '06-01-2019', '07-01-2019', '08-01-2019', '09-01-2019'])
df_conass_20['mes'] = df_conass_20['mes'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9'], ['01-01-2020', '02-01-2020', '03-01-2020', '04-01-2020', '05-01-2020', '06-01-2020', '07-01-2020', '08-01-2020', '09-01-2020'])

cols = ['UF', 'mes', 'mun', 'CONASS 19']
df_conass_19 = df_conass_19.drop(df_conass_19.columns.difference(cols), axis=1)
cols = ['UF', 'mes', 'mun', 'CONASS 20']
df_conass_20 = df_conass_20.drop(df_conass_20.columns.difference(cols), axis=1)

df_conass_19 = df_conass_19.groupby(['UF', 'mes', 'mun']).sum()
df_conass_20 = df_conass_20.groupby(['UF', 'mes', 'mun']).sum()

df_conass_19 = df_conass_19.reset_index()
df_conass_20 = df_conass_20.reset_index()

df_conass = df_conass_19.merge(df_conass_20, on=['mes', 'mun', 'UF'], how='outer')

df_conass.loc[(df_conass['mun'] == 'novo gama'), 'UF'] = 'GO'
df_conass.loc[(df_conass['mun'] == 'brasilandia'), 'UF'] = 'MS'
df_conass.loc[(df_conass['mun'] == 'guara'), 'UF'] = 'SP'
df_conass.loc[(df_conass['mun'] == 'bandeirantes') & (df_conass['UF'] == 'DF'), 'UF'] = 'MS'
df_conass.loc[(df_conass['mun'] == 'parauna'), 'UF'] = 'GO'
df_conass.loc[(df_conass['mun'] == 'planaltina'), 'UF'] = 'GO'
df_conass.loc[(df_conass['mun'] == 'sambaiba'), 'UF'] = 'MA'
df_conass.loc[(df_conass['mun'] == 'sobradinho'), 'UF'] = 'BA'
df_conass.loc[(df_conass['mun'] == 'taguatinga'), 'UF'] = 'TO'
df_conass.loc[(df_conass['mun'] == 'santarem'), 'UF'] = 'PA'
df_conass.loc[(df_conass['mun'] == 'campo grande') & (df_conass['UF'] == 'RN'), 'UF'] = 'MS'

df_conass = df_conass.groupby(['UF', 'mes', 'mun']).sum()
df_conass = df_conass.reset_index()
df_conass['CONASS'] = df_conass['CONASS 19'] + df_conass['CONASS 20']
df_conass = df_conass.drop(columns={'CONASS 19', 'CONASS 20'})

toc = time()
print(str(round((toc - tic) / 60, 1)) + ' minutes.')

print('CNES')
meses_19 = {'Dezembro': '12-01-2019', 'Novembro': '11-01-2019', 'Outubro': '10-01-2019', 'Setembro': '09-01-2019', 'Agosto': '08-01-2019', 'Julho': '07-01-2019',
            'Junho': '06-01-2019', 'Maio': '05-01-2019', 'Abril': '04-01-2019', 'Março': '03-01-2019', 'Fevereiro': '02-01-2019', 'Janeiro': '01-01-2019'}
meses_20 = {'Dezembro': '12-01-2020', 'Novembro': '11-01-2020', 'Outubro': '10-01-2020', 'Setembro': '09-01-2020', 'Agosto': '08-01-2020', 'Julho': '07-01-2020',
            'Junho': '06-01-2020', 'Maio': '05-01-2020', 'Abril': '04-01-2020', 'Março': '03-01-2020', 'Fevereiro': '02-01-2020', 'Janeiro': '01-01-2020'}

aux2 = pd.DataFrame()
for k, v in meses_19.items():
    aux = pd.read_excel(cnes_path + r'Leitos de Internação - 2019.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux['cod_mun'] = aux['"Município";"Quantidade existente"'].str[1:7]
    aux[['mun', 'Leitos 19']] = aux['"Município";"Quantidade existente"'].str.split(pat=";", expand=True)
    aux['mun'] = aux['mun'].str[8:-1]
    aux['Leitos 19'] = aux['Leitos 19'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Quantidade existente"', 'mun'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_cnes = aux2

aux2 = pd.DataFrame()
for k, v in meses_20.items():
    aux = pd.read_excel(cnes_path + r'Leitos de Internação - 2020.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux['cod_mun'] = aux['"Município";"Quantidade existente"'].str[1:7]
    aux[['mun', 'Leitos 20']] = aux['"Município";"Quantidade existente"'].str.split(pat=";", expand=True)
    aux['mun'] = aux['mun'].str[8:-1]
    aux['Leitos 20'] = aux['Leitos 20'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Quantidade existente"', 'mun'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_cnes = df_cnes.merge(aux2, on=['mes', 'cod_mun'], how='outer')
df_cnes = df_cnes.fillna(0)
df_cnes['Leitos'] = df_cnes['Leitos 19'].astype(int) + df_cnes['Leitos 20'].astype(int)
df_cnes = df_cnes.drop(columns={'Leitos 19', 'Leitos 20'})

tic = time()
print(str(round((tic - toc) / 60, 1)) + ' minutes.')

print('DataSUS')

aux2 = pd.DataFrame()
for k, v in meses_20.items():
    aux = pd.read_excel(data_sus_path + r'Óbitos - 2020 - Local de Internação.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux['cod_mun'] = aux['"Município";"Óbitos"'].str[1:7]
    aux[['mun', 'SUS Ób Int 20']] = aux['"Município";"Óbitos"'].str.split(pat=";", expand=True)
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Ób Int 20'] = aux['SUS Ób Int 20'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Óbitos"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = aux2

aux2 = pd.DataFrame()
for k, v in meses_19.items():
    aux = pd.read_excel(data_sus_path + r'Óbitos - 2019 - Local de Internação.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux[['mun', 'SUS Ób Int 19']] = aux['"Município";"Óbitos"'].str.split(pat=";", expand=True)
    aux['cod_mun'] = aux['mun'].str[1:7]
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Ób Int 19'] = aux['SUS Ób Int 19'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Óbitos"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

aux2 = pd.DataFrame()
for k, v in meses_20.items():
    aux = pd.read_excel(data_sus_path + r'Óbitos - 2020 - Local de Residência.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux['cod_mun'] = aux['"Município";"Óbitos"'].str[1:7]
    aux[['mun', 'SUS Ób Res 20']] = aux['"Município";"Óbitos"'].str.split(pat=";", expand=True)
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Ób Res 20'] = aux['SUS Ób Res 20'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Óbitos"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

aux2 = pd.DataFrame()
for k, v in meses_19.items():
    aux = pd.read_excel(data_sus_path + r'Óbitos - 2019 - Local de Residência.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux[['mun', 'SUS Ób Res 19']] = aux['"Município";"Óbitos"'].str.split(pat=";", expand=True)
    aux['cod_mun'] = aux['mun'].str[1:7]
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Ób Res 19'] = aux['SUS Ób Res 19'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Óbitos"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

aux2 = pd.DataFrame()
for k, v in meses_20.items():
    aux = pd.read_excel(data_sus_path + r'Internações - 2020 - Local de Internação.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux['cod_mun'] = aux['"Município";"Internações"'].str[1:7]
    aux[['mun', 'SUS Int Int 20']] = aux['"Município";"Internações"'].str.split(pat=";", expand=True)
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Int Int 20'] = aux['SUS Int Int 20'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Internações"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

aux2 = pd.DataFrame()
for k, v in meses_19.items():
    aux = pd.read_excel(data_sus_path + r'Internações - 2019 - Local de Internação.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux[['mun', 'SUS Int Int 19']] = aux['"Município";"Internações"'].str.split(pat=";", expand=True)
    aux['cod_mun'] = aux['mun'].str[1:7]
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Int Int 19'] = aux['SUS Int Int 19'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Internações"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

aux2 = pd.DataFrame()
for k, v in meses_20.items():
    aux = pd.read_excel(data_sus_path + r'Internações - 2020 - Local de Residência.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux['cod_mun'] = aux['"Município";"Internações"'].str[1:7]
    aux[['mun', 'SUS Int Res 20']] = aux['"Município";"Internações"'].str.split(pat=";", expand=True)
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Int Res 20'] = aux['SUS Int Res 20'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Internações"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

aux2 = pd.DataFrame()
for k, v in meses_19.items():
    aux = pd.read_excel(data_sus_path + r'Internações - 2019 - Local de Residência.xlsx', sheet_name=f'{k}')
    aux['mes'] = v
    aux[['mun', 'SUS Int Res 19']] = aux['"Município";"Internações"'].str.split(pat=";", expand=True)
    aux['cod_mun'] = aux['mun'].str[1:7]
    aux['mun'] = aux['mun'].str[8:-1]
    aux['SUS Int Res 19'] = aux['SUS Int Res 19'].replace({'-': np.nan})
    aux = aux.iloc[:-1]
    aux['filtro'] = aux['cod_mun'].str[2:]
    aux = aux[aux.filtro != '0000']
    aux = aux.drop(columns=['filtro', '"Município";"Internações"'])

    aux2 = pd.concat([aux2, aux], axis=0)

df_sus = df_sus.merge(aux2, on=['mes', 'cod_mun', 'mun'], how='outer')

df_sus = df_sus.fillna(0)
df_sus = df_sus.drop(columns='mun')
df_sus['SUS Ób Int'] = df_sus['SUS Ób Int 19'].astype(int) + df_sus['SUS Ób Int 20'].astype(int)
df_sus['SUS Ób Res'] = df_sus['SUS Ób Res 19'].astype(int) + df_sus['SUS Ób Res 20'].astype(int)
df_sus['SUS Int Int'] = df_sus['SUS Int Int 19'].astype(int) + df_sus['SUS Int Int 20'].astype(int)
df_sus['SUS Int Res'] = df_sus['SUS Int Res 19'].astype(int) + df_sus['SUS Int Res 20'].astype(int)
df_sus = df_sus.drop(columns={'SUS Ób Int 19', 'SUS Ób Int 20', 'SUS Ób Res 19', 'SUS Ób Res 20', 'SUS Int Int 19', 'SUS Int Int 20', 'SUS Int Res 19', 'SUS Int Res 20'})

toc = time()
print(str(round((toc - tic) / 60, 1)) + ' minutes.')

print('DataFrames for Analysis - Full')
df = pd.DataFrame()

df['01-01-2019'] = df_pib['cod_mun']

for column in ['01-01-2019', '02-01-2019', '03-01-2019', '04-01-2019', '05-01-2019', '06-01-2019',
               '07-01-2019', '08-01-2019', '09-01-2019', '10-01-2019', '11-01-2019', '12-01-2019',
               '01-01-2020', '02-01-2020', '03-01-2020', '04-01-2020', '05-01-2020', '06-01-2020',
               '07-01-2020', '08-01-2020', '09-01-2020', '10-01-2020', '11-01-2020', '12-01-2020']:
    df[f'{column}'] = df['01-01-2019']

df = df.stack().reset_index()
df = df.rename(columns={0: 'cod_mun', 'level_1': 'mes'})

df = df.merge(df_pib, on='cod_mun')
df = df.merge(df_area, on=['cod_mun', 'UF'], how='outer')
df['mun'] = df['mun'].astype(str).str.lower().apply(unidecode)

df = df.merge(df_sus, on=['mes', 'cod_mun'], how='outer')
df = df.merge(df_srag, on=['mes', 'cod_mun'], how='outer')
df = df.merge(df_cnes, on=['mes', 'cod_mun'], how='outer')
df = df.merge(df_conass, on=['mes', 'mun', 'UF'], how='outer')

df['mes'] = pd.to_datetime(df['mes'])
df = df.sort_values(by=['mun', 'UF', 'mes'])
df = df.dropna(subset=['level_0'])
df.loc[df['mes'] < '2020-04-01', 'pandemia'] = 0
df.loc[df['mes'] >= '2020-04-01', 'pandemia'] = 1
df = df.fillna(0)

cols = ['SRAG Casos', 'SRAG Óbitos', 'SRAG UTI', 'SUS Ób Int','SUS Ób Res', 'SUS Int Int', 'SUS Int Res', 'CONASS']

df[cols] = df[cols].astype(float)

for col in cols:
    df[f'{col} 1mm'] = (df[f'{col}']/df['populacao'])

cols = ['SRAG Casos', 'SRAG Óbitos', 'SRAG UTI', 'SUS Ób Int','SUS Ób Res', 'SUS Int Int', 'SUS Int Res', 'CONASS', 'populacao', 'pib']

# Microrregioes
df_micro = df.groupby(['cod_mic', 'mes'])[cols].sum()

df_micro['pib_per_capita'] = df_micro['pib'] / df_micro['populacao']
df_micro['mediana -'] = np.where((df_micro['pib_per_capita'] < df_micro['pib_per_capita'].median()), 1, 0)
df_micro['mediana +'] = np.where((df_micro['pib_per_capita'] >= df_micro['pib_per_capita'].median()), 1, 0)
df_micro['25% -'] = np.where((df_micro['pib_per_capita'] < np.percentile(df_micro['pib_per_capita'], 25)), 1, 0)
df_micro['75% +'] = np.where((df_micro['pib_per_capita'] >= np.percentile(df_micro['pib_per_capita'], 75)), 1, 0)
df_micro['75% - 50%'] = np.where((df_micro['pib_per_capita'] < np.percentile(df_micro['pib_per_capita'], 75)) & (df_micro['pib_per_capita'] >= np.percentile(df_micro['pib_per_capita'], 50)), 1, 0)
df_micro['50% - 25%'] = np.where((df_micro['pib_per_capita'] < np.percentile(df_micro['pib_per_capita'], 50)) & (df_micro['pib_per_capita'] >= np.percentile(df_micro['pib_per_capita'], 25)), 1, 0)
df_micro['75% - 25%'] = np.where((df_micro['pib_per_capita'] < np.percentile(df_micro['pib_per_capita'], 75)) & (df_micro['pib_per_capita'] >= np.percentile(df_micro['pib_per_capita'], 25)), 1, 0)
df_micro['25% +'] = np.where((df_micro['25% -'] == 0), 1, 0)

# TODO CHECAR DADOS DE INSUMOS ENTREGUE A CADA MUNICIPIO
# TODO CHECAR OBITOS SUS JULHO
# TODO CHECAR RDD OR EVENT STUDY

df_4 = df.loc[df['75% +'] == 1]
df_1 = df.loc[df['25% -'] == 1]
df_5 = df.loc[df['25% +'] == 1]
df_3 = df.loc[df['75% - 50%'] == 1]
df_2 = df.loc[df['50% - 25%'] == 1]
df_6 = df.loc[df['75% - 25%'] == 1]
df_acima = df.loc[df['mediana +'] == 1]
df_abaixo = df.loc[df['mediana -'] == 1]

cols = ['SRAG Casos', 'SRAG Óbitos', 'SRAG UTI', 'SUS Ób Int','SUS Ób Res', 'SUS Int Int', 'SUS Int Res', 'CONASS',
        'SRAG Casos 1mm', 'SRAG Óbitos 1mm', 'SRAG UTI 1mm', 'SUS Ób Int 1mm', 'SUS Ób Res 1mm', 'SUS Int Int 1mm', 'SUS Int Res 1mm', 'CONASS 1mm']

df_6 = df_6.groupby(['mes'])[cols].mean()
df_5 = df_5.groupby(['mes'])[cols].mean()
df_4 = df_4.groupby(['mes'])[cols].mean()
df_3 = df_3.groupby(['mes'])[cols].mean()
df_2 = df_2.groupby(['mes'])[cols].mean()
df_1 = df_1.groupby(['mes'])[cols].mean()
df_acima = df_acima.groupby(['mes'])[cols].mean()
df_abaixo = df_abaixo.groupby(['mes'])[cols].mean()

writer = pd.ExcelWriter(save_path + r'Analysis & Charts.xlsx')
df.to_excel(writer, sheet_name='Full')
df_6.to_excel(writer, sheet_name='75% - 25%')
df_5.to_excel(writer, sheet_name='25% +')
df_4.to_excel(writer, sheet_name='75% +')
df_3.to_excel(writer, sheet_name='75% - 50%')
df_2.to_excel(writer, sheet_name='50% - 25%')
df_1.to_excel(writer, sheet_name='25% -')
df_acima.to_excel(writer, sheet_name='Mediana +')
df_abaixo.to_excel(writer, sheet_name='Mediana -')
writer.close()

tic = time()
print(str(round((tic - toc) / 60, 1)) + ' minutes.')

print('DataFrame for Analysis - Região Metropolitana')
df_rm = df[df['RM'] == 1]

df_rm['mediana -'] = np.where((df_rm['pib_per_capita'] < df_rm['pib_per_capita'].median()), 1, 0)
df_rm['mediana +'] = np.where((df_rm['pib_per_capita'] >= df_rm['pib_per_capita'].median()), 1, 0)
df_rm['25% -'] = np.where((df_rm['pib_per_capita'] < np.percentile(df_rm['pib_per_capita'], 25)), 1, 0)
df_rm['75% +'] = np.where((df_rm['pib_per_capita'] >= np.percentile(df_rm['pib_per_capita'], 75)), 1, 0)
df_rm['75% - 50%'] = np.where((df_rm['pib_per_capita'] < np.percentile(df_rm['pib_per_capita'], 75)) & (df_rm['pib_per_capita'] >= np.percentile(df_rm['pib_per_capita'], 50)), 1, 0)
df_rm['50% - 25%'] = np.where((df_rm['pib_per_capita'] < np.percentile(df_rm['pib_per_capita'], 50)) & (df_rm['pib_per_capita'] >= np.percentile(df_rm['pib_per_capita'], 25)), 1, 0)
df_rm['75% - 25%'] = np.where((df_rm['pib_per_capita'] < np.percentile(df_rm['pib_per_capita'], 75)) & (df_rm['pib_per_capita'] >= np.percentile(df_rm['pib_per_capita'], 25)), 1, 0)
df_rm['25% +'] = np.where((df_rm['25% -'] == 0), 1, 0)

df_rm_4 = df_rm.loc[df_rm['75% +'] == 1]
df_rm_1 = df_rm.loc[df_rm['25% -'] == 1]
df_rm_5 = df_rm.loc[df_rm['25% +'] == 1]
df_rm_3 = df_rm.loc[df_rm['75% - 50%'] == 1]
df_rm_2 = df_rm.loc[df_rm['50% - 25%'] == 1]
df_rm_6 = df_rm.loc[df_rm['75% - 25%'] == 1]
df_rm_acima = df_rm.loc[df_rm['mediana +'] == 1]
df_rm_abaixo = df_rm.loc[df_rm['mediana -'] == 1]

df_rm_6 = df_rm_6.groupby(['mes'])[cols].mean()
df_rm_5 = df_rm_5.groupby(['mes'])[cols].mean()
df_rm_4 = df_rm_4.groupby(['mes'])[cols].mean()
df_rm_3 = df_rm_3.groupby(['mes'])[cols].mean()
df_rm_2 = df_rm_2.groupby(['mes'])[cols].mean()
df_rm_1 = df_rm_1.groupby(['mes'])[cols].mean()
df_rm_acima = df_rm_acima.groupby(['mes'])[cols].mean()
df_rm_abaixo = df_rm_abaixo.groupby(['mes'])[cols].mean()

writer = pd.ExcelWriter(save_path + r'Analysis & Charts - RM.xlsx')
df_rm.to_excel(writer, sheet_name='Full')
df_rm_6.to_excel(writer, sheet_name='75% - 25%')
df_rm_5.to_excel(writer, sheet_name='25% +')
df_rm_4.to_excel(writer, sheet_name='75% +')
df_rm_3.to_excel(writer, sheet_name='75% - 50%')
df_rm_2.to_excel(writer, sheet_name='50% - 25%')
df_rm_1.to_excel(writer, sheet_name='25% -')
df_rm_acima.to_excel(writer, sheet_name='Mediana +')
df_rm_abaixo.to_excel(writer, sheet_name='Mediana -')
writer.close()

toc = time()
print(str(round((toc - tic) / 60, 1)) + ' minutes.')

print('It took ' + str(round((time() - start_time) / 60, 1)) + ' minutes to run the routine.')