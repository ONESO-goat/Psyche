-- memories.sql

create TABLE Storage(
    storage_id TEXT PRIMARY KEY,

    linx_id TEXT NOT NULL references Linx(linx_id),

);


create TABLE Memory(
    memory_id INT PRIMARY KEY,

    storage_id TEXT NOT NULL references Storage(storage_id),

    context TEXT NOT NULL,
    importance float,
    related_emotion TEXT,

    how_this_connects_with_topic text not null, -- topic = user or specialized field
    send_to_rosa BOOLEAN,

    time_to_live DATETIME,  -- How long this memory stays. Most of the time memories might stay for prolonged times.
    confidence float,
);

create table Memory_associations(
    memory_associations_id TEXT primary key,
    
    memory_id TEXT references Memory(memory_id),

    association TEXT references Memory(association)
);