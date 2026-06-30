import great_expectations as gx
import clickhouse_connect

def run_expectations():
    print("🔍 Running Great Expectations on Energy Data...")

    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='clickhouse',
        password='clickhouse'
    )

    df = client.query_df("""
        SELECT * FROM energy.raw_energy___energy_timeseries
        LIMIT 10000
    """)
    print(f"✅ Fetched {len(df):,} rows")

    context = gx.get_context(mode="ephemeral")

    datasource = context.data_sources.add_pandas("energy_data")
    asset = datasource.add_dataframe_asset("energy_timeseries")
    batch_definition = asset.add_batch_definition_whole_dataframe("full_batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    print("\n📋 Running expectations...")
    results = []

    expectations = [
        ("Timestamp not null", gx.expectations.ExpectColumnValuesToNotBeNull(column="timestamp")),
        ("Value 95% not null", gx.expectations.ExpectColumnValuesToNotBeNull(column="value", mostly=0.95)),
        ("Valid categories", gx.expectations.ExpectColumnValuesToBeInSet(column="category", value_set=["price", "generation", "consumption", "forecast"])),
        ("Region is DE", gx.expectations.ExpectColumnValuesToBeInSet(column="region", value_set=["DE"])),
        ("Resolution is hour", gx.expectations.ExpectColumnValuesToBeInSet(column="resolution", value_set=["hour"])),
        ("Valid filter IDs", gx.expectations.ExpectColumnValuesToBeInSet(column="filter_id", value_set=[4169, 4170, 4067, 4068, 1225, 410, 4359, 4071, 5097, 122])),
        ("Row count in range", gx.expectations.ExpectTableRowCountToBeBetween(min_value=1000, max_value=10000000)),
    ]

    for name, exp in expectations:
        result = batch.validate(exp)
        results.append((name, result.success))
        print(f"{'✅' if result.success else '❌'} {name}: {result.success}")

    passed = sum(1 for _, s in results if s)
    total = len(results)
    print(f"\n🎯 Results: {passed}/{total} expectations passed")
    print(f"Overall: {'✅ PASSED' if passed == total else '⚠️ SOME FAILED'}")

    return passed == total

if __name__ == "__main__":
    run_expectations()
