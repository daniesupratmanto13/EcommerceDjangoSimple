if (shipping == 'False') {
    document.getElementById('shipping-info').innerHTML = ''
}

if (user != 'AnonymousUser') {
    document.getElementById('user-info').innerHTML = ''
}

if (shipping == 'False' && user == 'AnonymousUser') {
    document.getElementById('form-wrapper').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
}

var form = document.getElementById('form')

csrftoken = form.getElementsByTagName('input')[0].value

form.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Form submitted....')
    document.getElementById('form-button').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
})

document.getElementById('make-payment').addEventListener('click', function(e){
    submitFormData()
})

function submitFormData(){
    console.log('Payment button clicked...')

    var user_form_data = {
        'name' : null,
        'email' : null,
        'total' : total,
    }

    var shipping_info = {
        'address' : null,
        'city' : null,
        'state' : null,
        'zipcode' : null,
    }

    if(shipping != 'False') {
        shipping_info.address = form.address.value
        shipping_info.city = form.city.value
        shipping_info.state = form.state.value
        shipping_info.zipcode = form.zipcode.value
    }

    if(user == 'AnonymousUser') {
        user_form_data.name = form.name.value
        user_form_data.email = form.email.value
    }

    var url = '/process_order/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'form': user_form_data, 'shipping': shipping_info})
        })
        .then((response) =>{
            return response.json();
        })

        .then((data) =>{
            console.log('Success : ', data);
            alert('Transaction complete');

            cart = {};
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

            window.location.href = index_url;
        })
}