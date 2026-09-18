# Urbis CKAN (Portal de Dados Abertos)

![Capa Urbis](https://raw.githubusercontent.com/OpenUrbis/urbis/master/apps/docs/public/cover.png)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE.md)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![CKAN](https://img.shields.io/badge/CKAN-2.10-008080.svg?logo=ckan&logoColor=white)](https://ckan.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Stars](https://img.shields.io/github/stars/OpenUrbis/urbis-ckan?style=social)](https://github.com/OpenUrbis/urbis-ckan/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/OpenUrbis/urbis-ckan?style=social)](https://github.com/OpenUrbis/urbis-ckan/network/members)
[![Contribute](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **Instância customizada do CKAN para o portal de Dados Abertos e Catálogo de Metadados Territoriais do ecossistema Urbis (Prefeitura de São Paulo / OpenUrbis).**

---

## 🌐 Links & Recursos do Ecossistema Urbis

- 📊 **Portal de Dados Abertos (CKAN)**: [dadosabertos.urbis.prefeitura.sp.gov.br](https://dadosabertos.urbis.prefeitura.sp.gov.br/)
- 🌐 **Mosaico (Portal Integrado)**: [urbis.prefeitura.sp.gov.br](https://urbis.prefeitura.sp.gov.br/)
- 🗺️ **Mapa Urbis (Web GIS)**: [mapa.urbis.prefeitura.sp.gov.br](https://mapa.urbis.prefeitura.sp.gov.br/)
- 📖 **Documentação Técnica Oficial**: [docs.urbis.prefeitura.sp.gov.br](https://docs.urbis.prefeitura.sp.gov.br)
- ⚖️ **Legis (Legislação e Normas)**: [legis.urbis.prefeitura.sp.gov.br](https://legis.urbis.prefeitura.sp.gov.br)
- 📝 **Viabiliza (Workflows)**: [viabiliza.urbis.prefeitura.sp.gov.br](https://viabiliza.urbis.prefeitura.sp.gov.br)

---

## 🏛️ Visão Geral do Projeto

Este repositório contém o código-fonte e a configuração da instância customizada do **CKAN** para o ecossistema Urbis. O projeto utiliza uma extensão personalizada, a `ckanext-codata`, para adaptar as funcionalidades da plataforma, com foco principal na customização de metadados, na integração de estatísticas do portal e na pré-visualização de arquivos geoespaciais (GeoJSON/Shapefile).

---

## ⚙️ Principais Funcionalidades e Customizações

As customizações estão concentradas na extensão `ckanext-codata`, que implementa lógicas de backend através do `plugin.py` e personaliza a interface do usuário com templates e arquivos estáticos.

### Funcionalidades do Plugin (`plugin.py`)

O arquivo `plugin.py` é o núcleo da extensão e implementa diversas interfaces do CKAN:

*   **`IConfigurer`**: Registra os diretórios customizados da extensão (`templates/`, `public/`, `assets/`), permitindo que a extensão sobrescreva templates padrão e sirva arquivos estáticos próprios (CSS, imagens, etc.).
*   **`IPackageController`**: Modifica o processo de indexação de dados. Através do método `before_dataset_index`, ele extrai o metadado `spatial_granularity` de cada recurso e o "promove" ao nível do dataset. Isso torna o campo "Granularidade Espacial" uma faceta pesquisável.
*   **`IFacets`**: Substitui os nomes técnicos das facetas de busca por títulos mais amigáveis, como "Organizações" e "Granularidade Espacial", melhorando a experiência de busca.
*   **`ITemplateHelpers`**: Implementa funções Python que podem ser chamadas diretamente dos templates para exibir informações dinâmicas.

### Funções de Template (Helpers)

Estas funções são expostas para serem usadas nos templates (`.html`) para exibir estatísticas sobre o portal:

*   **`_get_total_resources()`**: Retorna a quantidade total de recursos públicos no portal.
*   **`_get_total_datasets()`**: Retorna a quantidade total de datasets públicos.
*   **`_get_total_storage_gb()`**: Retorna o total de armazenamento de todos os recursos em Gigabytes.
*   **`_get_weekly_updates()`**: Retorna a quantidade de recursos atualizados na última semana.

### Indexação de Metadados (`before_dataset_index`)

Esta função é a customização de backend mais importante para a busca. O CKAN, por padrão, não permite filtrar datasets por metadados que existem apenas no nível do *recurso*.

A função **`before_dataset_index`** resolve isso:
1.  **Inspeciona o Dataset**: Acessa cada um dos recursos dentro do dataset que será indexado.
2.  **Coleta os Valores**: Lê o valor do campo `spatial_granularity` de cada recurso.
3.  **Promove os Dados**: Agrupa os valores únicos encontrados e os adiciona a uma nova lista no nível do *dataset*.
4.  **Habilita a Faceta**: Ao "promover" essa informação, o campo `spatial_granularity` se torna visível para o motor de busca (Solr), que consegue então criar um filtro (faceta) a partir dele.

---

## 🧩 Extensões Adicionais

Além da `ckanext-codata`, esta instância do CKAN utiliza outras extensões importantes:

*   **`ckanext-scheming`**: Permite a criação de esquemas de metadados personalizados através de arquivos YAML. É usada para definir o campo `spatial_granularity` no formulário de recursos.
*   **`ckanext-envvars`**: Permite que a configuração do CKAN seja lida a partir de variáveis de ambiente, o que é essencial para ambientes containerizados.
*   **`ckanext-pdf_view`**: Integra um visualizador de PDFs diretamente na página do recurso.
*   **`ckanext-geoview`**: Adiciona a capacidade de visualizar dados geoespaciais (como GeoJSON) em mapas interativos.

---

## 🚀 Deploy e CI/CD

O processo de deploy da aplicação é automatizado com GitHub Actions, definido no arquivo `.github/workflows/deploy_ckan.yml`.

### Processo de Build e Deploy
1.  **Build e Push das Imagens:** O workflow constrói as imagens Docker para `nginx`, `postgresql` e `ckan` e as envia para o Azure Container Registry (ACR) com a tag `latest`.
2.  **Deploy na VM:** Conecta-se via SSH na máquina virtual de produção no Azure, atualiza o repositório com `git pull` e reinicia os contêineres via `docker compose -f docker-compose.prod.yml up -d`.

---

## 🌐 Ecossistema de Repositórios (OpenUrbis no GitHub)

| Repositório | Stack / Tecnologias | Descrição & Finalidade |
| :--- | :--- | :--- |
| [**`OpenUrbis/urbis-agent`**](https://github.com/OpenUrbis/urbis-agent) | Markdown, Bash, Python, MCPs | Central de inteligência, guia mestre de arquitetura, mapeamento de clusters Azure AKS e orquestração de submódulos. |
| [**`OpenUrbis/urbis`**](https://github.com/OpenUrbis/urbis) | Next.js, React 18, Angular, NestJS, Deck.gl, Tailwind | Monorepo Turborepo com o portal Mosaico, Web GIS (Mapa Urbis), Legis, Contas, Docs e API Gateway. |
| [**`OpenUrbis/urbis-datalake`**](https://github.com/OpenUrbis/urbis-datalake) | Python 3.11+, Dagster, PostGIS, GeoPandas, GeoServer | Datalake geoespacial com pipelines de ingestão, higienização e catálogo de dados em arquitetura medalhão. |
| [**`OpenUrbis/urbis-ckan`**](https://github.com/OpenUrbis/urbis-ckan) *(este repositório)* | Python, CKAN 2.10, PostgreSQL, Solr, Docker | Portal de Dados Abertos e catálogo de metadados territoriais do Município de São Paulo. |
| [**`OpenUrbis/urbis-workflows`**](https://github.com/OpenUrbis/urbis-workflows) | React, Next.js, Radix UI, Tailwind | Frontend do **Viabiliza**: formulários inteligentes, caixas de entrada de processos e interface administrativa. |
| [**`OpenUrbis/urbis-workflows-api`**](https://github.com/OpenUrbis/urbis-workflows-api) | NestJS, TypeScript, PostgreSQL, TypeORM | Backend e API Gateway do **Viabiliza**: validações de regras urbanísticas, integração com o SEI e motor de processos. |
| [**`OpenUrbis/urbis-projeto-inteligente`**](https://github.com/OpenUrbis/urbis-projeto-inteligente) | .NET 8, C#, AutoCAD ObjectARX, accoreconsole, GeoJSON | Motor para extração geométrica, validação topológica, conversão CAD (DWG/DXF) e aplicação de chancela digital. |

---

## ⭐ Histórico de Estrelas (Star History)

[![Star History Chart](https://api.star-history.com/svg?repos=OpenUrbis/urbis-agent,OpenUrbis/urbis,OpenUrbis/urbis-datalake,OpenUrbis/urbis-ckan,OpenUrbis/urbis-workflows,OpenUrbis/urbis-workflows-api,OpenUrbis/urbis-projeto-inteligente&type=Date)](https://star-history.com/#OpenUrbis/urbis-agent&OpenUrbis/urbis&OpenUrbis/urbis-datalake&OpenUrbis/urbis-ckan&OpenUrbis/urbis-workflows&OpenUrbis/urbis-workflows-api&OpenUrbis/urbis-projeto-inteligente&Date)

---

## 📄 Licença

Este projeto é software livre e está licenciado sob a **GNU Affero General Public License v3.0 (AGPL v3)**. Consulte o arquivo [LICENSE.md](LICENSE.md) para obter o texto integral.

Documentações e conteúdos são licenciados sob **CC BY-SA 4.0**.

---

## 📬 Contato e Sugestões

Dúvidas, sugestões ou solicitações sobre o portal de dados abertos? Entre em contato pelo e-mail [codataurbis@prefeitura.sp.gov.br](mailto:codataurbis@prefeitura.sp.gov.br).
