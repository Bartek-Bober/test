import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from openrouter import chat_with_history

DB_URL = "sqlite:///./app.db" 

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

# =========================================================
# TA LINIJKA JEST KLUCZOWA - TWORZY TABELE W BAZIE DANYCH
# =========================================================
Base.metadata.create_all(bind=engine)


def run_chat(session_id="moja_sesja"):
    db = SessionLocal()
    
    db_conversations = db.query(Conversation).filter(Conversation.session_id == session_id).order_by(Conversation.id).all()
    
    history = [{"role": "system", "content": "Jesteś pomocnym asystentem."}]
    
    print("\n--- HISTORIA CZATU ---")
    for conv in db_conversations:
        history.append({"role": conv.role, "content": conv.content})
        prefix = "Ty" if conv.role == "user" else "AI"
        print(f"{prefix}: {conv.content}")
        
    print("--- ROZPOCZĘTO CZAT (wpisz 'wyjdz' aby skończyć) ---")
    
    while True:
        user_text = input("Ty: ")
        if user_text.lower() == "wyjdz":
            break
            
        db.add(Conversation(session_id=session_id, role="user", content=user_text))
        db.commit()
        
        # Dodaj do historii i zapytaj AI
        history.append({"role": "user", "content": user_text})
        print("AI pisze...")
        ai_response = chat_with_history(history)
        
        print(f"AI: {ai_response}")
        
        db.add(Conversation(session_id=session_id, role="assistant", content=ai_response))
        db.commit()
        
        history.append({"role": "assistant", "content": ai_response})

    db.close()


def summarize_messages():
    db = SessionLocal()
    
    messages = db.query(Message).all()
    
    if not messages:
        print("Brak wiadomości do podsumowania w tabeli 'messages'.")
        db.close()
        return
        
    wszystkie_teksty = "\n".join([f"- {m.content}" for m in messages])
    
    prompt = f"Podsumuj krótko poniższe wiadomości:\n{wszystkie_teksty}"
    
    history = [
        {"role": "system", "content": "Jesteś ekspertem od streszczeń."},
        {"role": "user", "content": prompt}
    ]
    
    print("\nGenerowanie podsumowania...")
    podsumowanie = chat_with_history(history)
    print(f"\n--- WYNIK PODSUMOWANIA ---\n{podsumowanie}\n")
    
    nowa_wiadomosc = Message(content=f"PODSUMOWANIE AI: {podsumowanie}")
    db.add(nowa_wiadomosc)
    db.commit()
    print("✅ Zapisano podsumowanie jako nową wiadomość w bazie danych.")
    
    db.close()


if __name__ == "__main__":
    while True:
        print("\nWYBIERZ AKCJĘ:")
        print("1. Uruchom Chatbota z pamięcią")
        print("2. Podsumuj wiadomości z bazy")
        print("3. Zakończ program")
        
        wybor = input("Twój wybór: ")
        
        if wybor == "1":
            run_chat()
        elif wybor == "2":
            summarize_messages()
        elif wybor == "3":
            print("Koniec pracy programu.")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")