### some useful sql code exercise
1. find medium number
```sql
select id, company, salary (
	select id, company, salary
	row_number() over*(partition by campany order by salary) as rank1;
	count(id) over(partition by company) as counts 
	from employee) T 
where rank1 between counts / 2.0 and count / 2.0 + 1
order by 2, 3
```


2. generate full list of date
```sql
with cte as (
	select cast(getdate() as date) as dim_date
	union all 
	select dateadd(day, -1, dim_date) from cte 
	where dim_date >= (day, -30, getdate())
)
select * from cte 

-- mysql
with recursive cte (dim_date) as 
(
	select date(now()) as dim_date 
	union all 
	select dim_date + inerval - 1 day from cte 
	where dim_date + interval - 1 day >=  date(now()) + interval - 30 day 
)
select * from cte

-- postgres 
with recursive cte (dim_date) as 
(
	select date(now()) as dim_date 
	union all 
	select dim_date - 1 from cte 
	where dim_date - 1 >=  date(now()) - 30 
)
select * from cte
```