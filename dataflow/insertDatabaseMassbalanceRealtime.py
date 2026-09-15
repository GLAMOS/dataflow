#!/usr/bin/env python3
"""
insertDatabaseMassbalanceRealtime.py

Cronjob: download the GLAMOS current-year "state of Swiss glaciers" file, join
it with a local lookup table (vw_glacier_short.csv) to resolve each glacier's
UUID, and load the result into the PostgreSQL `realtime` table.

Runs on Python 3.6+.

Database credentials are NEVER stored in this script. They are read at runtime
from an external INI config file (see DB_CONFIG below), so this file is safe to
commit to a public repository. Make sure the .cfg file itself is git-ignored.

Built for an unattended cronbox:
  - DB credentials read from an external .cfg file (nothing secret in the code)
  - the lookup CSV and the .cfg are read from the same folder as this script,
    so it can be launched with no arguments from any working directory
  - download with timeout + retries
  - only stdlib + psycopg2 needed (no pandas/requests to install)
  - a fresh uuid4 is generated for every row's primary key (pk)
  - idempotent per day: within one transaction it removes any existing rows for
    the current date_of_state and inserts the fresh set, so re-running the same
    day refreshes instead of duplicating

Dependency:
    pip install psycopg2-binary

Config file format (INI), e.g. databaseAccessConfiguration.gldirw.cfg:
    [Access]
    host = vawsrv01.ethz.ch
    dbname = glamos
    user = gldirw
    password = ********
    timeout = 10

Target table columns (mass_balance.realtime):
    pk             uuid    -- generated here, one per row
    fk_glacier     uuid    -- glacier UUID, from lookup.pk (join on SGI-ID)
    state_of_mb            -- .dat "State of mass balance(sigma)"
    class_of_state         -- .dat "Classification(-)"
    massbalance           -- .dat "B(m w.e.)"
    data_driven    boolean -- .dat "Data (1/0)"
    monitoring     boolean -- .dat "Moni (1/0)"
    date_of_state  date    -- .dat "State of Swiss glacier on:"

The lookup CSV (vw_glacier_short.csv) and the DB config file are read from the
same directory as this script, so it can be run with no arguments:
    python insertDatabaseMassbalanceRealtime.py
(Each path can still be overridden with the LOOKUP_CSV / DB_CONFIG env vars.)

Example crontab entry (daily 06:15, output appended to a log):
    15 6 * * *  /opt/glamos/venv/bin/python \
        /opt/glamos/insertDatabaseMassbalanceRealtime.py \
        >> /var/log/glamos/import.log 2>&1
"""

import configparser
import csv
import logging
import os
import re
import sys
import time
import urllib.request
import uuid
from datetime import date
from typing import Dict, List, Optional, Tuple

import psycopg2
import psycopg2.extras

# --------------------------------------------------------------------------- #
# Configuration (override via environment variables)
# --------------------------------------------------------------------------- #
# Directory this script lives in. The lookup CSV and the DB config file are
# expected to sit next to the script, so it can be run with no arguments from
# any working directory (e.g. from cron, which uses a different CWD).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_URL = os.environ.get(
    "GLAMOS_URL",
    "https://doi.glamos.ch/figures/massbalance_current/massbalance_current.dat",
)
LOOKUP_CSV = os.environ.get("LOOKUP_CSV", os.path.join(SCRIPT_DIR, "vw_glacier_short.csv"))

# Path to the external DB credentials file. Keep this file OUT of git.
DB_CONFIG = os.environ.get(
    "DB_CONFIG", os.path.join(SCRIPT_DIR, "databaseAccessConfiguration.gldirw.cfg")
)
DB_CONFIG_SECTION = os.environ.get("DB_CONFIG_SECTION", "Access")

TARGET_SCHEMA = os.environ.get("TARGET_SCHEMA", "mass_balance")
TARGET_TABLE = os.environ.get("TARGET_TABLE", "realtime")

# If true (default), delete existing rows for this date_of_state before
# inserting, so a re-run for the same day refreshes rather than duplicates.
# Set to "0"/"false" to append unconditionally.
REPLACE_EXISTING_DATE = os.environ.get("REPLACE_EXISTING_DATE", "1").lower() not in (
    "0", "false", "no",
)

HTTP_TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "30"))
HTTP_RETRIES = int(os.environ.get("HTTP_RETRIES", "3"))

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("glamos")


# --------------------------------------------------------------------------- #
# DB credentials (read from external file — nothing secret in this script)
# --------------------------------------------------------------------------- #
def read_db_config(path, section):
    # type: (str, str) -> dict
    """Read connection settings from the INI config file into psycopg2 kwargs."""
    if not os.path.exists(path):
        raise IOError(
            "Database config file not found: {}. "
            "Set DB_CONFIG to its location.".format(path)
        )
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    if section not in parser:
        raise KeyError("Section [{}] missing in {}".format(section, path))
    sec = parser[section]

    missing = [k for k in ("host", "dbname", "user", "password") if k not in sec]
    if missing:
        raise KeyError("Missing keys {} in [{}] of {}".format(missing, section, path))

    params = {
        "host": sec.get("host"),
        "dbname": sec.get("dbname"),
        "user": sec.get("user"),
        "password": sec.get("password"),
        "connect_timeout": sec.getint("timeout", fallback=10),
    }
    if sec.get("port"):
        params["port"] = sec.getint("port")
    # Log everything EXCEPT the password
    log.info(
        "DB config loaded from %s: host=%s dbname=%s user=%s timeout=%s",
        path, params["host"], params["dbname"], params["user"],
        params["connect_timeout"],
    )
    return params


def connect():
    return psycopg2.connect(**read_db_config(DB_CONFIG, DB_CONFIG_SECTION))


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #
def download(url):
    # type: (str) -> str
    """Fetch the .dat file as text, with retries and a timeout."""
    last_err = None  # type: Optional[Exception]
    for attempt in range(1, HTTP_RETRIES + 1):
        try:
            log.info("Downloading %s (attempt %d/%d)", url, attempt, HTTP_RETRIES)
            req = urllib.request.Request(url, headers={"User-Agent": "glamos-import/1.0"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            log.info("Downloaded %d characters", len(raw))
            return raw
        except Exception as err:
            last_err = err
            log.warning("Download failed: %s", err)
            if attempt < HTTP_RETRIES:
                time.sleep(2 ** attempt)
    raise RuntimeError("Could not download {}: {}".format(url, last_err))


# --------------------------------------------------------------------------- #
# Parse the .dat
# --------------------------------------------------------------------------- #
def parse_state_date(first_line):
    # type: (str) -> date
    """Parse 'State of Swiss glacier on: 2026 09 15' -> date."""
    m = re.search(r"(\d{4})\s+(\d{1,2})\s+(\d{1,2})", first_line)
    if not m:
        raise ValueError(
            "Could not parse the state date from the first line of the .dat "
            "(needed for date_of_state). Line was: {!r}".format(first_line)
        )
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def to_bool(v):
    # type: (str) -> Optional[bool]
    v = v.strip()
    if v == "1":
        return True
    if v == "0":
        return False
    return None


def parse_dat(raw):
    # type: (str) -> Tuple[date, List[dict]]
    """Return (state_date, list-of-row-dicts) from the raw .dat text."""
    lines = raw.splitlines()
    if len(lines) < 6:
        raise ValueError("Unexpected .dat: only {} lines".format(len(lines)))

    state_date = parse_state_date(lines[0])
    log.info("date_of_state = %s", state_date)

    reader = csv.reader(lines[5:])  # skip 4 metadata lines + 1 column header
    rows = []  # type: List[dict]
    for fields in reader:
        if not fields or not fields[0].strip():
            continue
        if len(fields) != 7:
            log.warning("Skipping malformed row (%d fields): %r", len(fields), fields)
            continue
        rows.append(
            {
                "sgi_id": fields[0].strip(),
                "state_of_mb": float(fields[1]),
                "class_of_state": int(fields[2]),
                "massbalance": float(fields[3]),
                "data_driven": to_bool(fields[4]),
                "monitoring": to_bool(fields[5]),
                # fields[6] (glacier short name) is not stored in `realtime`
            }
        )
    log.info("Parsed %d data rows from .dat", len(rows))
    return state_date, rows


# --------------------------------------------------------------------------- #
# Lookup CSV + join
# --------------------------------------------------------------------------- #
def load_sgi_to_uuid(path):
    # type: (str) -> Dict[str, str]
    """Map SGI-ID (pk_sgi) -> glacier UUID (pk)."""
    if not os.path.exists(path):
        raise IOError("Lookup CSV not found: {}".format(path))
    mapping = {}  # type: Dict[str, str]
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sgi = (row.get("pk_sgi") or "").strip()
            glacier_uuid = (row.get("pk") or "").strip()
            if sgi and sgi != "NULL" and glacier_uuid and glacier_uuid != "NULL":
                mapping[sgi] = glacier_uuid
    log.info("Loaded %d SGI->UUID entries from %s", len(mapping), path)
    return mapping


def build_rows(state_date, dat_rows, sgi_to_uuid):
    # type: (date, List[dict], Dict[str, str]) -> List[dict]
    """Resolve fk_glacier, generate a pk per row, attach date_of_state."""
    out = []  # type: List[dict]
    unmatched = 0
    for r in dat_rows:
        fk_glacier = sgi_to_uuid.get(r["sgi_id"])
        if fk_glacier is None:
            unmatched += 1
            log.warning("No glacier UUID for SGI-ID %s — skipping row", r["sgi_id"])
            continue
        out.append(
            {
                "pk": str(uuid.uuid4()),          # fresh UUID per entry
                "fk_glacier": fk_glacier,
                "state_of_mb": r["state_of_mb"],
                "class_of_state": r["class_of_state"],
                "massbalance": r["massbalance"],
                "data_driven": r["data_driven"],
                "monitoring": r["monitoring"],
                "date_of_state": state_date,
            }
        )
    if unmatched:
        log.warning("%d rows skipped (no matching glacier UUID)", unmatched)
    log.info("Built %d rows ready to load", len(out))
    return out


# --------------------------------------------------------------------------- #
# PostgreSQL load
# --------------------------------------------------------------------------- #
COLUMNS = [
    "pk", "fk_glacier", "state_of_mb", "class_of_state",
    "massbalance", "data_driven", "monitoring", "date_of_state",
]

# For fresh deployments only. Does nothing if the table already exists.
DDL = """
CREATE TABLE IF NOT EXISTS {table} (
    pk             uuid PRIMARY KEY,
    fk_glacier     uuid NOT NULL,
    state_of_mb    double precision,
    class_of_state smallint,
    massbalance    double precision,
    data_driven    boolean,
    monitoring     boolean,
    date_of_state  date NOT NULL
);
"""


def load(rows, state_date):
    # type: (List[dict], date) -> None
    if not rows:
        log.warning("No rows to load — skipping.")
        return

    fq_table = '"{}"."{}"'.format(TARGET_SCHEMA, TARGET_TABLE)
    col_list = ", ".join('"{}"'.format(c) for c in COLUMNS)
    values = [tuple(r[c] for c in COLUMNS) for r in rows]

    conn = connect()
    try:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(DDL.format(table=fq_table))  # no-op if table exists

            if REPLACE_EXISTING_DATE:
                cur.execute(
                    'DELETE FROM {} WHERE "date_of_state" = %s'.format(fq_table),
                    (state_date,),
                )
                log.info("Removed %d existing rows for %s", cur.rowcount, state_date)

            psycopg2.extras.execute_values(
                cur,
                "INSERT INTO {} ({}) VALUES %s".format(fq_table, col_list),
                values,
                page_size=500,
            )
        conn.commit()
        log.info("Inserted %d rows into %s for %s", len(rows), fq_table, state_date)
    except Exception:
        conn.rollback()
        log.exception("Load failed — transaction rolled back.")
        raise
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main():
    # type: () -> int
    try:
        raw = download(DATA_URL)
        state_date, dat_rows = parse_dat(raw)
        sgi_to_uuid = load_sgi_to_uuid(LOOKUP_CSV)
        rows = build_rows(state_date, dat_rows, sgi_to_uuid)
        load(rows, state_date)
    except Exception:
        log.exception("Run failed.")
        return 1
    log.info("Run completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())