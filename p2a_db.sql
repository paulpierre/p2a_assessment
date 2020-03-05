CREATE TABLE IF NOT EXISTS "users"
(
    [user_id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [user_first_name] NVARCHAR(160)  NOT NULL,
    [user_last_name] NVARCHAR(160)  NOT NULL,
    [user_email] NVARCHAR(160)  NOT NULL,
    [user_phone_number] NVARCHAR(160)  NOT NULL,
    [user_date] DATETIME NOT NULL
);
