program TestCase2;
var
    x : integer;

function f(b : integer): integer;
var
    tmp : integer;
begin
    if b > 0 then tmp := b
    else begin
        tmp := 0 - b;
    end;
    f := tmp;
end;

begin
    x := f (100);
    write(x);
end.