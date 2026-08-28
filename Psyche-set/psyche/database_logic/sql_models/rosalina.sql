-- rosalina.sql

-- Think Rosa as "God", and Lina as "Satan".

create table Rosa( -- Rosa holds data, breaks herself into pieces called generals (SLMs) on that data, and interacts
    rosa_id TEXT NOT NULL PRIMARY KEY UNIQUE, -- ID might be 100+ characters
    access_key_id TEXT UNIQUE references Access_key(access_key_id),
    

    rosa_name TEXT NOT NULL,

    active_model_id   TEXT,        -- points at the model artifact/registry currently in use
    model_version     TEXT,        -- e.g. 'v0.3' — bump this each retrain, keep history in rosa_model_history
    status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'retraining', 'offline')),

    created_at DATETIME default CURRENT_TIMESTAMP,
    last_retrained_at DATETIME
);

-- ROSA's self-description changes over time and you explicitly want to
-- observe that drift ("psychological interest") — a single overwritten
-- column can't do that. One row per snapshot instead.
CREATE TABLE Rosa_self_reflections( -- Something that updates once a while. Just to see how the being thinks of it self. Psychological interest
    reflection_id     TEXT PRIMARY KEY,
    rosa_id           TEXT NOT NULL REFERENCES Rosa(rosa_id),

    explanation       TEXT NOT NULL,  -- "who am I" at this point in time
    reflected_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);


create table Lina( -- Lina holds data aswell, but holds dangerous, harmful, or "dead" data (like killed guardians).
    lina_id           TEXT PRIMARY KEY,
    access_key_id TEXT UNIQUE references Access_key(access_key_id),
    

    lina_name         TEXT NOT NULL,

    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP

);


-- What Lina is actually holding, and why it ended up with her.
-- One row per General/LINX/data-blob she's taken custody of.
CREATE TABLE Lina_holdings(
    holding_id        TEXT PRIMARY KEY,
    lina_id           TEXT NOT NULL REFERENCES Lina(lina_id),

    held_type         TEXT NOT NULL CHECK (held_type IN ('general', 'linx', 'data')),
    held_id           TEXT NOT NULL,  -- id within whichever table held_type points to (app-enforced, see note below)

    reason            TEXT NOT NULL,  -- e.g. 'accuracy too low', 'harmful output', 'killed by rosa'
    quarantined_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);




create table Field(
    field_id TEXT PRIMARY KEY,

    domain TEXT NOT NULL UNIQUE,
    niche_id text not null references Niches(niche_id),

    knowledge text,
    key_points text,


    guardian_connection BOOLEAN DEFAULT FALSE,


    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_at DATETIME NULL,
);

create table Field_associations(
    field_association_id TEXT PRIMARY KEY,

    field_id TEXT references Field(field_id),

    -- Only 1 can be set at a time.
    association_id INT references Field(association_id), -- Field connect. Set if so

    association_context TEXT, -- A figure, game, etc that connects. Set if so. 
);


-- remove 
create table Sources( -- sources are areas agents can reference to obtain data
    source_id TEXT PRIMARY key,

    source_type text not null, -- Wiki, Github, research paper, chat, etc
    source_title text not null,

    targeted_field text REFERENCES Field(field_id),
    usefulness float, -- usefulness will be calculated by how much times it's used and grabbed from
    added_at DATETIME default CURRENT_TIMESTAMP,

);

create table Thought(
    thought_id TEXT PRIMARY key unique, 

    thinker_id text not null,
    memory_id INT references Memory(memory_id), -- set if so
    thought_type text check (thought_type in ('theory', 'thought'))

    context text not null,
    thought_at DATETIME default CURRENT_TIMESTAMP,

    time_to_live int,
);

create table Related_fields_for_thought(
    related_fields_for_thought_id int generated always as identity primary key,
    thought int references Thought(thought_id),
    related_field text not null
);