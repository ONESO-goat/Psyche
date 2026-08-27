-- GLINX.sql

create TABLE General(
    general_id STRING           PRIMARY KEY,
    name                        TEXT NOT NULL,
    domain                      TEXT NOT NULL,

    follows_id                  TEXT check (follows_id in (rosa(rosa_id), lina(lina_id))),
    createdAt                   DATETIME DEFAULT CURRENT_TIMESTAMP,

    creator                     TEXT not null default "rosa",
    field_specialization_id     TEXT not null REFERENCES field(field_id),
    valuation                   float, -- 0 - 10. < 5 means less value, > 5 means it's fairly valuable or important.
    -- example,  
    -- general cheese -> knows how to make cheese easily, safely, and quickly -> valuation is between 5-7 depending on the market.
    
    accuracy                    float, -- 0.18 = 18%, 1.0 = 100%. min = 0.0 max = 1.0
    mark_for_removal            BOOLEAN default FALSE, -- if accuracy is too low, the general risk harm, etc, kill.
    -- when a general is killed and it created LINX's, the linx's either get transferred to an upgraded version
    -- of said general, or get killed if their valuation is too low.

    available_for_purchase      BOOLEAN default FALSE, -- determined by me/team
);



-- Niches are the "topic" a LINX cares about (music, crypto, etc.)
-- Pulling this into its own table means you're not hardcoding
-- niche names as strings everywhere, and it gives you a place
-- to hang niche-level config (like default refresh rate).
CREATE TABLE niches (
    niche_id            SERIAL PRIMARY KEY,
    name                TEXT NOT NULL UNIQUE,
    default_refresh_sec INTEGER DEFAULT 3600,  -- how often data gets pulled by default

    target_field_id     TEXT REFERENCES field(field_id)
);

-- The core LINX table. One table for both types, distinguished
-- by linx_type + nullable owner columns. This avoids duplicating
-- structure across two tables when the behavior overlaps so much.
CREATE TABLE linx (
    linx_id         INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    linx_type       TEXT NOT NULL CHECK (linx_type IN ('manager', 'independent')),
    niche_id        INTEGER NOT NULL REFERENCES niches(niche_id),

    -- exactly one of these should be set, enforced at the app layer
    -- (or with a CHECK constraint once you're comfortable with those)
    general_id      INTEGER REFERENCES generals(general_id),   -- set if manager
    owner_user_id   INTEGER REFERENCES users(user_id),         -- set if independent

    rule_based      BOOLEAN DEFAULT TRUE,   -- flips to FALSE once/if it graduates to its own SLM
    refresh_sec     INTEGER,                -- overrides niche default when set (managers get faster cadence)
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP

    valuation       float,
);

-- Every piece of data a LINX pulls in. This is the "data on data" table.
CREATE TABLE linx_data (
    data_id         INTEGER PRIMARY KEY,
    linx_id         INTEGER NOT NULL REFERENCES linx(linx_id),
    source          TEXT,               -- where it came from
    source_id       TEXT references source(source_id),
    payload         TEXT,               -- raw data / JSON blob
    ingested_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);