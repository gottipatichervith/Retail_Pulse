
-- =====================================================
-- PIPELINE FILE AUDIT TABLE
-- Stores information about each file-processing run.
-- =====================================================

CREATE TABLE IF NOT EXISTS pipeline_file_audit (
    run_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL DEFAULT 'IN_PROGRESS',

    total_records INTEGER DEFAULT 0,
    valid_records INTEGER DEFAULT 0,
    rejected_records INTEGER DEFAULT 0,

    inserted_records INTEGER DEFAULT 0,
    updated_records INTEGER DEFAULT 0,
    skipped_records INTEGER DEFAULT 0,

    error_message TEXT
);


-- =====================================================
-- PIPELINE BATCH AUDIT TABLE
-- Stores information about individual batches.
-- =====================================================

CREATE TABLE IF NOT EXISTS pipeline_batch_audit (
    batch_audit_id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    batch_number INTEGER NOT NULL,

    started_at TEXT NOT NULL,
    completed_at TEXT,

    status TEXT NOT NULL DEFAULT 'IN_PROGRESS',

    records_read INTEGER DEFAULT 0,
    valid_records INTEGER DEFAULT 0,
    rejected_records INTEGER DEFAULT 0,

    inserted_records INTEGER DEFAULT 0,
    updated_records INTEGER DEFAULT 0,
    skipped_records INTEGER DEFAULT 0,

    error_message TEXT,

    FOREIGN KEY (run_id)
        REFERENCES pipeline_file_audit(run_id)
);


-- =====================================================
-- INDEXES FOR FASTER AUDIT SEARCHES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_file_audit_filename
ON pipeline_file_audit(filename);

CREATE INDEX IF NOT EXISTS idx_batch_audit_filename
ON pipeline_batch_audit(filename);

CREATE INDEX IF NOT EXISTS idx_batch_audit_run
ON pipeline_batch_audit(run_id);

CREATE INDEX IF NOT EXISTS idx_batch_audit_status
ON pipeline_batch_audit(status);
