/*
 running average of the most recent 4 weeks of sales in which flag was FALSE. The average is actually a baseline, so it does not include the current week's sales.

week    flag    sales
1       FALSE   3
2       FALSE   1
3       FALSE   3
4       FALSE   0
5       FALSE   3
6       FALSE   6
7       TRUE    3
8       TRUE    1
9       FALSE   3
10      FALSE   9
11      FALSE   6
12      FALSE   4
13      TRUE    4
14      TRUE    2
15      FALSE   1


-- result
week    avg
1       NULL
2       NULL
3       NULL
4       NULL
5       1.75
6       1.75
7       3
8       3
9       3
10      3
11      5.25
12      6
13      5.5
14      5.5
15      5.5
 */


#standardSQL
SELECT week,
  (SELECT IF(COUNT(1) = 4, AVG(sales), NULL) 
    FROM (
      SELECT sales FROM UNNEST(arr) WHERE NOT flag ORDER BY week DESC LIMIT 4
    ) 
  )
FROM (
  SELECT week, ARRAY_AGG(STRUCT(week, flag, sales)) OVER(win) arr
  FROM `project.dataset.table` 
  WINDOW win AS (ORDER BY week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)
)
-- ORDER BY week 