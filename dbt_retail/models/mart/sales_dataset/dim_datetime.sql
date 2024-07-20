with sales as (
	select *
	from {{ ref("int__sales")}}
),
distinct_dates as (
	select 
		distinct date,
		isholiday
	from sales
)

select 
{{ dbt_utils.generate_surrogate_key(['date']) }} as date_id,
date,
isholiday,
CAST(date as datetime) AS datetime,
extract(day  from date) as day,
extract(month from date) as month,
extract(year from date) as year
from distinct_dates