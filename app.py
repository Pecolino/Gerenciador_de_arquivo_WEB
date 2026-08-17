from pathlib import Path
from flask import (
    Flask, render_template, send_from_directory, abort,
    redirect, url_for, request, flash,
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "troque-essa-chave-por-qualquer-coisa-secreta"  # necessário para flash()

# Pasta que o site vai expor. Troque para o caminho que quiser compartilhar.
RAIZ = Path("C:/FTP").resolve()


def caminho_seguro(subcaminho: str) -> Path:
    """Resolve o caminho pedido e garante que ele continua DENTRO da RAIZ."""
    alvo = (RAIZ / subcaminho).resolve()
    if RAIZ not in alvo.parents and alvo != RAIZ:
        abort(403)  # tentativa de sair da pasta permitida
    if not alvo.exists():
        abort(404)
    return alvo


@app.route("/")
def index():
    return redirect(url_for("navegar", subcaminho=""))


@app.route("/browse/", defaults={"subcaminho": ""}, methods=["GET", "POST"])
@app.route("/browse/<path:subcaminho>", methods=["GET", "POST"])
def navegar(subcaminho):
    atual = caminho_seguro(subcaminho)

    if atual.is_file():
        abort(404)  # arquivos não têm mais página própria, só download direto

    if request.method == "POST":
        arquivo = request.files.get("arquivo")
        if arquivo and arquivo.filename:
            nome_seguro = secure_filename(arquivo.filename)
            if nome_seguro:
                arquivo.save(atual / nome_seguro)
                flash(f"Arquivo '{nome_seguro}' enviado com sucesso!")
            else:
                flash("Nome de arquivo inválido.")
        else:
            flash("Nenhum arquivo selecionado.")
        return redirect(url_for("navegar", subcaminho=subcaminho))

    itens = []
    for item in sorted(atual.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        itens.append({
            "nome": item.name,
            "tipo": "📁" if item.is_dir() else "📄",
            "caminho": str(item.relative_to(RAIZ)).replace("\\", "/"),
        })

    caminho_pai = None
    if atual != RAIZ:
        caminho_pai = str(atual.parent.relative_to(RAIZ)).replace("\\", "/")

    return render_template(
        "browse.html",
        itens=itens,
        caminho_atual=str(atual.relative_to(RAIZ)).replace("\\", "/") or ".",
        caminho_pai=caminho_pai,
        subcaminho_atual=subcaminho,
    )


@app.route("/download/<path:subcaminho>")
def baixar(subcaminho):
    atual = caminho_seguro(subcaminho)
    if not atual.is_file():
        abort(404)
    return send_from_directory(atual.parent, atual.name, as_attachment=True)


if __name__ == "__main__":
    # debug=True só em desenvolvimento; tire em produção
    app.run(debug=True, host="0.0.0.0", port=5000)
