program TestCase4;
var
    x : integer;

function f(b : integer): integer;
begin
    if b < 1 then f := 1
    else begin
        f := b * f (b - 1);
    end;
end;

begin
    x := f (6);
    write(x);
end.