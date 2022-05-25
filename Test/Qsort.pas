program Qsort;
var
    n : integer;
    k : integer;
    a : array [1..10000] of integer;
    x : integer;
procedure qsort(l,r:integer);
var
    i,j,m,t:integer;
begin
    i:=l;
    j:=r;
    t := (l+r) / 2;
    while i < j do
    begin
        m := a[t];
        while a[i]<m do i:=i+1;
	    while a[j]>m do j:=j-1;

        if i < j then
        begin
            t:=a[i];
            a[i]:=a[j];
            a[j]:=t;
            i:=i+1;
            j:=j-1;
        end;

    end;
    if l<j then qsort(l,j);
    if i<r then qsort(i,r);
end;
	
begin
    read(n);
    for k := 1 to n do
    begin
        read(a[k]);
    end;
    qsort(1,n);
    for k := 1 to n do
        write(a[k]);
end.