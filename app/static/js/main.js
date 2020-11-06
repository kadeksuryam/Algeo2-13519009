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
    $("#livebox").on("input", function(e){
        textinlivebox = $("#livebox").val();
        console.log(textinlivebox);
        $.ajax({
            method:"post",
            url:"/search",
            data:{text:textinlivebox},
            success:function(docs){
                /*
                $("#searchres > ol").remove();
                $("#searchres").append("<ol></ol>")    */
                $("#search-item").empty();
                if(docs.length == 0){
                    $("#search-item").append('<div class="mt-4 text-center">');
                    console.log('test');
                    $("#search-item .text-center:first").append(`
                        <p>Input Queries Are Empty...</p>
                        <p>Try to type some keywords...</p>  
                    `);
                }
                $("#search-item").append("<ol></ol>");
                for(doc=0;doc<docs.length;doc++){
                    $("#search-item").append(`<h4 class="mb-1"><a href="#">${docs[doc][0]}</a></h4>`);
                    $("#search-item").append(`<p>Jumlah kata: ${docs[doc][1]} </p>`);
                    $("#search-item").append(`<p>Tingkat Kemiripan: ${docs[doc][2]}</p>`);
                    $("#search-item").append(`<p>Konten:</p>`);
                    $("#search-item").append(`<div class="content-box">${docs[doc][3]}</div>`);
                    $("#search-item").append(`<hr/>`);
                    /*
                        <h4 class="mb-1"><a href="#"></a>${docs[doc][0]}</h4>
                        <li></li>
                        <li><p>${docs[doc][0]}</p></li>
                        <p>Jumlah kata: ${docs[doc][1]} </p>
                        <p>Tingkat Kemiripan: ${docs[doc][2]} </p>
                        <p>${docs[doc][3]}</p>
                        <br/>
                    `); */  
                    //$("#search-item").append(`<h4 class="mb-1"><a href="#">${docs[doc][0]}</a></h4>`);
                    
                }
                console.log(docs);
            }
        })
    }); 
    $("#external-url-list").keyup(function(e){
        textinlivebox = $("#external-url-list").val();
        console.log(textinlivebox);
        $.ajax({
            method:"post",
            url:"/externalDoc",
            data:{text:textinlivebox},
            success:function(){
                //alert("test");
            }
        })
    });
    $("#number-of-internal-doc").keyup(function(e){
        textinlivebox = $("#number-of-internal-doc").val();
        console.log(textinlivebox);
        $.ajax({
            method:"post",
            url:"/internalDoc",
            data:{text:textinlivebox},
            success:function(docs){
                $("#livebox").trigger("input");
            }
        })
    });
    $("#vehicle1").click(function(e){
        //alert("test");
        textinlivebox = this.checked
        console.log(textinlivebox);
        $.ajax({
            method:"post",
            url:"/search",
            data:{text:textinlivebox},
            success:function(docs){
                //alert("test");
            }
        })
    });
})