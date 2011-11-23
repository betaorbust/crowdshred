function loadNewPieces(){
// Ask the server for a new set of pieces
    // Remove board content
    $('#board').empty();    
	$.getJSON(jsonLocation,jsonRequestParams,
        function(data){ 	
            // blank everything
            pieces = {};
            id_hash = '';
            
            // get the hash
            id_hash = data.pair;
            // build the pieces
            $.each(data.images, function(i, image){
                var pname = "piece"+i;
                pieces[pname] = {
                    id:image.id,
                    jsid:pname,
                    src:image.src,
                    locx:0,
                    locy:0,
                    rot:0,
                    width:0,
                    height:0
                };

                var img = $("<img/>").attr({"src":image.src, "class":"imagepiece","id":pname})
                    .load(function(){
                        if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                             alert('broken image!');
                         } else {
                            // append to the dom
                            $("#board").append(img);
                            
							//draggable time!
                            $('#'+pname).draggable({ 
								containment: "parent",
								start: function(event, ui){
									myid = ui.helper.context.id;
									var pos = $('#'+myid).offset()
									startLoc=[pos.left,pos.top];
									if(consoleDebugging){console.log(myid+' started dragging at '+startLoc);}
								},
								stop: function(event, ui){
									myid = ui.helper.context.id;
									var pos = $('#'+myid).offset();
									endLoc=[pos.left,pos.top];
									
									// update the actual position.
									pieces[myid].locx = pieces[myid].locx+endLoc[0]-startLoc[0];
									pieces[myid].locy = pieces[myid].locy+endLoc[1]-startLoc[1];
									if(consoleDebugging){
										console.log(myid+' stopped dragging at '+endLoc);
										console.log('for a total change of x:'+(endLoc[0]-startLoc[0])+', y:'+(endLoc[1]-startLoc[1]));
										console.log('The new location for '+myid+' is x:'+pieces[myid].locx+' y:'+pieces[myid].locy);
									}
								}
							});
							
                            // get the INSANE location data etc. Browser rotation dimension incompatibiliy, thy name is hatred. 
                            pieces[pname].width=$('#'+pname).width();
                            pieces[pname].height=$('#'+pname).height();
                            var pos = $('#'+pname).offset();
                            pieces[pname].locx=pos.left+0.5*pieces[pname].width;
                            pieces[pname].locy=pos.top+0.5*pieces[pname].height;
							if(consoleDebugging){
								console.log('Starting position for '+pname+' is x: '+pieces[pname].locx+', y:'+pieces[pname].locy);
                            }		
                        } 
                });
            });
			if(consoleDebugging){    
				console.log(pieces);
			}
        });
}

// submit a vote via AJAX
function submitVote(hash, vote, delx, dely, r0, r1){
    // oh look! I did this already! Go me!
    var voteParams = {
        hash_id:hash,
        state:vote,
        dx:delx,
        dy:dely,
        rot0:r0,
        rot1:r1
    };
    
    $.getJSON(jsonVoteLocation,voteParams, function(data){
        if(data.message = "Accepted"){
            console.log('Successfully submitted!');
            //alert('Successfully submitted!');
        }else{
            console.log('Successfully submitted!');
            //alert('Vote failed!');
        }
    });
    // TODO: add deltas and rotations to vote
    // TODO: add POST instead of GET
}


// Allows the detection of browser information to let us whitelist the user agents
BrowserDetect = {
	init: function () {
		this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
		this.version = this.searchVersion(navigator.userAgent)
			|| this.searchVersion(navigator.appVersion)
			|| "an unknown version";
		this.OS = this.searchString(this.dataOS) || "an unknown OS";
	},
	searchString: function (data) {
		for (var i=0;i<data.length;i++)	{
			var dataString = data[i].string;
			var dataProp = data[i].prop;
			this.versionSearchString = data[i].versionSearch || data[i].identity;
			if (dataString) {
				if (dataString.indexOf(data[i].subString) != -1)
					return data[i].identity;
			}
			else if (dataProp)
				return data[i].identity;
		}
	},
	searchVersion: function (dataString) {
		var index = dataString.indexOf(this.versionSearchString);
		if (index == -1) return;
		return parseFloat(dataString.substring(index+this.versionSearchString.length+1));
	},
	dataBrowser: [
		{
			string: navigator.userAgent,
			subString: "Chrome",
			identity: "Chrome"
		},
		{ 	string: navigator.userAgent,
			subString: "OmniWeb",
			versionSearch: "OmniWeb/",
			identity: "OmniWeb"
		},
		{
			string: navigator.vendor,
			subString: "Apple",
			identity: "Safari",
			versionSearch: "Version"
		},
		{
			prop: window.opera,
			identity: "Opera",
			versionSearch: "Version"
		},
		{
			string: navigator.vendor,
			subString: "iCab",
			identity: "iCab"
		},
		{
			string: navigator.vendor,
			subString: "KDE",
			identity: "Konqueror"
		},
		{
			string: navigator.userAgent,
			subString: "Firefox",
			identity: "Firefox"
		},
		{
			string: navigator.vendor,
			subString: "Camino",
			identity: "Camino"
		},
		{		// for newer Netscapes (6+)
			string: navigator.userAgent,
			subString: "Netscape",
			identity: "Netscape"
		},
		{
			string: navigator.userAgent,
			subString: "MSIE",
			identity: "Explorer",
			versionSearch: "MSIE"
		},
		{
			string: navigator.userAgent,
			subString: "Gecko",
			identity: "Mozilla",
			versionSearch: "rv"
		},
		{ 		// for older Netscapes (4-)
			string: navigator.userAgent,
			subString: "Mozilla",
			identity: "Netscape",
			versionSearch: "Mozilla"
		}
	],
	dataOS : [
		{
			string: navigator.platform,
			subString: "Win",
			identity: "Windows"
		},
		{
			string: navigator.platform,
			subString: "Mac",
			identity: "Mac"
		},
		{
			   string: navigator.userAgent,
			   subString: "iPhone",
			   identity: "iPhone/iPod"
	    },
		{
			string: navigator.platform,
			subString: "Linux",
			identity: "Linux"
		}
	]

};
BrowserDetect.init();
