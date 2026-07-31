# Dicionário de Dados — Projeto 2 (SeedGraph)

Descreve todos os arquivos de `base_de_dados/`. As bases brutas alimentam o
**grafo de conhecimento** montado por `scripts/build_graph.py` (saídas em `grafo/`).
Datas de acesso: **julho/2026**.

---

## A. AGROVOC — taxonomia de hortaliças (FAO, RDF/SKOS via SPARQL)

Extraído do endpoint SPARQL `https://agrovoc.fao.org/sparql` (subgrafo de "vegetables").
Licença **CC-BY**.

### `agrovoc_hortalicas_nos.csv` (nós/conceitos)
| Coluna | Tipo | Descrição |
|---|---|---|
| `uri` | str | URI do conceito (ex.: `http://aims.fao.org/aos/agrovoc/c_12151`). Chave. |
| `agrovoc_id` | str | Id curto do conceito (ex.: `c_12151`). |
| `label_en` | str | Rótulo preferencial em inglês (ex.: "lettuces"). |
| `label_pt` | str | Rótulo preferencial em português (ex.: "alface"). |
| `label_es` | str | Rótulo preferencial em espanhol. |

### `agrovoc_hortalicas_arestas.csv` (relações hierárquicas)
| Coluna | Tipo | Descrição |
|---|---|---|
| `child_uri` / `child_id` | str | Conceito filho (mais específico). |
| `parent_uri` / `parent_id` | str | Conceito pai (mais genérico). |
| `rel` | str | Tipo de relação: `skos:broader`. |

### `agrovoc_hortalicas_raw.json`
Dump combinado `{nodes, edges}` para carga direta em grafo/RDF.

---

## B. Crop Ontology — traits padronizados por cultura (CGIAR, BrAPI v1)

De `https://cropontology.org/brapi/v1/traits/{ontology}`. Licença **CC-BY 4.0**.
Ontologias baixadas: Brassica (CO_348), Common Bean (CO_335), Potato (CO_330), Sweet Potato (CO_331).

### `cropontology_traits.csv`
| Coluna | Tipo | Descrição |
|---|---|---|
| `cultura` | str | Cultura (Brassica, Common Bean, Potato, Sweet Potato). |
| `ontology` | str | Código da ontologia (ex.: CO_348). |
| `traitDbId` / `traitId` | str | Id do trait (ex.: `CO_348:2000001`). Chave. |
| `traitName` | str | Nome do trait (ex.: "Plant stand", "Days to flowering"). |
| `defaultValue` | str | Valor padrão (quando houver). |
| `n_observation_variables` | int | Nº de variáveis de observação ligadas. |
| `observation_variables` | str | Ids das variáveis (separados por `; `). |

`cropontology_traits.json` — payload BrAPI bruto (com todos os campos).

---

## C. SIGEF — produção de sementes no Brasil (MAPA, CSV aberto, CC-BY)

De `dados.agricultura.gov.br` (CKAN). **Encoding Latin-1, separador `;`, decimal vírgula.**
Ver também `sigef_dicionario_oficial.pdf` (dicionário oficial do MAPA, v2.1).

### `sigef_campos_producao_sementes.csv` — **606.809 linhas** (36.324 de hortaliça)
1 linha = campo de produção de semente registrado.
| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `Safra` | str | — | Safra/ano-agrícola (ex.: `2013/2013`). |
| `Especie` | str | — | Nome científico da espécie (ex.: `Solanum lycopersicum L. = ...`). **Chave de cultura.** |
| `Categoria` | str | — | Categoria da semente (S1, S2, C1, C2, básica, etc.). |
| `Cultivar` | str | — | Nome do cultivar (ex.: `Rio Grande`). **Chave de cultivar.** |
| `Municipio` | str | — | Município do campo. |
| `UF` | str | — | Unidade da Federação. **Chave regional.** |
| `Status` | str | — | Situação (ex.: `Homologado`). |
| `Data do Plantio` | date | dd/mm/aaaa | Data de plantio. |
| `Data de Colheita` | date | dd/mm/aaaa | Data de colheita (pode faltar). |
| `Area` | float | ha | Área do campo de produção. |
| `Producao bruta` | float | t | Produção bruta colhida (pode faltar). |
| `Producao estimada` | float | t | Produção estimada. **Proxy de volume de lote.** |

### `sigef_declaracao_area_uso_proprio.csv`
Declarações de reserva de semente para uso próprio.
| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `TIPOPERIODO` / `PERIODO` | str | — | Tipo/valor do período declarado. |
| `AREATOTAL` | float | ha | Área total declarada. |
| `MUNICIPIO` / `UF` | str | — | Localização. |
| `ESPECIE` / `CULTIVAR` | str | — | Espécie e cultivar. |
| `AREAPLANTADA` / `AREAESTIMADA` | float | ha | Área plantada / estimada. |
| `QUANTRESERVADA` | float | kg | Quantidade de semente reservada. |
| `DATAPLANTIO` | date | — | Data de plantio. |

> ⚠️ **SIGEF não contém a empresa/mantenedor.** Essa dimensão vem do RNC/CultivarWeb
> (ver `scripts/cultivarweb_download.py` — requer sessão interativa/captcha; documentado
> como enriquecimento). O grafo funciona sem ela; a empresa entraria como nó `Company`
> ligado a `Cultivar` via `MAINTAINED_BY`.

---

## D. `grafo/` — o grafo de conhecimento montado (`build_graph.py`)

Property graph com **3.150 nós e 7.095 arestas**. Carregável em Neo4j, NetworkX, Gephi, yEd.

### `graph_nodes.csv`
| Coluna | Descrição |
|---|---|
| `id` | Id único (ex.: `crop:c_12151`, `species:solanum_lycopersicum`, `cultivar:rio_grande|...`). |
| `label` | Tipo do nó: **Crop** (120), **Cultivar** (2.389), **Trait** (600), **Region** (19), **Species** (17), **CropFamily** (4). |
| `name*` | Propriedades de nome (name, name_pt, name_en, name_sci, uf, ...). |

### `graph_edges.csv`
| Coluna | Descrição |
|---|---|
| `src` → `dst` | Nó origem → destino. |
| `rel` | Relação: **PRODUCED_IN** (3.998, com `area_ha`/`producao_t`/`n_campos`), **OF_SPECIES** (2.389), **HAS_TRAIT** (1.000), **BROADER** (120, taxonomia AGROVOC), **IS_A** (10, Species→Crop AGROVOC). |
| `area_ha` / `producao_t` / `n_campos` | Propriedades de aresta PRODUCED_IN (proxy de lote). |

### Outros
- `grafo_seedgraph.graphml` — grafo completo (NetworkX/Gephi).
- `neo4j_import.cypher` — script de carga via `LOAD CSV` no Neo4j.

### Modelo do grafo (esquema)
```
(Crop)-[:BROADER]->(Crop)              # taxonomia AGROVOC de hortaliças
(Species)-[:IS_A]->(Crop)              # espécie SIGEF ligada ao conceito AGROVOC
(Cultivar)-[:OF_SPECIES]->(Species)
(Cultivar)-[:PRODUCED_IN {area_ha, producao_t, n_campos}]->(Region)
(CropFamily)-[:HAS_TRAIT]->(Trait)     # Crop Ontology
(Species)-[:HOST_OF]->(Pest)           # EPPO (opcional, requer token)
```

---

## E. EPPO (opcional — requer token gratuito)

Gerados por `scripts/eppo_client.py` após registro em `data.eppo.int`:
- `eppo_pragas_por_cultura.csv` — vínculos cultura↔praga (`praga_eppo`, `praga_nome`, `labelclass`).
- `eppo_status_regulatorio.csv` — status regulatório/quarentenário por organização/país.

Licença **EPPO Open Data**.
