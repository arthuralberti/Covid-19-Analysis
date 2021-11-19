"
Autor: Arthur Alberti

- Rotina que faz a análise dos dados.
"
print('Libraries')
library('performance')
library('dplyr')
library('readxl')
library('plm')
library('stargazer')

rm(list = ls())

setwd('C:/Users/arthu/Desktop/TCC')

print('DataFrame')
df <- read_excel("DataFrame Final.xlsx")
colnames(df)

print('Conass')
print('Modelo Simples')
dd1 <- plm(CONASS ~ mediana_log_renda*pandemia, 
           data = df)
summary(dd1)

print('Modelo Simples + Controles Populacionais')
dd2 <- plm(CONASS ~ densidade + populacao + UF + idosos + acima70 
           + mediana_log_renda*pandemia, 
           data = df)
summary(dd2)

print('Modelo Simples + Controles Infraestrutura')
dd3 <- plm(CONASS ~ esgoto_geral + agua_geral + limpeza 
           + mediana_log_renda*pandemia, 
           data = df)
summary(dd3)

print('Modelo Simples + Controles A, E, D')
dd4 <- plm(CONASS ~ esgoto_geral + agua_geral + limpeza 
           + mediana_log_renda*pandemia, 
           data = df)
summary(dd4)

print('Modelo Completo')
dd5 <- plm(CONASS ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             mediana_log_renda*pandemia, 
           data = df)
summary(dd5)

print('Modelo Completo + Matriz de Covariância Robusta a la White 1')
summary(dd5, plm::vcovHC(dd5, 'white1', cluster='group'))
cov  <- plm::vcovHC(dd5, 'white1')
robust_se <- sqrt(diag(cov))
print('Modelo Completo + Matriz de Covariância Robusta a la White 2')
summary(dd5, plm::vcovHC(dd5, 'white2', cluster='group'))
cov  <- plm::vcovHC(dd5, 'white2')
robust_se <- sqrt(diag(cov))

print('Modelo Simples + Níveis de Renda')
dd6 <- plm(CONASS ~ mediana_log_renda*pandemia + abaixo_log_renda*pandemia, 
           data = df)
summary(dd6)

print('Modelo Completo + Níveis de Renda')
dd7 <- plm(CONASS ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             mediana_log_renda*pandemia +
             abaixo_log_renda*pandemia, 
           data = df)
summary(dd7)
summary(dd7, plm::vcovHC(dd7, 'white1', cluster='group'))

print('Modelo Completo')
dd8 <- plm(CONASS ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             pop_05_sm*pandemia, 
           data = df)
summary(dd8)
summary(dd8, plm::vcovHC(dd8, 'white1', cluster='group'))

print('Modelo Completo')
dd9 <- plm(CONASS ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             pop_025_sm*pandemia, 
           data = df)
summary(dd9)
summary(dd9, plm::vcovHC(dd9, 'white1', cluster='group'))

print('Modelo Completo')
dd10 <- plm(CONASS ~ densidade + populacao + UF + 
              idosos + acima70 +
              analfabetismo +
              desemprego +
              em_comp +
              esgoto_geral + 
              agua_geral +
              limpeza +
              primeiro_tercil_renda*pandemia +
              segundo_tercil_renda*pandemia, 
            data = df)
summary(dd10)
summary(dd10, plm::vcovHC(dd10, 'white1', cluster='group'))


print('DataSUS')
print('Modelo Simples')
dd11 <- plm(SUS_Ób_Int ~ mediana_log_renda*pandemia, 
           data = df)
summary(dd11)

print('Modelo Simples + Controles Populacionais')
dd12 <- plm(SUS_Ób_Int ~ densidade + populacao + UF + idosos + acima70 
           + mediana_log_renda*pandemia, 
           data = df)
summary(dd12)

print('Modelo Simples + Controles Infraestrutura')
dd13 <- plm(SUS_Ób_Int ~ esgoto_geral + agua_geral + limpeza 
           + mediana_log_renda*pandemia, 
           data = df)
summary(dd13)

print('Modelo Simples + Controles A, E, D')
dd14 <- plm(SUS_Ób_Int ~ esgoto_geral + agua_geral + limpeza 
           + mediana_log_renda*pandemia, 
           data = df)
summary(dd14)

print('Modelo Completo')
dd15 <- plm(SUS_Ób_Int ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             mediana_log_renda*pandemia, 
           data = df)
summary(dd15)

print('Modelo Completo + Matriz de Covariância Robusta a la White 1')
summary(dd15, plm::vcovHC(dd15, 'white1', cluster='group'))
cov  <- plm::vcovHC(dd15, 'white1')
robust_se <- sqrt(diag(cov))
print('Modelo Completo + Matriz de Covariância Robusta a la White 2')
summary(dd15, plm::vcovHC(dd15, 'white2', cluster='group'))
cov  <- plm::vcovHC(dd15, 'white2')
robust_se <- sqrt(diag(cov))

print('Modelo Simples + Níveis de Renda')
dd16 <- plm(SUS_Ób_Int ~ mediana_log_renda*pandemia + abaixo_log_renda*pandemia, 
           data = df)
summary(dd16)

print('Modelo Completo + Níveis de Renda')
dd17 <- plm(SUS_Ób_Int ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             mediana_log_renda*pandemia +
             abaixo_log_renda*pandemia, 
           data = df)
summary(dd17)
summary(dd17, plm::vcovHC(dd17, 'white1', cluster='group'))

print('Modelo Completo')
dd18 <- plm(SUS_Ób_Int ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             pop_05_sm*pandemia, 
           data = df)
summary(dd18)
summary(dd18, plm::vcovHC(dd18, 'white1', cluster='group'))

print('Modelo Completo')
dd19 <- plm(SUS_Ób_Int ~ densidade + populacao + UF + 
             idosos + acima70 +
             analfabetismo +
             desemprego +
             em_comp +
             esgoto_geral + 
             agua_geral +
             limpeza +
             pop_025_sm*pandemia, 
           data = df)
summary(dd19)
summary(dd19, plm::vcovHC(dd19, 'white1', cluster='group'))

print('Modelo Completo')
dd20 <- plm(SUS_Ób_Int ~ densidade + populacao + UF + 
              idosos + acima70 +
              analfabetismo +
              desemprego +
              em_comp +
              esgoto_geral + 
              agua_geral +
              limpeza +
              primeiro_tercil_renda*pandemia +
              segundo_tercil_renda*pandemia, 
            data = df)
summary(dd20)
summary(dd20, plm::vcovHC(dd20, 'white1', cluster='group'))

