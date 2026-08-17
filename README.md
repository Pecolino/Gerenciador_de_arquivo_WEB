# 📂 Gerenciador de Arquivos Web

Um mini servidor de arquivos para a rede local, feito em Python com Flask. Ele transforma uma pasta do seu computador em um diretório acessível por qualquer dispositivo na mesma rede (celular, tablet, outro PC) direto pelo navegador — sem precisar instalar nenhum programa ou app nos outros dispositivos.

## ✨ O que ele faz

- **Navegação por pastas**: percorre subpastas do diretório compartilhado como um explorador de arquivos comum.
- **Download**: qualquer arquivo pode ser baixado direto pelo navegador.
- **Upload**: envie arquivos de qualquer dispositivo para a pasta atual do computador host.
- **Zero instalação nos clientes**: basta abrir o link no navegador — funciona em celular, tablet ou outro computador.

## 🖥️ Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## 🚀 Como rodar

```bash
pip install -r requirements.txt
python app.py
```

Por padrão, o servidor sobe em `http://0.0.0.0:5000`. Para acessar de outro dispositivo na mesma rede Wi-Fi, use o IP local do computador que está rodando o servidor:

```
http://SEU-IP-LOCAL:5000
```

> Não sabe seu IP local? No Windows, rode `ipconfig` no terminal e procure por "Endereço IPv4".

## ⚙️ Configuração

O diretório compartilhado é definido na variável `RAIZ`, no início do `app.py`:

```python
RAIZ = Path("C:/FTP").resolve()
```

Troque esse caminho para a pasta que você quer expor na rede.

## 🔒 Segurança

Este projeto foi pensado para uso doméstico, dentro de uma rede local confiável (sua própria casa). Alguns pontos importantes:

- **Sem autenticação**: qualquer pessoa conectada à mesma rede Wi-Fi consegue acessar, baixar e enviar arquivos. Não exponha esse servidor diretamente para a internet sem adicionar login antes.
- **Proteção contra path traversal**: o servidor impede que alguém acesse pastas fora do diretório `RAIZ` (ex: tentando `../../` na URL).
- **Conexão não criptografada (HTTP)**: por padrão, os dados trafegam sem criptografia. Isso é aceitável numa rede doméstica confiável, mas os arquivos podem, em teoria, ser interceptados por outros dispositivos na mesma rede.

## 🗺️ Possíveis melhorias futuras

- [ ] Autenticação por senha
- [ ] HTTPS com certificado local
- [ ] Criação/exclusão de pastas pela interface
- [ ] Barra de progresso no upload de arquivos grandes

## 📁 Estrutura do projeto

```
.
├── app.py                 # servidor Flask
├── requirements.txt       # dependências
└── templates/
    └── browse.html         # interface de navegação/upload
```
