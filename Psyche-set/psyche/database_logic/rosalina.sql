-- Think Rosa as "God", and Lina as "Satan".

create table rosa( -- Rosa holds data, breaks herself into pieces called generals (SLMs) on that data, and interacts
    rosa_id TEXT NOT NULL PRIMARY KEY UNIQUE, -- ID might be 100+ characters

    rosa_name TEXT NOT NULL,

    explain_who_you_are TEXT, -- Something that changes once a while. Just to see how the being thinks of it self. Psychological interest
    
    created_at DATETIME default CURRENT_TIMESTAMP
);


create table lina( -- Lina holds data aswell, but holds dangerous, harmful, or "dead" data (like killed guardians).
    lina_id TEXT NOT NULL PRIMARY KEY UNIQUE,

    lina_name TEXT NOT NULL,

    explain_who_you_are TEXT, -- Something that changes once a while. Just to see how the being thinks of it self. Psychological interest
    
    created_at DATETIME default CURRENT_TIMESTAMP



);




create table field(
    field_id INT PRIMARY KEY,

    domain TEXT NOT NULL UNIQUE,
    niche_id text not null references niche(niche_id),

    knowledge text,
    key_points text,


    guardian_connection BOOLEAN DEFAULT FALSE,


    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_at DATETIME NULL,
);

create table field_associations(
    field_association_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    field_id TEXT references field(field_id),

    -- Only 1 can be set at a time.
    association_id INT references field(association_id), -- Field connect. Set if so

    association_context TEXT, -- A figure, game, etc that connects. Set if so. 
);


create table sources( -- sources are areas agents can reference to obtain data
    source_id INT PRIMARY key,

    source_type text not null, -- Wiki, Github, research paper, chat, etc
    source_title text not null,

    targeted_field text REFERENCES field(field_id),
    usefulness float, -- usefulness will be calculated by how much times it's used and grabbed from
    added_at DATETIME default CURRENT_TIMESTAMP,

);

create table thought(
    thought_id int generated always as identity PRIMARY key, 

    thinker_id text not null,
    memory_id INT references memory(memory_id), -- set if so
    thought_type text check (thought_type in ("theory", "thought"))

    context text not null,
    thought_at DATETIME default CURRENT_TIMESTAMP,

    time_to_live int,
);

create table related_fields_for_thought(
    related_fields_for_thought_id int generated always as identity primary key,
    thought int references thoughts(thought_id),
    related_field text not null
);