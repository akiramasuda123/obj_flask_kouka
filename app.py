from flask import Flask, redirect, url_for
from extensions import db, mail
from views.reservation import reservation_bp
from views.loan import loan_bp
from views.return_book import return_bp

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # メール設定
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your-app-password'

    # 拡張機能の初期化
    db.init_app(app)
    mail.init_app(app)

    # Blueprintの登録
    app.register_blueprint(reservation_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(return_bp)

    # トップページ（例: 予約検索へリダイレクト）
    @app.route('/')
    def index():
        return redirect(url_for('reservation.ky01'))

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)