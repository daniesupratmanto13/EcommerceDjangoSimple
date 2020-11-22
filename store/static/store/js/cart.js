var update_btns = document.getElementsByClassName('update-cart')

for(var i = 0; i < update_btns.length; i++) {
    update_btns[i].addEventListener('click', function() {
        var product_id = this.dataset.product
        var action = this.dataset.action
        console.log('product_id: ', product_id)
        console.log('action: ', action)
        console.log('user : ', user)
        if(user === 'AnonymousUser'){
            addCookieItem(product_id, action)
        }else{
            updateUserOrder(product_id, action)
        }
    })
}


function addCookieItem(product_id, action) {
    console.log('Not logged in...')
    if (action === 'add'){
        if (cart[product_id] === undefined) {
            cart[product_id] = {'quantity': 1};
        }else{
            cart[product_id]['quantity'] += 1;
        }
    }else if (action === 'remove'){
        cart[product_id]['quantity'] -= 1;
        if (cart[product_id]['quantity'] <= 0){
            console.log('delete item');
            delete cart[product_id];
        }
    }
    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}


function updateUserOrder(product_id, action) {
    console.log('User is authenticated, sending data....');

    var url = '/update_item/';

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'product_id': product_id, 'action': action})
    })

    .then((response) =>{
        return response.json();
    })

    .then((data) =>{
        console.log('data : ', data);
        location.reload();
    });
}