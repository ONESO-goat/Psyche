create table association(
    association_id text unique not null primary key,

    association_one_id TEXT references topic(topic_id),
    association_two_id text references topic(topic_id),

    context text not null,

    source_id text null references source(source_id),
                 
    strength real,
    association_type text not null, 
    -- example: Friendship between 2 individuals, fruits, made by the same individual, etc...

    constraint sameId check (
        association_one_id != association_two_id and 
        association_two_id != association_one_id
    )
);

create table topic(
    topic_id text unique primary key,
    what text not null, -- example; apples
    context text not null,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
);