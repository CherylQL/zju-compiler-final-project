program TestCase1;
var
    x : integer;

function f(b : integer): integer;
var
    i : integer;
    tmp : integer;
begin
    tmp := 1;
    for i := 1 to b do
        tmp := tmp * i;
    f := tmp;
end;

begin
    x := f (3);
    write(x);
end.
