from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import Base, SessionLocal, engine
from models import Book, User

app = Flask(__name__)
Base.metadata.create_all(bind=engine)


@app.route('/')
def index():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User).order_by(User.nome)).all()
        livros = session.scalars(
            select(Book).options(selectinload(Book.user)).order_by(Book.titulo)
        ).all()
    return render_template('index.html', usuarios=usuarios, livros=livros)


@app.get('/usuarios/novo')
def novo_usuario_form():
    return render_template('user_form.html')


@app.post('/usuarios/novo')
def novo_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')

    if not nome or not email:
        return 'Dados inválidos', 400

    with SessionLocal() as session:
        usuario = User(nome=nome, email=email)
        session.add(usuario)
        session.commit()

    return redirect(url_for('index'))


@app.get('/livros/novo')
def novo_livro_form():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User).order_by(User.nome)).all()
    return render_template('book_form.html', usuarios=usuarios)


@app.post('/livros/novo')
def novo_livro():
    titulo = request.form.get('titulo')
    user_id = request.form.get('user_id')

    if not titulo or not user_id:
        return 'Dados inválidos', 400

    try:
        user_id = int(user_id)
    except ValueError:
        return 'Usuário inválido', 400

    with SessionLocal() as session:
        livro = Book(titulo=titulo, user_id=user_id)
        session.add(livro)
        session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)