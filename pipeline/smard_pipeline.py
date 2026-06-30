import requests
import polars as pl
import dlt
import io
from datetime import datetime
from minio import Minio
from config import (
    SLACK_WEBHOOK_URL,
    SMARD_BASE_URL,
    REGION,
    RESOLUTION,
    START_DATE,
    FILTERS,
    MAX_NULL_THRESHOLD,
    MIN_PRICE_EUR_MWH,
    MAX_PRICE_EUR_MWH,
    MIN_MWH,
    MAX_MWH,
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET,
)

# ── 1. HELPERS ──────────────────────────────────────────────────────────────

def get_cutoff_timestamp(date_str: str) -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(dt.timestamp() * 1000)

def fetch_timestamps(filter_id: int) -> list[int]:
    url = f"{SMARD_BASE_URL}/{filter_id}/{REGION}/index_{RESOLUTION}.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()["timestamps"]

def filter_timestamps(timestamps: list[int], cutoff: int, end_cutoff: int = None) -> list[int]:
    df = pl.DataFrame({"timestamp": timestamps})
    if end_cutoff:
        filtered = df.filter(
            (pl.col("timestamp") >= cutoff) & (pl.col("timestamp") <= end_cutoff)
        )
    else:
        filtered = df.filter(pl.col("timestamp") >= cutoff)
    return filtered["timestamp"].to_list()

def fetch_chunk(filter_id: int, timestamp: int) -> list:
    url = f"{SMARD_BASE_URL}/{filter_id}/{REGION}/{filter_id}_{REGION}_{RESOLUTION}_{timestamp}.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()["series"]

# ── 2. MINIO CLIENT ──────────────────────────────────────────────────────────

def get_minio_client() -> Minio:
    return Minio(
        MINIO_ENDPOINT.replace("http://", ""),
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

def save_to_minio(df: pl.DataFrame, filter_config: dict):
    """Save cleaned DataFrame as Parquet to MinIO data lake."""
    client = get_minio_client()
    category = filter_config["category"]
    filter_id = filter_config["id"]
    date_str = datetime.utcnow().strftime("%Y/%m")
    object_name = f"raw/{category}/{filter_id}/{date_str}/data.parquet"

    buffer = io.BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)
    size = buffer.getbuffer().nbytes

    client.put_object(
        MINIO_BUCKET,
        object_name,
        buffer,
        size,
        content_type="application/octet-stream"
    )
    print(f"   📦 MinIO: raw/{category}/{filter_id}/{date_str}/data.parquet")

# ── 3. POLARS NORMALIZATION ──────────────────────────────────────────────────

def normalize_series(
    series: list,
    filter_id: int,
    filter_name: str,
    unit: str,
    category: str,
) -> pl.DataFrame:
    timestamps = [row[0] for row in series]
    values = [row[1] for row in series]

    df = pl.DataFrame({
        "raw_timestamp": timestamps,
        "value": values,
    })

    df = df.with_columns([
        (pl.col("raw_timestamp").cast(pl.Int64) * 1000).cast(pl.Datetime("us")).alias("timestamp"),
        pl.lit(filter_id).alias("filter_id"),
        pl.lit(filter_name).alias("filter_name"),
        pl.lit(unit).alias("unit"),
        pl.lit(category).alias("category"),
        pl.lit(REGION).alias("region"),
        pl.lit(RESOLUTION).alias("resolution"),
        pl.lit(datetime.utcnow()).alias("ingested_at"),
    ]).drop("raw_timestamp")

    return df

# ── 4. QUALITY CHECKS ────────────────────────────────────────────────────────

def quality_check(df: pl.DataFrame, filter_config: dict) -> pl.DataFrame:
    total_rows = len(df)
    filter_name = filter_config["name"]
    unit = filter_config["unit"]

    null_count = df["value"].null_count()
    null_rate = null_count / total_rows
    if null_rate > MAX_NULL_THRESHOLD:
        print(f"⚠️  WARNING: {filter_name} has {null_rate:.1%} nulls")
    else:
        print(f"✅ Null check passed: {null_rate:.1%} nulls")

    if unit == "EUR/MWh":
        invalid = df.filter(
            (pl.col("value") < MIN_PRICE_EUR_MWH) |
            (pl.col("value") > MAX_PRICE_EUR_MWH)
        )
    else:
        invalid = df.filter(
            (pl.col("value") < MIN_MWH) |
            (pl.col("value") > MAX_MWH)
        )

    if len(invalid) > 0:
        print(f"⚠️  WARNING: {len(invalid)} rows outside valid range")
    else:
        print("✅ Range check passed")

    duplicates = total_rows - df["timestamp"].n_unique()
    if duplicates > 0:
        print(f"⚠️  WARNING: {duplicates} duplicate timestamps")
        df = df.unique(subset=["timestamp", "filter_id"])
    else:
        print("✅ Duplicate check passed")

    return df

# ── 5. FETCH ALL DATA ────────────────────────────────────────────────────────

def fetch_filter_data(filter_config: dict, cutoff: int, end_cutoff: int = None) -> pl.DataFrame:
    filter_id = filter_config["id"]
    filter_name = filter_config["name"]
    unit = filter_config["unit"]
    category = filter_config["category"]

    print(f"\n📡 Fetching: {filter_name} (ID: {filter_id})")

    all_timestamps = fetch_timestamps(filter_id)
    filtered_timestamps = filter_timestamps(all_timestamps, cutoff, end_cutoff)
    print(f"   Found {len(filtered_timestamps)} chunks to fetch")

    all_frames = []
    for i, ts in enumerate(filtered_timestamps):
        print(f"   Chunk {i+1}/{len(filtered_timestamps)}...", end="\r")
        series = fetch_chunk(filter_id, ts)
        df = normalize_series(series, filter_id, filter_name, unit, category)
        all_frames.append(df)

    combined = pl.concat(all_frames)
    print(f"   ✅ Fetched {len(combined):,} rows")

    # Quality checks
    combined = quality_check(combined, filter_config)

    # Save to MinIO data lake
    save_to_minio(combined, filter_config)

    return combined

# ── 6. DLT RESOURCE ─────────────────────────────────────────────────────────

@dlt.resource(
    name="energy_timeseries",
    write_disposition="append",
    primary_key=["timestamp", "filter_id"]
)
def energy_timeseries_resource(cutoff: int, end_cutoff: int = None):
    for filter_config in FILTERS:
        df = fetch_filter_data(filter_config, cutoff, end_cutoff)
        yield df.to_dicts()

# ── 7. MAIN ──────────────────────────────────────────────────────────────────

def run_pipeline(start_date_override=None, end_date_override=None):
    from slack_alerts import alert_pipeline_start, alert_pipeline_success, alert_pipeline_failure
    import time

    effective_start = start_date_override if start_date_override else START_DATE

    print("🚀 Starting Energy Timeseries Platform Pipeline")
    print(f"📅 Fetching data from: {effective_start}")
    if end_date_override:
        print(f"📅 Fetching data until: {end_date_override}")
    print(f"🔢 Filters: {len(FILTERS)}")

    start_time = time.time()
    cutoff = get_cutoff_timestamp(effective_start)
    end_cutoff = get_cutoff_timestamp(end_date_override) if end_date_override else None

    alert_pipeline_start(len(FILTERS), START_DATE)

    try:
        pipeline = dlt.pipeline(
            pipeline_name="energy_timeseries",
            destination="clickhouse",
            dataset_name="raw_energy"
        )

        print("\n📦 Staging to MinIO → Loading to ClickHouse...")
        load_info = pipeline.run(energy_timeseries_resource(cutoff=cutoff, end_cutoff=end_cutoff))

        duration = time.time() - start_time
        total_rows = len(FILTERS) * 12935

        print(f"✅ Load complete: {load_info}")
        print("\n🎉 Pipeline complete!")

        alert_pipeline_success(total_rows, duration)

    except Exception as e:
        alert_pipeline_failure(str(e))
        raise

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="SMARD Energy Pipeline")
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Start date for backfill (YYYY-MM-DD). Defaults to config START_DATE."
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="End date for backfill (YYYY-MM-DD). Defaults to today."
    )
    parser.add_argument(
        "--filter-id",
        type=int,
        default=None,
        help="Backfill only a specific filter ID instead of all 10."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Override START_DATE if backfill date provided
    backfill_start = args.start_date if args.start_date else START_DATE

    # Filter to single filter_id if specified
    if args.filter_id:
        original_filters = FILTERS[:]
        FILTERS[:] = [f for f in FILTERS if f["id"] == args.filter_id]
        if not FILTERS:
            print(f"❌ Filter ID {args.filter_id} not found in config")
            exit(1)
        print(f"🎯 Backfill mode: filter {args.filter_id} only")

    if args.start_date or args.end_date:
        print(f"🔄 BACKFILL MODE")
        print(f"   Start: {backfill_start}")
        print(f"   End: {args.end_date or 'today'}")

    run_pipeline(start_date_override=backfill_start, end_date_override=args.end_date)


def run_quality_validation():
    """Run Great Expectations validation after pipeline load."""
    import subprocess
    import sys
    result = subprocess.run(
        [sys.executable, "../great_expectations/energy_expectations.py"],
        capture_output=True,
        text=True,
        cwd="/Users/kaleab/Documents/energy-timeseries-platform/pipeline"
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ Quality validation failed: {result.stderr}")
        return False
    return True
