program Matrix;
var
    m1 : integer;
    n1 : integer;
    a : [0..100,0..100] of integer;
    m2 : integer;
    n2 : integer;
    b : [0..100,0..100] of integer;
    i,j,k,s : integer;
    c : [0..100,0..100] of integer;
begin
    read(m1);
    read(n1);
    for i:=1 to m1 do
        for j:=1 to n1 do
            read(a[i,j]);
    read(m2);
    read(n2);
    for i:=1 to m2 do
        for j:=1 to n2 do
            read(b[i,j]);

    if n1=m2 then
    begin
        for i:=1 to m1 do
            for j:=1 to n2 do
            begin 
                s:=0; 
                for k:=1 to n1 do 
                    s:=s+a[i,k]*b[k,j];
                c[i,j]:=s;
            end;

        for i:=1 to m1 do
            for j:=1 to n2 do
                write(c[i,j]:4);
            writeln;
    end;
    else writeln('Incompatible Dimensions');
end.