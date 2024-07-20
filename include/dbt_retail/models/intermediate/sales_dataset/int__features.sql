with features as (
	select *
	from {{ ref("stg__features") }}

),
remove_nulls as (
	select
		store_id,
		date,
		temperature,
		fuel_price,
		case when markdown1 = 'NA' then null else cast(markdown1 as float64) end as markdown1,
		case when markdown2 = 'NA' then null else cast(markdown2 as float64) end as markdown2,
		case when markdown3 = 'NA' then null else cast(markdown3 as float64) end as markdown3,
		case when markdown4 = 'NA' then null else cast(markdown4 as float64) end as markdown4,
		case when markdown5 = 'NA' then null else cast(markdown5 as float64) end as markdown5,
		case when cpi = 'NA' then null else cast(cpi as float64) end as cpi,
		case when unemployment = 'NA' then null else cast(unemployment as float64) end as unemployment,
		isholiday
	from features
)

select *
from remove_nulls