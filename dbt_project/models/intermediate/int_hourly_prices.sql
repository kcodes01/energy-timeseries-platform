with prices as (
    select * from {{ ref('stg_energy_timeseries') }}
    where category = 'price'
    and filter_id = 4169  -- Germany/Luxembourg
)

select
    date,
    hour_of_day,
    avg(value)          as avg_price_eur_mwh,
    min(value)          as min_price_eur_mwh,
    max(value)          as max_price_eur_mwh,
    count(*)            as data_points
from prices
group by date, hour_of_day
order by date, hour_of_day
