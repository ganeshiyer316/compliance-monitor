"""
Database utilities for compliance monitoring system.
Manages SQLite database with 4 core tables.
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


def get_db_path(data_dir: str = "data") -> str:
    """Get the path to the SQLite database file."""
    db_path = os.path.join(data_dir, "compliance.db")
    return db_path


def get_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path: str) -> None:
    """
    Initialize the database with all required tables.

    Tables:
    - sources: URLs to monitor
    - snapshots: Content snapshots with hashes
    - changes: Detected differences
    - compliance_items: Parsed compliance requirements
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        # Table 1: Sources
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table 2: Snapshots
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'success',
                error_message TEXT,
                FOREIGN KEY (source_id) REFERENCES sources(id)
            )
        """)

        # Table 3: Changes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                old_snapshot_id INTEGER,
                new_snapshot_id INTEGER NOT NULL,
                diff_text TEXT NOT NULL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                analyzed BOOLEAN DEFAULT 0,
                FOREIGN KEY (source_id) REFERENCES sources(id),
                FOREIGN KEY (old_snapshot_id) REFERENCES snapshots(id),
                FOREIGN KEY (new_snapshot_id) REFERENCES snapshots(id)
            )
        """)

        # Table 4: Compliance Items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compliance_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                change_id INTEGER NOT NULL,
                source_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                summary TEXT,
                deadline DATE,
                impact_level TEXT,
                mccs TEXT,
                regions TEXT,
                transaction_types TEXT,
                technical_requirements TEXT,
                keywords TEXT,
                relevance_score INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (change_id) REFERENCES changes(id),
                FOREIGN KEY (source_id) REFERENCES sources(id)
            )
        """)

        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_source ON snapshots(source_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_hash ON snapshots(content_hash)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_changes_source ON changes(source_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_changes_analyzed ON changes(analyzed)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_compliance_deadline ON compliance_items(deadline)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_compliance_relevance ON compliance_items(relevance_score)")

        conn.commit()
        logger.info("Database initialized successfully")

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to initialize database: {e}")
        raise
    finally:
        conn.close()


def insert_source(db_path: str, name: str, url: str, source_type: str, active: bool = True) -> int:
    """Insert a new source or update if exists."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO sources (name, url, type, active)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                name = excluded.name,
                type = excluded.type,
                active = excluded.active,
                updated_at = CURRENT_TIMESTAMP
        """, (name, url, source_type, active))

        conn.commit()
        source_id = cursor.lastrowid

        if source_id == 0:
            # If no insert happened (conflict), get the existing ID
            cursor.execute("SELECT id FROM sources WHERE url = ?", (url,))
            source_id = cursor.fetchone()[0]

        return source_id

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert source: {e}")
        raise
    finally:
        conn.close()


def insert_snapshot(db_path: str, source_id: int, content: str, content_hash: str,
                   status: str = 'success', error_message: Optional[str] = None) -> int:
    """Insert a new snapshot."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO snapshots (source_id, content, content_hash, status, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (source_id, content, content_hash, status, error_message))

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert snapshot: {e}")
        raise
    finally:
        conn.close()


def get_latest_snapshot(db_path: str, source_id: int) -> Optional[Dict[str, Any]]:
    """Get the most recent snapshot for a source."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT * FROM snapshots
            WHERE source_id = ? AND status = 'success'
            ORDER BY scraped_at DESC
            LIMIT 1
        """, (source_id,))

        row = cursor.fetchone()
        return dict(row) if row else None

    finally:
        conn.close()


def insert_change(db_path: str, source_id: int, old_snapshot_id: Optional[int],
                 new_snapshot_id: int, diff_text: str) -> int:
    """Insert a detected change."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO changes (source_id, old_snapshot_id, new_snapshot_id, diff_text)
            VALUES (?, ?, ?, ?)
        """, (source_id, old_snapshot_id, new_snapshot_id, diff_text))

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert change: {e}")
        raise
    finally:
        conn.close()


def insert_compliance_item(db_path: str, change_id: int, source_id: int, item_data: Dict[str, Any]) -> int:
    """Insert a compliance item extracted by intelligence agent."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO compliance_items (
                change_id, source_id, title, summary, deadline, impact_level,
                mccs, regions, transaction_types, technical_requirements,
                keywords, relevance_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            change_id,
            source_id,
            item_data.get('title'),
            item_data.get('summary'),
            item_data.get('deadline'),
            item_data.get('impact_level'),
            item_data.get('mccs'),  # JSON string
            item_data.get('regions'),  # JSON string
            item_data.get('transaction_types'),  # JSON string
            item_data.get('technical_requirements'),  # JSON string
            item_data.get('keywords'),  # JSON string
            item_data.get('relevance_score', 5)
        ))

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert compliance item: {e}")
        raise
    finally:
        conn.close()


def mark_change_analyzed(db_path: str, change_id: int) -> None:
    """Mark a change as analyzed."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE changes SET analyzed = 1 WHERE id = ?", (change_id,))
        conn.commit()
    finally:
        conn.close()


def get_active_sources(db_path: str) -> List[Dict[str, Any]]:
    """Get all active sources."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM sources WHERE active = 1")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_compliance_items(db_path: str, min_relevance: int = 0,
                        impact_level: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get compliance items with optional filtering."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        query = """
            SELECT ci.*, s.name as source_name, s.url as source_url
            FROM compliance_items ci
            JOIN sources s ON ci.source_id = s.id
            WHERE ci.relevance_score >= ?
        """
        params = [min_relevance]

        if impact_level:
            query += " AND ci.impact_level = ?"
            params.append(impact_level)

        query += " ORDER BY ci.deadline ASC, ci.relevance_score DESC"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_unanalyzed_changes(db_path: str) -> List[Dict[str, Any]]:
    """Get changes that haven't been analyzed yet."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT c.*, s.name as source_name, s.url as source_url
            FROM changes c
            JOIN sources s ON c.source_id = s.id
            WHERE c.analyzed = 0
            ORDER BY c.detected_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
