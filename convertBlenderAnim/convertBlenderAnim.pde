String fileName = "timeCurve.csv";
Table table = loadTable(fileName,"header");

int numRows = table.getRowCount();

for(int i = 0; i < numRows; i++){
    TableRow theRow = table.getRow(i);
    int t = theRow.getInt("time");
    t = int(float(t)/46000000);  //this divisor is not quite right.  check the perl script I eventually used as it has what I believe is the right number.
    theRow.setInt("time", t);
}
saveTable(table, fileName);
