# Comparación por modelo (Llama-3.2-3B-Instruct, Ministral-3-8B-Instruct-2512-BF16, gemma-4-12B-it)

Mismos experimentos y técnicas para todos los modelos. `★` = mejor modelo del experimento (sección 1) o de la fila (sección 2); `▲` = mejor técnica de columna. Experimentos ordenados: genéricas primero (all, collective, premises, no-info), luego tipeadas (a, a_no_info, b, b_no_info, c, c_no_info).

- `few_shot`: n = 3 ejemplos (campo `fewshot_examples` de `config.json`).

## 1. Resumen compacto — 1.1 Jueces

Filas = experimento; celda = mejor técnica con su valor.

#### Puntaje de calidad (juez 1)

| experimento | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| all | 0.7068 (zero_shot) | 0.8966 (few_shot)★ | 0.7485 (few_shot) |
| collective | 0.6867 (zero_shot) | 0.8873 (care)★ | 0.7346 (few_shot) |
| premises | 0.6620 (zero_shot) | 0.8549 (few_shot)★ | 0.7593 (few_shot) |
| no-info | 0.7160 (zero_shot) | 0.8657 (care)★ | 0.7438 (few_shot) |
| a | 0.6991 (zero_shot) | 0.9136 (tam)★ | 0.8503 (zero_shot) |
| a_no_info | 0.6960 (tam) | 0.9228 (tam)★ | 0.9043 (zero_shot) |
| b | 0.7024 (tam) | 0.9167 (care)★ | 0.7679 (zero_shot) |
| b_no_info | 0.7103 (system_message) | 0.9206 (care)★ | 0.8095 (zero_shot) |
| c | 0.6938 (system_message) | 0.9565 (zero_shot)★ | 0.7518 (zero_shot) |
| c_no_info | 0.7500 (zero_shot) | 0.9293 (tam)★ | 0.8007 (zero_shot) |

#### Tasa de preferencia (juez 2)

| experimento | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| all | 0.7778 (super_prompt) | 1.0000 (care)★ | 0.9259 (zero_shot) |
| collective | 0.8148 (system_message) | 1.0000 (care)★ | 0.8889 (tam) |
| premises | 0.8148 (system_message) | 1.0000 (care)★ | 0.8889 (tam) |
| no-info | 0.7778 (tam) | 1.0000 (care)★ | 0.7778 (care) |
| a | 1.0000 (system_message)★ | 1.0000 (care)★ | 1.0000 (few_shot)★ |
| a_no_info | 0.9630 (one_shot) | 1.0000 (care)★ | 1.0000 (care)★ |
| b | 1.0000 (one_shot)★ | 1.0000 (care)★ | 1.0000 (super_prompt)★ |
| b_no_info | 0.9524 (care) | 1.0000 (care)★ | 1.0000 (care)★ |
| c | 1.0000 (system_message)★ | 1.0000 (care)★ | 1.0000 (care)★ |
| c_no_info | 1.0000 (zero_shot)★ | 1.0000 (care)★ | 1.0000 (care)★ |

## 1. Resumen compacto — 1.2 Métricas automáticas

Filas = experimento; celda = mejor técnica con su valor.

#### ROUGE-1

| experimento | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| all | 0.2086 (few_shot)★ | 0.1943 (one_shot) | 0.1982 (few_shot) |
| collective | 0.2294 (few_shot)★ | 0.1909 (few_shot) | 0.2126 (few_shot) |
| premises | 0.2171 (few_shot)★ | 0.1912 (one_shot) | 0.2118 (few_shot) |
| no-info | 0.2062 (few_shot) | 0.1840 (few_shot) | 0.2086 (few_shot)★ |
| a | 0.1638 (few_shot)★ | 0.1395 (one_shot) | 0.1565 (one_shot) |
| a_no_info | 0.1506 (care) | 0.1528 (few_shot) | 0.1669 (few_shot)★ |
| b | 0.1826 (few_shot)★ | 0.1620 (few_shot) | 0.1602 (few_shot) |
| b_no_info | 0.1932 (one_shot)★ | 0.1601 (few_shot) | 0.1803 (few_shot) |
| c | 0.1755 (few_shot)★ | 0.1422 (one_shot) | 0.1690 (few_shot) |
| c_no_info | 0.1749 (few_shot)★ | 0.1580 (one_shot) | 0.1663 (few_shot) |

#### ROUGE-2

| experimento | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| all | 0.0357 (tam) | 0.0291 (one_shot) | 0.0367 (few_shot)★ |
| collective | 0.0475 (few_shot)★ | 0.0340 (few_shot) | 0.0324 (few_shot) |
| premises | 0.0437 (few_shot)★ | 0.0280 (one_shot) | 0.0414 (few_shot) |
| no-info | 0.0430 (few_shot)★ | 0.0293 (few_shot) | 0.0294 (few_shot) |
| a | 0.0218 (few_shot) | 0.0126 (care) | 0.0219 (few_shot)★ |
| a_no_info | 0.0196 (few_shot) | 0.0147 (one_shot) | 0.0205 (few_shot)★ |
| b | 0.0292 (few_shot)★ | 0.0237 (few_shot) | 0.0229 (one_shot) |
| b_no_info | 0.0248 (few_shot)★ | 0.0174 (one_shot) | 0.0182 (few_shot) |
| c | 0.0266 (zero_shot)★ | 0.0103 (care) | 0.0077 (one_shot) |
| c_no_info | 0.0336 (care)★ | 0.0133 (one_shot) | 0.0118 (few_shot) |

#### ROUGE-L

| experimento | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| all | 0.1606 (few_shot)★ | 0.1356 (one_shot) | 0.1468 (few_shot) |
| collective | 0.1649 (few_shot)★ | 0.1341 (few_shot) | 0.1501 (few_shot) |
| premises | 0.1566 (few_shot) | 0.1335 (one_shot) | 0.1589 (few_shot)★ |
| no-info | 0.1626 (few_shot)★ | 0.1345 (few_shot) | 0.1483 (few_shot) |
| a | 0.1146 (few_shot)★ | 0.1007 (one_shot) | 0.1128 (few_shot) |
| a_no_info | 0.1098 (one_shot) | 0.1105 (few_shot) | 0.1208 (few_shot)★ |
| b | 0.1499 (few_shot)★ | 0.1126 (few_shot) | 0.1212 (one_shot) |
| b_no_info | 0.1376 (one_shot)★ | 0.1143 (few_shot) | 0.1354 (one_shot) |
| c | 0.1246 (few_shot)★ | 0.1063 (few_shot) | 0.1133 (few_shot) |
| c_no_info | 0.1225 (care)★ | 0.1115 (one_shot) | 0.1145 (care) |

#### BERT-F1

| experimento | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| all | 0.7343 (few_shot)★ | 0.7107 (few_shot) | 0.7302 (few_shot) |
| collective | 0.7284 (few_shot) | 0.7135 (few_shot) | 0.7310 (few_shot)★ |
| premises | 0.7238 (few_shot) | 0.7069 (few_shot) | 0.7317 (few_shot)★ |
| no-info | 0.7340 (few_shot)★ | 0.7175 (few_shot) | 0.7316 (few_shot) |
| a | 0.7066 (few_shot)★ | 0.6896 (few_shot) | 0.7064 (one_shot) |
| a_no_info | 0.7027 (few_shot) | 0.6968 (few_shot) | 0.7076 (few_shot)★ |
| b | 0.7236 (care)★ | 0.7061 (few_shot) | 0.7199 (one_shot) |
| b_no_info | 0.7293 (few_shot)★ | 0.7099 (few_shot) | 0.7182 (few_shot) |
| c | 0.7069 (few_shot)★ | 0.6915 (few_shot) | 0.7045 (few_shot) |
| c_no_info | 0.7012 (few_shot)★ | 0.6920 (few_shot) | 0.7011 (few_shot) |

## 2. Detalle técnica × modelo

### all

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.5633 | 0.8673▲ | 0.7130 |
| few_shot | 0.5833 | 0.8966★▲ | 0.7485★ |
| one_shot | 0.6574 | 0.8241▲ | 0.6852 |
| super_prompt | 0.6049 | 0.8133▲ | 0.6296 |
| system_message | 0.6188 | 0.8148▲ | 0.6142 |
| tam | 0.6065 | 0.8765▲ | 0.7052 |
| zero_shot | 0.7068★ | 0.8503▲ | 0.7299 |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.2963 | 1.0000★▲ | 0.8148 |
| few_shot | 0.3333 | 0.9630▲ | 0.5926 |
| one_shot | 0.7037 | 1.0000★▲ | 0.6296 |
| super_prompt | 0.7778★ | 1.0000★▲ | 0.7778 |
| system_message | 0.6296 | 0.9630▲ | 0.8148 |
| tam | 0.7407 | 0.9630▲ | 0.8148 |
| zero_shot | 0.7407 | 0.9630▲ | 0.9259★ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1807▲ | 0.1675 | 0.1654 |
| few_shot | 0.2086★▲ | 0.1928 | 0.1982★ |
| one_shot | 0.1935 | 0.1943★▲ | 0.1845 |
| super_prompt | 0.1219 | 0.1544 | 0.1613▲ |
| system_message | 0.1643▲ | 0.1492 | 0.1519 |
| tam | 0.1757▲ | 0.1512 | 0.1723 |
| zero_shot | 0.1712▲ | 0.1384 | 0.1660 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0167 | 0.0196▲ | 0.0129 |
| few_shot | 0.0354 | 0.0263 | 0.0367★▲ |
| one_shot | 0.0336▲ | 0.0291★ | 0.0236 |
| super_prompt | 0.0251▲ | 0.0212 | 0.0172 |
| system_message | 0.0228▲ | 0.0161 | 0.0120 |
| tam | 0.0357★▲ | 0.0150 | 0.0172 |
| zero_shot | 0.0295▲ | 0.0156 | 0.0177 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1300▲ | 0.1163 | 0.1165 |
| few_shot | 0.1606★▲ | 0.1356 | 0.1468★ |
| one_shot | 0.1386▲ | 0.1356★ | 0.1342 |
| super_prompt | 0.0901 | 0.1054 | 0.1186▲ |
| system_message | 0.1206▲ | 0.1017 | 0.1129 |
| tam | 0.1268▲ | 0.1007 | 0.1175 |
| zero_shot | 0.1220▲ | 0.0978 | 0.1114 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7139▲ | 0.6952 | 0.7034 |
| few_shot | 0.7343★▲ | 0.7107★ | 0.7302★ |
| one_shot | 0.7117 | 0.7081 | 0.7189▲ |
| super_prompt | 0.6779 | 0.6900 | 0.6905▲ |
| system_message | 0.7059▲ | 0.6908 | 0.6920 |
| tam | 0.7066▲ | 0.6923 | 0.7027 |
| zero_shot | 0.7083▲ | 0.6895 | 0.6990 |

### collective

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.5694 | 0.8873★▲ | 0.6944 |
| few_shot | 0.6003 | 0.8657▲ | 0.7346★ |
| one_shot | 0.6080 | 0.7948▲ | 0.6744 |
| super_prompt | 0.6281 | 0.8349▲ | 0.6389 |
| system_message | 0.6744 | 0.7809▲ | 0.6327 |
| tam | 0.6296 | 0.8827▲ | 0.6867 |
| zero_shot | 0.6867★ | 0.8410▲ | 0.7191 |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.4074 | 1.0000★▲ | 0.8519 |
| few_shot | 0.4444 | 0.9630▲ | 0.4815 |
| one_shot | 0.5556 | 1.0000★▲ | 0.7778 |
| super_prompt | 0.7778 | 1.0000★▲ | 0.5185 |
| system_message | 0.8148★ | 0.9630▲ | 0.5926 |
| tam | 0.6296 | 1.0000★▲ | 0.8889★ |
| zero_shot | 0.7407 | 1.0000★▲ | 0.8519 |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1859▲ | 0.1579 | 0.1818 |
| few_shot | 0.2294★▲ | 0.1909★ | 0.2126★ |
| one_shot | 0.1920▲ | 0.1908 | 0.1881 |
| super_prompt | 0.1146 | 0.1448 | 0.1525▲ |
| system_message | 0.1778▲ | 0.1520 | 0.1551 |
| tam | 0.1802▲ | 0.1506 | 0.1604 |
| zero_shot | 0.1731▲ | 0.1418 | 0.1639 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0253▲ | 0.0229 | 0.0142 |
| few_shot | 0.0475★▲ | 0.0340★ | 0.0324★ |
| one_shot | 0.0336▲ | 0.0306 | 0.0236 |
| super_prompt | 0.0229▲ | 0.0175 | 0.0131 |
| system_message | 0.0236▲ | 0.0185 | 0.0099 |
| tam | 0.0293▲ | 0.0230 | 0.0148 |
| zero_shot | 0.0287▲ | 0.0209 | 0.0192 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1416▲ | 0.1131 | 0.1220 |
| few_shot | 0.1649★▲ | 0.1341★ | 0.1501★ |
| one_shot | 0.1388▲ | 0.1311 | 0.1345 |
| super_prompt | 0.0878 | 0.1021 | 0.1109▲ |
| system_message | 0.1207▲ | 0.1059 | 0.1087 |
| tam | 0.1267▲ | 0.1074 | 0.1135 |
| zero_shot | 0.1227▲ | 0.0994 | 0.1153 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7131▲ | 0.6946 | 0.7037 |
| few_shot | 0.7284★ | 0.7135★ | 0.7310★▲ |
| one_shot | 0.7101 | 0.7123 | 0.7205▲ |
| super_prompt | 0.6735 | 0.6898▲ | 0.6893 |
| system_message | 0.7040▲ | 0.6896 | 0.6910 |
| tam | 0.7066▲ | 0.6928 | 0.7038 |
| zero_shot | 0.7094▲ | 0.6894 | 0.7009 |

### premises

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.6049 | 0.8519▲ | 0.7068 |
| few_shot | 0.6250 | 0.8549★▲ | 0.7593★ |
| one_shot | 0.5772 | 0.7855▲ | 0.7269 |
| super_prompt | 0.5941 | 0.7793▲ | 0.6142 |
| system_message | 0.6497 | 0.7932▲ | 0.6204 |
| tam | 0.6574 | 0.8534▲ | 0.7315 |
| zero_shot | 0.6620★ | 0.8457▲ | 0.7469 |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.4815 | 1.0000★▲ | 0.8519 |
| few_shot | 0.4444 | 0.9630▲ | 0.5926 |
| one_shot | 0.5926 | 0.8889▲ | 0.6296 |
| super_prompt | 0.7407 | 0.9630▲ | 0.7407 |
| system_message | 0.8148★ | 1.0000★▲ | 0.7037 |
| tam | 0.7037 | 0.9259▲ | 0.8889★ |
| zero_shot | 0.7778 | 1.0000★▲ | 0.8519 |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1839▲ | 0.1572 | 0.1639 |
| few_shot | 0.2171★▲ | 0.1784 | 0.2118★ |
| one_shot | 0.1998▲ | 0.1912★ | 0.1892 |
| super_prompt | 0.1168 | 0.1505▲ | 0.1492 |
| system_message | 0.1788▲ | 0.1488 | 0.1419 |
| tam | 0.1800▲ | 0.1521 | 0.1663 |
| zero_shot | 0.1655▲ | 0.1438 | 0.1602 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0191▲ | 0.0184 | 0.0082 |
| few_shot | 0.0437★▲ | 0.0250 | 0.0414★ |
| one_shot | 0.0258 | 0.0280★▲ | 0.0257 |
| super_prompt | 0.0205▲ | 0.0134 | 0.0126 |
| system_message | 0.0251▲ | 0.0093 | 0.0140 |
| tam | 0.0273▲ | 0.0173 | 0.0169 |
| zero_shot | 0.0289▲ | 0.0196 | 0.0178 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1317▲ | 0.1054 | 0.1115 |
| few_shot | 0.1566★ | 0.1266 | 0.1589★▲ |
| one_shot | 0.1442▲ | 0.1335★ | 0.1396 |
| super_prompt | 0.0858 | 0.1062 | 0.1118▲ |
| system_message | 0.1288▲ | 0.0966 | 0.0964 |
| tam | 0.1344▲ | 0.1035 | 0.1166 |
| zero_shot | 0.1237▲ | 0.0992 | 0.1171 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7096▲ | 0.6891 | 0.6945 |
| few_shot | 0.7238★ | 0.7069★ | 0.7317★▲ |
| one_shot | 0.7144 | 0.7030 | 0.7203▲ |
| super_prompt | 0.6738 | 0.6855 | 0.6910▲ |
| system_message | 0.7074▲ | 0.6865 | 0.6898 |
| tam | 0.7057▲ | 0.6935 | 0.6991 |
| zero_shot | 0.7052▲ | 0.6901 | 0.6968 |

### no-info

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.5818 | 0.8657★▲ | 0.6497 |
| few_shot | 0.6481 | 0.8318▲ | 0.7438★ |
| one_shot | 0.6003 | 0.7762▲ | 0.6543 |
| super_prompt | 0.5802 | 0.8025▲ | 0.6096 |
| system_message | 0.6775 | 0.7438▲ | 0.5957 |
| tam | 0.6312 | 0.8441▲ | 0.6620 |
| zero_shot | 0.7160★ | 0.8488▲ | 0.6265 |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.4444 | 1.0000★▲ | 0.7778★ |
| few_shot | 0.5185 | 0.8519▲ | 0.6667 |
| one_shot | 0.5926 | 0.9259▲ | 0.6667 |
| super_prompt | 0.7037 | 0.9630▲ | 0.5926 |
| system_message | 0.7037 | 0.8889▲ | 0.5926 |
| tam | 0.7778★ | 1.0000★▲ | 0.7778★ |
| zero_shot | 0.7407 | 1.0000★▲ | 0.6667 |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1851▲ | 0.1641 | 0.1713 |
| few_shot | 0.2062★ | 0.1840★ | 0.2086★▲ |
| one_shot | 0.2053▲ | 0.1784 | 0.1973 |
| super_prompt | 0.1204 | 0.1646▲ | 0.1522 |
| system_message | 0.1614▲ | 0.1458 | 0.1538 |
| tam | 0.1764▲ | 0.1382 | 0.1542 |
| zero_shot | 0.1676▲ | 0.1366 | 0.1616 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0270▲ | 0.0182 | 0.0097 |
| few_shot | 0.0430★▲ | 0.0293★ | 0.0294★ |
| one_shot | 0.0345▲ | 0.0226 | 0.0242 |
| super_prompt | 0.0289▲ | 0.0164 | 0.0121 |
| system_message | 0.0237▲ | 0.0159 | 0.0075 |
| tam | 0.0273▲ | 0.0199 | 0.0095 |
| zero_shot | 0.0249▲ | 0.0156 | 0.0161 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1367▲ | 0.1100 | 0.1166 |
| few_shot | 0.1626★▲ | 0.1345★ | 0.1483★ |
| one_shot | 0.1443▲ | 0.1249 | 0.1322 |
| super_prompt | 0.0886 | 0.1060 | 0.1145▲ |
| system_message | 0.1128▲ | 0.1011 | 0.1063 |
| tam | 0.1224▲ | 0.1000 | 0.1056 |
| zero_shot | 0.1259▲ | 0.0940 | 0.1200 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7171▲ | 0.6969 | 0.7003 |
| few_shot | 0.7340★▲ | 0.7175★ | 0.7316★ |
| one_shot | 0.7169 | 0.7055 | 0.7179▲ |
| super_prompt | 0.6794 | 0.6908▲ | 0.6880 |
| system_message | 0.7005▲ | 0.6858 | 0.6887 |
| tam | 0.7029▲ | 0.6902 | 0.6988 |
| zero_shot | 0.7052▲ | 0.6877 | 0.6921 |

### a

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.5787 | 0.8549▲ | 0.7793 |
| few_shot | 0.6590 | 0.8796▲ | 0.7809 |
| one_shot | 0.6667 | 0.8519▲ | 0.7762 |
| super_prompt | 0.6111 | 0.8287▲ | 0.7392 |
| system_message | 0.6373 | 0.8086▲ | 0.6620 |
| tam | 0.6806 | 0.9136★▲ | 0.7593 |
| zero_shot | 0.6991★ | 0.8688▲ | 0.8503★ |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.8148 | 1.0000★▲ | 0.9630 |
| few_shot | 0.9630 | 1.0000★▲ | 1.0000★▲ |
| one_shot | 0.8889 | 1.0000★▲ | 1.0000★▲ |
| super_prompt | 0.9259 | 1.0000★▲ | 1.0000★▲ |
| system_message | 1.0000★▲ | 1.0000★▲ | 0.9630 |
| tam | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 0.9630 | 1.0000★▲ | 1.0000★▲ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1480▲ | 0.1362 | 0.1393 |
| few_shot | 0.1638★▲ | 0.1225 | 0.1515 |
| one_shot | 0.1479 | 0.1395★ | 0.1565★▲ |
| super_prompt | 0.0878 | 0.1260 | 0.1338▲ |
| system_message | 0.1414▲ | 0.1133 | 0.1371 |
| tam | 0.1378 | 0.1270 | 0.1393▲ |
| zero_shot | 0.1284 | 0.1174 | 0.1359▲ |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0090 | 0.0126★▲ | 0.0068 |
| few_shot | 0.0218★ | 0.0115 | 0.0219★▲ |
| one_shot | 0.0123 | 0.0107 | 0.0176▲ |
| super_prompt | 0.0096▲ | 0.0062 | 0.0073 |
| system_message | 0.0152▲ | 0.0083 | 0.0096 |
| tam | 0.0093 | 0.0111 | 0.0128▲ |
| zero_shot | 0.0158▲ | 0.0095 | 0.0124 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1024▲ | 0.0970 | 0.1021 |
| few_shot | 0.1146★▲ | 0.0898 | 0.1128★ |
| one_shot | 0.1074 | 0.1007★ | 0.1109▲ |
| super_prompt | 0.0651 | 0.0887 | 0.0928▲ |
| system_message | 0.0968 | 0.0806 | 0.1011▲ |
| tam | 0.0983▲ | 0.0912 | 0.0961 |
| zero_shot | 0.0954 | 0.0850 | 0.0963▲ |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.6958 | 0.6870 | 0.6989▲ |
| few_shot | 0.7066★▲ | 0.6896★ | 0.7048 |
| one_shot | 0.6964 | 0.6893 | 0.7064★▲ |
| super_prompt | 0.6553 | 0.6716 | 0.6896▲ |
| system_message | 0.6963▲ | 0.6727 | 0.6910 |
| tam | 0.6933 | 0.6792 | 0.6970▲ |
| zero_shot | 0.6926 | 0.6791 | 0.6941▲ |

### a_no_info

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.5602 | 0.8920▲ | 0.8657 |
| few_shot | 0.6204 | 0.8735▲ | 0.7639 |
| one_shot | 0.6620 | 0.8071▲ | 0.7469 |
| super_prompt | 0.5432 | 0.8395▲ | 0.7546 |
| system_message | 0.6127 | 0.8364▲ | 0.8179 |
| tam | 0.6960★ | 0.9228★▲ | 0.8580 |
| zero_shot | 0.6204 | 0.9213▲ | 0.9043★ |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.8889 | 1.0000★▲ | 1.0000★▲ |
| few_shot | 0.9259 | 1.0000★▲ | 0.9630 |
| one_shot | 0.9630★ | 1.0000★▲ | 1.0000★▲ |
| super_prompt | 0.8889 | 1.0000★▲ | 1.0000★▲ |
| system_message | 0.8519 | 1.0000★▲ | 1.0000★▲ |
| tam | 0.9630★ | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 0.8148 | 1.0000★▲ | 1.0000★▲ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1506★▲ | 0.1271 | 0.1363 |
| few_shot | 0.1410 | 0.1528★ | 0.1669★▲ |
| one_shot | 0.1469 | 0.1414 | 0.1579▲ |
| super_prompt | 0.0943 | 0.1174 | 0.1385▲ |
| system_message | 0.1177 | 0.1258▲ | 0.1227 |
| tam | 0.1320▲ | 0.1088 | 0.1242 |
| zero_shot | 0.1146 | 0.1035 | 0.1196▲ |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0148▲ | 0.0115 | 0.0128 |
| few_shot | 0.0196★ | 0.0129 | 0.0205★▲ |
| one_shot | 0.0137 | 0.0147★ | 0.0191▲ |
| super_prompt | 0.0156▲ | 0.0053 | 0.0105 |
| system_message | 0.0134▲ | 0.0086 | 0.0076 |
| tam | 0.0105▲ | 0.0042 | 0.0105 |
| zero_shot | 0.0152▲ | 0.0068 | 0.0069 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1090▲ | 0.0918 | 0.0964 |
| few_shot | 0.1055 | 0.1105★ | 0.1208★▲ |
| one_shot | 0.1098★ | 0.1062 | 0.1190▲ |
| super_prompt | 0.0728 | 0.0807 | 0.0999▲ |
| system_message | 0.0885 | 0.0950▲ | 0.0876 |
| tam | 0.0918▲ | 0.0782 | 0.0905 |
| zero_shot | 0.0885▲ | 0.0714 | 0.0870 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.6969 | 0.6829 | 0.6977▲ |
| few_shot | 0.7027★ | 0.6968★ | 0.7076★▲ |
| one_shot | 0.6982 | 0.6919 | 0.7067▲ |
| super_prompt | 0.6365 | 0.6771 | 0.6913▲ |
| system_message | 0.6965▲ | 0.6752 | 0.6908 |
| tam | 0.6907 | 0.6785 | 0.6930▲ |
| zero_shot | 0.6942▲ | 0.6758 | 0.6868 |

### b

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.5952 | 0.9167★▲ | 0.7599 |
| few_shot | 0.6984 | 0.8869▲ | 0.7520 |
| one_shot | 0.6290 | 0.9008▲ | 0.7123 |
| super_prompt | 0.6210 | 0.7937▲ | 0.6706 |
| system_message | 0.6151 | 0.8690▲ | 0.6429 |
| tam | 0.7024★ | 0.8909▲ | 0.7361 |
| zero_shot | 0.6528 | 0.9087▲ | 0.7679★ |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7143 | 1.0000★▲ | 0.9524 |
| few_shot | 0.8571 | 1.0000★▲ | 0.9048 |
| one_shot | 1.0000★▲ | 1.0000★▲ | 0.8571 |
| super_prompt | 0.7619 | 1.0000★▲ | 1.0000★▲ |
| system_message | 0.8095 | 0.9524▲ | 0.9048 |
| tam | 0.9048 | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 0.9048 | 1.0000★▲ | 1.0000★▲ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1726▲ | 0.1319 | 0.1434 |
| few_shot | 0.1826★▲ | 0.1620★ | 0.1602★ |
| one_shot | 0.1592▲ | 0.1468 | 0.1560 |
| super_prompt | 0.0985 | 0.1146 | 0.1291▲ |
| system_message | 0.1261 | 0.1177 | 0.1343▲ |
| tam | 0.1508▲ | 0.1105 | 0.1400 |
| zero_shot | 0.1339▲ | 0.1240 | 0.1273 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0241▲ | 0.0156 | 0.0076 |
| few_shot | 0.0292★▲ | 0.0237★ | 0.0126 |
| one_shot | 0.0160 | 0.0133 | 0.0229★▲ |
| super_prompt | 0.0158▲ | 0.0132 | 0.0047 |
| system_message | 0.0121 | 0.0133▲ | 0.0045 |
| tam | 0.0155▲ | 0.0085 | 0.0016 |
| zero_shot | 0.0117 | 0.0162▲ | 0.0078 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1314▲ | 0.0943 | 0.1005 |
| few_shot | 0.1499★▲ | 0.1126★ | 0.1054 |
| one_shot | 0.1246▲ | 0.1046 | 0.1212★ |
| super_prompt | 0.0775 | 0.0829 | 0.0929▲ |
| system_message | 0.1006▲ | 0.0885 | 0.0962 |
| tam | 0.1085▲ | 0.0821 | 0.0928 |
| zero_shot | 0.1026▲ | 0.0838 | 0.0942 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7236★▲ | 0.6980 | 0.7047 |
| few_shot | 0.7232▲ | 0.7061★ | 0.7157 |
| one_shot | 0.7206▲ | 0.7047 | 0.7199★ |
| super_prompt | 0.6688 | 0.6512 | 0.6936▲ |
| system_message | 0.7020▲ | 0.6903 | 0.6923 |
| tam | 0.7060▲ | 0.6900 | 0.7031 |
| zero_shot | 0.7045▲ | 0.6953 | 0.6983 |

### b_no_info

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.6250 | 0.9206★▲ | 0.8056 |
| few_shot | 0.6548 | 0.8909▲ | 0.6984 |
| one_shot | 0.6468 | 0.8671▲ | 0.7103 |
| super_prompt | 0.5238 | 0.8393▲ | 0.7341 |
| system_message | 0.7103★ | 0.9087▲ | 0.7222 |
| tam | 0.6845 | 0.9087▲ | 0.8016 |
| zero_shot | 0.6786 | 0.9028▲ | 0.8095★ |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.9524★ | 1.0000★▲ | 1.0000★▲ |
| few_shot | 0.8095 | 0.9524▲ | 0.9048 |
| one_shot | 0.8095 | 1.0000★▲ | 0.9048 |
| super_prompt | 0.8095 | 1.0000★▲ | 0.9524 |
| system_message | 0.9048 | 1.0000★▲ | 0.9524 |
| tam | 0.9048 | 1.0000★▲ | 0.9524 |
| zero_shot | 0.7619 | 1.0000★▲ | 1.0000★▲ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1779▲ | 0.1340 | 0.1629 |
| few_shot | 0.1826▲ | 0.1601★ | 0.1803★ |
| one_shot | 0.1932★▲ | 0.1513 | 0.1759 |
| super_prompt | 0.0933 | 0.1224 | 0.1344▲ |
| system_message | 0.1442▲ | 0.1117 | 0.1419 |
| tam | 0.1568▲ | 0.1094 | 0.1542 |
| zero_shot | 0.1399▲ | 0.1001 | 0.1351 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0193▲ | 0.0085 | 0.0150 |
| few_shot | 0.0248★▲ | 0.0160 | 0.0182★ |
| one_shot | 0.0224▲ | 0.0174★ | 0.0137 |
| super_prompt | 0.0088 | 0.0150▲ | 0.0118 |
| system_message | 0.0102▲ | 0.0036 | 0.0040 |
| tam | 0.0181▲ | 0.0065 | 0.0120 |
| zero_shot | 0.0165▲ | 0.0076 | 0.0083 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1305▲ | 0.0939 | 0.1104 |
| few_shot | 0.1344▲ | 0.1143★ | 0.1283 |
| one_shot | 0.1376★▲ | 0.1081 | 0.1354★ |
| super_prompt | 0.0725 | 0.0851 | 0.0891▲ |
| system_message | 0.1060▲ | 0.0836 | 0.0960 |
| tam | 0.1162▲ | 0.0772 | 0.1000 |
| zero_shot | 0.1004▲ | 0.0716 | 0.0964 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7222▲ | 0.6963 | 0.7075 |
| few_shot | 0.7293★▲ | 0.7099★ | 0.7182★ |
| one_shot | 0.7254▲ | 0.7069 | 0.7133 |
| super_prompt | 0.6732 | 0.6868 | 0.6959▲ |
| system_message | 0.6996▲ | 0.6845 | 0.6945 |
| tam | 0.7093▲ | 0.6865 | 0.7052 |
| zero_shot | 0.7038▲ | 0.6869 | 0.7015 |

### c

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.6268 | 0.8913▲ | 0.6522 |
| few_shot | 0.6341 | 0.8351▲ | 0.5942 |
| one_shot | 0.6703 | 0.8333▲ | 0.6232 |
| super_prompt | 0.6232 | 0.8641▲ | 0.6467 |
| system_message | 0.6938★ | 0.8696▲ | 0.6848 |
| tam | 0.6685 | 0.9203▲ | 0.7283 |
| zero_shot | 0.6793 | 0.9565★▲ | 0.7518★ |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.8696 | 1.0000★▲ | 1.0000★▲ |
| few_shot | 0.8261 | 1.0000★▲ | 0.7826 |
| one_shot | 0.8696 | 1.0000★▲ | 0.9130 |
| super_prompt | 0.9565 | 1.0000★▲ | 1.0000★▲ |
| system_message | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| tam | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1497▲ | 0.1400 | 0.1433 |
| few_shot | 0.1755★▲ | 0.1416 | 0.1690★ |
| one_shot | 0.1671▲ | 0.1422★ | 0.1448 |
| super_prompt | 0.0919 | 0.1164 | 0.1298▲ |
| system_message | 0.1444▲ | 0.1255 | 0.1226 |
| tam | 0.1437▲ | 0.1147 | 0.1380 |
| zero_shot | 0.1319▲ | 0.1267 | 0.1246 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0092 | 0.0103★▲ | 0.0063 |
| few_shot | 0.0175▲ | 0.0033 | 0.0035 |
| one_shot | 0.0191▲ | 0.0052 | 0.0077★ |
| super_prompt | 0.0155▲ | 0.0068 | 0.0053 |
| system_message | 0.0181▲ | 0.0048 | 0.0021 |
| tam | 0.0206▲ | 0.0066 | 0.0049 |
| zero_shot | 0.0266★▲ | 0.0098 | 0.0041 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1053▲ | 0.0896 | 0.1003 |
| few_shot | 0.1246★▲ | 0.1063★ | 0.1133★ |
| one_shot | 0.1209▲ | 0.1015 | 0.0990 |
| super_prompt | 0.0736 | 0.0802 | 0.0950▲ |
| system_message | 0.1065▲ | 0.0842 | 0.0855 |
| tam | 0.1037▲ | 0.0842 | 0.0982 |
| zero_shot | 0.0991▲ | 0.0837 | 0.0872 |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.6932 | 0.6835 | 0.6971▲ |
| few_shot | 0.7069★▲ | 0.6915★ | 0.7045★ |
| one_shot | 0.7034▲ | 0.6914 | 0.6987 |
| super_prompt | 0.6634 | 0.6488 | 0.6843▲ |
| system_message | 0.6993▲ | 0.6789 | 0.6857 |
| tam | 0.7007▲ | 0.6767 | 0.6878 |
| zero_shot | 0.6968▲ | 0.6759 | 0.6854 |

### c_no_info

#### Puntaje de calidad (juez 1)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7029 | 0.8804▲ | 0.6830 |
| few_shot | 0.6033 | 0.8623▲ | 0.6304 |
| one_shot | 0.6775 | 0.7953▲ | 0.6540 |
| super_prompt | 0.5833 | 0.8750▲ | 0.6558 |
| system_message | 0.7101 | 0.8442▲ | 0.7138 |
| tam | 0.6920 | 0.9293★▲ | 0.6993 |
| zero_shot | 0.7500★ | 0.9239▲ | 0.8007★ |

#### Tasa de preferencia (juez 2)

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.9565 | 1.0000★▲ | 1.0000★▲ |
| few_shot | 0.7826 | 1.0000★▲ | 0.8261 |
| one_shot | 0.9130 | 1.0000★▲ | 0.9130 |
| super_prompt | 0.8696 | 1.0000★▲ | 1.0000★▲ |
| system_message | 0.9130 | 1.0000★▲ | 1.0000★▲ |
| tam | 0.9565 | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |

#### ROUGE-1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1644▲ | 0.1271 | 0.1511 |
| few_shot | 0.1749★▲ | 0.1382 | 0.1663★ |
| one_shot | 0.1453 | 0.1580★▲ | 0.1411 |
| super_prompt | 0.0911 | 0.1103 | 0.1357▲ |
| system_message | 0.1288▲ | 0.1257 | 0.1264 |
| tam | 0.1368▲ | 0.1107 | 0.1189 |
| zero_shot | 0.1219▲ | 0.1026 | 0.1170 |

#### ROUGE-2

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.0336★▲ | 0.0086 | 0.0041 |
| few_shot | 0.0179▲ | 0.0063 | 0.0118★ |
| one_shot | 0.0146▲ | 0.0133★ | 0.0081 |
| super_prompt | 0.0116▲ | 0.0067 | 0.0042 |
| system_message | 0.0151▲ | 0.0107 | 0.0076 |
| tam | 0.0179▲ | 0.0051 | 0.0031 |
| zero_shot | 0.0157▲ | 0.0050 | 0.0077 |

#### ROUGE-L

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.1225★▲ | 0.0919 | 0.1145★ |
| few_shot | 0.1200▲ | 0.0910 | 0.1094 |
| one_shot | 0.1024 | 0.1115★▲ | 0.1017 |
| super_prompt | 0.0749 | 0.0763 | 0.0926▲ |
| system_message | 0.0929 | 0.0888 | 0.0981▲ |
| tam | 0.1049▲ | 0.0798 | 0.0842 |
| zero_shot | 0.0902 | 0.0761 | 0.0916▲ |

#### BERT-F1

| técnica | Llama-3.2-3B-Instruct | Ministral-3-8B-Instruct-2512-BF16 | gemma-4-12B-it |
| --- | --- | --- | --- |
| care | 0.7000▲ | 0.6854 | 0.6949 |
| few_shot | 0.7012★▲ | 0.6920★ | 0.7011★ |
| one_shot | 0.6970▲ | 0.6887 | 0.6970 |
| super_prompt | 0.6615 | 0.6647 | 0.6878▲ |
| system_message | 0.6931▲ | 0.6820 | 0.6909 |
| tam | 0.6912▲ | 0.6765 | 0.6890 |
| zero_shot | 0.6894 | 0.6711 | 0.6907▲ |

## 3. Test de signos entre modelos

Comparación emparejada por tweet (cada experimento comparte los mismos 27 tweets). Solo se listan las diferencias significativas (p < 0.05, test de signos bilateral); Δ media = A − B.

### Llama-3.2-3B-Instruct vs Ministral-3-8B-Instruct-2512-BF16

#### Puntaje de calidad (juez 1)

69 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana Ministral-3-8B-Instruct-2512-BF16 | p |
| --- | --- | --- | --- | --- | --- |
| a | care | -0.2762 | 0 | 20 | 0.0000 |
| a | few_shot | -0.2207 | 2 | 23 | 0.0000 |
| a | one_shot | -0.1852 | 1 | 16 | 0.0003 |
| a | super_prompt | -0.2176 | 1 | 20 | 0.0000 |
| a | system_message | -0.1713 | 1 | 15 | 0.0005 |
| a | tam | -0.2330 | 1 | 21 | 0.0000 |
| a | zero_shot | -0.1698 | 2 | 16 | 0.0013 |
| a_no_info | care | -0.3318 | 1 | 23 | 0.0000 |
| a_no_info | few_shot | -0.2531 | 0 | 20 | 0.0000 |
| a_no_info | one_shot | -0.1451 | 2 | 13 | 0.0074 |
| a_no_info | super_prompt | -0.2963 | 0 | 24 | 0.0000 |
| a_no_info | system_message | -0.2238 | 3 | 18 | 0.0015 |
| a_no_info | tam | -0.2269 | 0 | 21 | 0.0000 |
| a_no_info | zero_shot | -0.3009 | 0 | 25 | 0.0000 |
| all | care | -0.3040 | 0 | 21 | 0.0000 |
| all | few_shot | -0.3133 | 0 | 24 | 0.0000 |
| all | one_shot | -0.1667 | 3 | 18 | 0.0015 |
| all | super_prompt | -0.2083 | 1 | 19 | 0.0000 |
| all | system_message | -0.1960 | 0 | 17 | 0.0000 |
| all | tam | -0.2701 | 1 | 21 | 0.0000 |
| all | zero_shot | -0.1435 | 3 | 14 | 0.0127 |
| b | care | -0.3214 | 0 | 20 | 0.0000 |
| b | few_shot | -0.1885 | 0 | 15 | 0.0001 |
| b | one_shot | -0.2718 | 0 | 19 | 0.0000 |
| b | super_prompt | -0.1726 | 2 | 12 | 0.0129 |
| b | system_message | -0.2540 | 0 | 15 | 0.0001 |
| b | tam | -0.1885 | 1 | 14 | 0.0010 |
| b | zero_shot | -0.2560 | 0 | 17 | 0.0000 |
| b_no_info | care | -0.2956 | 0 | 21 | 0.0000 |
| b_no_info | few_shot | -0.2361 | 0 | 17 | 0.0000 |
| b_no_info | one_shot | -0.2202 | 0 | 15 | 0.0001 |
| b_no_info | super_prompt | -0.3155 | 0 | 18 | 0.0000 |
| b_no_info | system_message | -0.1984 | 0 | 13 | 0.0002 |
| b_no_info | tam | -0.2242 | 1 | 17 | 0.0001 |
| b_no_info | zero_shot | -0.2242 | 1 | 14 | 0.0010 |
| c | care | -0.2645 | 0 | 18 | 0.0000 |
| c | few_shot | -0.2011 | 1 | 15 | 0.0005 |
| c | one_shot | -0.1630 | 2 | 14 | 0.0042 |
| c | super_prompt | -0.2409 | 2 | 21 | 0.0001 |
| c | system_message | -0.1757 | 1 | 13 | 0.0018 |
| c | tam | -0.2518 | 0 | 17 | 0.0000 |
| c | zero_shot | -0.2772 | 0 | 21 | 0.0000 |
| c_no_info | care | -0.1775 | 1 | 15 | 0.0005 |
| c_no_info | few_shot | -0.2591 | 1 | 18 | 0.0001 |
| c_no_info | one_shot | -0.1178 | 4 | 13 | 0.0490 |
| c_no_info | super_prompt | -0.2917 | 1 | 20 | 0.0000 |
| c_no_info | tam | -0.2373 | 0 | 19 | 0.0000 |
| c_no_info | zero_shot | -0.1739 | 2 | 17 | 0.0007 |
| collective | care | -0.3179 | 0 | 24 | 0.0000 |
| collective | few_shot | -0.2654 | 0 | 21 | 0.0000 |
| collective | one_shot | -0.1867 | 1 | 16 | 0.0003 |
| collective | super_prompt | -0.2068 | 0 | 20 | 0.0000 |
| collective | system_message | -0.1065 | 4 | 14 | 0.0309 |
| collective | tam | -0.2531 | 0 | 21 | 0.0000 |
| collective | zero_shot | -0.1543 | 3 | 18 | 0.0015 |
| no-info | care | -0.2840 | 1 | 23 | 0.0000 |
| no-info | few_shot | -0.1836 | 1 | 18 | 0.0001 |
| no-info | one_shot | -0.1759 | 3 | 17 | 0.0026 |
| no-info | super_prompt | -0.2222 | 0 | 19 | 0.0000 |
| no-info | system_message | -0.0664 | 2 | 10 | 0.0386 |
| no-info | tam | -0.2130 | 1 | 19 | 0.0000 |
| no-info | zero_shot | -0.1327 | 2 | 16 | 0.0013 |
| premises | care | -0.2469 | 0 | 19 | 0.0000 |
| premises | few_shot | -0.2299 | 1 | 20 | 0.0000 |
| premises | one_shot | -0.2083 | 4 | 21 | 0.0009 |
| premises | super_prompt | -0.1852 | 0 | 17 | 0.0000 |
| premises | system_message | -0.1435 | 3 | 16 | 0.0044 |
| premises | tam | -0.1960 | 3 | 17 | 0.0026 |
| premises | zero_shot | -0.1836 | 3 | 21 | 0.0003 |

#### ROUGE-1

24 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana Ministral-3-8B-Instruct-2512-BF16 | p |
| --- | --- | --- | --- | --- | --- |
| a | super_prompt | -0.0382 | 4 | 23 | 0.0003 |
| a | system_message | +0.0281 | 21 | 6 | 0.0059 |
| a_no_info | tam | +0.0231 | 20 | 7 | 0.0192 |
| all | zero_shot | +0.0328 | 20 | 7 | 0.0192 |
| b | care | +0.0406 | 16 | 5 | 0.0266 |
| b | tam | +0.0402 | 16 | 5 | 0.0266 |
| b_no_info | care | +0.0439 | 17 | 4 | 0.0072 |
| b_no_info | one_shot | +0.0419 | 16 | 5 | 0.0266 |
| b_no_info | super_prompt | -0.0291 | 5 | 16 | 0.0266 |
| b_no_info | tam | +0.0474 | 17 | 4 | 0.0072 |
| c | super_prompt | -0.0246 | 4 | 18 | 0.0043 |
| c_no_info | super_prompt | -0.0192 | 5 | 18 | 0.0106 |
| c_no_info | tam | +0.0261 | 18 | 5 | 0.0106 |
| c_no_info | zero_shot | +0.0193 | 17 | 5 | 0.0169 |
| collective | care | +0.0280 | 20 | 7 | 0.0192 |
| collective | super_prompt | -0.0302 | 5 | 22 | 0.0015 |
| collective | zero_shot | +0.0313 | 20 | 7 | 0.0192 |
| no-info | care | +0.0209 | 20 | 7 | 0.0192 |
| no-info | super_prompt | -0.0442 | 2 | 25 | 0.0000 |
| no-info | tam | +0.0381 | 21 | 6 | 0.0059 |
| no-info | zero_shot | +0.0311 | 23 | 4 | 0.0003 |
| premises | care | +0.0268 | 22 | 5 | 0.0015 |
| premises | few_shot | +0.0387 | 22 | 5 | 0.0015 |
| premises | super_prompt | -0.0337 | 5 | 22 | 0.0015 |

#### ROUGE-2

9 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana Ministral-3-8B-Instruct-2512-BF16 | p |
| --- | --- | --- | --- | --- | --- |
| a | few_shot | +0.0104 | 12 | 3 | 0.0352 |
| all | tam | +0.0206 | 18 | 4 | 0.0043 |
| all | zero_shot | +0.0139 | 17 | 4 | 0.0072 |
| b_no_info | system_message | +0.0066 | 8 | 1 | 0.0391 |
| c | one_shot | +0.0139 | 8 | 1 | 0.0391 |
| c_no_info | care | +0.0250 | 12 | 2 | 0.0129 |
| c_no_info | tam | +0.0127 | 12 | 2 | 0.0129 |
| premises | few_shot | +0.0187 | 16 | 5 | 0.0266 |
| premises | system_message | +0.0158 | 17 | 1 | 0.0001 |

#### ROUGE-L

31 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana Ministral-3-8B-Instruct-2512-BF16 | p |
| --- | --- | --- | --- | --- | --- |
| a | few_shot | +0.0248 | 19 | 7 | 0.0290 |
| a | super_prompt | -0.0236 | 6 | 21 | 0.0059 |
| a | system_message | +0.0163 | 21 | 6 | 0.0059 |
| a_no_info | zero_shot | +0.0171 | 21 | 6 | 0.0059 |
| all | system_message | +0.0189 | 20 | 7 | 0.0192 |
| all | tam | +0.0261 | 20 | 7 | 0.0192 |
| all | zero_shot | +0.0242 | 21 | 6 | 0.0059 |
| b | care | +0.0371 | 16 | 5 | 0.0266 |
| b | few_shot | +0.0373 | 17 | 4 | 0.0072 |
| b_no_info | care | +0.0366 | 16 | 5 | 0.0266 |
| b_no_info | tam | +0.0391 | 18 | 3 | 0.0015 |
| b_no_info | zero_shot | +0.0288 | 16 | 5 | 0.0266 |
| c | care | +0.0157 | 18 | 5 | 0.0106 |
| c | system_message | +0.0223 | 17 | 6 | 0.0347 |
| c_no_info | tam | +0.0251 | 20 | 3 | 0.0005 |
| c_no_info | zero_shot | +0.0141 | 17 | 5 | 0.0169 |
| collective | care | +0.0285 | 20 | 6 | 0.0094 |
| collective | few_shot | +0.0309 | 19 | 7 | 0.0290 |
| collective | super_prompt | -0.0143 | 6 | 21 | 0.0059 |
| collective | tam | +0.0193 | 20 | 7 | 0.0192 |
| collective | zero_shot | +0.0233 | 20 | 7 | 0.0192 |
| no-info | care | +0.0267 | 22 | 5 | 0.0015 |
| no-info | few_shot | +0.0281 | 20 | 7 | 0.0192 |
| no-info | super_prompt | -0.0174 | 6 | 21 | 0.0059 |
| no-info | tam | +0.0224 | 21 | 6 | 0.0059 |
| no-info | zero_shot | +0.0320 | 24 | 3 | 0.0000 |
| premises | one_shot | +0.0107 | 22 | 5 | 0.0015 |
| premises | super_prompt | -0.0204 | 5 | 22 | 0.0015 |
| premises | system_message | +0.0322 | 23 | 4 | 0.0003 |
| premises | tam | +0.0309 | 20 | 5 | 0.0041 |
| premises | zero_shot | +0.0245 | 20 | 7 | 0.0192 |

#### BERT-F1

49 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana Ministral-3-8B-Instruct-2512-BF16 | p |
| --- | --- | --- | --- | --- | --- |
| a | few_shot | +0.0170 | 23 | 4 | 0.0003 |
| a | super_prompt | -0.0163 | 6 | 21 | 0.0059 |
| a | system_message | +0.0236 | 26 | 1 | 0.0000 |
| a | tam | +0.0141 | 23 | 4 | 0.0003 |
| a | zero_shot | +0.0135 | 24 | 3 | 0.0000 |
| a_no_info | super_prompt | -0.0407 | 1 | 26 | 0.0000 |
| a_no_info | system_message | +0.0213 | 21 | 6 | 0.0059 |
| a_no_info | tam | +0.0122 | 20 | 7 | 0.0192 |
| a_no_info | zero_shot | +0.0184 | 23 | 4 | 0.0003 |
| all | care | +0.0187 | 23 | 4 | 0.0003 |
| all | few_shot | +0.0236 | 23 | 4 | 0.0003 |
| all | super_prompt | -0.0121 | 6 | 21 | 0.0059 |
| all | system_message | +0.0151 | 21 | 6 | 0.0059 |
| all | tam | +0.0143 | 21 | 6 | 0.0059 |
| all | zero_shot | +0.0188 | 24 | 3 | 0.0000 |
| b | care | +0.0255 | 18 | 3 | 0.0015 |
| b | tam | +0.0160 | 17 | 4 | 0.0072 |
| b | zero_shot | +0.0092 | 16 | 5 | 0.0266 |
| b_no_info | care | +0.0259 | 19 | 2 | 0.0002 |
| b_no_info | few_shot | +0.0194 | 17 | 4 | 0.0072 |
| b_no_info | one_shot | +0.0184 | 18 | 3 | 0.0015 |
| b_no_info | super_prompt | -0.0136 | 4 | 17 | 0.0072 |
| b_no_info | system_message | +0.0151 | 17 | 4 | 0.0072 |
| b_no_info | tam | +0.0228 | 20 | 1 | 0.0000 |
| b_no_info | zero_shot | +0.0169 | 17 | 4 | 0.0072 |
| c | few_shot | +0.0154 | 18 | 5 | 0.0106 |
| c | system_message | +0.0204 | 19 | 4 | 0.0026 |
| c | tam | +0.0240 | 20 | 3 | 0.0005 |
| c | zero_shot | +0.0209 | 18 | 5 | 0.0106 |
| c_no_info | care | +0.0146 | 18 | 5 | 0.0106 |
| c_no_info | system_message | +0.0111 | 19 | 4 | 0.0026 |
| c_no_info | tam | +0.0147 | 18 | 5 | 0.0106 |
| c_no_info | zero_shot | +0.0182 | 19 | 4 | 0.0026 |
| collective | care | +0.0185 | 22 | 5 | 0.0015 |
| collective | super_prompt | -0.0163 | 7 | 20 | 0.0192 |
| collective | system_message | +0.0144 | 22 | 5 | 0.0015 |
| collective | tam | +0.0138 | 21 | 6 | 0.0059 |
| collective | zero_shot | +0.0200 | 24 | 3 | 0.0000 |
| no-info | care | +0.0202 | 24 | 3 | 0.0000 |
| no-info | few_shot | +0.0165 | 22 | 5 | 0.0015 |
| no-info | system_message | +0.0147 | 21 | 6 | 0.0059 |
| no-info | tam | +0.0126 | 22 | 5 | 0.0015 |
| no-info | zero_shot | +0.0175 | 23 | 4 | 0.0003 |
| premises | care | +0.0206 | 24 | 3 | 0.0000 |
| premises | few_shot | +0.0169 | 21 | 6 | 0.0059 |
| premises | super_prompt | -0.0117 | 7 | 20 | 0.0192 |
| premises | system_message | +0.0208 | 20 | 7 | 0.0192 |
| premises | tam | +0.0121 | 21 | 6 | 0.0059 |
| premises | zero_shot | +0.0152 | 21 | 6 | 0.0059 |

### Llama-3.2-3B-Instruct vs gemma-4-12B-it

#### Puntaje de calidad (juez 1)

29 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | care | -0.2006 | 2 | 15 | 0.0023 |
| a | few_shot | -0.1219 | 4 | 17 | 0.0072 |
| a | super_prompt | -0.1281 | 2 | 16 | 0.0013 |
| a | tam | -0.0787 | 2 | 10 | 0.0386 |
| a | zero_shot | -0.1512 | 1 | 14 | 0.0010 |
| a_no_info | care | -0.3056 | 1 | 22 | 0.0000 |
| a_no_info | few_shot | -0.1435 | 4 | 15 | 0.0192 |
| a_no_info | super_prompt | -0.2114 | 0 | 22 | 0.0000 |
| a_no_info | system_message | -0.2052 | 1 | 18 | 0.0001 |
| a_no_info | tam | -0.1620 | 2 | 19 | 0.0002 |
| a_no_info | zero_shot | -0.2840 | 0 | 20 | 0.0000 |
| all | care | -0.1497 | 0 | 10 | 0.0020 |
| all | few_shot | -0.1651 | 2 | 17 | 0.0007 |
| all | tam | -0.0988 | 2 | 11 | 0.0225 |
| b | care | -0.1647 | 0 | 15 | 0.0001 |
| b | one_shot | -0.0833 | 1 | 11 | 0.0063 |
| b | zero_shot | -0.1151 | 1 | 11 | 0.0063 |
| b_no_info | care | -0.1806 | 0 | 17 | 0.0000 |
| b_no_info | one_shot | -0.0635 | 3 | 12 | 0.0352 |
| b_no_info | super_prompt | -0.2103 | 1 | 14 | 0.0010 |
| b_no_info | tam | -0.1171 | 3 | 12 | 0.0352 |
| collective | care | -0.1250 | 2 | 13 | 0.0074 |
| collective | few_shot | -0.1343 | 3 | 17 | 0.0026 |
| no-info | few_shot | -0.0957 | 3 | 13 | 0.0213 |
| no-info | system_message | +0.0818 | 9 | 1 | 0.0215 |
| no-info | zero_shot | +0.0895 | 11 | 2 | 0.0225 |
| premises | care | -0.1019 | 1 | 10 | 0.0117 |
| premises | few_shot | -0.1343 | 4 | 16 | 0.0118 |
| premises | one_shot | -0.1497 | 4 | 14 | 0.0309 |

#### ROUGE-1

11 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | super_prompt | -0.0460 | 3 | 24 | 0.0000 |
| a_no_info | super_prompt | -0.0442 | 5 | 22 | 0.0015 |
| all | super_prompt | -0.0394 | 4 | 23 | 0.0003 |
| b | super_prompt | -0.0306 | 4 | 17 | 0.0072 |
| b_no_info | super_prompt | -0.0411 | 3 | 18 | 0.0015 |
| c | super_prompt | -0.0380 | 4 | 19 | 0.0026 |
| c_no_info | super_prompt | -0.0446 | 2 | 21 | 0.0001 |
| collective | super_prompt | -0.0379 | 4 | 22 | 0.0005 |
| no-info | care | +0.0138 | 20 | 7 | 0.0192 |
| no-info | super_prompt | -0.0318 | 6 | 21 | 0.0059 |
| premises | tam | +0.0136 | 20 | 7 | 0.0192 |

#### ROUGE-2

15 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| all | system_message | +0.0108 | 12 | 2 | 0.0129 |
| b | super_prompt | +0.0112 | 14 | 2 | 0.0042 |
| b | tam | +0.0140 | 9 | 1 | 0.0215 |
| c | super_prompt | +0.0102 | 12 | 3 | 0.0352 |
| c | system_message | +0.0160 | 8 | 1 | 0.0391 |
| c | zero_shot | +0.0225 | 13 | 3 | 0.0213 |
| c_no_info | care | +0.0295 | 11 | 2 | 0.0225 |
| c_no_info | super_prompt | +0.0074 | 8 | 1 | 0.0391 |
| c_no_info | tam | +0.0148 | 11 | 2 | 0.0225 |
| collective | super_prompt | +0.0098 | 18 | 6 | 0.0227 |
| no-info | care | +0.0173 | 16 | 3 | 0.0044 |
| no-info | super_prompt | +0.0168 | 21 | 2 | 0.0001 |
| no-info | system_message | +0.0163 | 16 | 3 | 0.0044 |
| premises | care | +0.0108 | 13 | 3 | 0.0213 |
| premises | super_prompt | +0.0079 | 16 | 5 | 0.0266 |

#### ROUGE-L

12 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | super_prompt | -0.0277 | 6 | 21 | 0.0059 |
| all | super_prompt | -0.0285 | 5 | 22 | 0.0015 |
| b | care | +0.0309 | 16 | 5 | 0.0266 |
| b | few_shot | +0.0444 | 17 | 4 | 0.0072 |
| b_no_info | super_prompt | -0.0166 | 5 | 16 | 0.0266 |
| c | super_prompt | -0.0214 | 4 | 19 | 0.0026 |
| c_no_info | super_prompt | -0.0177 | 6 | 17 | 0.0347 |
| no-info | care | +0.0201 | 18 | 7 | 0.0433 |
| no-info | super_prompt | -0.0259 | 5 | 22 | 0.0015 |
| premises | super_prompt | -0.0260 | 6 | 21 | 0.0059 |
| premises | system_message | +0.0323 | 23 | 4 | 0.0003 |
| premises | tam | +0.0179 | 20 | 7 | 0.0192 |

#### BERT-F1

27 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Llama-3.2-3B-Instruct | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | super_prompt | -0.0343 | 1 | 26 | 0.0000 |
| a_no_info | super_prompt | -0.0548 | 1 | 26 | 0.0000 |
| a_no_info | zero_shot | +0.0075 | 21 | 6 | 0.0059 |
| all | care | +0.0105 | 20 | 7 | 0.0192 |
| all | super_prompt | -0.0125 | 5 | 22 | 0.0015 |
| all | system_message | +0.0139 | 22 | 5 | 0.0015 |
| all | zero_shot | +0.0092 | 22 | 5 | 0.0015 |
| b | care | +0.0188 | 17 | 4 | 0.0072 |
| b | few_shot | +0.0076 | 16 | 5 | 0.0266 |
| b | super_prompt | -0.0249 | 2 | 19 | 0.0002 |
| b | system_message | +0.0097 | 16 | 5 | 0.0266 |
| b_no_info | care | +0.0147 | 16 | 5 | 0.0266 |
| b_no_info | few_shot | +0.0111 | 16 | 5 | 0.0266 |
| b_no_info | super_prompt | -0.0227 | 2 | 19 | 0.0002 |
| c | super_prompt | -0.0209 | 4 | 19 | 0.0026 |
| c | system_message | +0.0135 | 20 | 3 | 0.0005 |
| c | tam | +0.0129 | 17 | 6 | 0.0347 |
| c_no_info | care | +0.0051 | 17 | 6 | 0.0347 |
| c_no_info | super_prompt | -0.0263 | 2 | 21 | 0.0001 |
| collective | super_prompt | -0.0158 | 7 | 20 | 0.0192 |
| no-info | care | +0.0168 | 22 | 5 | 0.0015 |
| no-info | system_message | +0.0118 | 25 | 2 | 0.0000 |
| no-info | zero_shot | +0.0131 | 21 | 6 | 0.0059 |
| premises | care | +0.0151 | 20 | 7 | 0.0192 |
| premises | super_prompt | -0.0172 | 4 | 23 | 0.0003 |
| premises | system_message | +0.0176 | 22 | 5 | 0.0015 |
| premises | zero_shot | +0.0085 | 21 | 6 | 0.0059 |

### Ministral-3-8B-Instruct-2512-BF16 vs gemma-4-12B-it

#### Puntaje de calidad (juez 1)

62 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Ministral-3-8B-Instruct-2512-BF16 | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | care | +0.0756 | 8 | 1 | 0.0391 |
| a | few_shot | +0.0988 | 15 | 2 | 0.0023 |
| a | one_shot | +0.0756 | 14 | 3 | 0.0127 |
| a | system_message | +0.1466 | 14 | 0 | 0.0001 |
| a | tam | +0.1543 | 16 | 1 | 0.0003 |
| a_no_info | few_shot | +0.1096 | 15 | 2 | 0.0023 |
| a_no_info | one_shot | +0.0602 | 13 | 4 | 0.0490 |
| a_no_info | super_prompt | +0.0849 | 13 | 4 | 0.0490 |
| a_no_info | tam | +0.0648 | 12 | 0 | 0.0005 |
| all | care | +0.1543 | 14 | 0 | 0.0001 |
| all | few_shot | +0.1481 | 18 | 2 | 0.0004 |
| all | one_shot | +0.1389 | 18 | 2 | 0.0004 |
| all | super_prompt | +0.1836 | 17 | 2 | 0.0007 |
| all | system_message | +0.2006 | 18 | 0 | 0.0000 |
| all | tam | +0.1713 | 19 | 2 | 0.0002 |
| all | zero_shot | +0.1204 | 16 | 3 | 0.0044 |
| b | care | +0.1567 | 15 | 1 | 0.0005 |
| b | few_shot | +0.1349 | 14 | 0 | 0.0001 |
| b | one_shot | +0.1885 | 19 | 0 | 0.0000 |
| b | system_message | +0.2262 | 15 | 0 | 0.0001 |
| b | tam | +0.1548 | 13 | 1 | 0.0018 |
| b | zero_shot | +0.1409 | 13 | 0 | 0.0002 |
| b_no_info | care | +0.1151 | 14 | 0 | 0.0001 |
| b_no_info | few_shot | +0.1925 | 19 | 1 | 0.0000 |
| b_no_info | one_shot | +0.1567 | 15 | 0 | 0.0001 |
| b_no_info | super_prompt | +0.1052 | 11 | 2 | 0.0225 |
| b_no_info | system_message | +0.1865 | 15 | 1 | 0.0005 |
| b_no_info | tam | +0.1071 | 13 | 1 | 0.0018 |
| c | care | +0.2391 | 17 | 0 | 0.0000 |
| c | few_shot | +0.2409 | 17 | 0 | 0.0000 |
| c | one_shot | +0.2101 | 17 | 1 | 0.0001 |
| c | super_prompt | +0.2174 | 18 | 2 | 0.0004 |
| c | system_message | +0.1848 | 15 | 0 | 0.0001 |
| c | tam | +0.1920 | 14 | 0 | 0.0001 |
| c | zero_shot | +0.2047 | 17 | 0 | 0.0000 |
| c_no_info | care | +0.1975 | 18 | 0 | 0.0000 |
| c_no_info | few_shot | +0.2319 | 20 | 0 | 0.0000 |
| c_no_info | one_shot | +0.1413 | 13 | 2 | 0.0074 |
| c_no_info | super_prompt | +0.2192 | 18 | 0 | 0.0000 |
| c_no_info | system_message | +0.1304 | 12 | 2 | 0.0129 |
| c_no_info | tam | +0.2301 | 16 | 0 | 0.0000 |
| c_no_info | zero_shot | +0.1232 | 15 | 3 | 0.0075 |
| collective | care | +0.1929 | 20 | 1 | 0.0000 |
| collective | few_shot | +0.1312 | 16 | 1 | 0.0003 |
| collective | one_shot | +0.1204 | 16 | 2 | 0.0013 |
| collective | super_prompt | +0.1960 | 18 | 1 | 0.0001 |
| collective | system_message | +0.1481 | 14 | 1 | 0.0010 |
| collective | tam | +0.1960 | 18 | 1 | 0.0001 |
| collective | zero_shot | +0.1219 | 16 | 4 | 0.0118 |
| no-info | care | +0.2160 | 20 | 2 | 0.0001 |
| no-info | few_shot | +0.0880 | 12 | 2 | 0.0129 |
| no-info | one_shot | +0.1219 | 16 | 5 | 0.0266 |
| no-info | super_prompt | +0.1929 | 17 | 0 | 0.0000 |
| no-info | system_message | +0.1481 | 13 | 0 | 0.0002 |
| no-info | tam | +0.1821 | 15 | 0 | 0.0001 |
| no-info | zero_shot | +0.2222 | 23 | 0 | 0.0000 |
| premises | care | +0.1451 | 14 | 1 | 0.0010 |
| premises | one_shot | +0.0586 | 13 | 4 | 0.0490 |
| premises | super_prompt | +0.1651 | 17 | 0 | 0.0000 |
| premises | system_message | +0.1728 | 15 | 0 | 0.0001 |
| premises | tam | +0.1219 | 13 | 4 | 0.0490 |
| premises | zero_shot | +0.0988 | 17 | 3 | 0.0026 |

#### ROUGE-1

11 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Ministral-3-8B-Instruct-2512-BF16 | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | one_shot | -0.0171 | 7 | 19 | 0.0290 |
| a_no_info | zero_shot | -0.0161 | 6 | 21 | 0.0059 |
| all | tam | -0.0211 | 5 | 21 | 0.0025 |
| b | tam | -0.0295 | 5 | 16 | 0.0266 |
| b_no_info | care | -0.0289 | 4 | 16 | 0.0118 |
| b_no_info | tam | -0.0448 | 3 | 18 | 0.0015 |
| b_no_info | zero_shot | -0.0350 | 4 | 17 | 0.0072 |
| c | tam | -0.0233 | 4 | 19 | 0.0026 |
| c_no_info | few_shot | -0.0280 | 6 | 17 | 0.0347 |
| c_no_info | super_prompt | -0.0254 | 5 | 18 | 0.0106 |
| c_no_info | tam | -0.0082 | 6 | 17 | 0.0347 |

#### ROUGE-2

4 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Ministral-3-8B-Instruct-2512-BF16 | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| b | super_prompt | +0.0085 | 10 | 2 | 0.0386 |
| b | system_message | +0.0088 | 8 | 1 | 0.0391 |
| b | tam | +0.0069 | 8 | 1 | 0.0391 |
| collective | care | +0.0087 | 15 | 4 | 0.0192 |

#### ROUGE-L

9 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Ministral-3-8B-Instruct-2512-BF16 | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | one_shot | -0.0102 | 7 | 19 | 0.0290 |
| b_no_info | one_shot | -0.0272 | 4 | 17 | 0.0072 |
| b_no_info | tam | -0.0228 | 5 | 16 | 0.0266 |
| b_no_info | zero_shot | -0.0248 | 2 | 19 | 0.0002 |
| c | super_prompt | -0.0148 | 6 | 17 | 0.0347 |
| c | tam | -0.0141 | 4 | 19 | 0.0026 |
| collective | few_shot | -0.0161 | 7 | 20 | 0.0192 |
| no-info | zero_shot | -0.0261 | 4 | 23 | 0.0003 |
| premises | zero_shot | -0.0178 | 4 | 23 | 0.0003 |

#### BERT-F1

37 de 70 comparaciones significativas (p < 0.05).

| Experimento | Técnica | Δ media | gana Ministral-3-8B-Instruct-2512-BF16 | gana gemma-4-12B-it | p |
| --- | --- | --- | --- | --- | --- |
| a | care | -0.0119 | 6 | 21 | 0.0059 |
| a | few_shot | -0.0152 | 6 | 21 | 0.0059 |
| a | one_shot | -0.0171 | 6 | 21 | 0.0059 |
| a | system_message | -0.0183 | 1 | 26 | 0.0000 |
| a | tam | -0.0178 | 1 | 26 | 0.0000 |
| a | zero_shot | -0.0150 | 4 | 23 | 0.0003 |
| a_no_info | care | -0.0148 | 4 | 23 | 0.0003 |
| a_no_info | few_shot | -0.0108 | 5 | 22 | 0.0015 |
| a_no_info | one_shot | -0.0148 | 7 | 20 | 0.0192 |
| a_no_info | super_prompt | -0.0142 | 7 | 20 | 0.0192 |
| a_no_info | system_message | -0.0156 | 5 | 22 | 0.0015 |
| a_no_info | tam | -0.0145 | 4 | 23 | 0.0003 |
| a_no_info | zero_shot | -0.0109 | 6 | 21 | 0.0059 |
| all | few_shot | -0.0195 | 4 | 23 | 0.0003 |
| b | care | -0.0067 | 5 | 16 | 0.0266 |
| b | few_shot | -0.0096 | 5 | 16 | 0.0266 |
| b | super_prompt | -0.0425 | 3 | 18 | 0.0015 |
| b_no_info | care | -0.0112 | 5 | 16 | 0.0266 |
| b_no_info | system_message | -0.0100 | 5 | 16 | 0.0266 |
| b_no_info | tam | -0.0188 | 2 | 19 | 0.0002 |
| b_no_info | zero_shot | -0.0146 | 1 | 20 | 0.0000 |
| c | care | -0.0136 | 6 | 17 | 0.0347 |
| c | super_prompt | -0.0355 | 5 | 18 | 0.0106 |
| c | zero_shot | -0.0095 | 5 | 18 | 0.0106 |
| c_no_info | care | -0.0095 | 5 | 18 | 0.0106 |
| c_no_info | super_prompt | -0.0231 | 5 | 18 | 0.0106 |
| c_no_info | system_message | -0.0089 | 5 | 18 | 0.0106 |
| c_no_info | tam | -0.0125 | 6 | 17 | 0.0347 |
| c_no_info | zero_shot | -0.0196 | 3 | 20 | 0.0005 |
| collective | care | -0.0090 | 6 | 21 | 0.0059 |
| collective | few_shot | -0.0174 | 5 | 22 | 0.0015 |
| collective | tam | -0.0110 | 6 | 21 | 0.0059 |
| no-info | few_shot | -0.0141 | 3 | 24 | 0.0000 |
| no-info | one_shot | -0.0125 | 7 | 20 | 0.0192 |
| no-info | tam | -0.0086 | 6 | 21 | 0.0059 |
| premises | few_shot | -0.0248 | 3 | 24 | 0.0000 |
| premises | one_shot | -0.0173 | 4 | 23 | 0.0003 |

## 4. Ranking global

`Experimentos ganados` = configs donde el modelo logra el mejor valor con su mejor técnica (de la sección 1). `Media de mejores` = promedio de esos valores. `Media global` = promedio de todas las técnicas en todos los experimentos.

### 4.1 Jueces

#### Puntaje de calidad (juez 1)

| modelo | Experimentos ganados | Media de mejores | Media global |
| --- | --- | --- | --- |
| Llama-3.2-3B-Instruct | 0/10 | 0.7023 | 0.6392 |
| Ministral-3-8B-Instruct-2512-BF16 | 10/10 | 0.9064 | 0.8584 |
| gemma-4-12B-it | 0/10 | 0.7871 | 0.7136 |

#### Tasa de preferencia (juez 2)

| modelo | Experimentos ganados | Media de mejores | Media global |
| --- | --- | --- | --- |
| Llama-3.2-3B-Instruct | 4/10 | 0.9101 | 0.7900 |
| Ministral-3-8B-Instruct-2512-BF16 | 10/10 | 1.0000 | 0.9865 |
| gemma-4-12B-it | 6/10 | 0.9482 | 0.8706 |

### 4.2 Métricas automáticas

#### ROUGE-1

| modelo | Experimentos ganados | Media de mejores | Media global |
| --- | --- | --- | --- |
| Llama-3.2-3B-Instruct | 8/10 | 0.1902 | 0.1552 |
| Ministral-3-8B-Instruct-2512-BF16 | 0/10 | 0.1675 | 0.1406 |
| gemma-4-12B-it | 2/10 | 0.1830 | 0.1537 |

#### ROUGE-2

| modelo | Experimentos ganados | Media de mejores | Media global |
| --- | --- | --- | --- |
| Llama-3.2-3B-Instruct | 7/10 | 0.0326 | 0.0215 |
| Ministral-3-8B-Instruct-2512-BF16 | 0/10 | 0.0212 | 0.0142 |
| gemma-4-12B-it | 3/10 | 0.0243 | 0.0130 |

#### ROUGE-L

| modelo | Experimentos ganados | Media de mejores | Media global |
| --- | --- | --- | --- |
| Llama-3.2-3B-Instruct | 8/10 | 0.1404 | 0.1139 |
| Ministral-3-8B-Instruct-2512-BF16 | 0/10 | 0.1193 | 0.0989 |
| gemma-4-12B-it | 2/10 | 0.1322 | 0.1093 |

#### BERT-F1

| modelo | Experimentos ganados | Media de mejores | Media global |
| --- | --- | --- | --- |
| Llama-3.2-3B-Instruct | 7/10 | 0.7191 | 0.7009 |
| Ministral-3-8B-Instruct-2512-BF16 | 0/10 | 0.7034 | 0.6891 |
| gemma-4-12B-it | 3/10 | 0.7182 | 0.7004 |
