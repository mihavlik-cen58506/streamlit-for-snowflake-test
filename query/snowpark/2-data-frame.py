import _utils
from snowflake.snowpark.functions import call_function, col

session = _utils.getSession()


avgSales = (
    session.table("EMPLOYEES")
    .select("DEPARTMENT", "SALARY")
    .group_by("DEPARTMENT")
    .agg({"SALARY": "avg"})
    .select("DEPARTMENT", call_function("floor", col("AVG(SALARY)")).alias("AVG_SAL"))
    .sort("DEPARTMENT")
)

# avgSales.show()

managers = (
    session.table("EMPLOYEES")
    .select("DEPARTMENT", "EMPLOYEE_NAME", "SALARY")
    .filter(col("JOB") == "MANAGER")
    .sort("EMPLOYEE_NAME", "DEPARTMENT")
)

# # you will get an array of rows (row objects)
# print(managers.collect())
# # you will get a dataframe
# managers.show()

(
    managers.join(avgSales, managers.department == avgSales.department)
    .select(  # joined on department
        managers.department.alias("DEPARTMENT"),
        managers.employee_name,
        managers.salary,
        (managers.salary + (0.1 * col("AVG_SAL"))).alias("NEW_SAL"),
    )
    .show()
)
