class GestureRecorder{
    Table table;
    
    int rowNum = 0;
    int numRows;
    
    TableRow theRow;
    String fileName;
    
    int sTime = 0;
    
    GestureRecorder(String iFileName){
	fileName = iFileName;
	table = new Table();
	
	table.addColumn("time");
	table.addColumn("value");
    }

    void clear(){
	table.clearRows();
	saveTable(table, fileName);
	rowNum = 0;
    }

    void addPosition(float position){
	if(rowNum++ == 0)
	    sTime = millis();
	theRow = table.addRow();
	theRow.setInt("time", millis() - sTime);
	theRow.setFloat("value", position);
	saveTable(table, fileName);
    }
}

