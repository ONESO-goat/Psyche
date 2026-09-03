-- user.sql

-- Users who can independently own LINX
create TABLE Users(
    user_id             TEXT PRIMARY KEY UNIQUE,

    username            varchar(255) NOT NULL UNIQUE,
    password_hash       varchar(255) NOT NULL,
    email               varchar(100),

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login          datetime default CURRENT_TIMESTAMP,

    settings_id            text references User_settings(settings_id)
);

create table User_preferences(
    perference_id       TEXT primary key,
    user_id             text references Users(user_id),
    preference          TEXT not null
    
);

