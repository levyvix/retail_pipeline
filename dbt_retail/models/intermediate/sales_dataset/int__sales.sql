with sales as (
	select
	*
	from {{ ref("stg__sales") }} as sales
)

select
	store
	dept
	date
	weekly_sales
	isholiday
from sales