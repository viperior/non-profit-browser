-- Create a 7-day moving average using the return_header_timestamp
-- Count the number of filings per day and compute a moving 7-day average
-- Output a table of dates, the # of filings on that date, and the 7-day SMA as of that date
select
	a.return_file_date,
	doc_count,
	round(
		avg(a.doc_count) over (
			order by a.return_file_date 
			rows between 6 preceding and current row
		),
		2
	)
	as seven_day_sma
from (
	select
		date(return_header_timestamp at time zone 'utc') as return_file_date,
		count(form_id) as doc_count
	from form
	group by return_file_date
) as a
;
