-- prvni cast mi dela odskoceni o 3 mezery kdyz se zanori do dalsi urovne
-- druha cast mi vytvori cestu k danemu zamestnanci od rootu retezene teckami
-- vysledek serazim podle cesty, aby byla hierarchie videt pod kazdym zamestnancem od managera az k nemu
-- connect by prior mi tvori strom zamestnancu, kde se zanoruje podle managera s tim ze hiearchie zacne u tech co nemaji managera
select repeat ('   ', level - 1) || employee_name as name, ltrim(sys_connect_by_path(employee_name, '.'), '.') as path
from employees
start with manager_name is null
connect by prior employee_name = manager_name
order by path

-- $1 is column in the first position, $2 is column in the second position
select repeat ('   ', level - 1) || $1 as name, ltrim(sys_connect_by_path($1, '.'), '.') as path
from employees
start with $2 is null
connect by prior $1 = $2
order by path

-- just to make it very generic
-- child_index is the column that is the child in the hierarchy, parent_index is the column that is the parent in the hierarchy, in this case we are selecting them from the select box
child_index, parent_index = cols.index(child) + 1, cols.index(parent) + 1

select repeat ('   ', level - 1) || ${child_index} as name,
    trim(sys_connect_by_path(${child_index}, '.'), '.') as path
from {tableName}
start with ${parent_index} is null
connect by prior ${child_index} = ${parent_index}
order by path