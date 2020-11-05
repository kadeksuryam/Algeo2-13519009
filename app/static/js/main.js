function showOptions(){
    var optButton = document.getElementsByClassName("optionsBox")[0];
      if (optButton.style.display === "none") optButton.style.display = "block";
      else optButton.style.display = "none";
}

$(document).ready(function(){
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
                    console.log('test');
                    $("#search-item .mt4:first").append(`
                        <p>Search Query Are Empty..</p>
                        <p>Try type some keywords..</p>
                    `);
                }
                $("#search-item").append("<ol></ol>");
                for(doc=0;doc<docs.length;doc++){
                    $("#search-item > ol").append(`
                        <li><p>${docs[doc][0]}</p></li>
                        <p>Jumlah kata: ${docs[doc][1]} </p>
                        <p>Tingkat Kemiripan: ${docs[doc][2]} </p>
                        <p>${docs[doc][3]}</p>
                        <br/>
                    `);  
                }
                console.log(docs);
            }
        })
    }); 
    $("#testing").keyup(function(e){
        textinlivebox = $("#testing").val();
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