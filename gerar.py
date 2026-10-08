"""Gera index.html a partir de perguntas-v3.md. Uso: python gerar.py"""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))

FONTES = {
    "escala 6x1": [["Plano de Lula", "https://planodegoverno2026.com.br/candidatos/presidente/lula/"],
                   ["Plano de Flávio", "https://planodegoverno2026.com.br/candidatos/presidente/flavio-bolsonaro/"]],
    "estatais": [["Plano de Lula", "https://planodegoverno2026.com.br/candidatos/presidente/lula/"],
                 ["Plano de Flávio", "https://planodegoverno2026.com.br/candidatos/presidente/flavio-bolsonaro/"]],
    "contas do governo": [["Corte de gastos de Flávio (CNN, via ac24horas)", "https://ac24horas.com/2026/09/25/flavio-planeja-pec-da-transicao-com-corte-de-gastos-de-r-300-bilhoes/"],
                          ["Plano de Lula", "https://planodegoverno2026.com.br/candidatos/presidente/lula/"]],
    "licença": [["Vetos de Lula (Exame)", "https://exame.com/brasil/congresso-pode-derrubar-63-vetos-de-lula-a-lei-de-licenciamento-ambiental/"],
                ["Plano de Flávio", "https://planodegoverno2026.com.br/candidatos/presidente/flavio-bolsonaro/"]],
    "Aposentadoria": [["Lula x Flávio na aposentadoria (A Revista)", "https://arevista.com.br/economia/lula-x-flavio-o-que-pode-mudar-na-aposentadoria-no-bpc-e-no-salario-minimo-apos-a-eleicao/"]],
    "aborto": [["Lula sobre aborto (Bloomberg Línea)", "https://www.bloomberglinea.com/br-pt/apos-reacoes-lula-diz-que-e-contra-aborto-mas-que-tema-e-de-saude-publica/"],
               ["Flávio e o STF (Gazeta do Povo)", "https://www.gazetadopovo.com.br/eleicoes/2026/flavio-aposta-em-mudancas-no-stf-para-recuperar-credibilidade-da-corte/"]],
    "cotas": [["O que cada candidato diz (Terra)", "https://www.terra.com.br/nos/lei-de-cotas-raciais-o-que-cada-candidato-diz-sobre-o-tema,de203a6c85ba7a2a60d0c43bd9ca4239k2yea5g8.html"],
              ["Propostas comparadas (Gazeta de SP)", "https://www.gazetasp.com.br/politica/eleicoes-2026-compare-as-propostas-de-governo-de-flavio-bolsonaro-e-lula-para-os-proximos-quatro-anos/"]],
    "cívico-militares": [["Lula: \"não é obrigação do MEC\" (SBT News)", "https://sbtnews.sbt.com.br/noticia/governo/253096-nao-e-obrigacao-do-mec-cuidar-disso-diz-lula-sobre-escolas-civico-militares"],
                         ["Plano de Flávio", "https://planodegoverno2026.com.br/candidatos/presidente/flavio-bolsonaro/"]],
    "Redes sociais": [["Plano de Flávio (GNews USA)", "https://gnewsusa.com/2026/08/plano-de-governo-de-flavio-bolsonaro-propoe-mudancas-no-stf-fim-da-reeleicao-e-reducao-de-ministerios/"],
                      ["Governo Lula no STF (Jornal de Brasília)", "https://jornaldebrasilia.com.br/noticias/politica-e-poder/governo-altera-posicao-em-julgamento-no-stf-sobre-redes-e-defende-derrubada-de-regra-do-marco-civil/"],
                      ["A decisão do STF (Mattos Filho)", "https://www.mattosfilho.com.br/unico/responsabilizacao-provedores-internet/"]],
    "misoginia": [["Posições sobre o projeto (Jornal de Brasília)", "https://jornaldebrasilia.com.br/noticias/politica-e-poder/pl-da-misoginia-tem-aval-de-lula-ressalvas-de-flavio-oposicao-de-zema-e-silencio-de-caiado/"]],
    "menor de idade": [["Plano de Flávio (Gazeta do Povo)", "https://www.gazetadopovo.com.br/eleicoes/2026/propostas-flavio-bolsonaro-plano-de-governo-seguranca-publica/"],
                       ["Lula e a maioridade (CNN)", "https://www.cnnbrasil.com.br/blogs/gustavo-uribe/politica/lula-mede-impacto-sobre-reducao-da-maioridade-penal/"]],
    "facções": [["EUA e PCC/CV (Gazeta do Povo)", "https://www.gazetadopovo.com.br/economia/como-o-selo-de-terrorista-para-pcc-e-cv-afeta-bancos-e-empresas-no-brasil/"],
                ["Governo Lula sobre facções (InfoMoney)", "https://www.infomoney.com.br/?p=3082986"]],
    "armas": [["Decreto de armas de Lula (Congresso em Foco)", "https://www.congressoemfoco.com.br/noticia/9475/lula-assina-decreto-de-limitacao-no-porte-de-armas"],
              ["Projetos contra o decreto (Congresso em Foco)", "https://www.congressoemfoco.com.br/noticia/116574/comissao-de-seguranca-analisa-revogacao-de-decreto-que-restringiu-cacs"]],
    "8 de janeiro": [["Flávio e a anistia (InfoMoney)", "https://www.infomoney.com.br/politica/flavio-diz-que-buscara-anistia-para-bolsonaro-ainda-durante-governo-de-transicao/"]],
    "STF": [["Plano de Flávio para o STF (Gazeta do Povo)", "https://www.gazetadopovo.com.br/eleicoes/2026/flavio-propoe-limitar-decisoes-monocraticas-stf-mudanca-regras-indicacao-ministros/"],
            ["Governistas e a PEC do STF (CNN)", "https://www.cnnbrasil.com.br/politica/pec-que-limita-decisoes-monocraticas-no-stf-acende-sinal-de-alerta-entre-governistas-no-senado/"]],
}


def limpa(t):
    return re.sub(r"\*\*(.+?)\*\*", r"\1", t).strip()


def lado(quem):
    q = quem.lower()
    if "não está claro" in q: return "U"
    if q.startswith("lula"): return "L"
    if q.startswith("flávio"): return "F"
    if q.startswith("os dois"): return "B"
    return "N"


def ler():
    md = open(os.path.join(AQUI, "perguntas-v3.md"), encoding="utf-8").read()
    corpo = md[md.index("## Bloco 1"):md.index("## Fontes das posições")]
    perguntas, bloco = [], None
    for parte in re.split(r"(?m)^(?=## Bloco |### )", corpo):
        if parte.startswith("## Bloco"):
            bloco = re.sub(r"^## Bloco \d+: ", "", parte.split("\n")[0]).strip()
            continue
        if not parte.startswith("### "):
            continue
        linhas = parte.strip().split("\n")
        cab = linhas[0][4:]
        conta = "ⓘ" not in cab
        titulo = re.sub(r"^\d+( ⓘ)?\. ", "", cab).replace(" (fora da contagem)", "")
        hoje = next(l for l in linhas if l.startswith("**Como é hoje:**"))[len("**Como é hoje:**"):]
        perg = next(l for l in linhas if l.startswith("**Pergunta:**"))[len("**Pergunta:**"):]
        opcoes = []
        for l in linhas:
            if l.startswith("| A.") or l.startswith("| B."):
                c = [limpa(x) for x in l.strip().strip("|").split("|")]
                opcoes.append({"t": re.sub(r"^[AB]\. ", "", c[0]), "muda": c[1], "ganho": c[2],
                               "risco": c[3], "quem": c[4], "lado": lado(c[4])})
        src = next((v for k, v in FONTES.items() if k.lower() in titulo.lower()), [])
        perguntas.append({"bloco": bloco, "titulo": titulo, "hoje": (lambda h: h[:1].upper() + h[1:])(limpa(hoje)), "p": limpa(perg),
                          "conta": conta, "op": opcoes, "src": src})
    assert len(perguntas) == 15, len(perguntas)
    return perguntas


TEMPLATE = open(os.path.join(AQUI, "modelo.html"), encoding="utf-8").read()
dados = ler()
html = TEMPLATE.replace("/*DADOS*/[]", json.dumps(dados, ensure_ascii=False, indent=1))
destino = os.path.join(AQUI, "index.html")
open(destino + ".tmp", "w", encoding="utf-8").write(html)
os.replace(destino + ".tmp", destino)
print("ok:", len(dados), "perguntas,", sum(q["conta"] for q in dados), "contam")
