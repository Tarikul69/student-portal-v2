const displayresult=document.getElementById("Standard_result");
let temp="",answer=0;
function display(symbol,name)
{
	if(answer!=0 && name!=="number"){
		temp+=(answer+symbol);
	}
	else{
	temp+=symbol;
	}
	answer=0;
	displayresult.value=temp;
	
}
function backspace()
{
	temp=temp.substring(0,temp.length-1);
	displayresult.value=temp;

}
function clearAll()
{
	displayresult.value="0";
	temp="";
}
function result()
{

	try{
		displayresult.value=eval(displayresult.value);
		answer=displayresult.value;
	}
	catch(err){
		alert("Syntax Error");
		displayresult.value="0";
	}
	finally{
		temp="";
	}

}
function negative(){
	try{
		//temp=-eval(temp);
		displayresult.value=-eval(displayresult.value);
		answer=displayresult.value;
	}
	catch(err){
		alert("Syntax Error");
		displayresult.value="0";
	}
	finally{
		temp="";
	}
}

const displayresult_s=document.getElementById("Scientific_result");
let temp_s="",answer_s=0;
function display_s(symbol,name)
{
	if(answer_s!=0 && name!=="number" && name!=="log" && name!=="ln" && name!="sin" && name!=="cos" && name!=="tan" && name!=="root"){
		temp_s+=(answer_s+symbol);
	}
	else{
	temp_s+=symbol;
	}
	answer_s=0;
	displayresult_s.value=temp_s;
	
}
function backspace_s()
{
	temp_s=temp_s.substring(0,temp_s.length-1);
	displayresult_s.value=temp_s;

}
function clearALL_s()
{
	displayresult_s.value="0";
	temp_s="";
	answer_s=0;
}
function calculate_s()
{
	temp_s=temp_s.replace("sin","Math.sin");
	temp_s=temp_s.replace("cos","Math.cos");
	temp_s=temp_s.replace("tan","Math.tan");
	temp_s=temp_s.replace("log","Math.log10");
	temp_s=temp_s.replace("ln","Math.log");
	temp_s=temp_s.replace("exp","Math.exp");
	temp_s=temp_s.replace("sqrt","Math.sqrt");
	temp_s=temp_s.replace("PI","Math.PI");

	var i,j;
	for(j=0;j<temp_s.length;j++){
		if(temp_s.charAt(j)==="^"){
			var operand1="",operand2="",pos1,pos2;

			var index=temp_s.indexOf("^");
			if(temp_s.charAt(index-1)===")"){
				for(i=index-2;i>=-1;i--)
				{
					if(temp_s.charAt(i)==="(")
					{
						pos1=i;
						operand1=eval(temp_s.slice(i,index));
						break;
					}
				}
			}
			else{
				for(i=index-1;i>=-1;i--){
					if(!(/^[0-9]$/.test(temp_s.charAt(i)))){
						pos1=i+1;
						operand1=temp_s.slice(i+1,index);
						break;
					}
				}
			}
			if(temp_s.charAt(index+1)==="("){
				for(i=index+2;i<=temp_s.length;i++)
				{
					if(temp_s.charAt(i)===")")
					{
						pos2=i;
						operand2=eval(temp_s.slice(index+1,i+1));
						break;
					}
				}
			}
			else{
				for(i=index+1;i<=temp_s.length;i++){
					if(!(/^[0-9]$/.test(temp_s.charAt(i)))){
						pos2=i-1;
						operand2=temp_s.slice(index+1,i);
						break;
					}
				}
			}
			temp_s=temp_s.replace(temp_s.substring(pos1,pos2+1),"Math.pow("+operand1+","+operand2+")");

		}
	}
	for(j=0;j<temp_s.length;j++){
		if(temp_s.charAt(j)==="!")
		{
			var operand1;
			var index=temp_s.indexOf("!");
			if(temp_s.charAt(index-1)===")"){
				for(i=index-2;i>=-1;i--)
				{
					if(temp_s.charAt(i)==="(")
					{
						pos1=i;
						operand1=eval(temp_s.slice(i,index));
						break;
					}
				}
			}
			else{
				for(i=index-1;i>=-1;i--){
					if(!(/^[0-9]$/.test(temp_s.charAt(i)))){
						pos1=i+1;
						operand1=temp_s.slice(i+1,index);
						break;
					}
				}
			}
			var f=Number(operand1);
			var k,factorial=1;
			for(k=1;k<=f;k++)
			{
				factorial=factorial*k;
			}
			temp_s=temp_s.replace(temp_s.substring(pos1,index+1),factorial);

		}
	}
	try{
		displayresult_s.value=eval(temp_s);
		answer_s=displayresult_s.value;
	}
	catch(err){
		alert("Syntax Error");
		displayresult_s.value="0";
	}
	finally{
		temp_s="";
	}

}
function negative_s(){

	try{
		//temp=-eval(temp);
		displayresult_s.value=-eval(displayresult_s.value);
		answer_s=displayresult_s.value;
	}
	catch(err){
		alert("Syntax Error");
		displayresult_s.value="0";
	}
	finally{
		temp_s="";
	}
}
function percentage()
{


	try{
		displayresult_s.value=eval(displayresult_s.value)*0.01;
		answer_s=displayresult_s.value;
	}
	catch(err){
		alert("Syntax Error");
		displayresult_s.value="0";
	}
	finally{
		temp_s="";
	
	}
}
