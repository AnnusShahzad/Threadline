-- Initial schema: investigations, typed entities, and the edges between them.
-- Timestamps are ISO-8601 UTC text so they sort lexicographically without extensions.

CREATE TABLE IF NOT EXISTS investigations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    investigation_id TEXT NOT NULL REFERENCES investigations (id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    value TEXT NOT NULL,
    properties TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    UNIQUE (investigation_id, type, value)
);

CREATE TABLE IF NOT EXISTS edges (
    id TEXT PRIMARY KEY,
    investigation_id TEXT NOT NULL REFERENCES investigations (id) ON DELETE CASCADE,
    source_id TEXT NOT NULL REFERENCES entities (id) ON DELETE CASCADE,
    target_id TEXT NOT NULL REFERENCES entities (id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    -- The transform that produced this edge; null for edges the analyst draws by hand.
    transform TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (investigation_id, source_id, target_id, label)
);

CREATE INDEX IF NOT EXISTS entities_by_investigation ON entities (investigation_id);
CREATE INDEX IF NOT EXISTS edges_by_source ON edges (investigation_id, source_id);
