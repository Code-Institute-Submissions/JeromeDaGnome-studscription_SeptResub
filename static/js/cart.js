var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        var product_id = this.dataset.product;
        var action = this.dataset.action;
        if (user == "AnonymousUser") {
            swal({
                title: "Sorry, you need to login first.",
                text: "Redirecting in 2 seconds.",
                type: "warning",
                timer: 2000,
                showConfirmButton: false
              }, function(){
                    location.href = "/accounts/login";
              });
        } else {
            updateUserOrder(product_id, action);
        }
    });
}
function updateUserOrder(product_id, action, prod_selected_ids=getvalues()) {
  var url = "/cart/update_cart/";

    fetch(url, {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
                "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify({"product_id": product_id, "action":action, "prod_selected_ids":prod_selected_ids})
    })

    .then((response)=>{
        return response.json();
    })

    .then((data)=>{
        location.reload();
    });
}

function getvalues() {
    var selected = [];
    var chkbox = document.querySelectorAll("[id*='id_selected_product_']");
    console.log(selected);
    for (var i = 0; i < chkbox.length; i++) {
      if (chkbox[i].checked) {
        selected.push(chkbox[i].value);
      }
    }
    if (selected.length > 0) {
      return selected;
    }
  }

// Limit checkbox selection only to 5

$("input[type=checkbox]").change(function(e){
    if ($("input[type=checkbox]:checked").length > 5) {
         $(this).prop("checked", false), swal({
            title: "Sorry!",
            text: "You can only choose 5 products",
            type: "warning",
            timer: 2000,
            showConfirmButton: true
          }, function(){
            swal.close ();
          });
    }
 });
