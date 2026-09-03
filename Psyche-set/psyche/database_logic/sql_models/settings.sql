-- settings.sql


-- Linx will likely be an interface. I plan for Linx's to have a face.

create table User_settings(
    settings_id         TEXT PRIMARY KEY,

    -- p == preferred
    p_language          TEXT,
    p_theme             TEXT, -- dark, blue, pink, etc. Edits the visuals on linx's face
    email_notifications BOOLEAN default TRUE
    -- linx_settings_id       TEXT references Linx_attributes(linx_settings_id)
);

create table Linx_attributes(
    linx_settings_id                TEXT PRIMARY KEY,

    creative_weight                 INT default 5, -- < 5 more serious, > 5 more creative
    linx_id                         TEXT references Linx(linx_id),

    attachment_to_topic             float default 0.0

    -- Emotion meters. In python (version 0.1) I split all emotions into its own class. But that was tedious.
    -- Emotions are important components for creating emotional based systems of beings in the real world.
    -- It's everywhere; Humans, pets, etc..
    -- Emotions will be a 5x5 grid of numbers that tune one another. Instead of a singler float or int
    -- Tunning these numbers alter the linx's persona. Become more aggressive, more nonchalant, or a mixed of emotions.
    -- ex; anger = vector<vector<int>> = int starts at 0;   

);

CREATE TABLE Linx_personality_traits (
    trait_id                        SERIAL PRIMARY KEY,
    linx_settings_id                TEXT REFERENCES Linx_attributes(linx_settings_id),
    trait                           TEXT NOT NULL -- Niche or user-gained traits (e.g., 'aggressive', 'nonchalant')
);

CREATE TABLE meter (
    meter_id      TEXT PRIMARY KEY,

    linx_id       TEXT NOT NULL REFERENCES linx(linx_id),
    emotion       TEXT NOT NULL CHECK (emotion IN ('anger', 'joy', 'sadness', 'disgust', 'fear')),
    row_index     INT NOT NULL CHECK (row_index BETWEEN 1 AND 5),

    col_1         INT DEFAULT 0,
    col_2         INT DEFAULT 0,
    col_3         INT DEFAULT 0,
    col_4         INT DEFAULT 0,
    col_5         INT DEFAULT 0,

    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- one row per (linx, emotion, row_index) — no duplicate rows for the same cell-row
    UNIQUE (linx_id, emotion, row_index)
);