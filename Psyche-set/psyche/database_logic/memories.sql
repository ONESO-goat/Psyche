-- memories.sql

create TABLE storage(
    storage_id TEXT PRIMARY KEY,

    linx_id TEXT NOT NULL references linx(linx_id),

);


create TABLE memory(
    memory_id INT PRIMARY KEY,

    storage_id TEXT NOT NULL references storage(storage_id),

    context TEXT NOT NULL,
    importance float,
    related_emotion TEXT,

    how_this_connects_with_topic text not null, -- topic = user or specialized field
    send_to_rosa BOOLEAN,

    time_to_live DATETIME,  -- How long this memory stays. Most of the time memories might stay for prolonged times.
    confidence float,
);

create table memory_associations(
    memory_id int references memory(memory_id),

    association int references memory(association)
);