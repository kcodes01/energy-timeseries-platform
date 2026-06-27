with source as (
    select * from {{ source('raw_energy', 'energy_timeseries') }}
),

cleaned as (
    select
        timestamp,
        filter_id,
        filter_name,
        value,
        unit,
        category,
        region,
        resolution,
        ingested_at,
        -- derived columns
        toDate(timestamp)           as date,
        toHour(timestamp)           as hour_of_day,
        toDayOfWeek(timestamp)      as day_of_week,
        toMonth(timestamp)          as month,
        toYear(timestamp)           as year
    from source
    where value is not null
)

select * from cleaned
