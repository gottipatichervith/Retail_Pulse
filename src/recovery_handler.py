
from datetime import datetime


def save_checkpoint(
    connection,
    filename,
    batch_number,
    status="IN_PROGRESS"
):
    """
    Save the latest successfully completed batch.

    This function must be called inside the same
    database transaction as the batch processing.
    """

    updated_at = datetime.now().isoformat(
        timespec="seconds"
    )

    connection.execute(
        """
        INSERT INTO pipeline_checkpoints (
            filename,
            last_completed_batch,
            status,
            updated_at
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(filename)
        DO UPDATE SET
            last_completed_batch = excluded.last_completed_batch,
            status = excluded.status,
            updated_at = excluded.updated_at
        """,
        (
            filename,
            batch_number,
            status,
            updated_at
        )
    )


def get_checkpoint(connection, filename):
    """
    Retrieve the last completed batch for a file.

    Returns 0 when the file has no checkpoint.
    """

    result = connection.execute(
        """
        SELECT last_completed_batch
        FROM pipeline_checkpoints
        WHERE filename = ?
        """,
        (filename,)
    ).fetchone()

    if result is None:
        return 0

    return result[0]


def get_checkpoint_status(connection, filename):
    """
    Retrieve the current processing status of a file.
    """

    result = connection.execute(
        """
        SELECT status
        FROM pipeline_checkpoints
        WHERE filename = ?
        """,
        (filename,)
    ).fetchone()

    if result is None:
        return None

    return result[0]
