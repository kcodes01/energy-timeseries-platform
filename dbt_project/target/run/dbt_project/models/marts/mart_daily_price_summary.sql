
  
    
    
    
        
        insert into `energy_marts_marts`.`mart_daily_price_summary__dbt_backup`
        ("date", "avg_price_eur_mwh", "min_price_eur_mwh", "max_price_eur_mwh", "price_volatility", "negative_price_hours", "high_price_hours", "total_hours")with prices as (
    select * from `energy_marts_staging`.`stg_energy_timeseries`
    where category = 'price'
    and filter_id = 4169
)

select
    date,
    round(avg(value), 2)            as avg_price_eur_mwh,
    round(min(value), 2)            as min_price_eur_mwh,
    round(max(value), 2)            as max_price_eur_mwh,
    round(stddevPop(value), 2)      as price_volatility,
    countIf(value < 0)              as negative_price_hours,
    countIf(value > 100)            as high_price_hours,
    count(*)                        as total_hours
from prices
group by date
order by date desc
  