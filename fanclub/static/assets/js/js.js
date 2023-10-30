function like(n){
    var patch = '{% url /: "lik_post" 0 %}'.replace('0', n);
    $.ajax({
           type: "POST",
           url: patch,
           data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
           dataType: "json",
           success: function(response) {
                document.getElementById("like_count"+response.myid).innerHTML = response.likes_count
               ("dislike_count"+response.myid).innerHTML = response.dislikes_count
            },
            error: function(rs, e) {
            }
      });
 }
function dislike(n){
    var patch = '{% url "d_post" 0 %}'.replace('0', n);
    $.ajax({
           type: "POST",
           url: patch,
           data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
           dataType: "json",
           success: function(response) {
                document.getElementById("like_count"+response.myid).innerHTML = response.likes_count
                document.getElementById("dislike_count"+response.myid).innerHTML = response.dislikes_count
            },
            error: function(rs, e) {
            }
      });
}
