with sales as (
	select
	*
	from {{ ref("stg__sales") }} as sales
)

select
	store_id,
	dept_id,
	date,
	weekly_sales,
	isholiday
from sales