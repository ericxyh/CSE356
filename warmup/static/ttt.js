var t = document.getElementById('ttt');
var winner = false;

var tClick = function(n){
	return function(){
		if (! winner){
			var box = t.rows[(n-n%3)/3].cells[n%3];
			if ( box.innerHTML!= 'X' && box.innerHTML!= 'O'){
				box.innerHTML = 'X';
				var g = Array(9);
				for (var i=0; i<3; i++){
					for (var j=0; j<3; j++){
						g[i*3+j] = t.rows[i].cells[j].innerHTML;
					}
				}
				var xml = new XMLHttpRequest();
				xml.open("POST", "/ttt/play");
				xml.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
				xml.onreadystatechange = function() {
					if (this.readyState == 4 && this.status == 200){
						var gr = JSON.parse(this.responseText);
						var gri = gr['grid']
						for (var i = 0; i < 3; i++) {
							for (var j = 0; j < 3; j++) {
								t.rows[i].cells[j].innerHTML = gri[i*3+j];
							}
						}
						if (gr['winner'] != ' '){
							document.getElementById("win").innerHTML = gr['winner'];
							winner = true;
						}
					}
				}
				xml.send(JSON.stringify({'grid':g}));
				//make json
			}
		}
	}
}

for (var i=0; i<t.rows.length; i++){
	for (var j=0; j<t.rows[i].cells.length; j++){
		t.rows[i].cells[j].addEventListener('click',tClick(i*3+j));
	}
}

