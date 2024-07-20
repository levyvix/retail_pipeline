with sales as (
	select *
	from {{ ref("int__sales") }} as sales
),
stores as (
	select *
	from {{ ref("dim_stores") }} as stores
),
datetime as (
	select *
	from {{ ref("dim_datetime") }} as datetime
)


select
	{{ dbt_utils.generate_surrogate_key(['stores.store_id', 'datetime.date_id']) }} as sales_id,
	stores.store_id,
	datetime.date_id,

	sales.weekly_sales

from sales
left join stores on sales.store_id = stores.store_id
left join datetime on sales.date = datetime.date