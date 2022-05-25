program matrix;
var
    row1, col1, row2, col2: integer;
    A, B: array [1..30,1..30] of integer;
    C: array [1..30,1..30] of integer;
    i, j, k: integer;

begin
    read(row1);
    read(col1);
    for i := 1 to row1  do
    begin
        for j := 1 to col1  do
            read(A[i,j]);
    end;

    read(row2);
    read(col2);
    for i := 1 to row2  do
    begin
        for j := 1 to col2  do
            read(B[i,j]);        
    end;

    if col1 <> row2 then
        writeln
    else
    begin
        for i := 1 to row1 do
        begin
            for j := 1 to col2 do
                C[i,j] := 0;
        end;
        for i := 1 to row1 do
        begin
            for j := 1 to col2 do
                for k := 1 to row2 do
                    C[i,j] := C[i,j] + A[i,k] * B[k,j];
        end;

        for i := 1 to row1 do
        begin
            for j := 1 to col2 do
                write(C[i,j]);
            writeln;
        end;
    end;
end.