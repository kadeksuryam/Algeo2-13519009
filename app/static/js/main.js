function showOptions(){
    var optButton = document.getElementsByClassName("optionsBox")[0];
      if (optButton.style.display === "none") optButton.style.display = "block";
      else optButton.style.display = "none";
}

function clearSearchBox(){
    document.getElementById("livebox").value
    var searchBox = dddd;
    searchBox.value = "";
}

$(document).ready(function(){
    $("#clear-button").click(function(){
        $("#livebox").val('');
        $("#livebox").trigger("input");
    });
    //Main function
    $("#livebox").on("input", function(e){
        clearTimeout( $(this).data('timer'));
        
        var timer = setTimeout(function(){
            textinlivebox = $("#livebox").val();
            //console.log(textinlivebox);
            $.ajax({
                method:"post",
                url:"/search",
                data:{text:textinlivebox},
                success:function(docs){
                    $("#search-item").empty();
                    if(docs["result"].length == 0){
                        $("#search-item").append('<div class="mt-4 text-center">');
                        //console.log('test');
                        $("#search-item .text-center:first").append(`
                            <p>Input Queries Are Empty...</p>
                            <p>Try to type some keywords...</p>  
                        `);
                    }
                    
                    $('#details .table thead tr').empty()
                    $('#details .table thead tr').append(`<th scope="col">Term</th>`)
                    $('#details .table thead tr').append(`<th scope="col">Query</th>`)
                    //console.log(docs)
                    $('#details .table tbody').empty()
                    //Masukkan header
                    for(var i=0;i<docs["result"].length;i++) $('#details .table thead tr').append(`<th scope="col">D${i+1}</th>`)
                    //Masukkan terms
                    for(var j=0;j<docs["terms"].length;j++){
                        $('#details .table tbody').append(`<tr class="isi"><th scope="row">${docs["terms"][j]}</th></tr>`)
                    }
    
                    //Masukkan kemunculan term
          
                    for(var j=0;j<docs["vec_terms"].length;j++){
                        for(var k=0;k<docs["vec_terms"][j].length;k++){
                            $(`#details .table tbody .isi:nth-child(${k+1})`).append(`<td>${docs["vec_terms"][j][k]}</td>`)
                        }
                    }
                    
                    $("#search-item").append("<ol></ol>");
                    for(doc=0;doc<docs["result"].length;doc++){
                        if(docs["result"][doc][4] == 'internal_txt'){
                            $("#search-item").append(`<h4 class="mb-1"><a href=/search/${docs["result"][doc][0]}.txt target="_blank">${docs["result"][doc][0]}</a></h4>`);
                        }
                        else if(docs["result"][doc][4] == `internal_html_${docs["result"][doc][4].substring(14)}`){
                            //console.log(docs["result"][doc][4].substring(14))
                            $("#search-item").append(`<h4 class="mb-1"><a href=/search/${docs["result"][doc][4].substring(14)}.html target="_blank">${docs["result"][doc][0]}</a></h4>`);
                        }
                        else{
                            $("#search-item").append(`<h4 class="mb-1"><a href=${docs["result"][doc][4]} target="_blank">${docs["result"][doc][0]}</a></h4>`);
                        }
                        $("#search-item").append(`<p style="color:green">${docs["result"][doc][4]}</p>`)
                        $("#search-item").append(`<p>Jumlah kata: ${docs["result"][doc][1]} </p>`);
                        $("#search-item").append(`<p>Tingkat Kemiripan: ${docs["result"][doc][2]}% </p>`);
                        $("#search-item").append(`<p>Konten:</p>`);
                        $("#search-item").append(`<div class="content-box">${docs["result"][doc][3]}</div>`);
                        $("#search-item").append(`<hr/>`);  
                    } 
                    //console.log(docs["terms"]);
                }
            })           
        }, 300)
        $(this).data('timer', timer);
    }); 
    $("#external-url-list").keyup(function(e){
        textinlivebox = $("#external-url-list").val();
        //console.log(textinlivebox);
        $.ajax({
            method:"post",
            url:"/externalDoc",
            data:{text:textinlivebox},
            success:function(){
                //alert("test");
                $("#livebox").trigger("input");
            }
        })
    });

    $(function() {
        $('#upload-file-btn').click(function() {
            var form_data = new FormData();
            var ins = document.getElementById('multiFiles').files.length;
            
            if(ins == 0) {
                $('#msg').html('<span style="color:red">Select at least one file</span>');
                return;
            }
            
            for (var x = 0; x < ins; x++) {
                form_data.append("files[]", document.getElementById('multiFiles').files[x]);
            }
            var form_data = new FormData($('#upload-file')[0]);
            $.ajax({
                type: 'POST',
                url: '/uploadajax',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    //console.log(data)
                    $('#options .row .col-md-4:nth-child(3) p').empty();
                    $('#options .row .col-md-4:nth-child(3) p').append(`Files in server: `);
                    $('#msg').html('<span style="color:green">Files successfuly uploaded</span>');
                    fileinserver(data);
                    $("#livebox").trigger("input");
                },
                error: function(){
                    $('#msg').html('<span style="color:red">Files must be in txt or html</span>');
                },
            });
        });
    });

    function fileinserver(data){
        $('#options .row .col-md-4:nth-child(3) .fileinserver').empty()
        //console.log(data.length)
        if(data.length === 0){
            $('#options .row .col-md-4:nth-child(3) p').empty();
            $('#options .row .col-md-4:nth-child(3) p').append(`Files in server: Empty`);
        }  
        for(var x=0;x<data.length;x++){
            $('#options .row .col-md-4:nth-child(3) .fileinserver').append(`<p><button type"button" class="rmv_button btn btn-primary btn-sm" value=${data[x]}>remove</button>${data[x]}</p>`)
        } 
        $('.rmv_button').click(function(){
        //    console.log($(this).val())
            var fileName = $(this).val()
            $.ajax({
                type: 'GET',
                url: '/deletefile',
                data:{text:fileName},
                success: function(data) {
                    fileinserver(data)
                    $("#livebox").trigger("input");
                },
            }); 
        }); 
    }
    //saat awal html ready
    if($('#options .row .col-md-4:nth-child(3) .fileinserver').is(':empty')){
        $.get("/uploadajax", function(data){
            if(data.length != 0){
                $('#options .row .col-md-4:nth-child(3) p').empty();
               $('#options .row .col-md-4:nth-child(3) p').append(`Files in server: `);
               fileinserver(data);       
            }
        });
    }
    //0console.log($('#options .row .col-md-4:nth-child(3) .fileinserver p '))

});