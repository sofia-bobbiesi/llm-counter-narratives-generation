# Resumen (Llama-3.2-3B-Instruct)

Éxito evaluado **por métrica, sin combinar**. `★` = mejor de la columna, `▲` = mejor de la fila. Agrupación: genéricas (mismos 27 tweets) y tipeadas (a/b/c comparten tweets solo dentro de su par).

- `few_shot`: n = 3 ejemplos (campo `fewshot_examples` de `config.json`).

## PARTE I — Jueces

El puntaje de calidad (juez 1) y la tasa de preferencia (juez 2) se analizan por separado; ⚠ marca cuando el ganador difiere entre ambos.

### 1.1 Cruce genéricas (técnica × experimento)

#### Puntaje de calidad (juez 1)

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.5633 | 0.5694 | 0.6049▲ | 0.5818 |
| few_shot (n=3) | 0.5833 | 0.6003 | 0.6250 | 0.6481▲ |
| one_shot | 0.6574▲ | 0.6080 | 0.5772 | 0.6003 |
| super_prompt | 0.6049 | 0.6281▲ | 0.5941 | 0.5802 |
| system_message | 0.6188 | 0.6744 | 0.6497 | 0.6775▲ |
| tam | 0.6065 | 0.6296 | 0.6574▲ | 0.6312 |
| zero_shot | 0.7068★ | 0.6867★ | 0.6620★ | 0.7160★▲ |

#### Tasa de preferencia (juez 2)

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.2963 | 0.4074 | 0.4815▲ | 0.4444 |
| few_shot (n=3) | 0.3333 | 0.4444 | 0.4444 | 0.5185▲ |
| one_shot | 0.7037▲ | 0.5556 | 0.5926 | 0.5926 |
| super_prompt | 0.7778★▲ | 0.7778▲ | 0.7407 | 0.7037 |
| system_message | 0.6296 | 0.8148★▲ | 0.8148★▲ | 0.7037 |
| tam | 0.7407 | 0.6296 | 0.7037 | 0.7778★▲ |
| zero_shot | 0.7407 | 0.7407 | 0.7778▲ | 0.7407 |

### 1.2 Cruce tipeadas (técnica × experimento)

#### Puntaje de calidad (juez 1)

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.5787 | 0.5602 | 0.5952 | 0.6250 | 0.6268 | 0.7029▲ |
| few_shot (n=3) | 0.6590 | 0.6204 | 0.6984▲ | 0.6548 | 0.6341 | 0.6033 |
| one_shot | 0.6667 | 0.6620 | 0.6290 | 0.6468 | 0.6703 | 0.6775▲ |
| super_prompt | 0.6111 | 0.5432 | 0.6210 | 0.5238 | 0.6232▲ | 0.5833 |
| system_message | 0.6373 | 0.6127 | 0.6151 | 0.7103★▲ | 0.6938★ | 0.7101 |
| tam | 0.6806 | 0.6960★ | 0.7024★▲ | 0.6845 | 0.6685 | 0.6920 |
| zero_shot | 0.6991★ | 0.6204 | 0.6528 | 0.6786 | 0.6793 | 0.7500★▲ |

#### Tasa de preferencia (juez 2)

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.8148 | 0.8889 | 0.7143 | 0.9524★ | 0.8696 | 0.9565▲ |
| few_shot (n=3) | 0.9630▲ | 0.9259 | 0.8571 | 0.8095 | 0.8261 | 0.7826 |
| one_shot | 0.8889 | 0.9630★ | 1.0000★▲ | 0.8095 | 0.8696 | 0.9130 |
| super_prompt | 0.9259 | 0.8889 | 0.7619 | 0.8095 | 0.9565▲ | 0.8696 |
| system_message | 1.0000★▲ | 0.8519 | 0.8095 | 0.9048 | 1.0000★▲ | 0.9130 |
| tam | 1.0000★▲ | 0.9630★ | 0.9048 | 0.9048 | 1.0000★▲ | 0.9565 |
| zero_shot | 0.9630 | 0.8148 | 0.9048 | 0.7619 | 1.0000★▲ | 1.0000★▲ |

### 1.3 Mejor técnica por experimento

| Experimento | Mejor (juez 1) | Puntaje de calidad (juez 1) | Mejor (juez 2) | Tasa de preferencia (juez 2) | ¿coinciden? |
| --- | --- | --- | --- | --- | --- |
| all | zero_shot | 0.7068 | super_prompt | 0.7778 | ⚠ no |
| collective | zero_shot | 0.6867 | system_message | 0.8148 | ⚠ no |
| premises | zero_shot | 0.6620 | system_message | 0.8148 | ⚠ no |
| no-info | zero_shot | 0.7160 | tam | 0.7778 | ⚠ no |
| a | zero_shot | 0.6991 | system_message | 1.0000 | ⚠ no |
| a_no_info | tam | 0.6960 | one_shot | 0.9630 | ⚠ no |
| b | tam | 0.7024 | one_shot | 1.0000 | ⚠ no |
| b_no_info | system_message | 0.7103 | care | 0.9524 | ⚠ no |
| c | system_message | 0.6938 | system_message | 1.0000 | ★ |
| c_no_info | zero_shot | 0.7500 | zero_shot | 1.0000 | ★ |

### 1.4 Mejor experimento por técnica — genéricas

| técnica | Puntaje de calidad (juez 1) | Tasa de preferencia (juez 2) |
| --- | --- | --- |
| care | premises (0.6049) | premises (0.4815) |
| few_shot (n=3) | no-info (0.6481) | no-info (0.5185) |
| one_shot | all (0.6574) | all (0.7037) |
| super_prompt | collective (0.6281) | all (0.7778) |
| system_message | no-info (0.6775) | collective (0.8148) |
| tam | premises (0.6574) | no-info (0.7778) |
| zero_shot | no-info (0.7160) | premises (0.7778) |

### 1.5 Mejor global — genéricas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| Puntaje de calidad (juez 1) | no-info / zero_shot (0.7160) |
| Tasa de preferencia (juez 2) | collective / system_message (0.8148) |

### 1.6 Mejor experimento por técnica — tipeadas

| técnica | Puntaje de calidad (juez 1) | Tasa de preferencia (juez 2) |
| --- | --- | --- |
| care | c_no_info (0.7029) | c_no_info (0.9565) |
| few_shot (n=3) | b (0.6984) | a (0.9630) |
| one_shot | c_no_info (0.6775) | b (1.0000) |
| super_prompt | c (0.6232) | c (0.9565) |
| system_message | b_no_info (0.7103) | a (1.0000) |
| tam | b (0.7024) | a (1.0000) |
| zero_shot | c_no_info (0.7500) | c (1.0000) |

### 1.7 Mejor global — tipeadas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| Puntaje de calidad (juez 1) | c_no_info / zero_shot (0.7500) |
| Tasa de preferencia (juez 2) | a / system_message (1.0000) |

### 1.8 Efecto de la información (pares con tweets compartidos)

Cada par difiere solo en si se inyecta la información del tipo (`a`→con info, `a_no_info`→sin info). Positivo = conviene inyectarla.

#### Puntaje de calidad (juez 1)

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0185 | 8 | 7 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | +0.0386 | 8 | 7 | 1.0000 |
| a vs a_no_info | one_shot | +0.0046 | 9 | 10 | 1.0000 |
| a vs a_no_info | super_prompt | +0.0679 | 14 | 5 | 0.0636 |
| a vs a_no_info | system_message | +0.0247 | 7 | 4 | 0.5488 |
| a vs a_no_info | tam | -0.0154 | 5 | 9 | 0.4240 |
| a vs a_no_info | zero_shot | +0.0787 | 10 | 6 | 0.4545 |
| b vs b_no_info | care | -0.0298 | 0 | 5 | 0.0625 |
| b vs b_no_info | few_shot (n=3) | +0.0437 | 11 | 4 | 0.1185 |
| b vs b_no_info | one_shot | -0.0179 | 4 | 4 | 1.0000 |
| b vs b_no_info | super_prompt | +0.0972 | 9 | 1 | 0.0215 |
| b vs b_no_info | system_message | -0.0952 | 1 | 7 | 0.0703 |
| b vs b_no_info | tam | +0.0179 | 5 | 4 | 1.0000 |
| b vs b_no_info | zero_shot | -0.0258 | 8 | 10 | 0.8145 |
| c vs c_no_info | care | -0.0761 | 2 | 9 | 0.0654 |
| c vs c_no_info | few_shot (n=3) | +0.0308 | 6 | 5 | 1.0000 |
| c vs c_no_info | one_shot | -0.0072 | 6 | 8 | 0.7905 |
| c vs c_no_info | super_prompt | +0.0399 | 7 | 3 | 0.3438 |
| c vs c_no_info | system_message | -0.0163 | 5 | 8 | 0.5811 |
| c vs c_no_info | tam | -0.0236 | 5 | 6 | 1.0000 |
| c vs c_no_info | zero_shot | -0.0707 | 3 | 9 | 0.1460 |

## PARTE II — Métricas automáticas

Métricas: ROUGE-1, ROUGE-2, ROUGE-L, BERT-F1 (por separado).

### 2.1 Cruce genéricas (técnica × experimento)

#### ROUGE-1

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.1807 | 0.1859▲ | 0.1839 | 0.1851 |
| few_shot (n=3) | 0.2086★ | 0.2294★▲ | 0.2171★ | 0.2062★ |
| one_shot | 0.1935 | 0.1920 | 0.1998 | 0.2053▲ |
| super_prompt | 0.1219▲ | 0.1146 | 0.1168 | 0.1204 |
| system_message | 0.1643 | 0.1778 | 0.1788▲ | 0.1614 |
| tam | 0.1757 | 0.1802▲ | 0.1800 | 0.1764 |
| zero_shot | 0.1712 | 0.1731▲ | 0.1655 | 0.1676 |

#### ROUGE-2

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.0167 | 0.0253 | 0.0191 | 0.0270▲ |
| few_shot (n=3) | 0.0354 | 0.0475★▲ | 0.0437★ | 0.0430★ |
| one_shot | 0.0336 | 0.0336 | 0.0258 | 0.0345▲ |
| super_prompt | 0.0251 | 0.0229 | 0.0205 | 0.0289▲ |
| system_message | 0.0228 | 0.0236 | 0.0251▲ | 0.0237 |
| tam | 0.0357★▲ | 0.0293 | 0.0273 | 0.0273 |
| zero_shot | 0.0295▲ | 0.0287 | 0.0289 | 0.0249 |

#### ROUGE-L

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.1300 | 0.1416▲ | 0.1317 | 0.1367 |
| few_shot (n=3) | 0.1606★ | 0.1649★▲ | 0.1566★ | 0.1626★ |
| one_shot | 0.1386 | 0.1388 | 0.1442 | 0.1443▲ |
| super_prompt | 0.0901▲ | 0.0878 | 0.0858 | 0.0886 |
| system_message | 0.1206 | 0.1207 | 0.1288▲ | 0.1128 |
| tam | 0.1268 | 0.1267 | 0.1344▲ | 0.1224 |
| zero_shot | 0.1220 | 0.1227 | 0.1237 | 0.1259▲ |

#### BERT-F1

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.7139 | 0.7131 | 0.7096 | 0.7171▲ |
| few_shot (n=3) | 0.7343★▲ | 0.7284★ | 0.7238★ | 0.7340★ |
| one_shot | 0.7117 | 0.7101 | 0.7144 | 0.7169▲ |
| super_prompt | 0.6779 | 0.6735 | 0.6738 | 0.6794▲ |
| system_message | 0.7059 | 0.7040 | 0.7074▲ | 0.7005 |
| tam | 0.7066▲ | 0.7066 | 0.7057 | 0.7029 |
| zero_shot | 0.7083 | 0.7094▲ | 0.7052 | 0.7052 |

### 2.2 Cruce tipeadas (técnica × experimento)

#### ROUGE-1

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.1480 | 0.1506★ | 0.1726 | 0.1779▲ | 0.1497 | 0.1644 |
| few_shot (n=3) | 0.1638★ | 0.1410 | 0.1826★ | 0.1826▲ | 0.1755★ | 0.1749★ |
| one_shot | 0.1479 | 0.1469 | 0.1592 | 0.1932★▲ | 0.1671 | 0.1453 |
| super_prompt | 0.0878 | 0.0943 | 0.0985▲ | 0.0933 | 0.0919 | 0.0911 |
| system_message | 0.1414 | 0.1177 | 0.1261 | 0.1442 | 0.1444▲ | 0.1288 |
| tam | 0.1378 | 0.1320 | 0.1508 | 0.1568▲ | 0.1437 | 0.1368 |
| zero_shot | 0.1284 | 0.1146 | 0.1339 | 0.1399▲ | 0.1319 | 0.1219 |

#### ROUGE-2

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.0090 | 0.0148 | 0.0241 | 0.0193 | 0.0092 | 0.0336★▲ |
| few_shot (n=3) | 0.0218★ | 0.0196★ | 0.0292★▲ | 0.0248★ | 0.0175 | 0.0179 |
| one_shot | 0.0123 | 0.0137 | 0.0160 | 0.0224▲ | 0.0191 | 0.0146 |
| super_prompt | 0.0096 | 0.0156 | 0.0158▲ | 0.0088 | 0.0155 | 0.0116 |
| system_message | 0.0152 | 0.0134 | 0.0121 | 0.0102 | 0.0181▲ | 0.0151 |
| tam | 0.0093 | 0.0105 | 0.0155 | 0.0181 | 0.0206▲ | 0.0179 |
| zero_shot | 0.0158 | 0.0152 | 0.0117 | 0.0165 | 0.0266★▲ | 0.0157 |

#### ROUGE-L

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.1024 | 0.1090 | 0.1314▲ | 0.1305 | 0.1053 | 0.1225★ |
| few_shot (n=3) | 0.1146★ | 0.1055 | 0.1499★▲ | 0.1344 | 0.1246★ | 0.1200 |
| one_shot | 0.1074 | 0.1098★ | 0.1246 | 0.1376★▲ | 0.1209 | 0.1024 |
| super_prompt | 0.0651 | 0.0728 | 0.0775▲ | 0.0725 | 0.0736 | 0.0749 |
| system_message | 0.0968 | 0.0885 | 0.1006 | 0.1060 | 0.1065▲ | 0.0929 |
| tam | 0.0983 | 0.0918 | 0.1085 | 0.1162▲ | 0.1037 | 0.1049 |
| zero_shot | 0.0954 | 0.0885 | 0.1026▲ | 0.1004 | 0.0991 | 0.0902 |

#### BERT-F1

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.6958 | 0.6969 | 0.7236★▲ | 0.7222 | 0.6932 | 0.7000 |
| few_shot (n=3) | 0.7066★ | 0.7027★ | 0.7232 | 0.7293★▲ | 0.7069★ | 0.7012★ |
| one_shot | 0.6964 | 0.6982 | 0.7206 | 0.7254▲ | 0.7034 | 0.6970 |
| super_prompt | 0.6553 | 0.6365 | 0.6688 | 0.6732▲ | 0.6634 | 0.6615 |
| system_message | 0.6963 | 0.6965 | 0.7020▲ | 0.6996 | 0.6993 | 0.6931 |
| tam | 0.6933 | 0.6907 | 0.7060 | 0.7093▲ | 0.7007 | 0.6912 |
| zero_shot | 0.6926 | 0.6942 | 0.7045▲ | 0.7038 | 0.6968 | 0.6894 |

### 2.3 Mejor técnica por experimento

| Experimento | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| all | few_shot (n=3) | tam | few_shot (n=3) | few_shot (n=3) |
| collective | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| premises | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| no-info | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| a | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| a_no_info | care | few_shot (n=3) | one_shot | few_shot (n=3) |
| b | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | care |
| b_no_info | one_shot | few_shot (n=3) | one_shot | few_shot (n=3) |
| c | few_shot (n=3) | zero_shot | few_shot (n=3) | few_shot (n=3) |
| c_no_info | few_shot (n=3) | care | care | few_shot (n=3) |

### 2.4 Mejor experimento por técnica — genéricas

| técnica | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| care | collective (0.1859) | no-info (0.0270) | collective (0.1416) | no-info (0.7171) |
| few_shot (n=3) | collective (0.2294) | collective (0.0475) | collective (0.1649) | all (0.7343) |
| one_shot | no-info (0.2053) | no-info (0.0345) | no-info (0.1443) | no-info (0.7169) |
| super_prompt | all (0.1219) | no-info (0.0289) | all (0.0901) | no-info (0.6794) |
| system_message | premises (0.1788) | premises (0.0251) | premises (0.1288) | premises (0.7074) |
| tam | collective (0.1802) | all (0.0357) | premises (0.1344) | all (0.7066) |
| zero_shot | collective (0.1731) | all (0.0295) | no-info (0.1259) | collective (0.7094) |

### 2.5 Mejor global — genéricas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| ROUGE-1 | collective / few_shot (n=3) (0.2294) |
| ROUGE-2 | collective / few_shot (n=3) (0.0475) |
| ROUGE-L | collective / few_shot (n=3) (0.1649) |
| BERT-F1 | all / few_shot (n=3) (0.7343) |

### 2.6 Mejor experimento por técnica — tipeadas

| técnica | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| care | b_no_info (0.1779) | c_no_info (0.0336) | b (0.1314) | b (0.7236) |
| few_shot (n=3) | b_no_info (0.1826) | b (0.0292) | b (0.1499) | b_no_info (0.7293) |
| one_shot | b_no_info (0.1932) | b_no_info (0.0224) | b_no_info (0.1376) | b_no_info (0.7254) |
| super_prompt | b (0.0985) | b (0.0158) | b (0.0775) | b_no_info (0.6732) |
| system_message | c (0.1444) | c (0.0181) | c (0.1065) | b (0.7020) |
| tam | b_no_info (0.1568) | c (0.0206) | b_no_info (0.1162) | b_no_info (0.7093) |
| zero_shot | b_no_info (0.1399) | c (0.0266) | b (0.1026) | b (0.7045) |

### 2.7 Mejor global — tipeadas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| ROUGE-1 | b_no_info / one_shot (0.1932) |
| ROUGE-2 | c_no_info / care (0.0336) |
| ROUGE-L | b / few_shot (n=3) (0.1499) |
| BERT-F1 | b_no_info / few_shot (n=3) (0.7293) |

### 2.8 Efecto de la información (pares con tweets compartidos)

#### ROUGE-1

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0026 | 13 | 14 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | +0.0228 | 20 | 6 | 0.0094 |
| a vs a_no_info | one_shot | +0.0010 | 13 | 14 | 1.0000 |
| a vs a_no_info | super_prompt | -0.0065 | 11 | 16 | 0.4421 |
| a vs a_no_info | system_message | +0.0237 | 19 | 8 | 0.0522 |
| a vs a_no_info | tam | +0.0058 | 13 | 14 | 1.0000 |
| a vs a_no_info | zero_shot | +0.0139 | 15 | 12 | 0.7011 |
| b vs b_no_info | care | -0.0053 | 10 | 10 | 1.0000 |
| b vs b_no_info | few_shot (n=3) | -0.0001 | 10 | 10 | 1.0000 |
| b vs b_no_info | one_shot | -0.0340 | 8 | 13 | 0.3833 |
| b vs b_no_info | super_prompt | +0.0052 | 12 | 8 | 0.5034 |
| b vs b_no_info | system_message | -0.0181 | 7 | 14 | 0.1892 |
| b vs b_no_info | tam | -0.0061 | 8 | 13 | 0.3833 |
| b vs b_no_info | zero_shot | -0.0060 | 10 | 11 | 1.0000 |
| c vs c_no_info | care | -0.0147 | 11 | 12 | 1.0000 |
| c vs c_no_info | few_shot (n=3) | +0.0007 | 14 | 9 | 0.4049 |
| c vs c_no_info | one_shot | +0.0218 | 12 | 11 | 1.0000 |
| c vs c_no_info | super_prompt | +0.0007 | 11 | 12 | 1.0000 |
| c vs c_no_info | system_message | +0.0157 | 14 | 9 | 0.4049 |
| c vs c_no_info | tam | +0.0069 | 10 | 13 | 0.6776 |
| c vs c_no_info | zero_shot | +0.0099 | 13 | 10 | 0.6776 |

#### ROUGE-2

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0059 | 6 | 7 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | +0.0023 | 7 | 8 | 1.0000 |
| a vs a_no_info | one_shot | -0.0014 | 4 | 6 | 0.7539 |
| a vs a_no_info | super_prompt | -0.0061 | 6 | 13 | 0.1671 |
| a vs a_no_info | system_message | +0.0018 | 9 | 7 | 0.8036 |
| a vs a_no_info | tam | -0.0012 | 8 | 8 | 1.0000 |
| a vs a_no_info | zero_shot | +0.0007 | 8 | 7 | 1.0000 |
| b vs b_no_info | care | +0.0047 | 5 | 4 | 1.0000 |
| b vs b_no_info | few_shot (n=3) | +0.0044 | 8 | 6 | 0.7905 |
| b vs b_no_info | one_shot | -0.0064 | 5 | 8 | 0.5811 |
| b vs b_no_info | super_prompt | +0.0070 | 13 | 6 | 0.1671 |
| b vs b_no_info | system_message | +0.0019 | 6 | 4 | 0.7539 |
| b vs b_no_info | tam | -0.0026 | 7 | 5 | 0.7744 |
| b vs b_no_info | zero_shot | -0.0048 | 6 | 7 | 1.0000 |
| c vs c_no_info | care | -0.0243 | 2 | 11 | 0.0225 |
| c vs c_no_info | few_shot (n=3) | -0.0004 | 6 | 5 | 1.0000 |
| c vs c_no_info | one_shot | +0.0046 | 6 | 5 | 1.0000 |
| c vs c_no_info | super_prompt | +0.0039 | 10 | 4 | 0.1796 |
| c vs c_no_info | system_message | +0.0030 | 7 | 6 | 1.0000 |
| c vs c_no_info | tam | +0.0028 | 8 | 6 | 0.7905 |
| c vs c_no_info | zero_shot | +0.0109 | 12 | 4 | 0.0768 |

#### ROUGE-L

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0066 | 9 | 17 | 0.1686 |
| a vs a_no_info | few_shot (n=3) | +0.0091 | 17 | 9 | 0.1686 |
| a vs a_no_info | one_shot | -0.0024 | 13 | 14 | 1.0000 |
| a vs a_no_info | super_prompt | -0.0077 | 8 | 19 | 0.0522 |
| a vs a_no_info | system_message | +0.0083 | 13 | 13 | 1.0000 |
| a vs a_no_info | tam | +0.0065 | 16 | 11 | 0.4421 |
| a vs a_no_info | zero_shot | +0.0069 | 16 | 11 | 0.4421 |
| b vs b_no_info | care | +0.0009 | 10 | 11 | 1.0000 |
| b vs b_no_info | few_shot (n=3) | +0.0155 | 13 | 8 | 0.3833 |
| b vs b_no_info | one_shot | -0.0129 | 8 | 13 | 0.3833 |
| b vs b_no_info | super_prompt | +0.0050 | 9 | 12 | 0.6636 |
| b vs b_no_info | system_message | -0.0054 | 10 | 11 | 1.0000 |
| b vs b_no_info | tam | -0.0078 | 6 | 15 | 0.0784 |
| b vs b_no_info | zero_shot | +0.0022 | 8 | 13 | 0.3833 |
| c vs c_no_info | care | -0.0173 | 9 | 14 | 0.4049 |
| c vs c_no_info | few_shot (n=3) | +0.0046 | 15 | 8 | 0.2100 |
| c vs c_no_info | one_shot | +0.0185 | 15 | 8 | 0.2100 |
| c vs c_no_info | super_prompt | -0.0014 | 13 | 10 | 0.6776 |
| c vs c_no_info | system_message | +0.0136 | 14 | 9 | 0.4049 |
| c vs c_no_info | tam | -0.0012 | 15 | 8 | 0.2100 |
| c vs c_no_info | zero_shot | +0.0089 | 15 | 8 | 0.2100 |

#### BERT-F1

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0011 | 14 | 13 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | +0.0038 | 17 | 10 | 0.2478 |
| a vs a_no_info | one_shot | -0.0017 | 11 | 16 | 0.4421 |
| a vs a_no_info | super_prompt | +0.0188 | 19 | 8 | 0.0522 |
| a vs a_no_info | system_message | -0.0002 | 12 | 15 | 0.7011 |
| a vs a_no_info | tam | +0.0026 | 14 | 13 | 1.0000 |
| a vs a_no_info | zero_shot | -0.0017 | 14 | 13 | 1.0000 |
| b vs b_no_info | care | +0.0013 | 12 | 9 | 0.6636 |
| b vs b_no_info | few_shot (n=3) | -0.0061 | 9 | 12 | 0.6636 |
| b vs b_no_info | one_shot | -0.0047 | 9 | 12 | 0.6636 |
| b vs b_no_info | super_prompt | -0.0044 | 11 | 10 | 1.0000 |
| b vs b_no_info | system_message | +0.0024 | 13 | 8 | 0.3833 |
| b vs b_no_info | tam | -0.0033 | 9 | 12 | 0.6636 |
| b vs b_no_info | zero_shot | +0.0007 | 10 | 11 | 1.0000 |
| c vs c_no_info | care | -0.0068 | 9 | 14 | 0.4049 |
| c vs c_no_info | few_shot (n=3) | +0.0058 | 16 | 7 | 0.0931 |
| c vs c_no_info | one_shot | +0.0064 | 13 | 10 | 0.6776 |
| c vs c_no_info | super_prompt | +0.0019 | 13 | 10 | 0.6776 |
| c vs c_no_info | system_message | +0.0062 | 17 | 6 | 0.0347 |
| c vs c_no_info | tam | +0.0095 | 19 | 4 | 0.0026 |
| c vs c_no_info | zero_shot | +0.0074 | 12 | 11 | 1.0000 |
