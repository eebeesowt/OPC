Element.prototype.getElementById = function(req) {
    var elem = this, children = elem.childNodes, i, len, id;

    for (i = 0, len = children.length; i < len; i++) {
        elem = children[i];

        //we only want real elements
        if (elem.nodeType !== 1 )
            continue;

        id = elem.id || elem.getAttribute('id');

        if (id === req) {
            return elem;
        }
        //recursion ftw
        //find the correct element (or nothing) within the child node
        id = elem.getElementById(req);

        if (id)
            return id;
    }
    //no match found, return null
    return null;
}

function Grouped(id)
{
    $.ajax({
        url: '/grouped',         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        data:{"data": id}
    });
    var ckbx_label = document.getElementById(id).getElementById("grplabel");
    var ckbx = document.getElementById(id).getElementById("groupCheck");
    if ($(ckbx).is(":checked")){
        ckbx_label.innerText = 'Group'
    } else {
        ckbx_label.innerText = ''
    }
}

function Power(id){
    $.ajax({
        url: '/power',         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        data:{"data": id},
        success:function(res){
            element = document.getElementById(id).getElementById("power_but")
            if (res == 'on') {
                $(element).removeClass('btn-danger').addClass('btn-success')
            }else if (res == 'off') {
                $(element).removeClass('btn-success').addClass('btn-danger')
            } else {
                alert(res)
            }
        }
    });
}

function Shutter(id){
    $.ajax({
        url: '/shutter',         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        data:{"data": id},
        async: false,
        success:function(res){
            element = document.getElementById(id).getElementById("shutter_but")
            if (res == 'on') {
                $(element).removeClass('btn-dark').addClass('btn-light')
                $(element).value = 'lol'
            }else{
                $(element).removeClass('btn-light').addClass('btn-dark')
            }
        }
    });
}

function set_Shutter_in(val, id){
    $.ajax({
        url: '/shutter_in',         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        data:{"data": id,
              "time": val},
        async: false,
    });
}

function set_Shutter_out(val, id){
    $.ajax({
        url: '/shutter_out',         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        data:{"data": id,
              "time": val},
        async: false,
    });
}

document.addEventListener("DOMContentLoaded", function(){
var scrn_format = document.querySelectorAll(".btn-outline-primary")
for (let index = 0; index < scrn_format.length; index++) {
    scrn_format[index].addEventListener("click", function(){
        this.className += " active"; 
    })}


})

function setScreenFormat(val, id){
    $.ajax({
        url: '/setScreenFormat',         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        data:{"data": id,
              "format": val},
        async: false,
    });
    var current = document.getElementById(id).getElementsByClassName("active");
    $(current).removeClass("active")

}