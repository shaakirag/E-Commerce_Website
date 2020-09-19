document.addEventListener('DOMContentLoaded', function() {

	var updateBtns = document.getElementsByClassName('update-cart')
	var updateQuantity = document.getElementsByClassName('update-cart-quantity')
	var quantityInput = document.getElementById('quantity')
	var fav = document.getElementsByClassName('fav')
	var review = document.getElementsByClassName('review')

	for (i = 0; i < review.length; i++) {
		review[i].addEventListener('click', function(){
			var reviewId = this.dataset.review
			var action = this.dataset.action
			console.log('reviewId:', reviewId, 'action:', action)
			
			reviewDelete(reviewId, action)

		})
	} 

	function reviewDelete(reviewId, action){
		console.log('User is authenticated, sending data...')

		var url = '/delete_review/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'reviewId':reviewId, 'action':action})
		})
		.then((response) => {
		return response.json();
		})
		.then((data) => {
			location.reload()
		});
	}

	for (i = 0; i < fav.length; i++) {
		fav[i].addEventListener('click', function(){
			var productId = this.dataset.product
			var action = this.dataset.action
			console.log('productId:', productId, 'action:', action)
			
			addFav(productId, action)

		})
	} 

	function addFav(productId, action){
		console.log('User is authenticated, sending data...')

		var url = '/update_fav/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		return response.json();
		})
		.then((data) => {
			location.reload()
		});
	}

	for (i = 0; i < updateBtns.length; i++) {
		updateBtns[i].addEventListener('click', function(){
			var productId = this.dataset.product
			var action = this.dataset.action
			console.log('productId:', productId, 'Action:', action)
			console.log('USER:', user)

			if (user == 'AnonymousUser'){
				addCookieItem(productId, action)
			}else{
				updateUserOrder(productId, action)
			}
		})
	}

	for (i = 0; i < updateQuantity.length; i++) {
		updateQuantity[i].addEventListener('click', function(){
			var productId = this.dataset.product
			var action = this.dataset.action
			var quantity = parseInt(document.getElementById('quantity').value, 10)

			console.log('productId:', productId, 'Action:', action, 'Quantity:', quantity)
			console.log('USER:', user)

			if (user == 'AnonymousUser'){
				console.log('Anon')
				addCookieItemQuantity(productId, action, quantity)	
				document.getElementById('quantity').value = 1
			}else{
				updateUserOrderQuantity(productId, action, quantity)
				document.getElementById('quantity').value = 1
			}
		})
	}

	function updateUserOrder(productId, action){
		console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		return response.json();
		})
		.then((data) => {
			location.reload()
		});
	}

	function updateUserOrderQuantity(productId, action, quantity){
		console.log('User is authenticated, sending data...')

		var url = '/update_item_quantity/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'quantity': quantity})
		})
		.then((response) => {
		return response.json();
		})
		.then((data) => {
			location.reload()
		});
	}

	
	quantityInput.addEventListener('input', function() {
		var add = document.getElementById('add')
		var remove = document.getElementById('remove')
		var quantity2 = this.value

		console.log('Input has been changed')

		add.innerHTML =  `Add (${quantity2}) to Cart`;
		remove.innerHTML =  `Remove (${quantity2}) from Cart`;
	})
	

	function addCookieItem(productId, action){
		console.log('User is not authenticated')

		if (action == 'add'){
			if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}

			}else{
				cart[productId]['quantity'] += 1
			}
		}

		if (action == 'remove'){
			cart[productId]['quantity'] -= 1

			if (cart[productId]['quantity'] <= 0){
				console.log('Item should be deleted')
				delete cart[productId];
			}
		}

		if (action == 'delete'){
			cart[productId]['quantity'] = 0
			delete cart[productId];
		}
		console.log('CART:', cart)
		document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		
		location.reload()
	}

	function addCookieItemQuantity(productId, action, quantity){
		console.log('User is not authenticated')

		if (action == 'add'){
			if (cart[productId] == undefined){
			cart[productId] = {'quantity':quantity}

			}else{
				cart[productId]['quantity'] += quantity
			}
		}

		if (action == 'remove'){
			cart[productId]['quantity'] -= quantity

			if (cart[productId]['quantity'] <= 0){
				console.log('Item should be deleted')
				delete cart[productId];
			}
		}
		console.log('CART:', cart)
		document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		
		location.reload()
	}
})

	
