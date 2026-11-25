# E Se Factory

**Plataforma de automação de produção de vídeos utilizando Python, inteligência artificial e integração com APIs.**

O E Se Factory é um projeto desenvolvido para automatizar etapas da criação de vídeos curtos, desde a geração de ideias e roteiros até a produção de narrações, imagens, edição e publicação.

## Funcionalidades

- Geração automatizada de ideias.
- Criação de roteiros.
- Geração de imagens.
- Conversão de texto em narração.
- Edição e montagem de vídeos.
- Integração com serviços externos.
- Automação do processo de publicação.

*O status de cada funcionalidade depende da implementação atual do projeto.*

## Tecnologias utilizadas

- Python
- APIs REST
- FFmpeg
- Edge TTS
- Google OAuth 2.0
- Git e GitHub

## Estrutura do projeto

```text
E-Se-Factory/
│
├── src/
│   ├── editor.py
│   ├── gerador_ideias.py
│   ├── gerador_imagens.py
│   ├── gerador_roteiros.py
│   ├── main.py
│   ├── narracao.py
│   └── publicacao.py
│
├── roteiros/
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SergioAntoniodev/E-Se-Factory.git
```

Entre na pasta:

```bash
cd E-Se-Factory
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Configure suas credenciais e variáveis de ambiente localmente.

**Nunca publique tokens, senhas, chaves de API ou arquivos `.env`.**

## Objetivo

Desenvolver uma plataforma modular de automação de conteúdo audiovisual, aplicando conceitos de desenvolvimento backend, integração de APIs, processamento de mídia e automação com Python.

## Desenvolvedor

**Sérgio Antônio**

GitHub: [@SergioAntoniodev](https://github.com/SergioAntoniodev)
