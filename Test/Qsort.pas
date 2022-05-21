program Qsort;
var
    n : integer;
    i : integer;
    a : array [1..100] of integer;
    x : integer;
procedure qsort(l,r:integer);
var
    i,j,m,t:integer;
begin
    i:=l;
    j:=r;
    t := (l+r) / 2;
    repeat
        while a[i]<a[t] do i:=i+1;
	    while a[j]>a[t] do j:=j-1;

	if not(i>j) then
	begin
	    t:=a[i];
	    a[i]:=a[j];
 	    a[j]:=t;
	    i:=i+1;
	    j:=j-1;
	end;
    until i>j;
    if l<j then qsort(l,j);
    if i<r then qsort(i,r);
end;
	
begin
    read(n);
    for i := 1 to n do
        begin
            read(x);
            a[i] := x;
        end;
    qsort(1,n);
    for i := 1 to n do
        write(a[i]);
end.