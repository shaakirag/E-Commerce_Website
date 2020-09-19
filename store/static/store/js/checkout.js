document.addEventListener('DOMContentLoaded', function() { 

    var total = parseFloat('{{order.get_cart_total}}')
    var shipping = '{{order.shipping}}'

    if (shipping == 'False'){
        document.getElementById('shipping-info').innerHTML = ''
    }

    if (user != 'AnonymousUser'){
        document.getElementById('user-info').innerHTML = ''
        }

    if (shipping == 'False' && user != 'AnonymousUser'){
        //Hide entire form if user is logged in and shipping is false
            document.getElementById('form-wrapper').classList.add("hidden");
            //Show payment if logged in user wants to buy an item that does not require shipping
            document.getElementById('payment-info').classList.remove("hidden");
    }

    var form = document.getElementById('form')
    form.addEventListener('submit', function(e){
        e.preventDefault()
        console.log('Form Submitted...')
        document.getElementById('form-button').classList.add("hidden");
        document.getElementById('payment-info').classList.remove("hidden");
    })

    
    document.getElementById('make-payment').addEventListener('click', function(e){
        submitFormData()
    })
    

    function submitFormData(){
        console.log('Payment button clicked')

        var userFormData = {
            'firstName':null,
            'lastName':null,
            'email':null,
            'total':total,
        }

        var shippingInfo = {
            'country':null,
            'address':null,
            'city':null,
            'province':null,
            'zipcode':null,
        }

        if (shipping != 'False'){
            shippingInfo.country = form.country.value
            shippingInfo.address = form.address.value
            shippingInfo.city = form.city.value
            shippingInfo.province = form.province.value
            shippingInfo.zipcode = form.zipcode.value
        }

        if (user == 'AnonymousUser'){
            userFormData.firstName = form.firstName.value
            userFormData.lastName = form.lastName.value
            userFormData.email = form.email.value
        }

        console.log('Shipping Info:', shippingInfo)
        console.log('User Info:', userFormData)

        var url = "/process_order/"
        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'applicaiton/json',
                'X-CSRFToken':csrftoken,
            }, 
            body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
            
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            alert('Transaction completed');  

            cart = {}
            document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

            window.location.href = ""
            window.location.href = "{% url 'store:products %}"            
            })
    }
})