program TestCase3;
var
    x : integer;

function f(b : integer): integer;
var
    arr : array [1..10] of integer;
begin
    for i := 1 to 10 do
        arr[i] := i;

    f := arr[b];
end;

begin
    x := f (6);
    write(x);
end.