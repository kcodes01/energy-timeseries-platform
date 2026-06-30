import great_expectations as gx
import clickhouse_connect
import json
from datetime import datetime

def run_and_report():
    print("🔍 Running Great Expectations Validation Report...")
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 60)

    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='clickhouse',
        password='clickhouse'
    )

    # Get stats first
    stats = client.query_df("""
        SELECT 
            filter_name,
            count(*) as row_count,
            round(avg(value), 2) as avg_value,
            countIf(value IS NULL) as null_count,
            max(timestamp) as latest_timestamp
        FROM energy.raw_energy___energy_timeseries
        GROUP BY filter_name
        ORDER BY filter_name
    """)

    print("\n📊 Data Freshness & Row Counts:")
    print("-" * 60)
    for _, row in stats.iterrows():
        freshness = row['latest_timestamp']
        print(f"  {row['filter_name'][:40]:<40} | {row['row_count']:>8,} rows | latest: {freshness}")

    # Run expectations
    df = client.query_df("""
        SELECT * FROM energy.raw_energy___energy_timeseries
        LIMIT 10000
    """)

    context = gx.get_context(mode="ephemeral")
    datasource = context.data_sources.add_pandas("energy_data")
    asset = datasource.add_dataframe_asset("energy_timeseries")
    batch_definition = asset.add_batch_definition_whole_dataframe("full_batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    expectations = [
        ("Timestamp not null", gx.expectations.ExpectColumnValuesToNotBeNull(column="timestamp")),
        ("Value 95% not null", gx.expectations.ExpectColumnValuesToNotBeNull(column="value", mostly=0.95)),
        ("Valid categories", gx.expectations.ExpectColumnValuesToBeInSet(column="category", value_set=["price", "generation", "consumption", "forecast"])),
        ("Region is DE", gx.expectations.ExpectColumnValuesToBeInSet(column="region", value_set=["DE"])),
        ("Resolution is hour", gx.expectations.ExpectColumnValuesToBeInSet(column="resolution", value_set=["hour"])),
        ("Valid filter IDs", gx.expectations.ExpectColumnValuesToBeInSet(column="filter_id", value_set=[4169, 4170, 4067, 4068, 1225, 410, 4359, 4071, 5097, 122])),
        ("Row count in range", gx.expectations.ExpectTableRowCountToBeBetween(min_value=1000, max_value=10000000)),
    ]

    print("\n📋 Expectation Results:")
    print("-" * 60)
    results = []
    for name, exp in expectations:
        result = batch.validate(exp)
        status = "✅ PASS" if result.success else "❌ FAIL"
        results.append((name, result.success))
        print(f"  {status} | {name}")

    passed = sum(1 for _, s in results if s)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"🎯 Summary: {passed}/{total} expectations passed")
    print(f"📦 Total rows in warehouse: {stats['row_count'].sum():,}")
    print(f"🕐 Report generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Overall status: {'✅ ALL PASSED' if passed == total else '⚠️ SOME FAILED'}")
    print("=" * 60)

    return passed == total

if __name__ == "__main__":
    run_and_report()
