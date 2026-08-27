-- user.sql

-- Users who can independently own LINX
create TABLE user(
    user_id             INT PRIMARY KEY UNIQUE,

    username            varchar(255) NOT NULL UNIQUE,
    hashed_passed       varchar(255) NOT NULL,
    email               varchar(100)

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login          datetime default CURRENT_TIMESTAMP,

    owned_linx          TEXT references linx(linx_id),

    settings            int references user_settings(settings)
);

create table user_preferences(
    perference_id       int generated always unique primary key,
    user_id             INT references user(user_id),

    perference          TEXT not null
    
);

