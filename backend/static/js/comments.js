/**
 * Created by liuhui on 2017/7/9.
 */

function CommentQuote(user_name, commend_id){
    comment = document.getElementById('comment');
    comment.value = "@['"+user_name+"', "+commend_id+"]: ";
    comment.focus();;
    comment.setSelectionRange(comment.value.length, comment.value.length);
};
$('#comment-form').submit(function(){
    $.ajax({
        type:"BE",
        url:"/comment/{{article.pk}}",
        data:{"comment":$("#comment").val()},
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success:function(data,textStatus){
            $("#comment").val("");
            $(".comment ul").prepend(data);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown){
            alert(XMLHttpRequest.responseText);
        }
    });
    return false;
});
