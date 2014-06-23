class GesturePlayer{
    int cTime, sTime;
    float position;
    
    Table table;
    
    int rowNum;
    int numRows;
    
    TableRow theRow;

    boolean backAtZero;
    
    GesturePlayer(String fileName){
	init(fileName);
    }

    void init(String fileName){
	rowNum = 0;
	backAtZero = false;
	table = loadTable(fileName,"header");
	numRows = table.getRowCount();
	theRow = table.getRow(rowNum);
	cTime = theRow.getInt("time");
	sTime = millis();
	position = theRow.getFloat("value");     
    }
    
    boolean update(float iTime){
	if(backAtZero)
	    sTime = millis();

	backAtZero = false;

	if(iTime - sTime >= cTime){
	    rowNum++;
	    if(rowNum >= numRows){
		rowNum = 0;
		backAtZero = true;
	    }
	    
	    theRow = table.getRow(rowNum);
	    cTime = theRow.getInt("time");
	    position = theRow.getFloat("value");     
	} 
	return backAtZero;
    }
    
    int getTime(){
	return cTime;
    }
    
    float getPosition(){
	return position;
    }
}