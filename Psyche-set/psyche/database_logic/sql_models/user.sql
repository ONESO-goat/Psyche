-- user.sql

-- Users who can independently own LINX
create TABLE Users(
    user_id             TEXT PRIMARY KEY UNIQUE,

    username            varchar(255) NOT NULL UNIQUE,
    hashed_passed       varchar(255) NOT NULL,
    email               varchar(100)

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login          datetime default CURRENT_TIMESTAMP,

    settings            int references User_settings(settings)
);

create table User_preferences(
    perference_id       TEXT primary key,
    user_id             INT references Users(user_id),
    perference          TEXT not null
    
);

