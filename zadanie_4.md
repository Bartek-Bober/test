# 1.

## 1.1
### prompt:
Zaprojektuj schemat bazy danych dla komunikatora internetowego. Zwróć odpowiedź wyłącznie w formacie JSON, uwzględniając tabele users, chats i messages wraz z typami pól
### odpowiedź:
``json
{
  "tables": [
    {
      "name": "users",
      "fields": [
        {
          "name": "user_id",
          "type": "BIGINT",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "username",
          "type": "VARCHAR(50)",
          "unique": true,
          "not_null": true
        },
        {
          "name": "email",
          "type": "VARCHAR(255)",
          "unique": true,
          "not_null": true
        },
        {
          "name": "password_hash",
          "type": "VARCHAR(255)",
          "not_null": true
        },
        {
          "name": "created_at",
          "type": "TIMESTAMP",
          "default": "CURRENT_TIMESTAMP"
        },
        {
          "name": "status",
          "type": "ENUM('active', 'inactive', 'banned')",
          "default": "'active'"
        },
        {
          "name": "avatar_url",
          "type": "VARCHAR(255)",
          "nullable": true
        }
      ]
    },
    {
      "name": "chats",
      "fields": [
        {
          "name": "chat_id",
          "type": "BIGINT",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "chat_name",
          "type": "VARCHAR(100)",
          "nullable": true
        },
        {
          "name": "chat_type",
          "type": "ENUM('direct', 'group', 'channel')",
          "default": "'direct'"
        },
        {
          "name": "created_at",
          "type": "TIMESTAMP",
          "default": "CURRENT_TIMESTAMP"
        },
        {
          "name": "admin_user_id",
          "type": "BIGINT",
          "references": "users(user_id)",
          "nullable": true
        },
        {
          "name": "last_message_id",
          "type": "BIGINT",
          "references": "messages(message_id)",
          "nullable": true
        },
        {
          "name": "is_active",
          "type": "BOOLEAN",
          "default": true
        }
      ]
    },
    {
      "name": "messages",
      "fields": [
        {
          "name": "message_id",
          "type": "BIGINT",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "chat_id",
          "type": "BIGINT",
          "not_null": true,
          "references": "chats(chat_id)"
        },
        {
          "name": "sender_id",
          "type": "BIGINT",
          "not_null": true,
          "references": "users(user_id)"
        },
        {
          "name": "content",
          "type": "TEXT",
          "not_null": true
        },
        {
          "name": "created_at",
          "type": "TIMESTAMP",
          "default": "CURRENT_TIMESTAMP"
        },
        {
          "name": "is_edited",
          "type": "BOOLEAN",
          "default": false
        },
        {
          "name": "edited_at",
          "type": "TIMESTAMP",
          "nullable": true
        },
        {
          "name": "is_deleted",
          "type": "BOOLEAN",
          "default": false
        }
      ]
    },
    {
      "name": "chat_participants",
      "fields": [
        {
          "name": "user_id",
          "type": "BIGINT",
          "not_null": true,
          "references": "users(user_id)"
        },
        {
          "name": "chat_id",
          "type": "BIGINT",
          "not_null": true,
          "references": "chats(chat_id)"
        },
        {
          "name": "joined_at",
          "type": "TIMESTAMP",
          "default": "CURRENT_TIMESTAMP"
        },
        {
          "name": "role",
          "type": "ENUM('admin', 'moderator', 'member')",
          "default": "'member'"
        },
        {
          "name": "is_muted",
          "type": "BOOLEAN",
          "default": false
        }
      ],
      "primary_key": ["user_id", "chat_id"]
    }
  ],
  "indexes": [
    {
      "table": "users",
      "name": "idx_users_username",
      "fields": ["username"]
    },
    {
      "table": "users",
      "name": "idx_users_email",
      "fields": ["email"]
    },
    {
      "table": "messages",
      "name": "idx_messages_chat_id",
      "fields": ["chat_id"]
    },
    {
      "table": "messages",
      "name": "idx_messages_sender_id",
      "fields": ["sender_id"]
    },
    {
      "table": "messages",
      "name": "idx_messages_created_at",
      "fields": ["created_at"]
    },
    {
      "table": "chat_participants",
      "name": "idx_chat_participants_user_id",
      "fields": ["user_id"]
    },
    {
      "table": "chat_participants",
      "name": "idx_chat_participants_chat_id",
      "fields": ["chat_id"]
    }
  ]
}
```

## 1.2

### prompt:
Opisz kluczowe elementy bazy danych dla aplikacji do przesyłania wiadomości. Przedstaw odpowiedź w formie listy punktowej. 

## odpowiedź:
 -**Tabela `users`** – przechowuje informacje o użytkownikach (identyfikator, login, e‑mail, hash hasła, data rejestracji, status, avatar).  
- **Tabela `chats`** – reprezentuje rozmowy (czaty grupowe, prywatne, kanały); zawiera nazwę, typ, datę utworzenia, administratora oraz odwołanie do ostatniego komunikatu.
- **Tabela `messages`** – przechowuje pojedyncze wiadomości (identyfikator, odwołanie do czatu i nadawcy, treść, timestamp, flagi edycji/usuwania).
- **Tabela `chat_participants`** – many‑to‑many łączy użytkowników z czatami, określa rolę (admin, moderator, member) oraz dodatkowe ustawienia (np. mute).  - **Klucze obce** – zapewniają spójność referencyjną: `messages.chat_id → chats.chat_id`, `messages.sender_id → users.user_id`, `chat_participants.user_id → users.user_id`, `chat_participants.chat_id → chats.chat_id`.
- **Indeksy** – przyspieszają wyszukiwania: po nazwie użytkownika i e‑mail w `users`, po `chat_id` i `sender_id` w `messages`, po `created_at` w `messages`, oraz w tabeli `chat_participants`.  - **Typy danych i ograniczenia** – stosuje się odpowiednie typy (BIGINT, VARCHAR, ENUM, BOOLEAN, TIMESTAMP) oraz restrykcje (`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`).
- **Bezpieczeństwo** – przechowywanie hasła w postaci haszu, opcjonalne flagi statusu (`active`, `inactive`, `banned`) oraz mute w `chat_participants`.
- **Audyt i historie** – pola `created_at`, `edited_at`, `is_deleted` umożliwiają śledzenie zmian i przywracanie wiadomości.  - **Rozszerzalność** – możliwość dodawania nowych typów czatów, powiadomień, reakcji czy załączników poprzez dodatkowe tabele lub kolumny.

## 1.3

### prompt:
Stwórz schemat bazy danych SQL dla prostego czatu. Wymagane tabele: users, rooms, messages . Zwróć wyłącznie gotowy kod SQL do wklejenia w konsolę bazy danych.

### odpowiedź:

 ```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

# 2.

### prompt:

Podsumuj krótko czym jest Python. Zwróć odpowiedź wyłącznie w formacie JSON bez żadnego dodatkowego tekstu.
Struktura:
{
"title": "Tytuł",
"summary": "Krótki opis",
"tags": ["tag1", "tag2"]
}

### odpowiedź:

{
  "title": "Python",
  "summary": "Python to wysokopoziomowy, interpretowany język programowania z prostą składnią, dużą czytelnością i rozbudowaną biblioteką standardową.",
  "tags": ["programowanie", "interpretowany", "wieloplatformowy"]
}

# 3. 

### prompt:

Sklasyfikuj wiadomość użytkownika jako: bug, feature_request lub question.

Przykłady:

User: Nie widzę przycisku wyślij. -> Label: bug

User: Czy możecie dodać naklejki? -> Label: feature_request

User: Jak zmienić hasło w profilu? -> Label: question

Wiadomość: [TUTAJ WKLEJ TREŚĆ]
Label:

### odpowiedzi:
Aplikacja wyłącza się przy starcie
{
  "label": "bug"
}

 Czy moje dane są szyfrowane?

 {
  "label": "question"
}

Chciałbym eksportować czaty do PDF

 {
  "label": "feature_request"
}

# 4.

### prompt:
Wyjaśnij czym jest REST API w maksymalnie 30 słowach. Bądź konkretny, nie używaj wstępów.

### odpoweidź:
REST API to styl architektoniczny wykorzystujący HTTP do komunikacji klient-serwer, oparty na zasobach i metodach GET, POST, PUT, DELETE.