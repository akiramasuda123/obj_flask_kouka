# seed.py
from app import create_app
from extensions import db
from models import Member, Book, Item, Reservation, Loan
from datetime import date, timedelta

app = create_app()

def seed_data():
    with app.app_context():
        # 既存データをクリアしてリセットしたい場合は以下を有効化
        db.drop_all()
        db.create_all()

        print("データの登録を開始します...")

        # ------------------------------------
        # 1. 会員データ (Member)
        # ------------------------------------
        member_student = Member(
            member_number="0000000",
            name="大原 太郎",
            email="xxx@example.com",
            member_type="student"  # 学生（上限6冊・雑誌貸出不可）
        )
        member_staff = Member(
            member_number="1111111",
            name="大原 花子",
            email="staff@example.com",
            member_type="staff"    # 教職員（上限12冊・雑誌貸出可）
        )
        db.session.add_all([member_student, member_staff])
        db.session.commit()

        # ------------------------------------
        # 2. 書籍・雑誌データ (Book)
        # ------------------------------------
        book1 = Book(
            isbn="1234567890123",
            title="簡単Javascript",
            book_type="book"       # 書籍
        )
        book2 = Book(
            isbn="1234567890124",
            title="Javascript入門 初めてのJavascript-第2版",
            book_type="book"       # 書籍
        )
        book3 = Book(
            isbn="1234567890125",
            title="週間Javascriptマガジン",
            book_type="magazine"   # 雑誌（1冊のみ）
        )
        book4 = Book(
            isbn="1234567890126",
            title="週刊少年マガヅン",
            book_type="magazine"   # 雑誌（1冊のみ）
        )
        db.session.add_all([book1, book2, book3, book4])
        db.session.commit()

        # ------------------------------------
        # 3. 図書所蔵データ (Item)
        # ------------------------------------
        # 「簡単Javascript」は書籍のため複数冊（2冊）作成
        item1_1 = Item(management_number="0123456789012", book_id=book1.id, is_borrowed=False)
        item1_2 = Item(management_number="0123456789013", book_id=book1.id, is_borrowed=False)
        
        # 「Javascript入門」
        item2_1 = Item(management_number="0123456789014", book_id=book2.id, is_borrowed=False)
        
        # 雑誌は各1冊のみ
        item3_1 = Item(management_number="0123456789015", book_id=book3.id, is_borrowed=False)
        item4_1 = Item(management_number="0123456789016", book_id=book4.id, is_borrowed=False)

        db.session.add_all([item1_1, item1_2, item2_1, item3_1, item4_1])
        db.session.commit()

        # ------------------------------------
        # 4. 事前予約データ (Reservation) - テスト用
        # ------------------------------------
        # 返却時に取り置きメール通知ダイアログ（HK03）を確認するためのサンプル予約データ
        reservation1 = Reservation(
            member_id=member_student.id,
            book_id=book3.id, # 週間Javascriptマガジン
            status="reserved"
        )
        reservation2 = Reservation(
            member_id=member_staff.id,
            book_id=book1.id, # 簡単Javascript
            status="reserved"
        )
        db.session.add_all([reservation1, reservation2])
        db.session.commit()

        print("仮データの登録が完了しました！")

if __name__ == '__main__':
    seed_data()