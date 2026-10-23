# PoC: Detecção de vulnerabilidades em código-fonte com Semgrep (SAST)

   ![Semgrep](https://github.com/pauloosmt/poc-semgrep-sast/actions/workflows/semgrep.yml/badge.svg)

Prova de conceito do trabalho de **Prospecção Tecnológica (2026-2)**.
Autor: Paulo Sergio Mendes Taciano

## Objetivo
Mostrar como uma ferramenta de **análise estática de segurança (SAST)**, o Semgrep, detecta vulnerabilidades comuns em código-fonte, e demonstrar duas capacidades que vão além de rodar regras prontas:

1. **Criar e ajustar regras próprias**, cobrindo uma falha que a ferramenta deixou passar e reduzindo um falso positivo.
2. **Integrar a análise a um pipeline automatizado (CI)**, que reprova código vulnerável e aprova o corrigido.

## Estrutura do repositório
| Pasta | Conteúdo |
|---|---|
| `app/` | Aplicação Flask **propositalmente vulnerável** (SQL Injection, XSS, segredo hardcoded) e um arquivo de configuração inofensivo usado para testar falso positivo |
| `fixed/` | Versão corrigida da aplicação |
| `rules/` | Regra customizada do Semgrep (`hardcoded-key.yml`) |
| `src/` | Código analisado pelo pipeline de CI |
| `evidencias/` | Prints e saídas de cada etapa da PoC |
| `.github/workflows/` | Workflow do GitHub Actions que roda o Semgrep |

> **Atenção:** o código em `app/` é vulnerável de propósito. Ele serve apenas para ser escaneado e **não deve ser executado ou publicado como aplicação**. O segredo que aparece nele é **falso**.

## Como reproduzir

Pré-requisitos: Python 3 e `pip`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install semgrep
```

**1. Scan base com regras prontas do registro**
```bash
semgrep --config p/owasp-top-ten app/
```

**2. Regra customizada**
```bash
semgrep --config rules/ app/
```

**3. Código corrigido**
```bash
semgrep --config p/owasp-top-ten --config rules/ fixed/
```

**4. Comportamento do CI (sai com código 1 se houver achados)**
```bash
semgrep scan --config rules/ --error app/    # saída: 1
semgrep scan --config rules/ --error fixed/  # saída: 0
```

Obs.: dentro de um repositório Git, o Semgrep escaneia apenas arquivos rastreados pelo Git (`git add` antes de rodar em arquivos novos). Foi usada a versão gratuita (Community Edition), sem login.

## Resultados

| Etapa | Resultado |
|---|---|
| Scan base (`p/owasp-top-ten`) em `app/` | 5 alertas para 2 falhas reais: SQL Injection (2 alertas) e XSS (3 alertas). Parte das regras é de Django, e a aplicação usa Flask |
| Segredo hardcoded | **Falso negativo:** nenhuma regra do registro detectou o `API_KEY` |
| Regra customizada | Detecta o segredo hardcoded (CWE-798) |
| Falso positivo | A primeira versão da regra marcou `PASSWORD_FIELD = "password"` |
| Regra ajustada | Passou a considerar também o valor (8+ caracteres e ao menos um número), eliminando o falso positivo |
| Código corrigido (`fixed/`) | 0 achados |
| CI com código vulnerável | Build reprovado (6 achados: 5 do registro e 1 da regra customizada) |
| CI com código corrigido | Build aprovado (0 achados) |

## Correções aplicadas
- **SQL Injection:** consulta parametrizada (`cur.execute("... WHERE name = ?", (nome,))`).
- **XSS:** renderização com template e escape automático (`render_template_string` com variável).
- **Segredo hardcoded:** valor lido de variável de ambiente (`os.environ`).

## Limitações
- A versão gratuita analisa **um arquivo por vez**, sem fluxo de dados entre arquivos, o que pode gerar falsos negativos.
- A regra ajustada é uma heurística: reduzir falsos positivos pode criar novos falsos negativos (por exemplo, uma senha real sem nenhum número).
- Poucas vulnerabilidades, uma linguagem e um único ambiente foram testados.
- Zero achados **não significa** código seguro. SAST deve ser combinado com DAST e SCA e com revisão humana.

## Referências
- [Documentação do Semgrep](https://semgrep.dev/docs/)
- [OWASP Top 10:2025](https://top10.owasp.org/2025/)
- [Documentação do CodeQL](https://codeql.github.com/docs/)
