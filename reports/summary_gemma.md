# Resumen (gemma-4-12B-it)

Éxito evaluado **por métrica, sin combinar**. `★` = mejor de la columna, `▲` = mejor de la fila. Agrupación: genéricas (mismos 27 tweets) y tipeadas (a/b/c comparten tweets solo dentro de su par).

- `few_shot`: n = 3 ejemplos (campo `fewshot_examples` de `config.json`).

## PARTE I — Jueces

El puntaje de calidad (juez 1) y la tasa de preferencia (juez 2) se analizan por separado; ⚠ marca cuando el ganador difiere entre ambos.

### 1.1 Cruce genéricas (técnica × experimento)

#### Puntaje de calidad (juez 1)

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.7130▲ | 0.6944 | 0.7068 | 0.6497 |
| few_shot (n=3) | 0.7485★ | 0.7346★ | 0.7593★▲ | 0.7438★ |
| one_shot | 0.6852 | 0.6744 | 0.7269▲ | 0.6543 |
| super_prompt | 0.6296 | 0.6389▲ | 0.6142 | 0.6096 |
| system_message | 0.6142 | 0.6327▲ | 0.6204 | 0.5957 |
| tam | 0.7052 | 0.6867 | 0.7315▲ | 0.6620 |
| zero_shot | 0.7299 | 0.7191 | 0.7469▲ | 0.6265 |

#### Tasa de preferencia (juez 2)

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.8148 | 0.8519▲ | 0.8519▲ | 0.7778★ |
| few_shot (n=3) | 0.5926 | 0.4815 | 0.5926 | 0.6667▲ |
| one_shot | 0.6296 | 0.7778▲ | 0.6296 | 0.6667 |
| super_prompt | 0.7778▲ | 0.5185 | 0.7407 | 0.5926 |
| system_message | 0.8148▲ | 0.5926 | 0.7037 | 0.5926 |
| tam | 0.8148 | 0.8889★▲ | 0.8889★▲ | 0.7778★ |
| zero_shot | 0.9259★▲ | 0.8519 | 0.8519 | 0.6667 |

### 1.2 Cruce tipeadas (técnica × experimento)

#### Puntaje de calidad (juez 1)

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.7793 | 0.8657▲ | 0.7599 | 0.8056 | 0.6522 | 0.6830 |
| few_shot (n=3) | 0.7809▲ | 0.7639 | 0.7520 | 0.6984 | 0.5942 | 0.6304 |
| one_shot | 0.7762▲ | 0.7469 | 0.7123 | 0.7103 | 0.6232 | 0.6540 |
| super_prompt | 0.7392 | 0.7546▲ | 0.6706 | 0.7341 | 0.6467 | 0.6558 |
| system_message | 0.6620 | 0.8179▲ | 0.6429 | 0.7222 | 0.6848 | 0.7138 |
| tam | 0.7593 | 0.8580▲ | 0.7361 | 0.8016 | 0.7283 | 0.6993 |
| zero_shot | 0.8503★ | 0.9043★▲ | 0.7679★ | 0.8095★ | 0.7518★ | 0.8007★ |

#### Tasa de preferencia (juez 2)

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.9630 | 1.0000★▲ | 0.9524 | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| few_shot (n=3) | 1.0000★▲ | 0.9630 | 0.9048 | 0.9048 | 0.7826 | 0.8261 |
| one_shot | 1.0000★▲ | 1.0000★▲ | 0.8571 | 0.9048 | 0.9130 | 0.9130 |
| super_prompt | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 0.9524 | 1.0000★▲ | 1.0000★▲ |
| system_message | 0.9630 | 1.0000★▲ | 0.9048 | 0.9524 | 1.0000★▲ | 1.0000★▲ |
| tam | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 0.9524 | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |

### 1.3 Mejor técnica por experimento

| Experimento | Mejor (juez 1) | Puntaje de calidad (juez 1) | Mejor (juez 2) | Tasa de preferencia (juez 2) | ¿coinciden? |
| --- | --- | --- | --- | --- | --- |
| all | few_shot (n=3) | 0.7485 | zero_shot | 0.9259 | ⚠ no |
| collective | few_shot (n=3) | 0.7346 | tam | 0.8889 | ⚠ no |
| premises | few_shot (n=3) | 0.7593 | tam | 0.8889 | ⚠ no |
| no-info | few_shot (n=3) | 0.7438 | care | 0.7778 | ⚠ no |
| a | zero_shot | 0.8503 | few_shot (n=3) | 1.0000 | ⚠ no |
| a_no_info | zero_shot | 0.9043 | care | 1.0000 | ⚠ no |
| b | zero_shot | 0.7679 | super_prompt | 1.0000 | ⚠ no |
| b_no_info | zero_shot | 0.8095 | care | 1.0000 | ⚠ no |
| c | zero_shot | 0.7518 | care | 1.0000 | ⚠ no |
| c_no_info | zero_shot | 0.8007 | care | 1.0000 | ⚠ no |

### 1.4 Mejor experimento por técnica — genéricas

| técnica | Puntaje de calidad (juez 1) | Tasa de preferencia (juez 2) |
| --- | --- | --- |
| care | all (0.7130) | collective (0.8519) |
| few_shot (n=3) | premises (0.7593) | no-info (0.6667) |
| one_shot | premises (0.7269) | collective (0.7778) |
| super_prompt | collective (0.6389) | all (0.7778) |
| system_message | collective (0.6327) | all (0.8148) |
| tam | premises (0.7315) | collective (0.8889) |
| zero_shot | premises (0.7469) | all (0.9259) |

### 1.5 Mejor global — genéricas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| Puntaje de calidad (juez 1) | premises / few_shot (n=3) (0.7593) |
| Tasa de preferencia (juez 2) | all / zero_shot (0.9259) |

### 1.6 Mejor experimento por técnica — tipeadas

| técnica | Puntaje de calidad (juez 1) | Tasa de preferencia (juez 2) |
| --- | --- | --- |
| care | a_no_info (0.8657) | a_no_info (1.0000) |
| few_shot (n=3) | a (0.7809) | a (1.0000) |
| one_shot | a (0.7762) | a (1.0000) |
| super_prompt | a_no_info (0.7546) | a (1.0000) |
| system_message | a_no_info (0.8179) | a_no_info (1.0000) |
| tam | a_no_info (0.8580) | a (1.0000) |
| zero_shot | a_no_info (0.9043) | a (1.0000) |

### 1.7 Mejor global — tipeadas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| Puntaje de calidad (juez 1) | a_no_info / zero_shot (0.9043) |
| Tasa de preferencia (juez 2) | a / few_shot (n=3) (1.0000) |

### 1.8 Efecto de la información (pares con tweets compartidos)

Cada par difiere solo en si se inyecta la información del tipo (`a`→con info, `a_no_info`→sin info). Positivo = conviene inyectarla.

#### Puntaje de calidad (juez 1)

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0864 | 2 | 9 | 0.0654 |
| a vs a_no_info | few_shot (n=3) | +0.0170 | 10 | 7 | 0.6291 |
| a vs a_no_info | one_shot | +0.0293 | 10 | 7 | 0.6291 |
| a vs a_no_info | super_prompt | -0.0154 | 6 | 10 | 0.4545 |
| a vs a_no_info | system_message | -0.1559 | 0 | 14 | 0.0001 |
| a vs a_no_info | tam | -0.0988 | 4 | 13 | 0.0490 |
| a vs a_no_info | zero_shot | -0.0540 | 1 | 8 | 0.0391 |
| b vs b_no_info | care | -0.0456 | 2 | 7 | 0.1797 |
| b vs b_no_info | few_shot (n=3) | +0.0536 | 10 | 4 | 0.1796 |
| b vs b_no_info | one_shot | +0.0020 | 3 | 4 | 1.0000 |
| b vs b_no_info | super_prompt | -0.0635 | 2 | 7 | 0.1797 |
| b vs b_no_info | system_message | -0.0794 | 1 | 6 | 0.1250 |
| b vs b_no_info | tam | -0.0655 | 5 | 11 | 0.2101 |
| b vs b_no_info | zero_shot | -0.0417 | 4 | 8 | 0.3877 |
| c vs c_no_info | care | -0.0308 | 4 | 5 | 1.0000 |
| c vs c_no_info | few_shot (n=3) | -0.0362 | 2 | 4 | 0.6875 |
| c vs c_no_info | one_shot | -0.0308 | 2 | 4 | 0.6875 |
| c vs c_no_info | super_prompt | -0.0091 | 2 | 3 | 1.0000 |
| c vs c_no_info | system_message | -0.0290 | 3 | 5 | 0.7266 |
| c vs c_no_info | tam | +0.0290 | 6 | 4 | 0.7539 |
| c vs c_no_info | zero_shot | -0.0489 | 2 | 6 | 0.2891 |

## PARTE II — Métricas automáticas

Métricas: ROUGE-1, ROUGE-2, ROUGE-L, BERT-F1 (por separado).

### 2.1 Cruce genéricas (técnica × experimento)

#### ROUGE-1

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.1654 | 0.1818▲ | 0.1639 | 0.1713 |
| few_shot (n=3) | 0.1982★ | 0.2126★▲ | 0.2118★ | 0.2086★ |
| one_shot | 0.1845 | 0.1881 | 0.1892 | 0.1973▲ |
| super_prompt | 0.1613▲ | 0.1525 | 0.1492 | 0.1522 |
| system_message | 0.1519 | 0.1551▲ | 0.1419 | 0.1538 |
| tam | 0.1723▲ | 0.1604 | 0.1663 | 0.1542 |
| zero_shot | 0.1660▲ | 0.1639 | 0.1602 | 0.1616 |

#### ROUGE-2

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.0129 | 0.0142▲ | 0.0082 | 0.0097 |
| few_shot (n=3) | 0.0367★ | 0.0324★ | 0.0414★▲ | 0.0294★ |
| one_shot | 0.0236 | 0.0236 | 0.0257▲ | 0.0242 |
| super_prompt | 0.0172▲ | 0.0131 | 0.0126 | 0.0121 |
| system_message | 0.0120 | 0.0099 | 0.0140▲ | 0.0075 |
| tam | 0.0172▲ | 0.0148 | 0.0169 | 0.0095 |
| zero_shot | 0.0177 | 0.0192▲ | 0.0178 | 0.0161 |

#### ROUGE-L

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.1165 | 0.1220▲ | 0.1115 | 0.1166 |
| few_shot (n=3) | 0.1468★ | 0.1501★ | 0.1589★▲ | 0.1483★ |
| one_shot | 0.1342 | 0.1345 | 0.1396▲ | 0.1322 |
| super_prompt | 0.1186▲ | 0.1109 | 0.1118 | 0.1145 |
| system_message | 0.1129▲ | 0.1087 | 0.0964 | 0.1063 |
| tam | 0.1175▲ | 0.1135 | 0.1166 | 0.1056 |
| zero_shot | 0.1114 | 0.1153 | 0.1171 | 0.1200▲ |

#### BERT-F1

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.7034 | 0.7037▲ | 0.6945 | 0.7003 |
| few_shot (n=3) | 0.7302★ | 0.7310★ | 0.7317★▲ | 0.7316★ |
| one_shot | 0.7189 | 0.7205▲ | 0.7203 | 0.7179 |
| super_prompt | 0.6905 | 0.6893 | 0.6910▲ | 0.6880 |
| system_message | 0.6920▲ | 0.6910 | 0.6898 | 0.6887 |
| tam | 0.7027 | 0.7038▲ | 0.6991 | 0.6988 |
| zero_shot | 0.6990 | 0.7009▲ | 0.6968 | 0.6921 |

### 2.2 Cruce tipeadas (técnica × experimento)

#### ROUGE-1

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.1393 | 0.1363 | 0.1434 | 0.1629▲ | 0.1433 | 0.1511 |
| few_shot (n=3) | 0.1515 | 0.1669★ | 0.1602★ | 0.1803★▲ | 0.1690★ | 0.1663★ |
| one_shot | 0.1565★ | 0.1579 | 0.1560 | 0.1759▲ | 0.1448 | 0.1411 |
| super_prompt | 0.1338 | 0.1385▲ | 0.1291 | 0.1344 | 0.1298 | 0.1357 |
| system_message | 0.1371 | 0.1227 | 0.1343 | 0.1419▲ | 0.1226 | 0.1264 |
| tam | 0.1393 | 0.1242 | 0.1400 | 0.1542▲ | 0.1380 | 0.1189 |
| zero_shot | 0.1359▲ | 0.1196 | 0.1273 | 0.1351 | 0.1246 | 0.1170 |

#### ROUGE-2

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.0068 | 0.0128 | 0.0076 | 0.0150▲ | 0.0063 | 0.0041 |
| few_shot (n=3) | 0.0219★▲ | 0.0205★ | 0.0126 | 0.0182★ | 0.0035 | 0.0118★ |
| one_shot | 0.0176 | 0.0191 | 0.0229★▲ | 0.0137 | 0.0077★ | 0.0081 |
| super_prompt | 0.0073 | 0.0105 | 0.0047 | 0.0118▲ | 0.0053 | 0.0042 |
| system_message | 0.0096▲ | 0.0076 | 0.0045 | 0.0040 | 0.0021 | 0.0076 |
| tam | 0.0128▲ | 0.0105 | 0.0016 | 0.0120 | 0.0049 | 0.0031 |
| zero_shot | 0.0124▲ | 0.0069 | 0.0078 | 0.0083 | 0.0041 | 0.0077 |

#### ROUGE-L

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.1021 | 0.0964 | 0.1005 | 0.1104 | 0.1003 | 0.1145★▲ |
| few_shot (n=3) | 0.1128★ | 0.1208★ | 0.1054 | 0.1283▲ | 0.1133★ | 0.1094 |
| one_shot | 0.1109 | 0.1190 | 0.1212★ | 0.1354★▲ | 0.0990 | 0.1017 |
| super_prompt | 0.0928 | 0.0999▲ | 0.0929 | 0.0891 | 0.0950 | 0.0926 |
| system_message | 0.1011▲ | 0.0876 | 0.0962 | 0.0960 | 0.0855 | 0.0981 |
| tam | 0.0961 | 0.0905 | 0.0928 | 0.1000▲ | 0.0982 | 0.0842 |
| zero_shot | 0.0963 | 0.0870 | 0.0942 | 0.0964▲ | 0.0872 | 0.0916 |

#### BERT-F1

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.6989 | 0.6977 | 0.7047 | 0.7075▲ | 0.6971 | 0.6949 |
| few_shot (n=3) | 0.7048 | 0.7076★ | 0.7157 | 0.7182★▲ | 0.7045★ | 0.7011★ |
| one_shot | 0.7064★ | 0.7067 | 0.7199★▲ | 0.7133 | 0.6987 | 0.6970 |
| super_prompt | 0.6896 | 0.6913 | 0.6936 | 0.6959▲ | 0.6843 | 0.6878 |
| system_message | 0.6910 | 0.6908 | 0.6923 | 0.6945▲ | 0.6857 | 0.6909 |
| tam | 0.6970 | 0.6930 | 0.7031 | 0.7052▲ | 0.6878 | 0.6890 |
| zero_shot | 0.6941 | 0.6868 | 0.6983 | 0.7015▲ | 0.6854 | 0.6907 |

### 2.3 Mejor técnica por experimento

| Experimento | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| all | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| collective | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| premises | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| no-info | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| a | one_shot | few_shot (n=3) | few_shot (n=3) | one_shot |
| a_no_info | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| b | few_shot (n=3) | one_shot | one_shot | one_shot |
| b_no_info | few_shot (n=3) | few_shot (n=3) | one_shot | few_shot (n=3) |
| c | few_shot (n=3) | one_shot | few_shot (n=3) | few_shot (n=3) |
| c_no_info | few_shot (n=3) | few_shot (n=3) | care | few_shot (n=3) |

### 2.4 Mejor experimento por técnica — genéricas

| técnica | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| care | collective (0.1818) | collective (0.0142) | collective (0.1220) | collective (0.7037) |
| few_shot (n=3) | collective (0.2126) | premises (0.0414) | premises (0.1589) | premises (0.7317) |
| one_shot | no-info (0.1973) | premises (0.0257) | premises (0.1396) | collective (0.7205) |
| super_prompt | all (0.1613) | all (0.0172) | all (0.1186) | premises (0.6910) |
| system_message | collective (0.1551) | premises (0.0140) | all (0.1129) | all (0.6920) |
| tam | all (0.1723) | all (0.0172) | all (0.1175) | collective (0.7038) |
| zero_shot | all (0.1660) | collective (0.0192) | no-info (0.1200) | collective (0.7009) |

### 2.5 Mejor global — genéricas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| ROUGE-1 | collective / few_shot (n=3) (0.2126) |
| ROUGE-2 | premises / few_shot (n=3) (0.0414) |
| ROUGE-L | premises / few_shot (n=3) (0.1589) |
| BERT-F1 | premises / few_shot (n=3) (0.7317) |

### 2.6 Mejor experimento por técnica — tipeadas

| técnica | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| care | b_no_info (0.1629) | b_no_info (0.0150) | c_no_info (0.1145) | b_no_info (0.7075) |
| few_shot (n=3) | b_no_info (0.1803) | a (0.0219) | b_no_info (0.1283) | b_no_info (0.7182) |
| one_shot | b_no_info (0.1759) | b (0.0229) | b_no_info (0.1354) | b (0.7199) |
| super_prompt | a_no_info (0.1385) | b_no_info (0.0118) | a_no_info (0.0999) | b_no_info (0.6959) |
| system_message | b_no_info (0.1419) | a (0.0096) | a (0.1011) | b_no_info (0.6945) |
| tam | b_no_info (0.1542) | a (0.0128) | b_no_info (0.1000) | b_no_info (0.7052) |
| zero_shot | a (0.1359) | a (0.0124) | b_no_info (0.0964) | b_no_info (0.7015) |

### 2.7 Mejor global — tipeadas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| ROUGE-1 | b_no_info / few_shot (n=3) (0.1803) |
| ROUGE-2 | b / one_shot (0.0229) |
| ROUGE-L | b_no_info / one_shot (0.1354) |
| BERT-F1 | b / one_shot (0.7199) |

### 2.8 Efecto de la información (pares con tweets compartidos)

#### ROUGE-1

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0030 | 13 | 13 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | -0.0154 | 7 | 18 | 0.0433 |
| a vs a_no_info | one_shot | -0.0013 | 13 | 13 | 1.0000 |
| a vs a_no_info | super_prompt | -0.0047 | 13 | 14 | 1.0000 |
| a vs a_no_info | system_message | +0.0143 | 16 | 10 | 0.3269 |
| a vs a_no_info | tam | +0.0151 | 17 | 9 | 0.1686 |
| a vs a_no_info | zero_shot | +0.0163 | 15 | 12 | 0.7011 |
| b vs b_no_info | care | -0.0195 | 7 | 13 | 0.2632 |
| b vs b_no_info | few_shot (n=3) | -0.0201 | 5 | 16 | 0.0266 |
| b vs b_no_info | one_shot | -0.0199 | 7 | 14 | 0.1892 |
| b vs b_no_info | super_prompt | -0.0053 | 9 | 12 | 0.6636 |
| b vs b_no_info | system_message | -0.0076 | 11 | 10 | 1.0000 |
| b vs b_no_info | tam | -0.0142 | 9 | 12 | 0.6636 |
| b vs b_no_info | zero_shot | -0.0077 | 10 | 11 | 1.0000 |
| c vs c_no_info | care | -0.0077 | 9 | 14 | 0.4049 |
| c vs c_no_info | few_shot (n=3) | +0.0027 | 11 | 11 | 1.0000 |
| c vs c_no_info | one_shot | +0.0038 | 13 | 10 | 0.6776 |
| c vs c_no_info | super_prompt | -0.0059 | 11 | 11 | 1.0000 |
| c vs c_no_info | system_message | -0.0038 | 13 | 10 | 0.6776 |
| c vs c_no_info | tam | +0.0191 | 15 | 8 | 0.2100 |
| c vs c_no_info | zero_shot | +0.0076 | 16 | 7 | 0.0931 |

#### ROUGE-2

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0060 | 1 | 8 | 0.0391 |
| a vs a_no_info | few_shot (n=3) | +0.0014 | 6 | 7 | 1.0000 |
| a vs a_no_info | one_shot | -0.0015 | 4 | 6 | 0.7539 |
| a vs a_no_info | super_prompt | -0.0032 | 4 | 5 | 1.0000 |
| a vs a_no_info | system_message | +0.0020 | 7 | 4 | 0.5488 |
| a vs a_no_info | tam | +0.0024 | 7 | 5 | 0.7744 |
| a vs a_no_info | zero_shot | +0.0055 | 8 | 6 | 0.7905 |
| b vs b_no_info | care | -0.0074 | 3 | 7 | 0.3438 |
| b vs b_no_info | few_shot (n=3) | -0.0056 | 4 | 5 | 1.0000 |
| b vs b_no_info | one_shot | +0.0092 | 8 | 5 | 0.5811 |
| b vs b_no_info | super_prompt | -0.0072 | 2 | 6 | 0.2891 |
| b vs b_no_info | system_message | +0.0005 | 1 | 3 | 0.6250 |
| b vs b_no_info | tam | -0.0105 | 1 | 7 | 0.0703 |
| b vs b_no_info | zero_shot | -0.0005 | 4 | 3 | 1.0000 |
| c vs c_no_info | care | +0.0022 | 4 | 2 | 0.6875 |
| c vs c_no_info | few_shot (n=3) | -0.0083 | 2 | 6 | 0.2891 |
| c vs c_no_info | one_shot | -0.0004 | 3 | 4 | 1.0000 |
| c vs c_no_info | super_prompt | +0.0012 | 4 | 2 | 0.6875 |
| c vs c_no_info | system_message | -0.0055 | 1 | 5 | 0.2188 |
| c vs c_no_info | tam | +0.0018 | 4 | 2 | 0.6875 |
| c vs c_no_info | zero_shot | -0.0035 | 3 | 6 | 0.5078 |

#### ROUGE-L

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0057 | 15 | 11 | 0.5572 |
| a vs a_no_info | few_shot (n=3) | -0.0079 | 12 | 13 | 1.0000 |
| a vs a_no_info | one_shot | -0.0081 | 11 | 14 | 0.6900 |
| a vs a_no_info | super_prompt | -0.0072 | 11 | 16 | 0.4421 |
| a vs a_no_info | system_message | +0.0135 | 18 | 8 | 0.0755 |
| a vs a_no_info | tam | +0.0056 | 19 | 7 | 0.0290 |
| a vs a_no_info | zero_shot | +0.0093 | 17 | 10 | 0.2478 |
| b vs b_no_info | care | -0.0099 | 9 | 12 | 0.6636 |
| b vs b_no_info | few_shot (n=3) | -0.0229 | 5 | 15 | 0.0414 |
| b vs b_no_info | one_shot | -0.0142 | 9 | 11 | 0.8238 |
| b vs b_no_info | super_prompt | +0.0038 | 11 | 8 | 0.6476 |
| b vs b_no_info | system_message | +0.0002 | 10 | 10 | 1.0000 |
| b vs b_no_info | tam | -0.0073 | 11 | 10 | 1.0000 |
| b vs b_no_info | zero_shot | -0.0022 | 10 | 10 | 1.0000 |
| c vs c_no_info | care | -0.0142 | 6 | 17 | 0.0347 |
| c vs c_no_info | few_shot (n=3) | +0.0039 | 10 | 13 | 0.6776 |
| c vs c_no_info | one_shot | -0.0026 | 13 | 10 | 0.6776 |
| c vs c_no_info | super_prompt | +0.0024 | 10 | 13 | 0.6776 |
| c vs c_no_info | system_message | -0.0126 | 10 | 13 | 0.6776 |
| c vs c_no_info | tam | +0.0140 | 14 | 9 | 0.4049 |
| c vs c_no_info | zero_shot | -0.0044 | 11 | 12 | 1.0000 |

#### BERT-F1

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0012 | 13 | 14 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | -0.0028 | 11 | 16 | 0.4421 |
| a vs a_no_info | one_shot | -0.0003 | 17 | 10 | 0.2478 |
| a vs a_no_info | super_prompt | -0.0017 | 14 | 13 | 1.0000 |
| a vs a_no_info | system_message | +0.0002 | 12 | 15 | 0.7011 |
| a vs a_no_info | tam | +0.0040 | 18 | 9 | 0.1221 |
| a vs a_no_info | zero_shot | +0.0074 | 20 | 7 | 0.0192 |
| b vs b_no_info | care | -0.0028 | 12 | 9 | 0.6636 |
| b vs b_no_info | few_shot (n=3) | -0.0025 | 9 | 12 | 0.6636 |
| b vs b_no_info | one_shot | +0.0066 | 10 | 11 | 1.0000 |
| b vs b_no_info | super_prompt | -0.0022 | 8 | 13 | 0.3833 |
| b vs b_no_info | system_message | -0.0022 | 10 | 11 | 1.0000 |
| b vs b_no_info | tam | -0.0022 | 8 | 13 | 0.3833 |
| b vs b_no_info | zero_shot | -0.0033 | 8 | 13 | 0.3833 |
| c vs c_no_info | care | +0.0022 | 12 | 11 | 1.0000 |
| c vs c_no_info | few_shot (n=3) | +0.0034 | 16 | 7 | 0.0931 |
| c vs c_no_info | one_shot | +0.0017 | 12 | 11 | 1.0000 |
| c vs c_no_info | super_prompt | -0.0034 | 9 | 14 | 0.4049 |
| c vs c_no_info | system_message | -0.0051 | 8 | 15 | 0.2100 |
| c vs c_no_info | tam | -0.0012 | 13 | 10 | 0.6776 |
| c vs c_no_info | zero_shot | -0.0053 | 10 | 13 | 0.6776 |
