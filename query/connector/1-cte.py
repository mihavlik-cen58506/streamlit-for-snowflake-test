import _utils

conn = _utils.getConnection()

# get managers with projected 10% raise of avg per dept
query = """
with q1 as (
    select department, floor(avg(salary)) as avg_sal
    from employees
    group by department)
-- q1 is a temporary table that contains the average salary for each department for later use in the main query

select e.department, e.employee_name, e.salary,
   e.salary + (0.1 * q1.avg_sal) as new_sal
from employees e -- employees table alias is e
    join q1 on q1.department = e.department
where e.job = 'MANAGER'
order by e.department, e.employee_name;

"""
cur = conn.cursor()
cur.execute(query)
df = cur.fetch_pandas_all()
print(df)
