# Resumen (Ministral-3-8B-Instruct-2512-BF16)

Éxito evaluado **por métrica, sin combinar**. `★` = mejor de la columna, `▲` = mejor de la fila. Agrupación: genéricas (mismos 27 tweets) y tipeadas (a/b/c comparten tweets solo dentro de su par).

- `few_shot`: n = 3 ejemplos (campo `fewshot_examples` de `config.json`).

## PARTE I — Jueces

El puntaje de calidad (juez 1) y la tasa de preferencia (juez 2) se analizan por separado; ⚠ marca cuando el ganador difiere entre ambos.

### 1.1 Cruce genéricas (técnica × experimento)

#### Puntaje de calidad (juez 1)

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.8673 | 0.8873★▲ | 0.8519 | 0.8657★ |
| few_shot (n=3) | 0.8966★▲ | 0.8657 | 0.8549★ | 0.8318 |
| one_shot | 0.8241▲ | 0.7948 | 0.7855 | 0.7762 |
| super_prompt | 0.8133 | 0.8349▲ | 0.7793 | 0.8025 |
| system_message | 0.8148▲ | 0.7809 | 0.7932 | 0.7438 |
| tam | 0.8765 | 0.8827▲ | 0.8534 | 0.8441 |
| zero_shot | 0.8503▲ | 0.8410 | 0.8457 | 0.8488 |

#### Tasa de preferencia (juez 2)

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| few_shot (n=3) | 0.9630▲ | 0.9630▲ | 0.9630▲ | 0.8519 |
| one_shot | 1.0000★▲ | 1.0000★▲ | 0.8889 | 0.9259 |
| super_prompt | 1.0000★▲ | 1.0000★▲ | 0.9630 | 0.9630 |
| system_message | 0.9630 | 0.9630 | 1.0000★▲ | 0.8889 |
| tam | 0.9630 | 1.0000★▲ | 0.9259 | 1.0000★▲ |
| zero_shot | 0.9630 | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |

### 1.2 Cruce tipeadas (técnica × experimento)

#### Puntaje de calidad (juez 1)

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.8549 | 0.8920 | 0.9167★ | 0.9206★▲ | 0.8913 | 0.8804 |
| few_shot (n=3) | 0.8796 | 0.8735 | 0.8869 | 0.8909▲ | 0.8351 | 0.8623 |
| one_shot | 0.8519 | 0.8071 | 0.9008▲ | 0.8671 | 0.8333 | 0.7953 |
| super_prompt | 0.8287 | 0.8395 | 0.7937 | 0.8393 | 0.8641 | 0.8750▲ |
| system_message | 0.8086 | 0.8364 | 0.8690 | 0.9087▲ | 0.8696 | 0.8442 |
| tam | 0.9136★ | 0.9228★ | 0.8909 | 0.9087 | 0.9203 | 0.9293★▲ |
| zero_shot | 0.8688 | 0.9213 | 0.9087 | 0.9028 | 0.9565★▲ | 0.9239 |

#### Tasa de preferencia (juez 2)

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| few_shot (n=3) | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 0.9524 | 1.0000★▲ | 1.0000★▲ |
| one_shot | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| super_prompt | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| system_message | 1.0000★▲ | 1.0000★▲ | 0.9524 | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| tam | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |
| zero_shot | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ | 1.0000★▲ |

### 1.3 Mejor técnica por experimento

| Experimento | Mejor (juez 1) | Puntaje de calidad (juez 1) | Mejor (juez 2) | Tasa de preferencia (juez 2) | ¿coinciden? |
| --- | --- | --- | --- | --- | --- |
| all | few_shot (n=3) | 0.8966 | care | 1.0000 | ⚠ no |
| collective | care | 0.8873 | care | 1.0000 | ★ |
| premises | few_shot (n=3) | 0.8549 | care | 1.0000 | ⚠ no |
| no-info | care | 0.8657 | care | 1.0000 | ★ |
| a | tam | 0.9136 | care | 1.0000 | ⚠ no |
| a_no_info | tam | 0.9228 | care | 1.0000 | ⚠ no |
| b | care | 0.9167 | care | 1.0000 | ★ |
| b_no_info | care | 0.9206 | care | 1.0000 | ★ |
| c | zero_shot | 0.9565 | care | 1.0000 | ⚠ no |
| c_no_info | tam | 0.9293 | care | 1.0000 | ⚠ no |

### 1.4 Mejor experimento por técnica — genéricas

| técnica | Puntaje de calidad (juez 1) | Tasa de preferencia (juez 2) |
| --- | --- | --- |
| care | collective (0.8873) | all (1.0000) |
| few_shot (n=3) | all (0.8966) | all (0.9630) |
| one_shot | all (0.8241) | all (1.0000) |
| super_prompt | collective (0.8349) | all (1.0000) |
| system_message | all (0.8148) | premises (1.0000) |
| tam | collective (0.8827) | collective (1.0000) |
| zero_shot | all (0.8503) | collective (1.0000) |

### 1.5 Mejor global — genéricas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| Puntaje de calidad (juez 1) | all / few_shot (n=3) (0.8966) |
| Tasa de preferencia (juez 2) | all / care (1.0000) |

### 1.6 Mejor experimento por técnica — tipeadas

| técnica | Puntaje de calidad (juez 1) | Tasa de preferencia (juez 2) |
| --- | --- | --- |
| care | b_no_info (0.9206) | a (1.0000) |
| few_shot (n=3) | b_no_info (0.8909) | a (1.0000) |
| one_shot | b (0.9008) | a (1.0000) |
| super_prompt | c_no_info (0.8750) | a (1.0000) |
| system_message | b_no_info (0.9087) | a (1.0000) |
| tam | c_no_info (0.9293) | a (1.0000) |
| zero_shot | c (0.9565) | a (1.0000) |

### 1.7 Mejor global — tipeadas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| Puntaje de calidad (juez 1) | c / zero_shot (0.9565) |
| Tasa de preferencia (juez 2) | a / care (1.0000) |

### 1.8 Efecto de la información (pares con tweets compartidos)

Cada par difiere solo en si se inyecta la información del tipo (`a`→con info, `a_no_info`→sin info). Positivo = conviene inyectarla.

#### Puntaje de calidad (juez 1)

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | -0.0370 | 1 | 4 | 0.3750 |
| a vs a_no_info | few_shot (n=3) | +0.0062 | 5 | 4 | 1.0000 |
| a vs a_no_info | one_shot | +0.0448 | 8 | 2 | 0.1094 |
| a vs a_no_info | super_prompt | -0.0108 | 7 | 6 | 1.0000 |
| a vs a_no_info | system_message | -0.0278 | 5 | 7 | 0.7744 |
| a vs a_no_info | tam | -0.0093 | 2 | 3 | 1.0000 |
| a vs a_no_info | zero_shot | -0.0525 | 4 | 13 | 0.0490 |
| b vs b_no_info | care | -0.0040 | 4 | 2 | 0.6875 |
| b vs b_no_info | few_shot (n=3) | -0.0040 | 2 | 2 | 1.0000 |
| b vs b_no_info | one_shot | +0.0337 | 4 | 0 | 0.1250 |
| b vs b_no_info | super_prompt | -0.0456 | 4 | 10 | 0.1796 |
| b vs b_no_info | system_message | -0.0397 | 1 | 5 | 0.2188 |
| b vs b_no_info | tam | -0.0179 | 1 | 3 | 0.6250 |
| b vs b_no_info | zero_shot | +0.0060 | 5 | 3 | 0.7266 |
| c vs c_no_info | care | +0.0109 | 5 | 3 | 0.7266 |
| c vs c_no_info | few_shot (n=3) | -0.0272 | 2 | 5 | 0.4531 |
| c vs c_no_info | one_shot | +0.0380 | 6 | 5 | 1.0000 |
| c vs c_no_info | super_prompt | -0.0109 | 5 | 7 | 0.7744 |
| c vs c_no_info | system_message | +0.0254 | 7 | 6 | 1.0000 |
| c vs c_no_info | tam | -0.0091 | 5 | 5 | 1.0000 |
| c vs c_no_info | zero_shot | +0.0326 | 8 | 3 | 0.2266 |

## PARTE II — Métricas automáticas

Métricas: ROUGE-1, ROUGE-2, ROUGE-L, BERT-F1 (por separado).

### 2.1 Cruce genéricas (técnica × experimento)

#### ROUGE-1

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.1675▲ | 0.1579 | 0.1572 | 0.1641 |
| few_shot (n=3) | 0.1928▲ | 0.1909★ | 0.1784 | 0.1840★ |
| one_shot | 0.1943★▲ | 0.1908 | 0.1912★ | 0.1784 |
| super_prompt | 0.1544 | 0.1448 | 0.1505 | 0.1646▲ |
| system_message | 0.1492 | 0.1520▲ | 0.1488 | 0.1458 |
| tam | 0.1512 | 0.1506 | 0.1521▲ | 0.1382 |
| zero_shot | 0.1384 | 0.1418 | 0.1438▲ | 0.1366 |

#### ROUGE-2

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.0196 | 0.0229▲ | 0.0184 | 0.0182 |
| few_shot (n=3) | 0.0263 | 0.0340★▲ | 0.0250 | 0.0293★ |
| one_shot | 0.0291★ | 0.0306▲ | 0.0280★ | 0.0226 |
| super_prompt | 0.0212▲ | 0.0175 | 0.0134 | 0.0164 |
| system_message | 0.0161 | 0.0185▲ | 0.0093 | 0.0159 |
| tam | 0.0150 | 0.0230▲ | 0.0173 | 0.0199 |
| zero_shot | 0.0156 | 0.0209▲ | 0.0196 | 0.0156 |

#### ROUGE-L

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.1163▲ | 0.1131 | 0.1054 | 0.1100 |
| few_shot (n=3) | 0.1356▲ | 0.1341★ | 0.1266 | 0.1345★ |
| one_shot | 0.1356★▲ | 0.1311 | 0.1335★ | 0.1249 |
| super_prompt | 0.1054 | 0.1021 | 0.1062▲ | 0.1060 |
| system_message | 0.1017 | 0.1059▲ | 0.0966 | 0.1011 |
| tam | 0.1007 | 0.1074▲ | 0.1035 | 0.1000 |
| zero_shot | 0.0978 | 0.0994▲ | 0.0992 | 0.0940 |

#### BERT-F1

| técnica | all | collective | premises | no-info |
| --- | --- | --- | --- | --- |
| care | 0.6952 | 0.6946 | 0.6891 | 0.6969▲ |
| few_shot (n=3) | 0.7107★ | 0.7135★ | 0.7069★ | 0.7175★▲ |
| one_shot | 0.7081 | 0.7123▲ | 0.7030 | 0.7055 |
| super_prompt | 0.6900 | 0.6898 | 0.6855 | 0.6908▲ |
| system_message | 0.6908▲ | 0.6896 | 0.6865 | 0.6858 |
| tam | 0.6923 | 0.6928 | 0.6935▲ | 0.6902 |
| zero_shot | 0.6895 | 0.6894 | 0.6901▲ | 0.6877 |

### 2.2 Cruce tipeadas (técnica × experimento)

#### ROUGE-1

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.1362 | 0.1271 | 0.1319 | 0.1340 | 0.1400▲ | 0.1271 |
| few_shot (n=3) | 0.1225 | 0.1528★ | 0.1620★▲ | 0.1601★ | 0.1416 | 0.1382 |
| one_shot | 0.1395★ | 0.1414 | 0.1468 | 0.1513 | 0.1422★ | 0.1580★▲ |
| super_prompt | 0.1260▲ | 0.1174 | 0.1146 | 0.1224 | 0.1164 | 0.1103 |
| system_message | 0.1133 | 0.1258▲ | 0.1177 | 0.1117 | 0.1255 | 0.1257 |
| tam | 0.1270▲ | 0.1088 | 0.1105 | 0.1094 | 0.1147 | 0.1107 |
| zero_shot | 0.1174 | 0.1035 | 0.1240 | 0.1001 | 0.1267▲ | 0.1026 |

#### ROUGE-2

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.0126★ | 0.0115 | 0.0156▲ | 0.0085 | 0.0103★ | 0.0086 |
| few_shot (n=3) | 0.0115 | 0.0129 | 0.0237★▲ | 0.0160 | 0.0033 | 0.0063 |
| one_shot | 0.0107 | 0.0147★ | 0.0133 | 0.0174★▲ | 0.0052 | 0.0133★ |
| super_prompt | 0.0062 | 0.0053 | 0.0132 | 0.0150▲ | 0.0068 | 0.0067 |
| system_message | 0.0083 | 0.0086 | 0.0133▲ | 0.0036 | 0.0048 | 0.0107 |
| tam | 0.0111▲ | 0.0042 | 0.0085 | 0.0065 | 0.0066 | 0.0051 |
| zero_shot | 0.0095 | 0.0068 | 0.0162▲ | 0.0076 | 0.0098 | 0.0050 |

#### ROUGE-L

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.0970▲ | 0.0918 | 0.0943 | 0.0939 | 0.0896 | 0.0919 |
| few_shot (n=3) | 0.0898 | 0.1105★ | 0.1126★ | 0.1143★▲ | 0.1063★ | 0.0910 |
| one_shot | 0.1007★ | 0.1062 | 0.1046 | 0.1081 | 0.1015 | 0.1115★▲ |
| super_prompt | 0.0887▲ | 0.0807 | 0.0829 | 0.0851 | 0.0802 | 0.0763 |
| system_message | 0.0806 | 0.0950▲ | 0.0885 | 0.0836 | 0.0842 | 0.0888 |
| tam | 0.0912▲ | 0.0782 | 0.0821 | 0.0772 | 0.0842 | 0.0798 |
| zero_shot | 0.0850▲ | 0.0714 | 0.0838 | 0.0716 | 0.0837 | 0.0761 |

#### BERT-F1

| técnica | a | a_no_info | b | b_no_info | c | c_no_info |
| --- | --- | --- | --- | --- | --- | --- |
| care | 0.6870 | 0.6829 | 0.6980▲ | 0.6963 | 0.6835 | 0.6854 |
| few_shot (n=3) | 0.6896★ | 0.6968★ | 0.7061★ | 0.7099★▲ | 0.6915★ | 0.6920★ |
| one_shot | 0.6893 | 0.6919 | 0.7047 | 0.7069▲ | 0.6914 | 0.6887 |
| super_prompt | 0.6716 | 0.6771 | 0.6512 | 0.6868▲ | 0.6488 | 0.6647 |
| system_message | 0.6727 | 0.6752 | 0.6903▲ | 0.6845 | 0.6789 | 0.6820 |
| tam | 0.6792 | 0.6785 | 0.6900▲ | 0.6865 | 0.6767 | 0.6765 |
| zero_shot | 0.6791 | 0.6758 | 0.6953▲ | 0.6869 | 0.6759 | 0.6711 |

### 2.3 Mejor técnica por experimento

| Experimento | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| all | one_shot | one_shot | one_shot | few_shot (n=3) |
| collective | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| premises | one_shot | one_shot | one_shot | few_shot (n=3) |
| no-info | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| a | one_shot | care | one_shot | few_shot (n=3) |
| a_no_info | few_shot (n=3) | one_shot | few_shot (n=3) | few_shot (n=3) |
| b | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) | few_shot (n=3) |
| b_no_info | few_shot (n=3) | one_shot | few_shot (n=3) | few_shot (n=3) |
| c | one_shot | care | few_shot (n=3) | few_shot (n=3) |
| c_no_info | one_shot | one_shot | one_shot | few_shot (n=3) |

### 2.4 Mejor experimento por técnica — genéricas

| técnica | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| care | all (0.1675) | collective (0.0229) | all (0.1163) | no-info (0.6969) |
| few_shot (n=3) | all (0.1928) | collective (0.0340) | all (0.1356) | no-info (0.7175) |
| one_shot | all (0.1943) | collective (0.0306) | all (0.1356) | collective (0.7123) |
| super_prompt | no-info (0.1646) | all (0.0212) | premises (0.1062) | no-info (0.6908) |
| system_message | collective (0.1520) | collective (0.0185) | collective (0.1059) | all (0.6908) |
| tam | premises (0.1521) | collective (0.0230) | collective (0.1074) | premises (0.6935) |
| zero_shot | premises (0.1438) | collective (0.0209) | collective (0.0994) | premises (0.6901) |

### 2.5 Mejor global — genéricas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| ROUGE-1 | all / one_shot (0.1943) |
| ROUGE-2 | collective / few_shot (n=3) (0.0340) |
| ROUGE-L | all / one_shot (0.1356) |
| BERT-F1 | no-info / few_shot (n=3) (0.7175) |

### 2.6 Mejor experimento por técnica — tipeadas

| técnica | ROUGE-1 | ROUGE-2 | ROUGE-L | BERT-F1 |
| --- | --- | --- | --- | --- |
| care | c (0.1400) | b (0.0156) | a (0.0970) | b (0.6980) |
| few_shot (n=3) | b (0.1620) | b (0.0237) | b_no_info (0.1143) | b_no_info (0.7099) |
| one_shot | c_no_info (0.1580) | b_no_info (0.0174) | c_no_info (0.1115) | b_no_info (0.7069) |
| super_prompt | a (0.1260) | b_no_info (0.0150) | a (0.0887) | b_no_info (0.6868) |
| system_message | a_no_info (0.1258) | b (0.0133) | a_no_info (0.0950) | b (0.6903) |
| tam | a (0.1270) | a (0.0111) | a (0.0912) | b (0.6900) |
| zero_shot | c (0.1267) | b (0.0162) | a (0.0850) | b (0.6953) |

### 2.7 Mejor global — tipeadas

| Métrica | Mejor (experimento / técnica) |
| --- | --- |
| ROUGE-1 | b / few_shot (n=3) (0.1620) |
| ROUGE-2 | b / few_shot (n=3) (0.0237) |
| ROUGE-L | b_no_info / few_shot (n=3) (0.1143) |
| BERT-F1 | b_no_info / few_shot (n=3) (0.7099) |

### 2.8 Efecto de la información (pares con tweets compartidos)

#### ROUGE-1

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0090 | 16 | 11 | 0.4421 |
| a vs a_no_info | few_shot (n=3) | -0.0303 | 6 | 21 | 0.0059 |
| a vs a_no_info | one_shot | -0.0019 | 12 | 14 | 0.8450 |
| a vs a_no_info | super_prompt | +0.0086 | 16 | 11 | 0.4421 |
| a vs a_no_info | system_message | -0.0125 | 9 | 18 | 0.1221 |
| a vs a_no_info | tam | +0.0182 | 19 | 8 | 0.0522 |
| a vs a_no_info | zero_shot | +0.0139 | 19 | 8 | 0.0522 |
| b vs b_no_info | care | -0.0021 | 13 | 8 | 0.3833 |
| b vs b_no_info | few_shot (n=3) | +0.0019 | 11 | 10 | 1.0000 |
| b vs b_no_info | one_shot | -0.0045 | 8 | 13 | 0.3833 |
| b vs b_no_info | super_prompt | -0.0078 | 9 | 12 | 0.6636 |
| b vs b_no_info | system_message | +0.0060 | 12 | 9 | 0.6636 |
| b vs b_no_info | tam | +0.0011 | 8 | 13 | 0.3833 |
| b vs b_no_info | zero_shot | +0.0239 | 14 | 7 | 0.1892 |
| c vs c_no_info | care | +0.0129 | 12 | 11 | 1.0000 |
| c vs c_no_info | few_shot (n=3) | +0.0033 | 14 | 9 | 0.4049 |
| c vs c_no_info | one_shot | -0.0158 | 7 | 16 | 0.0931 |
| c vs c_no_info | super_prompt | +0.0061 | 15 | 8 | 0.2100 |
| c vs c_no_info | system_message | -0.0002 | 11 | 11 | 1.0000 |
| c vs c_no_info | tam | +0.0040 | 15 | 8 | 0.2100 |
| c vs c_no_info | zero_shot | +0.0241 | 17 | 6 | 0.0347 |

#### ROUGE-2

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0011 | 7 | 7 | 1.0000 |
| a vs a_no_info | few_shot (n=3) | -0.0015 | 6 | 7 | 1.0000 |
| a vs a_no_info | one_shot | -0.0039 | 5 | 8 | 0.5811 |
| a vs a_no_info | super_prompt | +0.0009 | 5 | 5 | 1.0000 |
| a vs a_no_info | system_message | -0.0003 | 5 | 6 | 1.0000 |
| a vs a_no_info | tam | +0.0069 | 8 | 3 | 0.2266 |
| a vs a_no_info | zero_shot | +0.0027 | 9 | 4 | 0.2668 |
| b vs b_no_info | care | +0.0071 | 11 | 4 | 0.1185 |
| b vs b_no_info | few_shot (n=3) | +0.0077 | 6 | 6 | 1.0000 |
| b vs b_no_info | one_shot | -0.0040 | 7 | 7 | 1.0000 |
| b vs b_no_info | super_prompt | -0.0018 | 7 | 10 | 0.6291 |
| b vs b_no_info | system_message | +0.0096 | 8 | 2 | 0.1094 |
| b vs b_no_info | tam | +0.0020 | 8 | 4 | 0.3877 |
| b vs b_no_info | zero_shot | +0.0086 | 8 | 6 | 0.7905 |
| c vs c_no_info | care | +0.0017 | 6 | 4 | 0.7539 |
| c vs c_no_info | few_shot (n=3) | -0.0030 | 3 | 4 | 1.0000 |
| c vs c_no_info | one_shot | -0.0081 | 3 | 9 | 0.1460 |
| c vs c_no_info | super_prompt | +0.0001 | 6 | 5 | 1.0000 |
| c vs c_no_info | system_message | -0.0059 | 2 | 7 | 0.1797 |
| c vs c_no_info | tam | +0.0015 | 5 | 3 | 0.7266 |
| c vs c_no_info | zero_shot | +0.0047 | 8 | 3 | 0.2266 |

#### ROUGE-L

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0051 | 15 | 12 | 0.7011 |
| a vs a_no_info | few_shot (n=3) | -0.0208 | 7 | 20 | 0.0192 |
| a vs a_no_info | one_shot | -0.0055 | 12 | 15 | 0.7011 |
| a vs a_no_info | super_prompt | +0.0080 | 13 | 14 | 1.0000 |
| a vs a_no_info | system_message | -0.0144 | 8 | 19 | 0.0522 |
| a vs a_no_info | tam | +0.0130 | 19 | 8 | 0.0522 |
| a vs a_no_info | zero_shot | +0.0136 | 22 | 5 | 0.0015 |
| b vs b_no_info | care | +0.0003 | 8 | 12 | 0.5034 |
| b vs b_no_info | few_shot (n=3) | -0.0017 | 11 | 10 | 1.0000 |
| b vs b_no_info | one_shot | -0.0035 | 9 | 12 | 0.6636 |
| b vs b_no_info | super_prompt | -0.0022 | 10 | 11 | 1.0000 |
| b vs b_no_info | system_message | +0.0049 | 12 | 9 | 0.6636 |
| b vs b_no_info | tam | +0.0049 | 11 | 10 | 1.0000 |
| b vs b_no_info | zero_shot | +0.0122 | 13 | 8 | 0.3833 |
| c vs c_no_info | care | -0.0022 | 8 | 15 | 0.2100 |
| c vs c_no_info | few_shot (n=3) | +0.0153 | 16 | 7 | 0.0931 |
| c vs c_no_info | one_shot | -0.0099 | 10 | 13 | 0.6776 |
| c vs c_no_info | super_prompt | +0.0038 | 15 | 8 | 0.2100 |
| c vs c_no_info | system_message | -0.0046 | 8 | 15 | 0.2100 |
| c vs c_no_info | tam | +0.0043 | 15 | 8 | 0.2100 |
| c vs c_no_info | zero_shot | +0.0077 | 15 | 8 | 0.2100 |

#### BERT-F1

| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |
| --- | --- | --- | --- | --- | --- |
| a vs a_no_info | care | +0.0041 | 17 | 10 | 0.2478 |
| a vs a_no_info | few_shot (n=3) | -0.0073 | 9 | 18 | 0.1221 |
| a vs a_no_info | one_shot | -0.0026 | 12 | 15 | 0.7011 |
| a vs a_no_info | super_prompt | -0.0055 | 16 | 11 | 0.4421 |
| a vs a_no_info | system_message | -0.0025 | 11 | 16 | 0.4421 |
| a vs a_no_info | tam | +0.0007 | 14 | 13 | 1.0000 |
| a vs a_no_info | zero_shot | +0.0033 | 15 | 12 | 0.7011 |
| b vs b_no_info | care | +0.0017 | 12 | 9 | 0.6636 |
| b vs b_no_info | few_shot (n=3) | -0.0038 | 8 | 13 | 0.3833 |
| b vs b_no_info | one_shot | -0.0022 | 13 | 8 | 0.3833 |
| b vs b_no_info | super_prompt | -0.0357 | 5 | 16 | 0.0266 |
| b vs b_no_info | system_message | +0.0058 | 13 | 8 | 0.3833 |
| b vs b_no_info | tam | +0.0035 | 12 | 9 | 0.6636 |
| b vs b_no_info | zero_shot | +0.0084 | 15 | 6 | 0.0784 |
| c vs c_no_info | care | -0.0019 | 11 | 12 | 1.0000 |
| c vs c_no_info | few_shot (n=3) | -0.0004 | 10 | 13 | 0.6776 |
| c vs c_no_info | one_shot | +0.0027 | 13 | 10 | 0.6776 |
| c vs c_no_info | super_prompt | -0.0159 | 11 | 12 | 1.0000 |
| c vs c_no_info | system_message | -0.0031 | 13 | 10 | 0.6776 |
| c vs c_no_info | tam | +0.0002 | 9 | 14 | 0.4049 |
| c vs c_no_info | zero_shot | +0.0047 | 13 | 10 | 0.6776 |
