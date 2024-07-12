const data_table_lead='adat';
var selected_data=data_table_lead+"0"+"_0";

const user_table_lead='egyen';
var selected_user=user_table_lead+"0";
var edited_user=user_table_lead+"0";
var editing_user=false;

const selectcolor = "#007BFF";
const selectcolor_text = "white";
const highlightcolor = "#6C757D"; 	
const highlightcolor_text = "white"
const clearcolor='white';
const tableheadcolor="#343A40";
const tableheadcolor_text='white';
const textcolor = 'black';

//table class
//class 

class Table {
  constructor(id,css_style,values) {
    this.id = id;
	this.style = css_style;
	this.values = values;
	this.selected_row='';
	this.editing_row=false;
	this.currently_edited_row='';
	this.POST_ROUTE = '';
	this.dropdown=[];
	this.dropdown_list=[];
	this.highestID=0;
	
	this.CommitRowEdit=this.CommitRowEdit.bind(this);
	this.EditRow=this.EditRow.bind(this);
	this.AddRowEdit=this.AddRowEdit.bind(this);
	this.CancelAddRowEdit=this.CancelAddRowEdit.bind(this);
	this.DelRowData=this.DelRowData.bind(this);
	this.Visibility=this.Visibility.bind(this);
	this.NewRow=this.NewRow.bind(this);
}
	//---------------------------------------------------
	addCell(row,object,id)
	{
		const td = row.insertCell();
		td.id = id;
		
		td.innerHTML=String(object);
	}
	//---------------------------------------------------
	createTable(dropdown_values=[])
	{
		var THIS=this;
		
		//dropdown (ha nem üres az érték lista)
		if(dropdown_values.length!=0)
		{
			//felső div
			var upper_div=document.createElement("div");
			document.body.appendChild(upper_div);
			upper_div.align="center";
			upper_div.style.backgroundColor=tableheadcolor;
			
			this.dropdown=createDropdown('Látható oszlopok',dropdown_values);
			this.dropdown_list=this.dropdown.querySelectorAll("a");
			var dropdown_list=this.dropdown_list;
			for(let i=0;i<dropdown_list.length;i++)
			{
				dropdown_list[i].classList.toggle('active');
				const x=i;
				dropdown_list[i].addEventListener("click",function(e){
					e.stopPropagation();
					THIS.toggleColumn(x);
					//dropdown_list[i].classList.toggle('active');
				});
			}
			upper_div.appendChild(this.dropdown);
		}
		
		
		//div
		this.div_element = document.createElement("div");
		this.div_element.classList.add(this.style);

		//tb
		this.tb_element = document.createElement('table');
		this.tb_element.id = this.id;

		this.tb_element.style.cssText =  'overflow-y: auto;'+
							'width: 99vw;'+
							'margin-left: auto;'+
							'margin-right: auto;';

		this.tb_element.classList.add("table");

		//table head
		const first_row = this.tb_element.insertRow();
		for(let i = 0;i<this.values.length;i++)
		{
			this.addCell(first_row, this.values[i] );
		}
		first_row.classList.add("tableHead");
		first_row.style.backgroundColor=tableheadcolor;
		first_row.style.color=tableheadcolor_text;
		
		//text field row for filter
		const trt = this.tb_element.insertRow();
		for(let i = 0;i<this.values.length;i++)
		{
			var tf = document.createElement("INPUT");
			tf.setAttribute("type", "text");
			tf.style.border = 'px-solid';
			tf.id = "c"+this.values[i];
			tf.addEventListener("input",function(){
				filterUpdate(this);
			});
			const td = trt.insertCell();
			td.appendChild( tf );
		}

		this.div_element.appendChild(this.tb_element);
		document.body.appendChild(this.div_element);
	}
	//-------------------------------------------------------------
	toggleColumn(n)
	{
		if(n<0)
		{
			n=this.dropdown_list.length+n+1;
		}
		if(n=='all') //mindent aktivál
		{
			for(var i=0;i<this.dropdown_list.length;i++)
			{
				if(!(this.dropdown_list[i].classList[2]=='active')){this.toggleColumn(i);}
			}
		}
		else
		{
			for(var i=0, row; row = this.tb_element.rows[i];i++)
			{
				for(var k=0, cell; cell = row.cells[k];k++)
				{
					if(k==n)
					{
						if(cell.style.display!='none')cell.style.display='none';
						else cell.style.display='table-cell';
					}
				}
			}
			if(this.dropdown_list[n]!=null) this.dropdown_list[n].classList.toggle('active');
		}
	}
	//---------------------------------------------------------------
	appendData(data)
	{
		var values=[];
		for(var row=0;row<data[0].length;row++)
		{
			for(var cell=0;cell<data.length;cell++)
			{
				values[cell]=data[cell][row];
			}
			this.NewRow(values);
		}
	}
	//----------------------------------------------------------------
	NewRow(values)
	{
		const SELF=this;
		var row = this.tb_element.insertRow();
		
		//legnagyobb id frissítése
		if(values[values.length-1]>this.highestID) this.highestID=values[values.length-1];
		
		//sor id
		if(values[values.length-1]!=''){
			row.id=this.id+String(values[values.length-1]);}
		else{
			this.highestID++;
			row.id=this.id+String(this.highestID);
		}
		
		//event listeners
		row.addEventListener("mouseover", function(){
			if(SELF.selected_row!=this.id&&SELF.editing_row==false) ChangeColor(this,highlightcolor_text,highlightcolor);
		});
		
		row.addEventListener("mouseout", function(){
			if(SELF.selected_row!=this.id&&SELF.editing_row==false) ChangeColor(this,textcolor,clearcolor);
		});
		
		row.addEventListener("click", function(){
			if(!SELF.editing_row){
				SELF.SelectRow(this.id);
				//updateDataTable();
			}
		});
		
		row.addEventListener("dblclick", function(){
			if(!this.editing_row){
				SELF.EditRow(this.id);}
		});
		
		for(var k=0;k<user_values.length;k++)
		{
			this.addCell(row, values[k], 'c'+user_values[k]+String(row.id));
		}
		return row.id
	}
	//---------------------------------------------------------------
	SelectRow(id)
	{
		this.selected_row = id;
		//i=2 mert az első kettő igazi sor az a cím, és kereső mező
		for(var i = 2, row; row = this.tb_element.rows[i]; i++)
		{
			if(row.id!=id) ChangeColor(row,textcolor,clearcolor);
			else ChangeColor(row,selectcolor_text,selectcolor);
		}
	}
	//---------------------------------------------------------------
	DeleteRow(id)
	{
		console.log(id);
		var row=document.getElementById(id);
		var i=row.rowIndex;
		this.tb_element.deleteRow(i);
	}
	//---------------------------------------------------------------
	EditRow(id)
	{
		this.editing_row=true;
		setUI('edit');
		
		for(var i = 1, row; row = this.tb_element.rows[i]; i++)
		{
			ChangeColor(row,textcolor,clearcolor);
			if(row.id==id)
			{
				for(var k = 0, cell; cell = row.cells[k];k++)
				{
					Text=cell.innerHTML;
					cell.innerHTML="";
					
					var TextInput = document.createElement("INPUT");
					TextInput.id = cell.id+'textinput';
					TextInput.setAttribute("type", "text");
					TextInput.style.textAlign="center";
					TextInput.style.backgroundColor='transparent';
					TextInput.value=Text;
					
					cell.appendChild(TextInput);
					
				}
			}
		}
		this.currently_edited_row=id;
	}
	//-----------------------------------------------------------------
	CommitRowEdit()
	{
		var buffer=[];
		console.log(this.currently_edited_row);
		var row=document.getElementById(this.currently_edited_row);
		for(var i=0,cell; cell = row.cells[i];i++)
		{
			var TextInput=document.getElementById(cell.id+'textinput');
			cell.innerHTML=TextInput.value;
			buffer[i]=TextInput.value;
		}
		//reset interface
		this.editing_row=false;
		setUI('main');
		
		//this.updateTable();
		this.SelectRow(this.currently_edited_row);
		//filter = filterTable(usertable,2,user_values);
		//updateUserTable(filter=filter);
		//send the data
		
		var ID=parseInt(this.currently_edited_row.replace(this.id,''));
		fetch(this.POST_ROUTE, {
			method: "POST",
			body: JSON.stringify({ userId:ID,
									data:buffer}),
		  });
		  
	}
	//---------------------------------------------------------------
	DelRowData(id)
	{
		var USERID=parseInt(id.replace(this.id,''));
		
		fetch("/del-user", {
			method: "POST",
			body: JSON.stringify({ userId:USERID }), });
		
		this.DeleteRow(id);
		this.SelectRow(this.id+"0");
		if(USERID == this.highestID) this.highestID-=1;
	}
	//---------------------------------------------------------------
	AddRowEdit()
	{
		this.toggleColumn('all');
		this.selected_row=this.NewRow(new Array(this.values.length+1).fill('',0,this.values.length+1));
		this.EditRow(this.selected_row);
		setUI('add');
		
		this.div_element.scrollTo({
			  top: this.div_element.scrollHeight,
			  behavior: "smooth"
			});
		
	}
	//----------------------------------------------------------------
	CancelAddRowEdit()
	{
		this.DeleteRow(this.selected_row);
		this.selected_row=this.id+"0";
		this.editing_row=false;
		setUI('main');
	}
	//----------------------------------------------------------------
	Visibility(filter=new Array(this.tb_element.rows.length).fill('table-row',0,this.tb_element.rows.length))
	{
		for(var i = 2, row; row = this.tb_element.rows[i]; i++)
		{
			if(filter[i]=='table-row') row.style.display='table-row';
			else row.style.display='none';
		}
	}
	
}

//-------- user, and data specific functions ----------

function SelectData(id)
{
	for(var i = 2, row; row = datatable.rows[i]; i++)
	{
		ChangeColor(row,textcolor,clearcolor);
	}
	
	selected_data = id;
}

function updateDataTable(filter=new Array(datatable.rows.length).fill('table-row',0,datatable.rows.length))
{
	userid = selected_user.replace(user_table_lead,'');
	for(var i = 2, row; row = datatable.rows[i]; i++)
	{
		if(row.id.split('_')[1] == userid && filter[i]=='table-row') row.style.display='table-row';
		else row.style.display='none';
	}
}

//-------- non specific functions ----------

function ChangeColor(object, textcolor ,bgcolor)
{
	object.style.backgroundColor = bgcolor;
	object.style.color = textcolor;
}

function match_lead(str1,str2)
{
	var x = str1; //x filter
	var y = str2; //y match
	y=y.slice(0, x.length);
	if(x==y) return true;
	else return false;
}

function filterTable(tb,start,values)
{
	match_list=[];
	filter=[];
	for(let i = start, row;row = tb.rows[i]; i++)
	{match_list[i]=0;}
	for(let k=0;k<values.length;k++)
	{
		var current_filter = document.getElementById("c"+values[k]);
		for(let i = start, row;row = tb.rows[i]; i++)
		{
			var cell = row.cells[k];
			if(!match_lead(current_filter.value,String(cell.innerHTML)) ) filter[i] = 'none';
			else match_list[i]+=1;
		}
	}
	for(let i = start, row;row = tb.rows[i]; i++)
	{
		if(match_list[i]==values.length){
			filter[i] = 'table-row';
		}
	}
	return filter;
}

function filterUpdate(tf)
{
	var filter_name = tf.id.slice(1,tf.id.length);
	var filter;
	if(user_values.includes(filter_name)) //egyén tábla filterezés
	{
		filter = filterTable(usertable,2,user_values);
		updateUserTable(filter=filter);
	}
	else if (data_values.includes(filter_name)) //adatok tábla filterezés
	{
		filter = filterTable(datatable,2,data_values);
		updateDataTable(filter=filter);
	}
	
}

function createButton(label,func=null,DIV=null,classes=['btn','btn-secondary'])
{
	if(DIV!=null) Div=DIV;
	else{
		Div = document.createElement("div");
		Div.classList.add("inlineDiv");
		//Div.classList.add("form-group");
		document.body.appendChild(Div);}

	let btn = document.createElement("button");
	btn.innerHTML = label;
	for(var i=0;i<classes.length;i++) {btn.classList.add(classes[i]);}
	if(func!=null){
		btn.addEventListener("click",function(){
			func();
		});}
	Div.appendChild(btn);
	return btn;
}

function createDropdown(label,values)
{
	Div = document.createElement("div");
	Div.classList.add("dropdown");
	document.body.appendChild(Div);
	
	btn=createButton(label=label,null,Div,['btn','btn-outline-light','dropdown-toggle']);
	btn.setAttribute("data-toggle","dropdown");
	btn.setAttribute("aria-haspopup","true");
	btn.setAttribute("aria-expanded","false");
	btn.setAttribute("data-bs-auto-close","outside");
	btn.id='dropdownMenuButton';
	
	Div_menu=document.createElement("div");
	Div_menu.classList.add("dropdown-menu");
	Div_menu.setAttribute("aria-labelledby","dropdownMenuButton");
	Div.appendChild(Div_menu);
	
	for(var i=0;i<values.length;i++)
	{
		var a=document.createElement("a");
		a.classList.add("dropdown-item");
		a.classList.add("noselect");
		a.innerHTML=values[i];		
		Div_menu.appendChild(a);
	}
	
	return Div;
}

function setModal(title,body,f_primary,f_secondary)
{
	modalTitle=document.getElementById("MODAL-TITLE");
	modalTitle.innerHTML=title;
	
	modalBody=document.getElementById("MODAL-BODY");
	modalBody.innerHTML=body;

	primary_button=document.getElementById("MODAL-PRIMARY");
	primary_button.addEventListener("click",f_primary);

	secondary_button=document.getElementById("MODAL-SECONDARY");
	secondary_button.addEventListener("click",f_secondary);
}

function showModal()
{
	modal=document.getElementById("MODAL");
	modal.style.display="initial";
}

function closeModal()
{
	modal=document.getElementById("MODAL");
	modal.style.display="none";
}