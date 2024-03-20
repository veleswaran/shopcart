document.addEventListener("DOMContentLoaded", (event) => {
  let plus = document.getElementById("btnPlus");
  let minus = document.getElementById("btnMinus");
  let qty = document.getElementById("txtQty");
  const pid = document.getElementById("pid");
  const btnCart = document.getElementById("btnCart");
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  plus.addEventListener("click", () => {
    let quantity = Number(qty.value);
    quantity = isNaN(quantity) ? 0 : quantity;
    if (quantity < 10) {
      quantity += 1;
      qty.value = quantity;
    }
  });

  minus.addEventListener("click", () => {
    let quantity = Number(qty.value);
    quantity = isNaN(quantity) ? 0 : quantity;
    if (quantity > 0) {
      quantity -= 1;
      qty.value = quantity;
    }
  });
  btnCart.addEventListener("click", () => {
    let quantity = Number(qty.value);
    quantity = isNaN(quantity) ? 0 : quantity;

    if (quantity > 0) {
      let postObj = {
        product_qty: quantity,
        pid: pid.value,
      };
      fetch("/addtocart/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(postObj),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => alert(data["status"]));
    } else {
      alert("Please Enter the Quantity");
    }
  });

  btnFav.addEventListener("click", () => {
    let postObj = {
      pid: pid.value,
    };
    fetch("/fav/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(postObj),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => alert(data["status"]));
  });
});
