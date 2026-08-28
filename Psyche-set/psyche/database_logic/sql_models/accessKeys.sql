
CREATE TABLE access_key( -- Access keys are keys required for generals, rosa's, etc.. to do certain features.
-- These keys will update every 6-12 months after creation.

    access_key_id     TEXT PRIMARY KEY,
    access_key        VARCHAR(700) UNIQUE NOT NULL,

    holder_type       TEXT NOT NULL CHECK (holder_type IN ('rosa', 'lina', 'general', 'facility')),
    holder_id         TEXT NOT NULL,  -- app-enforced FK into whichever table holder_type points to

    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiration_date   DATETIME NOT NULL,
    revoked           BOOLEAN DEFAULT FALSE,  -- lets you kill a key immediately, separate from natural expiry

    times_used        INT DEFAULT 0
);

